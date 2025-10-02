#!/usr/bin/env python3
"""
API Testing Script for MoMo SMS Data Processing System
Tests all CRUD endpoints with authentication
"""

import requests
import base64
import json
import time

class APITester:
    """Tests the MoMo SMS API endpoints"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.valid_credentials = "admin:password123"
        self.invalid_credentials = "invalid:credentials"
        
        # Setup headers
        valid_encoded = base64.b64encode(self.valid_credentials.encode()).decode()
        invalid_encoded = base64.b64encode(self.invalid_credentials.encode()).decode()
        
        self.valid_headers = {"Authorization": f"Basic {valid_encoded}"}
        self.invalid_headers = {"Authorization": f"Basic {invalid_encoded}"}
        
    def test_get_all_transactions(self):
        """Test GET /transactions"""
        print("Testing GET /transactions (List all transactions)")
        print("-" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/transactions", headers=self.valid_headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success: Found {data.get('count', 0)} transactions")
                if data.get('transactions'):
                    print(f"First transaction: {data['transactions'][0]['transaction_type']} - {data['transactions'][0]['amount']} {data['transactions'][0]['currency']}")
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    def test_get_specific_transaction(self, transaction_id=1):
        """Test GET /transactions/{id}"""
        print(f"Testing GET /transactions/{transaction_id} (Get specific transaction)")
        print("-" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/transactions/{transaction_id}", headers=self.valid_headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                tx = data.get('transaction', {})
                perf = data.get('performance_analysis', {})
                print(f"✅ Success: Transaction {tx.get('id')} - {tx.get('transaction_type')} - {tx.get('amount')} {tx.get('currency')}")
                print(f"Performance - Dict: {perf.get('dictionary_lookup', {}).get('time_ms', 0):.4f}ms, Linear: {perf.get('linear_search', {}).get('time_ms', 0):.4f}ms")
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    def test_unauthorized_access(self):
        """Test unauthorized access"""
        print("Testing Unauthorized Access (Invalid credentials)")
        print("-" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/transactions", headers=self.invalid_headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 401:
                print("✅ Success: Correctly returned 401 Unauthorized")
            else:
                print(f"❌ Failed: Expected 401, got {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    def test_create_transaction(self):
        """Test POST /transactions"""
        print("Testing POST /transactions (Create new transaction)")
        print("-" * 50)
        
        new_transaction = {
            "transaction_type": "send",
            "amount": 1500.00,
            "currency": "RWF",
            "sender": "API Test User",
            "receiver": "Jane Doe",
            "timestamp": "2024-10-02T15:30:00Z",
            "status": "completed",
            "reference_number": "API_TEST_001",
            "message": "Test transaction created via API"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/transactions", 
                headers={**self.valid_headers, "Content-Type": "application/json"},
                json=new_transaction
            )
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                tx = data.get('transaction', {})
                print(f"✅ Success: Created transaction {tx.get('id')} - {tx.get('transaction_type')} - {tx.get('amount')} {tx.get('currency')}")
                return tx.get('id')  # Return the new transaction ID for further tests
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        return None
    
    def test_update_transaction(self, transaction_id=1):
        """Test PUT /transactions/{id}"""
        print(f"Testing PUT /transactions/{transaction_id} (Update transaction)")
        print("-" * 50)
        
        update_data = {
            "status": "failed",
            "message": "Transaction failed - updated via API test"
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/transactions/{transaction_id}", 
                headers={**self.valid_headers, "Content-Type": "application/json"},
                json=update_data
            )
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                tx = data.get('transaction', {})
                print(f"✅ Success: Updated transaction {tx.get('id')} - Status: {tx.get('status')}")
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    def test_delete_transaction(self, transaction_id):
        """Test DELETE /transactions/{id}"""
        if not transaction_id:
            print("Skipping DELETE test - no transaction ID provided")
            print()
            return
            
        print(f"Testing DELETE /transactions/{transaction_id} (Delete transaction)")
        print("-" * 50)
        
        try:
            response = requests.delete(f"{self.base_url}/transactions/{transaction_id}", headers=self.valid_headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                tx = data.get('deleted_transaction', {})
                print(f"✅ Success: Deleted transaction {tx.get('id')} - {tx.get('transaction_type')}")
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    def test_performance_endpoint(self):
        """Test GET /performance"""
        print("Testing GET /performance (DSA performance comparison)")
        print("-" * 50)
        
        try:
            response = requests.get(f"{self.base_url}/performance", headers=self.valid_headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('test_results', [])
                analysis = data.get('analysis', {})
                print(f"✅ Success: Performance test completed on {len(results)} transactions")
                print(f"Recommendation: {analysis.get('recommendation', 'N/A')}")
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    def run_all_tests(self):
        """Run all API tests"""
        print("MoMo SMS API Testing Suite")
        print("=" * 50)
        print(f"Base URL: {self.base_url}")
        print(f"Testing with credentials: {self.valid_credentials}")
        print()
        
        # Test sequence
        self.test_get_all_transactions()
        self.test_get_specific_transaction(1)
        self.test_unauthorized_access()
        
        # Create, update, delete sequence
        new_tx_id = self.test_create_transaction()
        self.test_update_transaction(1)  # Update existing transaction
        self.test_delete_transaction(new_tx_id)  # Delete the newly created transaction
        
        # Performance test
        self.test_performance_endpoint()
        
        print("=" * 50)
        print("All tests completed!")

def main():
    """Main function to run API tests"""
    tester = APITester()
    
    # Check if server is running
    try:
        response = requests.get(tester.base_url, timeout=5)
        print(f"Server is running at {tester.base_url}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Server not running at {tester.base_url}")
        print("Please start the API server first using: python api/rest_api.py")
        return
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return
    
    # Run tests
    tester.run_all_tests()

if __name__ == '__main__':
    main()