@echo off
echo Testing MoMo SMS API Endpoints
echo ==============================
echo.

set BASE_URL=http://localhost:8000
set AUTH_HEADER=Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=

echo Testing API endpoints (make sure the server is running on port 8000)
echo.

echo 1. Testing GET /transactions (List all transactions)
echo.
curl -H "%AUTH_HEADER%" %BASE_URL%/transactions
echo.
echo.

echo 2. Testing GET /transactions/1 (Get specific transaction)
echo.
curl -H "%AUTH_HEADER%" %BASE_URL%/transactions/1
echo.
echo.

echo 3. Testing GET with invalid credentials (should return 401)
echo.
curl -H "Authorization: Basic aW52YWxpZDpjcmVkZW50aWFscw==" %BASE_URL%/transactions
echo.
echo.

echo 4. Testing POST /transactions (Create new transaction)
echo.
curl -X POST ^
     -H "%AUTH_HEADER%" ^
     -H "Content-Type: application/json" ^
     -d "{\"transaction_type\":\"send\",\"amount\":1500,\"currency\":\"RWF\",\"sender\":\"Test User\",\"receiver\":\"Jane Doe\",\"timestamp\":\"2024-10-02T15:30:00Z\",\"status\":\"completed\",\"reference_number\":\"TEST001\",\"message\":\"Test transaction\"}" ^
     %BASE_URL%/transactions
echo.
echo.

echo 5. Testing PUT /transactions/1 (Update transaction)
echo.
curl -X PUT ^
     -H "%AUTH_HEADER%" ^
     -H "Content-Type: application/json" ^
     -d "{\"status\":\"failed\",\"message\":\"Updated transaction status\"}" ^
     %BASE_URL%/transactions/1
echo.
echo.

echo 6. Testing DELETE /transactions/8 (Delete transaction)
echo.
curl -X DELETE ^
     -H "%AUTH_HEADER%" ^
     %BASE_URL%/transactions/8
echo.
echo.

echo 7. Testing GET /performance (DSA performance comparison)
echo.
curl -H "%AUTH_HEADER%" %BASE_URL%/performance
echo.
echo.

echo Testing completed!
pause
