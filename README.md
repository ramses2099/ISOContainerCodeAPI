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
http://127.0.0.1:8000
```

---

## Authentication

The implemented container lookup routes require a JWT access token.

1. Activate the virtual environment and install dependencies:

```bash
source env/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env`. Generate a signing secret with `openssl rand -hex 32`
   and set `JWT_SECRET_KEY` in `.env` to that value. Keep `.env` private (it is ignored
   by Git), and use the same secret across restarts and server instances. The API
   refuses to start without a secret of at least 32 bytes.

3. Create an account (password is prompted and stored as an Argon2 hash):

```bash
python create_user.py admin
```

4. Start the API:

```bash
uvicorn app:app --reload
```

5. Request a token using form data:

```bash
curl -X POST http://127.0.0.1:8000/token \
  -d 'username=admin' \
  --data-urlencode 'password=YOUR_PASSWORD'
```

The response contains `access_token` and `token_type`. Tokens expire after 30 minutes;
log in again to obtain another token. Refresh tokens are not implemented.

```bash
curl http://127.0.0.1:8000/isocontainertypesbycode/22G1 \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

Both `/isocontainertypesbygkey/{gkey}` and `/isocontainertypesbycode/{code}`
require authentication. Missing, invalid, or expired tokens return HTTP 401.
Disabling a user in the database rejects their existing tokens immediately.
Use HTTPS in production. JWT payloads are signed, not encrypted; do not put
passwords or other secrets in them.

Swagger UI is available at `http://127.0.0.1:8000/docs`; use **Authorize** to log in.
The other endpoints documented below describe planned functionality.

Run the authentication tests against an isolated in-memory database:

```bash
python -m unittest discover -s tests -v
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
  --header "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Swagger Documentation

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### OpenAPI Specification

```text
http://127.0.0.1:8000/openapi.json
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

Run all commands from the repository root. Use a Python version compatible with
`requirements.txt` (the current dependencies were tested with Python 3.14).

Linux / macOS:

```bash
python3 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Configure JWT Authentication

Copy `.env.example` to `.env` (Linux/macOS: `cp .env.example .env`;
PowerShell: `Copy-Item .env.example .env`). Generate a signing secret:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the generated value into `.env`:

```dotenv
JWT_SECRET_KEY=PASTE_YOUR_GENERATED_SECRET_HERE
```

Keep this secret private and stable across restarts. Environment variables take
precedence over `.env`. The application will refuse to start if the secret is
missing or shorter than 32 bytes.

Create your login account; enter and confirm a password of at least 12 characters:

```bash
python create_user.py admin
```

This creates the `users` table if necessary and stores a password hash in
`db/database.db`. It does not create default credentials.

### Run Application

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

Open Swagger UI, click **Authorize**, enter the account credentials, and try the
container lookup endpoints. The root URL `/` has no endpoint and returns 404.
Stop the development server with Ctrl+C. On subsequent starts, activate `env` and
run the same `uvicorn` command; reuse the existing `.env` and account.

### Test the API

With the server running, request a token (replace `YOUR_PASSWORD`):

```bash
curl -X POST http://127.0.0.1:8000/token \
  -d "username=admin" \
  --data-urlencode "password=YOUR_PASSWORD"
```

Copy the response's `access_token` into the following command:

```bash
curl http://127.0.0.1:8000/isocontainertypesbycode/22G1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

The lookup returns 200 and the container record when that code exists in your
database, or 404 when it does not. Missing, invalid, and expired tokens return 401.
On Windows PowerShell use `curl.exe` and put each command on one line.

Run the automated tests without starting the server:

```bash
python -m unittest discover -s tests -v
```

These tests use an isolated database and leave your application data unchanged.

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