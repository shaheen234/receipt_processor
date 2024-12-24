# Receipt Processor

## Overview
This project implements a web service for processing receipts and calculating points based on a set of rules. The service exposes two endpoints:

1. **Process Receipts**: Accepts a receipt in JSON format and returns a unique ID for the receipt.
2. **Get Points**: Accepts a receipt ID and returns the points calculated for that receipt.

The application uses in-memory storage, and data does not persist across restarts.

## Features
- Points calculation based on predefined rules.
- REST API implemented using Flask.
- Dockerized for easy deployment.

## Rules for Points Calculation
1. **Retailer Name**: 1 point for every alphanumeric character.
2. **Round Dollar Total**: 50 points if the total is a round dollar amount with no cents.
3. **Multiple of 0.25 Total**: 25 points if the total is a multiple of 0.25.
4. **Items Count**: 5 points for every two items on the receipt.
5. **Item Description Length**: If the trimmed length of the item description is a multiple of 3, multiply the item price by 0.2, round up to the nearest integer, and add the result to the points.
6. **Odd Purchase Day**: 6 points if the day of the purchase date is odd.
7. **Purchase Time**: 10 points if the purchase time is between 2:00 PM and 4:00 PM.

## Prerequisites
- Python 3.9+
- Flask library
- Docker (optional for containerization)

## Installation
### Local Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install flask
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. The service will be available at `http://127.0.0.1:5000`.

### Docker Setup
1. Build the Docker image:
   ```bash
   docker build -t receipt-processor .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 receipt-processor
   ```

3. The service will be available at `http://127.0.0.1:5000`.

## API Endpoints
### 1. Process Receipts
**Endpoint**: `/receipts/process`

**Method**: `POST`

**Request Payload**:
```json
{
  "retailer": "string",
  "purchaseDate": "YYYY-MM-DD",
  "purchaseTime": "HH:MM",
  "items": [
    {
      "shortDescription": "string",
      "price": "decimal"
    }
  ],
  "total": "decimal"
}
```

**Response**:
```json
{
  "id": "string"
}
```

### 2. Get Points
**Endpoint**: `/receipts/{id}/points`

**Method**: `GET`

**Response**:
```json
{
  "points": integer
}
```

## Example Usage
### Process Receipts
**Request**:
```bash
curl -X POST http://127.0.0.1:5000/receipts/process \
-H "Content-Type: application/json" \
-d '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    }
  ],
  "total": "35.35"
}'
```

**Response**:
```json
{
  "id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
}
```

### Get Points
**Request**:
```bash
curl -X GET http://127.0.0.1:5000/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points
```

**Response**:
```json
{
  "points": 28
}
```

## Testing
You can use tools like Postman or `curl` to test the API endpoints. Example requests are provided above.

## Notes
- The application uses in-memory storage; data is lost when the application restarts.
- Use Docker for a consistent runtime environment.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

