#!/usr/bin/env python3
"""
Screenshot Test Script for MoMo SMS API
Run this to get all the required API responses for screenshots
"""

import requests
import base64
import json
import time
import sys

class ScreenshotTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.valid_auth = self._encode_auth("admin:password123")
        self.invalid_auth = self._encode_auth("invalid:credentials")
        
    def _encode_auth(self, credentials):
        encoded = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}
    
    def _print_separator(self, title):
        print("\n" + "="*60)
        print(f" {title}")
        print("="*60)
    
    def _print_response(self, response, description):
        print(f"\n{description}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
        print("-"*60)
        input("Press Enter to continue to next test...")
    
    def test_server_connection(self):
        """Check if server is running"""
        try:
            response = requests.get(self.base_url, timeout=3)
            print("✅ Server is running!")
            return True
        except requests.exceptions.ConnectionError:
            print("❌ Server is not running!")
            print("Please start the server first using: run_server.bat")
            return False
    
    def screenshot_1_successful_get(self):
        """Screenshot 1: Successful GET with authentication"""
        self._print_separator("SCREENSHOT 1: SUCCESSFUL GET WITH AUTHENTICATION")
        
        response = requests.get(f"{self.base_url}/transactions", headers=self.valid_auth)
        self._print_response(response, "GET /transactions with valid credentials")
    
    def screenshot_2_unauthorized(self):
        """Screenshot 2: Unauthorized request"""
        self._print_separator("SCREENSHOT 2: UNAUTHORIZED REQUEST")
        
        response = requests.get(f"{self.base_url}/transactions", headers=self.invalid_auth)
        self._print_response(response, "GET /transactions with invalid credentials (should be 401)")
    
    def screenshot_3_get_specific(self):
        """Screenshot 3: Get specific transaction with performance"""
        self._print_separator("SCREENSHOT 3: GET SPECIFIC TRANSACTION WITH PERFORMANCE")
        
        response = requests.get(f"{self.base_url}/transactions/1", headers=self.valid_auth)
        self._print_response(response, "GET /transactions/1 with performance analysis")
    
    def screenshot_4_post_create(self):
        """Screenshot 4: Successful POST"""
        self._print_separator("SCREENSHOT 4: SUCCESSFUL POST (CREATE TRANSACTION)")
        
        new_transaction = {
            "transaction_type": "send",
            "amount": 2500.00,
            "currency": "RWF",
            "sender": "Screenshot Test User",
            "receiver": "API Demo User",
            "timestamp": "2024-10-02T16:00:00Z",
            "status": "completed",
            "reference_number": "SCREENSHOT_001",
            "message": "Test transaction created for screenshot demonstration"
        }
        
        response = requests.post(
            f"{self.base_url}/transactions", 
            headers={**self.valid_auth, "Content-Type": "application/json"},
            json=new_transaction
        )
        self._print_response(response, "POST /transactions - Create new transaction")
        
        # Return the created transaction ID for later use
        try:
            return response.json().get('transaction', {}).get('id')
        except:
            return None
    
    def screenshot_5_put_update(self):
        """Screenshot 5: Successful PUT"""
        self._print_separator("SCREENSHOT 5: SUCCESSFUL PUT (UPDATE TRANSACTION)")
        
        update_data = {
            "status": "failed",
            "message": "Transaction status updated for screenshot demonstration"
        }
        
        response = requests.put(
            f"{self.base_url}/transactions/1", 
            headers={**self.valid_auth, "Content-Type": "application/json"},
            json=update_data
        )
        self._print_response(response, "PUT /transactions/1 - Update transaction")
    
    def screenshot_6_delete(self, transaction_id=None):
        """Screenshot 6: Successful DELETE"""
        self._print_separator("SCREENSHOT 6: SUCCESSFUL DELETE")
        
        # Use the transaction ID from POST, or default to 8
        delete_id = transaction_id if transaction_id else 8
        
        response = requests.delete(f"{self.base_url}/transactions/{delete_id}", headers=self.valid_auth)
        self._print_response(response, f"DELETE /transactions/{delete_id}")
    
    def screenshot_7_performance(self):
        """Screenshot 7: DSA Performance comparison"""
        self._print_separator("SCREENSHOT 7: DSA PERFORMANCE COMPARISON")
        
        response = requests.get(f"{self.base_url}/performance", headers=self.valid_auth)
        self._print_response(response, "GET /performance - DSA algorithm comparison")
    
    def screenshot_8_final_state(self):
        """Screenshot 8: Final state of all transactions"""
        self._print_separator("SCREENSHOT 8: FINAL STATE - ALL TRANSACTIONS")
        
        response = requests.get(f"{self.base_url}/transactions", headers=self.valid_auth)
        self._print_response(response, "GET /transactions - Final state after all operations")
    
    def run_all_screenshot_tests(self):
        """Run all tests for screenshots"""
        print("MoMo SMS API - Screenshot Test Suite")
        print("="*60)
        print("This script will run through all the API tests needed for screenshots.")
        print("Make sure to take a screenshot of each response!")
        print("="*60)
        
        if not self.test_server_connection():
            return
        
        input("\nPress Enter to start the screenshot tests...")
        
        # Run all screenshot tests
        self.screenshot_1_successful_get()
        self.screenshot_2_unauthorized()
        self.screenshot_3_get_specific()
        
        # POST and capture the new transaction ID
        new_tx_id = self.screenshot_4_post_create()
        
        self.screenshot_5_put_update()
        self.screenshot_6_delete(new_tx_id)
        self.screenshot_7_performance()
        self.screenshot_8_final_state()
        
        print("\n" + "="*60)
        print(" ALL SCREENSHOT TESTS COMPLETED!")
        print("="*60)
        print("You should now have 8 screenshots showing:")
        print("1. Successful GET with authentication")
        print("2. 401 Unauthorized error")
        print("3. GET specific transaction with performance")
        print("4. Successful POST (create)")
        print("5. Successful PUT (update)")
        print("6. Successful DELETE")
        print("7. DSA Performance comparison")
        print("8. Final state of all transactions")

def main():
    tester = ScreenshotTester()
    tester.run_all_screenshot_tests()

if __name__ == '__main__':
    main()
