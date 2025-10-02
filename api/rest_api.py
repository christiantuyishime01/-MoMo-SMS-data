#!/usr/bin/env python3
"""
MoMo SMS Data Processing System - REST API
Week 2: API Implementation with Basic Authentication

This module implements a REST API for SMS transaction data with:
- CRUD operations (GET, POST, PUT, DELETE)
- Basic Authentication
- XML parsing and JSON conversion
- Data Structures & Algorithms (DSA) integration
"""

import json
import xml.etree.ElementTree as ET
import base64
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import sys
sys.path.append('.')
from etl.parse_xml import SMSTransactionParser

class SMSDataProcessor:
    """Handles SMS data parsing and storage"""
    
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path
        self.transactions = []
        self.transaction_dict = {}  # For DSA comparison
        self.sms_parser = SMSTransactionParser(xml_file_path)
        self.load_data()
    
    def load_data(self):
        """Parse XML file and load transactions into memory"""
        try:
            print(f"Loading SMS data from: {self.xml_file_path}")
            
            # First try to load from pre-generated JSON file
            json_file = 'data/processed/transactions.json'
            if os.path.exists(json_file):
                print(f"Loading from pre-generated JSON: {json_file}")
                with open(json_file, 'r', encoding='utf-8') as f:
                    self.transactions = json.load(f)
            else:
                # Parse SMS records and extract transactions
                self.sms_parser.parse_xml()
                self.transactions = self.sms_parser.process_sms_to_transactions()
            
            # Build dictionary for fast lookups
            for tx in self.transactions:
                self.transaction_dict[tx['id']] = tx
            
            print(f"Loaded {len(self.transactions)} transactions")
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.transactions = []
            self.transaction_dict = {}
    
    def linear_search(self, transaction_id):
        """Linear search algorithm - O(n) complexity"""
        start_time = time.time()
        
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                end_time = time.time()
                return transaction, (end_time - start_time) * 1000  # Convert to milliseconds
        
        end_time = time.time()
        return None, (end_time - start_time) * 1000
    
    def dictionary_lookup(self, transaction_id):
        """Dictionary lookup algorithm - O(1) complexity"""
        start_time = time.time()
        
        result = self.transaction_dict.get(transaction_id)
        
        end_time = time.time()
        return result, (end_time - start_time) * 1000  # Convert to milliseconds
    
    def get_all_transactions(self):
        """Get all transactions"""
        return self.transactions
    
    def get_transaction_by_id(self, transaction_id):
        """Get transaction by ID using both algorithms for comparison"""
        # Try dictionary lookup first (faster)
        result_dict, time_dict = self.dictionary_lookup(transaction_id)
        
        # Also try linear search for comparison
        result_linear, time_linear = self.linear_search(transaction_id)
        
        return {
            'transaction': result_dict,
            'performance': {
                'dictionary_lookup': {
                    'result': result_dict is not None,
                    'time_ms': time_dict
                },
                'linear_search': {
                    'result': result_linear is not None,
                    'time_ms': time_linear
                }
            }
        }
    
    def add_transaction(self, transaction_data):
        """Add new transaction"""
        # Generate new ID
        new_id = max([tx['id'] for tx in self.transactions], default=0) + 1
        transaction_data['id'] = new_id
        
        self.transactions.append(transaction_data)
        self.transaction_dict[new_id] = transaction_data
        
        return transaction_data
    
    def update_transaction(self, transaction_id, update_data):
        """Update existing transaction"""
        if transaction_id in self.transaction_dict:
            # Update in list
            for i, tx in enumerate(self.transactions):
                if tx['id'] == transaction_id:
                    self.transactions[i].update(update_data)
                    break
            
            # Update in dictionary
            self.transaction_dict[transaction_id].update(update_data)
            return self.transaction_dict[transaction_id]
        
        return None
    
    def delete_transaction(self, transaction_id):
        """Delete transaction"""
        if transaction_id in self.transaction_dict:
            # Remove from list
            self.transactions = [tx for tx in self.transactions if tx['id'] != transaction_id]
            
            # Remove from dictionary
            deleted_tx = self.transaction_dict.pop(transaction_id)
            return deleted_tx
        
        return None

class AuthenticatedHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler with Basic Authentication"""
    
    def __init__(self, *args, **kwargs):
        # Hardcoded credentials for demonstration (in production, use proper auth)
        self.valid_credentials = {
            'admin': 'password123',
            'user': 'momo2024',
            'api': 'sms_data'
        }
        super().__init__(*args, **kwargs)
    
    def do_HEAD(self):
        """Handle HEAD requests"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if not self.authenticate():
            return
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/transactions':
            self.get_all_transactions()
        elif path.startswith('/transactions/'):
            transaction_id = int(path.split('/')[-1])
            self.get_transaction_by_id(transaction_id)
        elif path == '/performance':
            self.get_performance_comparison()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        if not self.authenticate():
            return
        
        if self.path == '/transactions':
            self.create_transaction()
        else:
            self.send_error(404, "Not Found")
    
    def do_PUT(self):
        """Handle PUT requests"""
        if not self.authenticate():
            return
        
        if self.path.startswith('/transactions/'):
            transaction_id = int(self.path.split('/')[-1])
            self.update_transaction(transaction_id)
        else:
            self.send_error(404, "Not Found")
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        if not self.authenticate():
            return
        
        if self.path.startswith('/transactions/'):
            transaction_id = int(self.path.split('/')[-1])
            self.delete_transaction(transaction_id)
        else:
            self.send_error(404, "Not Found")
    
    def authenticate(self):
        """Basic Authentication implementation"""
        auth_header = self.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Basic '):
            self.send_authenticate_header()
            return False
        
        try:
            # Decode base64 credentials
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            
            # Check credentials
            if username in self.valid_credentials and self.valid_credentials[username] == password:
                return True
            else:
                self.send_authenticate_header()
                return False
                
        except Exception as e:
            self.send_authenticate_header()
            return False
    
    def send_authenticate_header(self):
        """Send 401 Unauthorized response"""
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMo SMS API"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        error_response = {
            'error': 'Unauthorized',
            'message': 'Valid credentials required',
            'status_code': 401
        }
        self.wfile.write(json.dumps(error_response, indent=2).encode())
    
    def get_all_transactions(self):
        """GET /transactions - List all transactions"""
        try:
            transactions = self.server.sms_processor.get_all_transactions()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'success',
                'count': len(transactions),
                'transactions': transactions
            }
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def get_transaction_by_id(self, transaction_id):
        """GET /transactions/{id} - Get specific transaction"""
        try:
            result = self.server.sms_processor.get_transaction_by_id(transaction_id)
            
            if result['transaction']:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {
                    'status': 'success',
                    'transaction': result['transaction'],
                    'performance_analysis': result['performance']
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
            else:
                self.send_error(404, "Transaction not found")
                
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def create_transaction(self):
        """POST /transactions - Create new transaction"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            transaction_data = json.loads(post_data.decode('utf-8'))
            
            # Validate required fields
            required_fields = ['transaction_type', 'amount', 'currency', 'sender', 'receiver']
            for field in required_fields:
                if field not in transaction_data:
                    self.send_error(400, f"Missing required field: {field}")
                    return
            
            new_transaction = self.server.sms_processor.add_transaction(transaction_data)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'success',
                'message': 'Transaction created successfully',
                'transaction': new_transaction
            }
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def update_transaction(self, transaction_id):
        """PUT /transactions/{id} - Update transaction"""
        try:
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            update_data = json.loads(put_data.decode('utf-8'))
            
            updated_transaction = self.server.sms_processor.update_transaction(transaction_id, update_data)
            
            if updated_transaction:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {
                    'status': 'success',
                    'message': 'Transaction updated successfully',
                    'transaction': updated_transaction
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
            else:
                self.send_error(404, "Transaction not found")
                
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def delete_transaction(self, transaction_id):
        """DELETE /transactions/{id} - Delete transaction"""
        try:
            deleted_transaction = self.server.sms_processor.delete_transaction(transaction_id)
            
            if deleted_transaction:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {
                    'status': 'success',
                    'message': 'Transaction deleted successfully',
                    'deleted_transaction': deleted_transaction
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
            else:
                self.send_error(404, "Transaction not found")
                
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def get_performance_comparison(self):
        """GET /performance - Compare DSA algorithms"""
        try:
            # Test with multiple transaction IDs
            test_ids = [1, 5, 10, 15, 20]
            results = []
            
            for tx_id in test_ids:
                result = self.server.sms_processor.get_transaction_by_id(tx_id)
                results.append({
                    'transaction_id': tx_id,
                    'found': result['transaction'] is not None,
                    'performance': result['performance']
                })
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'success',
                'message': 'DSA Performance Comparison',
                'test_results': results,
                'analysis': {
                    'dictionary_lookup': 'O(1) - Constant time complexity',
                    'linear_search': 'O(n) - Linear time complexity',
                    'recommendation': 'Dictionary lookup is significantly faster for large datasets'
                }
            }
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

class SMSAPIServer(HTTPServer):
    """Custom HTTP Server with SMS data processor"""
    
    def __init__(self, server_address, RequestHandlerClass, xml_file_path):
        super().__init__(server_address, RequestHandlerClass)
        self.sms_processor = SMSDataProcessor(xml_file_path)

def main():
    """Main function to start the API server"""
    # Configuration
    HOST = 'localhost'
    PORT = 8000
    XML_FILE_PATH = 'data/raw/modified_sms_v2.xml'
    
    # Check if XML file exists
    if not os.path.exists(XML_FILE_PATH):
        print(f"Error: XML file not found at {XML_FILE_PATH}")
        print("Please ensure the modified_sms_v2.xml file exists in the data/raw/ directory")
        return
    
    # Create server
    server = SMSAPIServer((HOST, PORT), AuthenticatedHTTPRequestHandler, XML_FILE_PATH)
    
    print(f"MoMo SMS API Server starting...")
    print(f"Server running at http://{HOST}:{PORT}")
    print(f"Loaded {len(server.sms_processor.transactions)} transactions from XML")
    print(f"Authentication required - use Basic Auth")
    print(f"Available endpoints:")
    print(f"   GET    /transactions           - List all transactions")
    print(f"   GET    /transactions/{{id}}     - Get specific transaction")
    print(f"   POST   /transactions           - Create new transaction")
    print(f"   PUT    /transactions/{{id}}     - Update transaction")
    print(f"   DELETE /transactions/{{id}}     - Delete transaction")
    print(f"   GET    /performance            - DSA performance comparison")
    print(f"\nValid credentials:")
    print(f"   admin:password123")
    print(f"   user:momo2024")
    print(f"   api:sms_data")
    print(f"\nPress Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\nServer stopped")
        server.shutdown()

if __name__ == '__main__':
    main()
