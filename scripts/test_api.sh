#!/bin/bash
# MoMo SMS API Testing Script
# Tests all CRUD endpoints with authentication

echo "MoMo SMS API Testing Script"
echo "================================"

# Configuration
API_BASE="http://localhost:8000"
ADMIN_CRED="admin:password123"
USER_CRED="user:momo2024"
API_CRED="api:sms_data"

# Encode credentials
ADMIN_AUTH=$(echo -n "$ADMIN_CRED" | base64)
USER_AUTH=$(echo -n "$USER_CRED" | base64)
API_AUTH=$(echo -n "$API_CRED" | base64)

echo "Testing Authentication..."
echo ""

# Test 1: Valid Authentication - GET /transactions
echo "Test 1: GET /transactions with valid credentials"
echo "Command: curl -H \"Authorization: Basic $ADMIN_AUTH\" $API_BASE/transactions"
echo ""
curl -s -H "Authorization: Basic $ADMIN_AUTH" "$API_BASE/transactions" | jq '.' 2>/dev/null || echo "Response received (jq not available)"
echo ""
echo "---"
echo ""

# Test 2: Invalid Authentication
echo "Test 2: GET /transactions with invalid credentials"
echo "Command: curl -H \"Authorization: Basic dXNlcjp3cm9uZ3Bhc3N3b3Jk\" $API_BASE/transactions"
echo ""
curl -s -H "Authorization: Basic dXNlcjp3cm9uZ3Bhc3N3b3Jk" "$API_BASE/transactions"
echo ""
echo "---"
echo ""

# Test 3: No Authentication
echo "Test 3: GET /transactions without authentication"
echo "Command: curl $API_BASE/transactions"
echo ""
curl -s "$API_BASE/transactions"
echo ""
echo "---"
echo ""

# Test 4: GET specific transaction
echo "Test 4: GET /transactions/1"
echo "Command: curl -H \"Authorization: Basic $ADMIN_AUTH\" $API_BASE/transactions/1"
echo ""
curl -s -H "Authorization: Basic $ADMIN_AUTH" "$API_BASE/transactions/1" | jq '.' 2>/dev/null || echo "Response received (jq not available)"
echo ""
echo "---"
echo ""

# Test 5: POST new transaction
echo "Test 5: POST /transactions"
echo "Command: curl -X POST -H \"Authorization: Basic $ADMIN_AUTH\" -H \"Content-Type: application/json\" -d '{...}' $API_BASE/transactions"
echo ""
curl -s -X POST \
  -H "Authorization: Basic $ADMIN_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "send",
    "amount": 2500.00,
    "currency": "RWF",
    "sender": "+250788123456",
    "receiver": "+250788234567",
    "timestamp": "2024-01-20T14:30:00Z",
    "status": "completed",
    "reference_number": "TXN_TEST_001",
    "message": "Test transaction via API"
  }' \
  "$API_BASE/transactions" | jq '.' 2>/dev/null || echo "Response received (jq not available)"
echo ""
echo "---"
echo ""

# Test 6: PUT update transaction
echo "Test 6: PUT /transactions/1"
echo "Command: curl -X PUT -H \"Authorization: Basic $ADMIN_AUTH\" -H \"Content-Type: application/json\" -d '{...}' $API_BASE/transactions/1"
echo ""
curl -s -X PUT \
  -H "Authorization: Basic $ADMIN_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "failed",
    "message": "Updated via API test"
  }' \
  "$API_BASE/transactions/1" | jq '.' 2>/dev/null || echo "Response received (jq not available)"
echo ""
echo "---"
echo ""

# Test 7: DELETE transaction
echo "Test 7: DELETE /transactions/20"
echo "Command: curl -X DELETE -H \"Authorization: Basic $ADMIN_AUTH\" $API_BASE/transactions/20"
echo ""
curl -s -X DELETE \
  -H "Authorization: Basic $ADMIN_AUTH" \
  "$API_BASE/transactions/20" | jq '.' 2>/dev/null || echo "Response received (jq not available)"
echo ""
echo "---"
echo ""

# Test 8: Performance analysis
echo "Test 8: GET /performance"
echo "Command: curl -H \"Authorization: Basic $ADMIN_AUTH\" $API_BASE/performance"
echo ""
curl -s -H "Authorization: Basic $ADMIN_AUTH" "$API_BASE/performance" | jq '.' 2>/dev/null || echo "Response received (jq not available)"
echo ""
echo "---"
echo ""

# Test 9: Test with different user credentials
echo "Test 9: GET /transactions with user credentials"
echo "Command: curl -H \"Authorization: Basic $USER_AUTH\" $API_BASE/transactions"
echo ""
curl -s -H "Authorization: Basic $USER_AUTH" "$API_BASE/transactions" | jq '.count' 2>/dev/null || echo "Response received (jq not available)"
echo ""
echo "---"
echo ""

# Test 10: Test with API credentials
echo "Test 10: GET /transactions with API credentials"
echo "Command: curl -H \"Authorization: Basic $API_AUTH\" $API_BASE/transactions"
echo ""
curl -s -H "Authorization: Basic $API_AUTH" "$API_BASE/transactions" | jq '.count' 2>/dev/null || echo "Response received (jq not available)"
echo ""
echo "---"
echo ""

echo "API Testing Complete!"
echo ""
echo "Test Summary:"
echo "Valid authentication tests"
echo "Invalid authentication tests"
echo "CRUD operations (GET, POST, PUT, DELETE)"
echo "Performance analysis"
echo "Multiple credential types"
echo ""
echo "Note: Install 'jq' for better JSON formatting:"
echo "   - Ubuntu/Debian: sudo apt install jq"
echo "   - macOS: brew install jq"
echo "   - Windows: choco install jq"
