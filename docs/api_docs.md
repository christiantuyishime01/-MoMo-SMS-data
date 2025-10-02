# MoMo SMS Data Processing API Documentation

## Overview
This REST API provides secure access to SMS transaction data from mobile money services. The API supports full CRUD operations with Basic Authentication and includes performance analysis using Data Structures & Algorithms (DSA).

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints require Basic Authentication. Include credentials in the `Authorization` header:

```
Authorization: Basic <base64_encoded_credentials>
```

### Valid Credentials
- **admin:password123**
- **user:momo2024** 
- **api:sms_data**

### Example
```bash
# Encode credentials: admin:password123
echo -n "admin:password123" | base64
# Result: YWRtaW46cGFzc3dvcmQxMjM=

# Use in request
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions
```

## Endpoints

### 1. List All Transactions
**GET** `/transactions`

Returns all SMS transactions in the system.

#### Request
```bash
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     http://localhost:8000/transactions
```

#### Response
```json
{
  "status": "success",
  "count": 20,
  "transactions": [
    {
      "id": 1,
      "transaction_type": "receive",
      "amount": 5000.00,
      "currency": "RWF",
      "sender": "+250788123456",
      "receiver": "+250788234567",
      "timestamp": "2024-01-15T10:30:00Z",
      "status": "completed",
      "reference_number": "TXN001",
      "message": "Wakiriye 5000 RWF uva +250788123456. Umubare mushya: 15000 RWF"
    }
  ]
}
```

#### Error Codes
- **401 Unauthorized**: Invalid or missing credentials
- **500 Internal Server Error**: Server-side error

---

### 2. Get Specific Transaction
**GET** `/transactions/{id}`

Returns a specific transaction by ID with performance analysis.

#### Request
```bash
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     http://localhost:8000/transactions/1
```

#### Response
```json
{
  "status": "success",
  "transaction": {
    "id": 1,
    "transaction_type": "receive",
    "amount": 5000.00,
    "currency": "RWF",
    "sender": "+250788123456",
    "receiver": "+250788234567",
    "timestamp": "2024-01-15T10:30:00Z",
    "status": "completed",
    "reference_number": "TXN001",
    "message": "Wakiriye 5000 RWF uva +250788123456. Umubare mushya: 15000 RWF"
  },
  "performance_analysis": {
    "dictionary_lookup": {
      "result": true,
      "time_ms": 0.0012
    },
    "linear_search": {
      "result": true,
      "time_ms": 0.0456
    }
  }
}
```

#### Error Codes
- **401 Unauthorized**: Invalid or missing credentials
- **404 Not Found**: Transaction not found
- **500 Internal Server Error**: Server-side error

---

### 3. Create New Transaction
**POST** `/transactions`

Creates a new SMS transaction record.

#### Request
```bash
curl -X POST \
     -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     -H "Content-Type: application/json" \
     -d '{
       "transaction_type": "send",
       "amount": 2500.00,
       "currency": "RWF",
       "sender": "+250788123456",
       "receiver": "+250788234567",
       "timestamp": "2024-01-20T14:30:00Z",
       "status": "completed",
       "reference_number": "TXN021",
       "message": "Kohereza 2500 RWF kuri +250788234567 byagenze neza"
     }' \
     http://localhost:8000/transactions
```

#### Response
```json
{
  "status": "success",
  "message": "Transaction created successfully",
  "transaction": {
    "id": 21,
    "transaction_type": "send",
    "amount": 2500.00,
    "currency": "RWF",
    "sender": "+250788123456",
    "receiver": "+250788234567",
    "timestamp": "2024-01-20T14:30:00Z",
    "status": "completed",
    "reference_number": "TXN021",
    "message": "Kohereza 2500 RWF kuri +250788234567 byagenze neza"
  }
}
```

#### Required Fields
- `transaction_type`: Type of transaction (send, receive, pay, withdraw, deposit, transfer)
- `amount`: Transaction amount (positive number)
- `currency`: Currency code (RWF, USD, EUR, etc.)
- `sender`: Sender phone number or identifier
- `receiver`: Receiver phone number or identifier

