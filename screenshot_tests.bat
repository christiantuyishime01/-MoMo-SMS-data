@echo off
echo ============================================
echo  MoMo SMS API - Screenshot Test Commands
echo ============================================
echo.
echo IMPORTANT: Make sure the API server is running first!
echo Run: run_server.bat in another terminal
echo.
echo Copy and paste these commands one by one for screenshots:
echo.

set BASE_URL=http://localhost:8000
set VALID_AUTH=Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
set INVALID_AUTH=Authorization: Basic aW52YWxpZDpjcmVkZW50aWFscw==

echo ============================================
echo 1. SUCCESSFUL GET REQUEST WITH AUTHENTICATION
echo ============================================
echo.
echo Command to copy:
echo curl -H "%VALID_AUTH%" %BASE_URL%/transactions
echo.
echo Expected: Should show all transactions (Status 200)
echo.
pause
echo.

echo ============================================
echo 2. UNAUTHORIZED REQUEST (WRONG CREDENTIALS)
echo ============================================
echo.
echo Command to copy:
echo curl -H "%INVALID_AUTH%" %BASE_URL%/transactions
echo.
echo Expected: Should return 401 Unauthorized error
echo.
pause
echo.

echo ============================================
echo 3. GET SPECIFIC TRANSACTION WITH PERFORMANCE
echo ============================================
echo.
echo Command to copy:
echo curl -H "%VALID_AUTH%" %BASE_URL%/transactions/1
echo.
echo Expected: Shows transaction details + DSA performance comparison
echo.
pause
echo.

echo ============================================
echo 4. SUCCESSFUL POST (CREATE NEW TRANSACTION)
echo ============================================
echo.
echo Command to copy (all in one line):
echo curl -X POST -H "%VALID_AUTH%" -H "Content-Type: application/json" -d "{\"transaction_type\":\"send\",\"amount\":2500,\"currency\":\"RWF\",\"sender\":\"Screenshot Test\",\"receiver\":\"API User\",\"timestamp\":\"2024-10-02T16:00:00Z\",\"status\":\"completed\",\"reference_number\":\"SCREENSHOT_001\",\"message\":\"Test transaction for screenshot\"}" %BASE_URL%/transactions
echo.
echo Expected: Should create new transaction (Status 201)
echo.
pause
echo.

echo ============================================
echo 5. SUCCESSFUL PUT (UPDATE TRANSACTION)
echo ============================================
echo.
echo Command to copy:
echo curl -X PUT -H "%VALID_AUTH%" -H "Content-Type: application/json" -d "{\"status\":\"failed\",\"message\":\"Updated for screenshot demo\"}" %BASE_URL%/transactions/1
echo.
echo Expected: Should update transaction (Status 200)
echo.
pause
echo.

echo ============================================
echo 6. SUCCESSFUL DELETE
echo ============================================
echo.
echo Command to copy:
echo curl -X DELETE -H "%VALID_AUTH%" %BASE_URL%/transactions/8
echo.
echo Expected: Should delete transaction (Status 200)
echo.
pause
echo.

echo ============================================
echo 7. DSA PERFORMANCE COMPARISON
echo ============================================
echo.
echo Command to copy:
echo curl -H "%VALID_AUTH%" %BASE_URL%/performance
echo.
echo Expected: Shows performance comparison of search algorithms
echo.
pause
echo.

echo ============================================
echo 8. GET ALL TRANSACTIONS (FINAL STATE)
echo ============================================
echo.
echo Command to copy:
echo curl -H "%VALID_AUTH%" %BASE_URL%/transactions
echo.
echo Expected: Shows all transactions including created/modified ones
echo.
echo.
echo ============================================
echo All screenshot commands provided!
echo Remember to take screenshots of each response!
echo ============================================
pause
