# Welcome to EarnIn Airline.

This is RESTful API for EarnIn Airline application. 

## Up and running
> _Please ensure that you have docker in your machine to run._ 

To start the service, you can run the following command.
```bash
docker compose up -d
```

__Create DB schema__. You can find `sql` file in [db](./db/) directory. To apply other SQL script, you can place a sql file in db dir, and replace `schema.sql` with your file name.
```bash
docker compose exec -it postgres bash -c "/home/scripts/exec_sql.sh schema.sql"
```

This system does not initial any data. You choose add some data to `flights` table. For `timezone` column, please choose from [List of timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) in `TZ identifier` column.

## APIs
### List all flights
```bash
curl http://localhost:8000/flights
```

### List passengers by flight
```bash
curl http://localhost:8000/flights/[flight-id]/passengers
```

### Create a passenger
The API will validate passenger's firstname and lastname with `Passport API` before creating a record. The customer record will create a new record if the passport ID doesn't exist in the system.

> `Passport API` use wiremock to stubbing the actual service. You can find configuration in [passport_api directory](./passport_api/). If you're new to wiremmock, we recommend to check out [wiremock documentation](https://wiremock.org/docs/stubbing/).

```bash
curl http://localhost:8000/flights/[flight-id]/passengers \
    -d '{"passport_id": "BC1500", "first_name": "Shauna", "last_name": "Davila"}' \
    -H "Content-Type:application/json"
```

### Update a passenger
To update information of customer info, we can use this API to update passport ID, firstname, and lastname.

```bash
curl -X PUT http://localhost:8000/flights/[flight-id]/passengers/[customer_id] \
    -d '{"passport_id": "BC1500", "first_name": "Shauna", "last_name": "Davila"}' \
    -H "Content-Type:application/json"
```


### Delete a passenger
To update information of customer info, we can use this API to update passport ID, firstname, and lastname.

```bash
curl -X DELETE http://localhost:8000/flights/[flight-id]/passengers/[customer_id]
```

# QA Automation Test Assignment

As part of the QA automation testing coverage, the following test scenarios must be automated for the EarnIn Airline API. 
Each test case should use its own mock data and services (e.g., Wiremock for Passport API).


### **Test Scenarios and Expected Results**

| **Test Scenario**                                                        | **Expected Result**                                                                                      |
|--------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| Create a flight booking with valid customer and flight details           | Booking is successfully created. Customer name is verified via Passport API |
| Attempt to create a booking with mismatched customer name in Passport API      | Booking fails. The Passport API returns a 'Firstname or Lastname is mismatch.' error.                                    |
| Retrieve flight details of the different timezone of departure and arrival airport.               | Booking details are retrieved, and departure time is converted to the UK timezone (GMT), and arrival time is converted to BKK timezone.              |
| Retrieve flight details of the same timezone of departure and arrival airport (Bangkok, ICT)         | Booking details are retrieved, and both departure time and arrival time are converted to the Thailand (Bangkok, ICT) timezone.      |
| Update customer contact information and flight details                   | Customer information is successfully updated, and name is verified via Passport API. |
| Attempt to update customer name with mismatched details in Passport API        | Update fails. The Passport API returns a 'Firstname or Lastname is mismatch.' error.                                     |
| Delete a valid booking                                                   | Booking is successfully deleted from the system.                                                         |


## Mock Data and Services

- Each test case should use mock data specific to the customer and flight information.
- Passport API service should be stubbed using Wiremock or an equivalent tool.
  - Passport API is used for name verification.

## Bonus: GitHub Actions for Automation

- To ensure the automation test suite runs consistently, integrate the tests into a GitHub Actions pipeline.
- Goal: Configure a GitHub Action that triggers on every Pull Request (PR) build. This action should:
	1.	Set up the necessary environment (including Docker services).
	2.	Run the full suite of automated tests.
	3.	Report any failures back to the PR.

## **Assignment Submission Guidelines**

Candidates are required to create a public or private repository (accessible by the hiring team) on their own GitHub account for the assignment. Please follow these steps for submission:

1. **Fork or clone** this repository to your own GitHub account.
2. Implement the necessary tests and ensure all test scenarios mentioned above are covered using automation.
3. Configure GitHub Actions to run the test suite on each pull request (PR) build as a bonus.
4. Once completed, **push the code** to your repository.
5. Send us the **repository link** via email or the designated platform.
6. Add a description to this file explaining how to run the test and where to find the test results/report.

> **Note**: If your repository is private, ensure to grant access to the provided GitHub account for review.

# How to run the test

Before run the test, make sure python3 is installed in system 

We have two approaches to run the test

# Approach 1

Trigger the compose.apitest.yml file
```bash
docker-compose -f compose.apitest.yml up -d
```

It will first 
1. Start the service
2. Create database
3. Trigger the tests
4. Store the test results in [reports](./tests/reports/) directory.


# Approach 2
first, make sure service is up and running.

To start the service, you can run the following command.
```bash
docker compose up -d
```

_Create DB schema_. You can find sql file in [db](./db/) directory. To apply other SQL script, you can place a sql file in db dir, and replace schema.sql with your file name.
```bash
docker compose exec -it postgres bash -c "/home/scripts/exec_sql.sh schema.sql"
```

# Move to [tests](./tests/) directory
 Tests are available under tests directory
```
cd tests
```


# Create virtual environment (Optional)
```
py -m venv venv
```

_**Activate virtual environment**_

for mac
```
source venv/bin/activate
```

for windows
```
venv\Scripts\activate
```

# Install dependencies
```
pip install -r requirements_test.txt
```

# Run the test

Before running the test, make sure to update the url in Script.
Script default url is set to use Docker's URL, comment that out first : 
```
# DOCKER URL
# BASE_URL = "http://airline_api_dev:8000"  # Airline API URL in Docker network
# PASSPORT_API_URL = "http://passport_api:8080"  # Mocked Passport API URL
# path = "/tests/passport_api/mappings/"
```

and un-comment the local machine's url
```
# LOCAL MACHINE URL
BASE_URL = "http://localhost:8000"  # Airline API URL
PASSPORT_API_URL = "http://localhost:8081"  # Mocked Passport API URL
path = "../passport_api/mappings/"
```

Now, Run the tests using following command :
```
pytest <test_file_name.py> --tb=short --disable-warnings --html=reports/report.html
```
example : 
```
 pytest test_flight_booking.py --tb=short --disable-warnings --html=reports/report.html
```

# REPORT
> Result will be stored in [reports](./tests/reports/) directory.
> 
> file name : report.html


#
# GITHUB ACTIONS

Git-hub actions are configured, it will upload the artifacts on server, but it will only send the result to Pull Request only when any test fail.
> you can find the yml file here : [GITHUB ACTIONS](./.github/workflows/docker-image.yml) 

> please check the Pull Request : actions_patch


# More resources
- [List of timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
- [Wiremock documentation](https://wiremock.org/docs/stubbing/)