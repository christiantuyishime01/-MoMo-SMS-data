# MoMo SMS API Testing Commands

This file contains all the commands needed to test the MoMo SMS API and get the required screenshots for the assignment.

## Quick Start

### Step 1: Start the API Server

```bash
# Navigate to project directory
cd MoMo-SMS-data-1

# Start the server (use one of these commands based on your Python installation)
python api/rest_api.py
# OR
python3 api/rest_api.py
# OR
py api/rest_api.py
```

**Expected Output:**
```
MoMo SMS API Server starting...
Server running at http://localhost:8000
Loaded X transactions from XML
Authentication required - use Basic Auth
Available endpoints:
   GET    /transactions           - List all transactions
   GET    /transactions/{id}     - Get specific transaction
   POST   /transactions           - Create new transaction
   PUT    /transactions/{id}     - Update transaction
   DELETE /transactions/{id}     - Delete transaction
   GET    /performance            - DSA performance comparison
```

### Step 2: Open New Terminal for Testing

Keep the server running and open a **new terminal** for testing commands.

---

## Screenshot Testing Commands

Run these commands **one by one** and take screenshots of each response:

### Screenshot 1: Successful GET with Authentication

```bash
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions
```

**Expected Result:** 
- Status: `200 OK`
- Shows list of all transactions with count
- Demonstrates successful authentication

---

### Screenshot 2: Unauthorized Request (Wrong Credentials)

```bash
curl -H "Authorization: Basic aW52YWxpZDpjcmVkZW50aWFscw==" http://localhost:8000/transactions
```

**Expected Result:**
- Status: `401 Unauthorized`
- Error message: "Valid credentials required"
- Demonstrates security implementation

---

### Screenshot 3: Get Specific Transaction with Performance Analysis

```bash
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions/1
```

**Expected Result:**
- Status: `200 OK`
- Shows transaction details
- Includes DSA performance comparison (dictionary vs linear search)
- Demonstrates algorithm efficiency analysis

---

### Screenshot 4: Successful POST (Create New Transaction)

**Multi-line version:**
```bash
curl -X POST \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "send",
    "amount": 2500.00,
    "currency": "RWF",
    "sender": "Screenshot Test User",
    "receiver": "API Demo User",
    "timestamp": "2024-10-02T16:00:00Z",
    "status": "completed",
    "reference_number": "SCREENSHOT_001",
    "message": "Test transaction created for screenshot demonstration"
  }' \
  http://localhost:8000/transactions
```

**Single-line version (if multi-line doesn't work):**
```bash
curl -X POST -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" -H "Content-Type: application/json" -d '{"transaction_type":"send","amount":2500,"currency":"RWF","sender":"Screenshot Test User","receiver":"API Demo User","timestamp":"2024-10-02T16:00:00Z","status":"completed","reference_number":"SCREENSHOT_001","message":"Test transaction for screenshot"}' http://localhost:8000/transactions
```

**Expected Result:**
- Status: `201 Created`
- Shows newly created transaction with auto-generated ID
- Demonstrates successful data creation

---

### Screenshot 5: Successful PUT (Update Transaction)

**Multi-line version:**
```bash
curl -X PUT \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "failed",
    "message": "Transaction status updated for screenshot demonstration"
  }' \
  http://localhost:8000/transactions/1
```

**Single-line version:**
```bash
curl -X PUT -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" -H "Content-Type: application/json" -d '{"status":"failed","message":"Transaction status updated for screenshot demonstration"}' http://localhost:8000/transactions/1
```

**Expected Result:**
- Status: `200 OK`
- Shows updated transaction with modified fields
- Demonstrates successful data modification

---

### Screenshot 6: Successful DELETE

```bash
curl -X DELETE -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions/8
```

**Expected Result:**
- Status: `200 OK`
- Shows details of deleted transaction
- Demonstrates successful data deletion

---

### Screenshot 7: DSA Performance Comparison

```bash
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/performance
```

**Expected Result:**
- Status: `200 OK`
- Shows performance comparison between different search algorithms
- Includes timing data for linear search vs dictionary lookup
- Demonstrates DSA integration and analysis

---

### Screenshot 8: Final State (All Transactions After Operations)

```bash
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions
```

**Expected Result:**
- Status: `200 OK`
- Shows all transactions including:
  - Original transactions from SMS data
  - Newly created transaction from POST
  - Modified transaction from PUT
  - Remaining transactions after DELETE
- Demonstrates complete CRUD functionality

---

## Authentication Details

### Valid Credentials:
- **Username:** `admin` **Password:** `password123`
- **Username:** `user` **Password:** `momo2024`
- **Username:** `api` **Password:** `sms_data`

### Base64 Encoded Credentials:
- `admin:password123` → `YWRtaW46cGFzc3dvcmQxMjM=`
- `user:momo2024` → `dXNlcjptb21vMjAyNA==`
- `api:sms_data` → `YXBpOnNtc19kYXRh`
- `invalid:credentials` → `aW52YWxpZDpjcmVkZW50aWFscw==` (for testing 401 errors)

---

## Alternative Testing Methods

### Using Postman:
1. Import the following as a new request
2. Set method to GET/POST/PUT/DELETE as needed
3. Add header: `Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=`
4. For POST/PUT: Set body to raw JSON

### Using Browser (for GET requests only):
1. Open browser
2. Go to: `http://admin:password123@localhost:8000/transactions`
3. This will automatically handle basic authentication

### Using Python requests:
```python
import requests
import base64

# Setup authentication
credentials = "admin:password123"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
headers = {"Authorization": f"Basic {encoded_credentials}"}

# Test GET request
response = requests.get("http://localhost:8000/transactions", headers=headers)
print(response.json())
```

---

## Screenshot Checklist

Make sure to capture these elements in your screenshots:

- [ ] **Screenshot 1**: GET all transactions - Status 200, transaction list
- [ ] **Screenshot 2**: Unauthorized access - Status 401, error message
- [ ] **Screenshot 3**: GET specific transaction - Status 200, performance data
- [ ] **Screenshot 4**: POST create - Status 201, new transaction details
- [ ] **Screenshot 5**: PUT update - Status 200, modified transaction
- [ ] **Screenshot 6**: DELETE - Status 200, deleted transaction details
- [ ] **Screenshot 7**: Performance endpoint - Status 200, DSA comparison
- [ ] **Screenshot 8**: Final state - Status 200, all remaining transactions

---

## Troubleshooting

### Server won't start:
- Check if Python is installed: `python --version`
- Try alternative Python commands: `python3` or `py`
- Check if port 8000 is already in use

### curl command not found:
- **Windows**: Install curl or use PowerShell's `Invoke-RestMethod`
- **macOS**: curl should be pre-installed
- **Linux**: Install with `sudo apt install curl`

### Connection refused:
- Make sure the server is running on port 8000
- Check firewall settings
- Try `http://127.0.0.1:8000` instead of `localhost`

### Authentication errors:
- Verify the Base64 encoding is correct
- Make sure there are no extra spaces in the header
- Check that credentials match exactly

---

## Data Source

This API processes real SMS data from `modified_sms_v2.xml` which contains 1,693 mobile money transaction SMS messages. The parser extracts transaction information including:

- Money received notifications
- Payment confirmations  
- Money transfer records
- Bank deposit notifications
- Airtime purchase receipts

All transaction data is processed from actual MoMo SMS messages and made available through the secure REST API endpoints.

---

## Team Members

- Kevin Nizeyimana
- Arnaud Manzi Ineza
- Tuyishime Christian
- Katsia Teta
- Karigirwa Ange

---

**Happy Testing!**
