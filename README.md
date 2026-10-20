# ISOContainerAPI

REST API for ISO 6346 container codes, owner codes, equipment categories, and container validation.

## Overview

ISOContainerAPI provides a simple and reliable interface for accessing container identification data based on the ISO 6346 standard and the ISO-Container-Codes dataset.

### Features

- Retrieve container owner information
- Validate ISO 6346 container numbers
- Calculate container check digits
- Search owner/operator codes
- Lookup equipment category identifiers
- JSON-based REST API
- OpenAPI/Swagger documentation

---

## Base URL

```http
https://api.yourdomain.com/api/v1
```

---

## Authentication

All requests require an API key.

### Header

```http
Authorization: Bearer YOUR_API_KEY
```

---

## Endpoints

### Get Owner Code

Returns information about a container owner code.

#### Request

```http
GET /owners/{code}
```

#### Example

```http
GET /owners/MAEU
```

#### Response

```json
{
  "success": true,
  "data": {
    "ownerCode": "MAEU",
    "company": "Maersk",
    "country": "Denmark",
    "status": "active"
  }
}
```

---

### Search Owner Codes

Search container operators by company name or owner code.

#### Request

```http
GET /owners/search?q=maersk
```

#### Response

```json
{
  "success": true,
  "data": [
    {
      "ownerCode": "MAEU",
      "company": "Maersk"
    }
  ]
}
```

---

### Validate Container Number

Validates an ISO 6346 container number.

#### Request

```http
GET /containers/validate/{containerNumber}
```

#### Example

```http
GET /containers/validate/MAEU1234567
```

#### Response

```json
{
  "success": true,
  "data": {
    "containerNumber": "MAEU1234567",
    "valid": true,
    "checkDigit": 7
  }
}
```

---

### Calculate Check Digit

Calculates the ISO 6346 check digit for a container number.

#### Request

```http
POST /containers/check-digit
```

#### Body

```json
{
  "containerPrefix": "MAEU123456"
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "containerPrefix": "MAEU123456",
    "checkDigit": 7,
    "fullContainerNumber": "MAEU1234567"
  }
}
```

---

### Get Equipment Category

Returns information about an equipment category code.

#### Request

```http
GET /equipment/{code}
```

#### Example

```http
GET /equipment/U
```

#### Response

```json
{
  "success": true,
  "data": {
    "code": "U",
    "description": "Freight Container"
  }
}
```

---

### Get All Equipment Categories

#### Request

```http
GET /equipment
```

#### Response

```json
{
  "success": true,
  "data": [
    {
      "code": "U",
      "description": "Freight Container"
    },
    {
      "code": "J",
      "description": "Detachable Freight Container Equipment"
    }
  ]
}
```

---

## Response Format

### Success

```json
{
  "success": true,
  "data": {}
}
```

### Error

```json
{
  "success": false,
  "message": "Error description"
}
```

---

## HTTP Status Codes

| Code | Description |
|--------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

## Example cURL

```bash
curl --request GET \
  --url https://api.yourdomain.com/api/v1/owners/MAEU \
  --header "Authorization: Bearer YOUR_API_KEY"
```

---

## Swagger Documentation

### Swagger UI

```text
https://api.yourdomain.com/swagger
```

### OpenAPI Specification

```text
https://api.yourdomain.com/openapi.json
```

---

## Rate Limiting

| Plan | Requests |
|--------|----------|
| Free | 100/hour |
| Standard | 5,000/hour |
| Enterprise | Unlimited |

---

## Use Cases

- Shipping companies
- Port terminals
- Container tracking systems
- Freight forwarders
- Logistics platforms
- Customs integrations
- Supply chain management systems

---

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- uvicorn
- Swagger/OpenAPI
- Docker

---

## Installation

### Clone Repository

```bash
git clone https://github.com/ramses2099/ISOContainerCodeAPI
cd ISOContainerCodeAPI
```

### Install Dependencies

```bash
# Create virtual enviroment windows
python3 -m venv env
.\env\Scripts\activate

pip install "fastapi[standard]"
pip install SQLAlchemy 
pip install uvicorn

# Create virtual enviroment linux
python3 -m venv env

source ./env/bin/activate


pip3 install "fastapi[standard]"
pip3 install SQLAlchemy 
pip3 install uvicorn

pip3 freeze > requirements.txt

pip3 install -r requirements.txt
```

### Run Application

```bash
fastapi dev
uvicorn app:app --reload
```

API will be available at:

```text
https://localhost:5001
```

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## License

MIT License

---

## Contact

**ISOContainerAPI**

Email: support@yourdomain.com

Website: https://yourdomain.com

---

Built for modern logistics, shipping, and container tracking systems.