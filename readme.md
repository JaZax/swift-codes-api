### Run the Project

1. Clone and enter the repo:
   ```bash
   git clone https://github.com/JaZax/swift-codes-api
   cd 
   ```

2. Run the docker container [docker hyperlink https://docs.docker.com/desktop/]:
    ```bash
    docker-compose up --build
    ```

3. Parse excel file (file is already included, but can be changed if needed)
    Run a shell inside the app container:
    ```bash
    docker-compose exec app bash
    ```
    ```bash
    make parse_excel FILE=/data/Interns_2025_SWIFT_CODES.xlsx
    ```

4. API: 
    http://localhost:8080/v1/swift-codes/
    documentation at http://localhost:8080/docs

5. Database access (mongosh hyperlink https://www.mongodb.com/try/download/shell)
    ```bash
    mongosh "localhost:27017"
    ```

6. testing:
    Run a shell inside the app container:
    ```bash
    docker-compose exec app bash
    ```
    ```bash
    pytest -v
    ```
   

### Project description

technologies used: fastapi, mongodb, pandas

A SWIFT code, also known as a Bank Identifier Code (BIC), is a unique identifier of a bank's branch or headquarter. It ensures that international wire transfers are directed to the correct bank and branch, acting as a bank's unique address within the global financial network.
Currently, SWIFT-related data for various countries is stored in a spreadsheet. While this format is convenient for offline management, we need to make this data accessible to our applications.

