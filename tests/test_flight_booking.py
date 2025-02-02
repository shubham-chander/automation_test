import pytest
import aiohttp
import os

BASE_URL = "http://airline_api_dev:8000"  # Airline API URL in Docker network
PASSPORT_API_URL = "http://passport_api:8080"  # Mocked Passport API URL
path = "/tests/passport_api/mappings/"


# LOCAL MACHINE

# BASE_URL = "http://localhost:8000"
# PASSPORT_API_URL = "http://localhost:8081"
# path = "../passport_api/mappings/"


@pytest.fixture(scope="module")
async def setup_wiremock():
    """Setup WireMock stubs for the Passport API"""
    stub_files = ["passport_match.json", "passport_any.json", "passport_update.json"]
    print("Setting up WireMock stubs...")
    try:
        async with aiohttp.ClientSession() as session:
            for stub_file in stub_files:
                # file_path = f"{path}{stub_file}"
                file_path = os.path.join("../passport_api/mappings", stub_file)
                with open(file_path, "r") as file:
                    stub = file.read()
                async with session.post(
                        f"{PASSPORT_API_URL}/__admin/mappings",
                        data=stub,
                        headers={"Content-Type": "application/json"}
                ) as response:
                    assert response.status == 201, f"Failed to upload stub: {response.status}, {await response.text()}"
    except Exception as e:
        pytest.fail(f"WireMock setup failed: {e}")
    yield
    # Teardown WireMock stubs
    async with aiohttp.ClientSession() as session:
        await session.post(f"{PASSPORT_API_URL}/__admin/reset")


@pytest.mark.asyncio
async def test_create_booking_with_passenger_valid():
    """Create a flight booking with valid customer and flight details"""
    flight_id = "AAA01"
    passport_id = "BC1500"
    first_name = "Shauna"
    last_name = "Davila"
    passenger_data = {
        "passport_id": passport_id,
        "first_name": first_name,
        "last_name": last_name
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{BASE_URL}/flights/{flight_id}/passengers",
                json=passenger_data
        ) as response:
            assert response.status == 200, f"Unexpected status code: {response.status}"
            passenger = await response.json()
            assert passenger["flight_id"] == flight_id
            assert passenger["passport_id"] == passport_id
            assert passenger["first_name"] == first_name
            assert passenger["last_name"] == last_name


@pytest.mark.asyncio
async def test_create_booking_with_invalid_passenger_invalid():
    """Attempt to create a flight booking with in-valid customer and flight details"""
    flight_id = "AAA01"
    passenger_data = {
        "passport_id": "BC1500",
        "first_name": "Gems",
        "last_name": "Doe"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{BASE_URL}/flights/{flight_id}/passengers",
                json=passenger_data
        ) as response:
            assert response.status == 400, f"Unexpected status code: {response.status}"
            error = await response.json()
            assert "detail" in error, "Expected 'detail' key in response"
            assert error["detail"] == "Firstname or Lastname is mismatch."


@pytest.mark.asyncio
async def test_retrieve_flight_details_different_timezone():
    """Retrieving flight details with different timezones"""
    flight_id = "AAA02"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/flights") as response:
            assert response.status == 200, f"Unexpected status code: {response.status}"
            flights_response = await response.json()
            assert "flights" in flights_response, "Expected 'flights' key in response"
            flights = flights_response["flights"]
            assert isinstance(flights, list), "Expected 'flights' to be a list"
            assert len(flights) > 0, "Expected at least one flight in the list"

            for flight in flights:
                # if flight["departure_timezone"] == "Europe/London" and flight["arrival_timezone"] == "Asia/Bangkok":
                if flight["id"] == flight_id:
                    assert flight["departure_time"] == "2024-12-01T10:00:00Z", "Expected departure time in GMT"
                    assert flight[
                               "arrival_time"] == "2024-12-01T21:00:00+07:00", "Expected arrival time in BKK timezone"
                    break
            else:
                pytest.fail("No flight found with the expected timezones")


@pytest.mark.asyncio
async def test_retrieve_flight_details_same_timezone():
    """Retrieving flight details with the same timezone"""
    flight_id = "AAA03"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/flights") as response:
            assert response.status == 200, f"Unexpected status code: {response.status}"
            flights_response = await response.json()
            assert "flights" in flights_response, "Expected 'flights' key in response"
            flights = flights_response["flights"]
            assert isinstance(flights, list), "Expected 'flights' to be a list"
            assert len(flights) > 0, "Expected at least one flight in the list"

            for flight in flights:
                # if flight["departure_timezone"] == "Asia/Bangkok" and flight["arrival_timezone"] == "Asia/Bangkok":
                if flight["id"] == flight_id:
                    assert flight[
                               "departure_time"] == "2024-12-01T07:00:00+07:00", "Expected departure time in BKK timezone"
                    assert flight[
                               "arrival_time"] == "2024-12-01T09:00:00+07:00", "Expected arrival time in BKK timezone"
                    break
            else:
                pytest.fail("No flight found with the expected timezones")


@pytest.mark.asyncio
async def test_update_customer_information():
    """Updating a passenger's details"""
    flight_id = "AAA01"
    customer_id = 1
    passport_id = "UPDATE"
    first_name = "Joey"
    last_name = "Tribbiani"
    updated_data = {
        "passport_id": passport_id,
        "first_name": first_name,
        "last_name": last_name
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(
                f"{BASE_URL}/flights/{flight_id}/passengers/{customer_id}",
                json=updated_data
        ) as response:
            assert response.status == 200, f"Unexpected status code: {response.status}"
            data = await response.json()
            assert data["flight_id"] == flight_id, f"Unexpected flight id: {data['flight_id']}"
            assert data["passport_id"] == passport_id, f"Unexpected passport id : {data['passport_id']}"
            assert data["first_name"] == first_name, f"Unexpected first name : {data['first_name']}"
            assert data["last_name"] == last_name, f"Unexpected last name : {data['last_name']}"


@pytest.mark.asyncio
async def test_update_customer_name_mismatch():
    """Attempt to update a customer's name with mismatched details"""
    flight_id = "AAA01"  # Existing flight
    customer_id = 1  # Existing customer ID
    updated_data = {
        "passport_id": "UPDATE",
        "first_name": "John",  # Mismatched first name
        "last_name": "Doe"  # Mismatched last name
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(
                f"{BASE_URL}/flights/{flight_id}/passengers/{customer_id}",
                json=updated_data
        ) as response:
            # Assert that the update fails with a 400 status code
            assert response.status == 400, f"Unexpected status code: {response.status}"
            error = await response.json()
            # Assert that the error message matches the expected mismatch error
            assert "detail" in error, "Expected 'detail' key in response"
            assert error["detail"] == "Firstname or Lastname is mismatch."


@pytest.mark.asyncio
async def test_delete_passenger():
    """Deleting a passenger"""
    flight_id = "AAA01"
    customer_id = 9992
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{BASE_URL}/flights/{flight_id}/passengers/{customer_id}") as response:
            assert response.status == 200, f"Unexpected status code: {response.status}"

        # Verify the passenger is deleted
        async with session.get(f"{BASE_URL}/flights/{flight_id}/passengers") as response:
            assert response.status == 200, f"Unexpected status code: {response.status}"
            passengers_response = await response.json()
            passengers = passengers_response["passengers"]
            assert all(p["customer_id"] != customer_id for p in passengers), "Passenger was not deleted"