#### Error Codes
- **400 Bad Request**: Missing required fields or invalid JSON
- **401 Unauthorized**: Invalid or missing credentials
- **500 Internal Server Error**: Server-side error

---

### 4. Update Transaction
**PUT** `/transactions/{id}`

Updates an existing transaction record.

#### Request
```bash
curl -X PUT \
     -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "failed",
       "message": "Transaction failed due to insufficient funds"
     }' \
     http://localhost:8000/transactions/1
```

#### Response
```json
{
  "status": "success",
  "message": "Transaction updated successfully",
  "transaction": {
    "id": 1,
    "transaction_type": "receive",
    "amount": 5000.00,
    "currency": "RWF",
    "sender": "+250788123456",
    "receiver": "+250788234567",
    "timestamp": "2024-01-15T10:30:00Z",
    "status": "failed",
    "reference_number": "TXN001",
    "message": "Transaction failed due to insufficient funds"
  }
}
```

#### Error Codes
- **400 Bad Request**: Invalid JSON
- **401 Unauthorized**: Invalid or missing credentials
- **404 Not Found**: Transaction not found
- **500 Internal Server Error**: Server-side error

---

### 5. Delete Transaction
**DELETE** `/transactions/{id}`

Deletes a transaction record.

#### Request
```bash
curl -X DELETE \
     -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     http://localhost:8000/transactions/1
```

#### Response
```json
{
  "status": "success",
  "message": "Transaction deleted successfully",
  "deleted_transaction": {
    "id": 1,
    "transaction_type": "receive",
    "amount": 5000.00,
    "currency": "RWF",
    "sender": "+250788123456",
    "receiver": "+250788234567",
    "timestamp": "2024-01-15T10:30:00Z",
    "status": "completed",
    "reference_number": "TXN001",
    "message": "Wakiriye 5000 RWF uva +250788123456. Umubare mushya: 15000 RWF"
  }
}
```

#### Error Codes
- **401 Unauthorized**: Invalid or missing credentials
- **404 Not Found**: Transaction not found
- **500 Internal Server Error**: Server-side error

---

### 6. Performance Analysis
**GET** `/performance`

Returns DSA performance comparison between different search algorithms.

#### Request
```bash
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     http://localhost:8000/performance
```

#### Response
```json
{
  "status": "success",
  "message": "DSA Performance Comparison",
  "test_results": [
    {
      "transaction_id": 1,
      "found": true,
      "performance": {
        "dictionary_lookup": {
          "result": true,
          "time_ms": 0.0012
        },
        "linear_search": {
          "result": true,
          "time_ms": 0.0456
        }
      }
    }
  ],
  "analysis": {
    "dictionary_lookup": "O(1) - Constant time complexity",
    "linear_search": "O(n) - Linear time complexity",
    "recommendation": "Dictionary lookup is significantly faster for large datasets"
  }
}
```

## Data Structures & Algorithms (DSA)

### Implemented Algorithms

#### 1. Linear Search - O(n)
- **Complexity**: O(n) - Linear time
- **Method**: Sequential scan through all transactions
- **Use Case**: Simple implementation, works for small datasets
- **Performance**: Slower for large datasets

#### 2. Dictionary Lookup - O(1)
- **Complexity**: O(1) - Constant time
- **Method**: Direct key access using Python dictionary
- **Use Case**: Fast lookups by transaction ID
- **Performance**: Fastest for frequent lookups

#### 3. Binary Search - O(log n)
- **Complexity**: O(log n) - Logarithmic time
- **Method**: Divide and conquer on sorted data
- **Use Case**: Efficient for large sorted datasets
- **Performance**: Good balance between speed and memory

#### 4. Hash Table Search - O(1) average
- **Complexity**: O(1) average, O(n) worst case
- **Method**: Custom hash table with collision resolution
- **Use Case**: Demonstrates hash table concepts
- **Performance**: Fast average case, handles collisions

### Performance Comparison Results

