# SWIFT Codes API
This project provides a RESTful API to manage and query SWIFT codes (Bank Identifier Codes) stored in a MongoDB database. The application parses SWIFT code data from an Excel file, stores it, and exposes endpoints to retrieve, add, and delete SWIFT code information. The solution is containerized using Docker.

## Prerequisites
Before running the project, ensure you have:
* Docker.
* mongosh (optional, for manual database access).

## Setup and Running the Project

### 1. **Clone the Repository**
```bash
git clone https://github.com/JaZax/swift-codes-api
cd swift-codes-api
```

### 2. **Start the Application**

Build and run the Docker containers:
```bash
docker-compose up --build
```
This starts the API at http://localhost:8080 and MongoDB at localhost:27017.

### 3. **Parse the Excel File**

The repository includes a sample Excel file (Interns_2025_SWIFT_CODES.xlsx). To parse it:
Access the app container's shell:
```bash
docker-compose exec app bash
```
Run the parsing command:
```
make parse_excel FILE=/data/Interns_2025_SWIFT_CODES.xlsx
```
You can replace the file path with a custom Excel file if needed, byt ensure the Excel file follows the expected format (see ```./data/Interns_2025_SWIFT_CODES.xlsx``` for reference).

### 4. **Access the API**

API Base URL: http://localhost:8080/v1/swift-codes/

API Documentation: http://localhost:8080/docs (interactive Swagger UI)

### 5. **Access the Database**

To manually query the MongoDB database:
```bash
mongosh "mongodb://localhost:27017"
```

###  6. **Run Tests**

Run tests inside the container, so the database connection can also be tested.

Access the app container's shell:
```bash
docker-compose exec app bash
```
Then:
```bash
python -m pytest tests/ -v
```

## Technologies Used

* **FastAPI**: For building the REST API.
* **MongoDB**: For storing SWIFT code data.
* **Pandas**: For parsing Excel files.
* **Docker**: For containerizing the application and database.
* **Pytest**: For unit and integration testing.

## Project Structure

```
swift-codes-api/
├── app/                    # FastAPI application code
├── tests/                  # Unit and integration tests
├── data/                   # Excel file(s) for parsing
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration for the app
├── Makefile                # Utility commands for parsing
└── README.md               # This file
```

This project is licensed under the MIT License.
