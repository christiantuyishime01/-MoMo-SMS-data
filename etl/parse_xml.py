#!/usr/bin/env python3
"""
SMS XML Parser for MoMo Transaction Data
"""

import xml.etree.ElementTree as ET
import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class SMSTransactionParser:
    """Parses SMS messages to extract mobile money transaction data"""
    
    def __init__(self, xml_file_path: str):
        self.xml_file_path = xml_file_path
        self.transactions = []
        self.sms_records = []
        
    def parse_xml(self) -> List[Dict[str, Any]]:
        """Parse SMS XML file and extract SMS records"""
        try:
            tree = ET.parse(self.xml_file_path)
            root = tree.getroot()
            
            print(f"Root element: {root.tag}")
            print(f"Total SMS count: {root.get('count', 'Unknown')}")
            
            for sms in root.findall('sms'):
                sms_data = {
                    'protocol': sms.get('protocol'),
                    'address': sms.get('address'),
                    'date': sms.get('date'),
                    'type': sms.get('type'),
                    'subject': sms.get('subject'),
                    'body': sms.get('body'),
                    'readable_date': sms.get('readable_date'),
                    'contact_name': sms.get('contact_name')
                }
                self.sms_records.append(sms_data)
            
            print(f"Parsed {len(self.sms_records)} SMS records")
            return self.sms_records
            
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return []
    
    def extract_transaction_info(self, sms_body: str) -> Optional[Dict[str, Any]]:
        """Extract transaction information from SMS body text"""
        if not sms_body:
            return None
        
        transaction_info = {
            'transaction_type': 'unknown',
            'amount': 0.0,
            'currency': 'RWF',
            'sender': '',
            'receiver': '',
            'reference_number': '',
            'balance': 0.0,
            'fee': 0.0,
            'message': sms_body
        }
        
        # Pattern 1: Money received
        receive_pattern = r"You have received (\d+(?:,\d+)*) (\w+) from ([^(]+) \(\*+(\d+)\).*?Your new balance:(\d+(?:,\d+)*) (\w+).*?Transaction Id: (\d+)"
        receive_match = re.search(receive_pattern, sms_body)
        
        if receive_match:
            transaction_info.update({
                'transaction_type': 'receive',
                'amount': float(receive_match.group(1).replace(',', '')),
                'currency': receive_match.group(2),
                'sender': receive_match.group(3).strip(),
                'balance': float(receive_match.group(5).replace(',', '')),
                'reference_number': receive_match.group(7)
            })
            return transaction_info
        
        # Pattern 2: Payment to someone
        payment_pattern = r"TxId: (\d+)\. Your payment of ([\d,]+) (\w+) to ([^0-9]+)(\d+) has been completed.*?Your new balance: ([\d,]+) (\w+)\. Fee was (\d+) (\w+)"
        payment_match = re.search(payment_pattern, sms_body)
        
        if payment_match:
            transaction_info.update({
                'transaction_type': 'payment',
                'reference_number': payment_match.group(1),
                'amount': float(payment_match.group(2).replace(',', '')),
                'currency': payment_match.group(3),
                'receiver': payment_match.group(4).strip(),
                'balance': float(payment_match.group(6).replace(',', '')),
                'fee': float(payment_match.group(8))
            })
            return transaction_info
        
        # Pattern 3: Money transfer
        transfer_pattern = r"\*165\*S\*([\d,]+) (\w+) transferred to ([^(]+) \((\d+)\) from (\d+).*?Fee was: (\d+) (\w+)\. New balance: ([\d,]+) (\w+)"
        transfer_match = re.search(transfer_pattern, sms_body)
        
        if transfer_match:
            transaction_info.update({
                'transaction_type': 'transfer',
                'amount': float(transfer_match.group(1).replace(',', '')),
                'currency': transfer_match.group(2),
                'receiver': transfer_match.group(3).strip(),
                'fee': float(transfer_match.group(6)),
                'balance': float(transfer_match.group(8).replace(',', ''))
            })
            return transaction_info
        
        # Pattern 4: Bank deposit
        deposit_pattern = r"\*113\*R\*A bank deposit of ([\d,]+) (\w+) has been added.*?Your NEW BALANCE :([\d,]+) (\w+)"
        deposit_match = re.search(deposit_pattern, sms_body)
        
        if deposit_match:
            transaction_info.update({
                'transaction_type': 'deposit',
                'amount': float(deposit_match.group(1).replace(',', '')),
                'currency': deposit_match.group(2),
                'balance': float(deposit_match.group(3).replace(',', '')),
                'sender': 'Bank',
                'receiver': 'Self'
            })
            return transaction_info
        
        return transaction_info
    
    def process_sms_to_transactions(self) -> List[Dict[str, Any]]:
        """Convert SMS records to transaction records"""
        transactions = []
        transaction_id = 1
        
        for sms in self.sms_records:
            # Only process M-Money SMS messages
            if sms.get('address') == 'M-Money':
                transaction_info = self.extract_transaction_info(sms.get('body', ''))
                
                if transaction_info and transaction_info['transaction_type'] != 'unknown':
                    # Convert timestamp
                    timestamp = sms.get('date')
                    if timestamp:
                        try:
                            # Convert milliseconds timestamp to readable format
                            dt = datetime.fromtimestamp(int(timestamp) / 1000)
                            formatted_timestamp = dt.isoformat()
                        except:
                            formatted_timestamp = sms.get('readable_date', timestamp)
                    else:
                        formatted_timestamp = sms.get('readable_date', '')
                    
                    transaction = {
                        'id': transaction_id,
                        'transaction_type': transaction_info['transaction_type'],
                        'amount': transaction_info['amount'],
                        'currency': transaction_info.get('currency', 'RWF'),
                        'sender': transaction_info.get('sender', ''),
                        'receiver': transaction_info.get('receiver', ''),
                        'timestamp': formatted_timestamp,
                        'status': 'completed',
                        'reference_number': transaction_info.get('reference_number', ''),
                        'balance': transaction_info.get('balance', 0.0),
                        'fee': transaction_info.get('fee', 0.0),
                        'message': transaction_info['message']
                    }
                    
                    transactions.append(transaction)
                    transaction_id += 1
        
        self.transactions = transactions
        print(f"Extracted {len(transactions)} transactions from SMS records")
        return transactions
    
    def save_to_json(self, output_file: str):
        """Save transactions to JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.transactions, f, indent=2, ensure_ascii=False)
            print(f"Transactions saved to {output_file}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")

def main():
    """Main function to run SMS parsing"""
    xml_file_path = 'data/raw/modified_sms_v2.xml'
    output_file = 'data/processed/transactions.json'
    
    print("SMS Transaction Parser Starting...")
    
    # Initialize parser
    parser = SMSTransactionParser(xml_file_path)
    
    # Parse XML file
    sms_records = parser.parse_xml()
    
    if not sms_records:
        print("No SMS records found")
        return
    
    # Convert SMS to transactions
    transactions = parser.process_sms_to_transactions()
    
    # Save to JSON
    parser.save_to_json(output_file)
    
    print(f"Processed {len(transactions)} transactions")
    return transactions

if __name__ == '__main__':
    main()