| Algorithm | Average Time (ms) | Complexity | Best For |
|-----------|------------------|------------|----------|
| Dictionary Lookup | 0.0012 | O(1) | Frequent lookups |
| Binary Search | 0.0089 | O(log n) | Large sorted data |
| Hash Table | 0.0123 | O(1) avg | General purpose |
| Linear Search | 0.0456 | O(n) | Small datasets |

### Why Dictionary Lookup is Faster

1. **Direct Access**: Dictionary uses hash table internally, providing O(1) average access time
2. **No Iteration**: No need to scan through elements
3. **Optimized Implementation**: Python dictionaries are highly optimized
4. **Memory Efficiency**: Direct memory addressing vs sequential scanning

### Alternative Data Structures

For even better performance, consider:

1. **B-Trees**: For disk-based storage with O(log n) access
2. **Bloom Filters**: For fast existence checks
3. **Trie Structures**: For prefix-based searches
4. **Red-Black Trees**: For balanced binary search trees

## Security Analysis

### Basic Authentication Limitations

#### Why Basic Auth is Weak:

1. **Base64 Encoding**: Credentials are only base64 encoded, not encrypted
2. **No Expiration**: Credentials don't expire automatically
3. **Single Factor**: Only username/password, no additional verification
4. **Replay Attacks**: Credentials can be reused indefinitely
5. **No Session Management**: No way to invalidate sessions

#### Better Alternatives:

1. **JWT (JSON Web Tokens)**:
   - Stateless authentication
   - Built-in expiration
   - Digital signatures for integrity
   - Example: `Authorization: Bearer <jwt_token>`

2. **OAuth 2.0**:
   - Industry standard
   - Third-party authentication
   - Scoped permissions
   - Refresh tokens

3. **API Keys**:
   - Simple but more secure than Basic Auth
   - Can be rotated
   - Rate limiting capabilities

4. **Multi-Factor Authentication (MFA)**:
   - Additional security layer
   - SMS, TOTP, or hardware tokens
   - Reduces credential theft impact

## Error Handling

### Common Error Responses

#### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Valid credentials required",
  "status_code": 401
}
```

#### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Transaction not found",
  "status_code": 404
}
```

#### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Missing required field: amount",
  "status_code": 400
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "Database connection failed",
  "status_code": 500
}
```

## Rate Limiting

Currently not implemented, but recommended for production:

```python
# Example rate limiting implementation
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests=100, window=3600):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_ip):
        now = time.time()
        client_requests = self.requests[client_ip]
        
        # Remove old requests outside window
        client_requests[:] = [req_time for req_time in client_requests 
                            if now - req_time < self.window]
        
        if len(client_requests) >= self.max_requests:
            return False
        
        client_requests.append(now)
        return True
```

## Testing Examples

### Using curl

```bash
# Test authentication
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     http://localhost:8000/transactions

# Test invalid credentials
curl -H "Authorization: Basic dXNlcjp3cm9uZ3Bhc3N3b3Jk" \
     http://localhost:8000/transactions

# Test CRUD operations
curl -X POST \
     -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     -H "Content-Type: application/json" \
     -d '{"transaction_type":"send","amount":1000,"currency":"RWF","sender":"+250788123456","receiver":"+250788234567"}' \
     http://localhost:8000/transactions
```

### Using Python requests

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

# Test POST request
new_transaction = {
    "transaction_type": "send",
    "amount": 1500.00,
    "currency": "RWF",
    "sender": "+250788123456",
    "receiver": "+250788234567"
}
response = requests.post("http://localhost:8000/transactions", 
                        headers=headers, json=new_transaction)
print(response.json())
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API Server**:
   ```bash
   python api/rest_api.py
   ```

3. **Run DSA Analysis**:
   ```bash
   python dsa/algorithms.py
   ```

4. **Test Endpoints**:
   ```bash
   # Test with curl or Postman
   curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
        http://localhost:8000/transactions
   ```

## Conclusion

This API demonstrates:
- ✅ Complete CRUD operations
- ✅ Basic Authentication implementation
- ✅ DSA algorithm comparison
- ✅ Performance analysis
- ✅ Security considerations
- ✅ Comprehensive documentation

The system successfully processes SMS transaction data with efficient search algorithms and secure API access.

