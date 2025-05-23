# SWIFT Codes API

This project provides a RESTful API to manage and query SWIFT codes (Bank Identifier Codes) stored in a MongoDB database. It parses SWIFT code data from an Excel file, stores it, and exposes endpoints to retrieve, add, and delete SWIFT code information. The solution is containerized using Docker, and tested using Pytest.

Since I'm interested in joining the Data Engineering team, I did the task using python (as per the email).

---

## Prerequisites

Before running the project, ensure you have:

- [Docker](https://docs.docker.com/desktop/)
- [Mongosh](https://www.mongodb.com/try/download/shell) (optional, for manual DB access)

---

## Setup and Running the Project

### 1. Clone the Repository

```sh
# Clone the repository and navigate to the project folder
$ git clone https://github.com/JaZax/swift-codes-api
$ cd swift-codes-api
```

---

### 2. Start the Application

Ensure Docker is installed and running

```sh
# Build and start the container
$ docker-compose up --build -d
```

- The API will be available at: `http://localhost:8080`
- MongoDB will be running at: `localhost:27017`

---

### 3. Parse the Excel File

Sample file included: `./data/Interns_2025_SWIFT_CODES.xlsx`

```sh
# Access the app container's shell
$ docker-compose exec app bash
```

```sh
# Inside the container: parse the Excel file
$ make parse_excel FILE=/data/Interns_2025_SWIFT_CODES.xlsx
```

*You can replace the file path with your own, but make sure the format matches the sample file.*

---

### 4. Access the API

- **API Endpoints Documentation**: [available here](./endpoints.md)
- **Swagger Docs:** `http://localhost:8080/docs`
- **Base URL:** `http://localhost:8080/v1/swift-codes/`

---

### 5. Access the Database (Optional)

Make sure that mongosh is [added to PATH](https://www.mongodb.com/docs/mongodb-shell/install/).

*In a new terminal*: 

```sh
# Open a connection to MongoDB
$ mongosh "localhost:27017"
```

---

### 6. Run Tests

*In a new terminal*: 

```sh
# Access the app container's shell
$ docker-compose exec app bash
```

```sh
# Inside the container: run the tests
$ python -m pytest tests/ -v
```

---

## Technologies Used

- **FastAPI** — API framework  
- **MongoDB** — Database 
- **Pandas** — Excel parsing
- **Pydantic** — Validation
- **Pytest** — Testing framework
- **Docker** — Containerization  

---

## Project Structure

```
swift-codes-api/
├── app/                  # FastAPI application
├── tests/                # Unit & integration tests
├── data/                 # Excel files to parse
├── docker-compose.yml    # Docker Compose config
├── Dockerfile            # Dockerfile for app
├── Makefile              # Utility commands (parse_excel)
└── README.md             # This file :)
```

---

## Author

Email: iza.janeczekk@gmail.com

---

## License

This project is licensed under the MIT License.
