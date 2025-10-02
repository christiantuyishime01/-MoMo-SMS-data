#!/usr/bin/env python3
"""
Simple test script to run the SMS parser and generate transaction data
"""

from etl.parse_xml import SMSTransactionParser

def test_parser():
    """Test the SMS parser with the real data"""
    xml_file_path = 'data/raw/modified_sms_v2.xml'
    output_file = 'data/processed/transactions.json'
    
    print("Testing SMS Transaction Parser...")
    print(f"Input file: {xml_file_path}")
    print(f"Output file: {output_file}")
    
    try:
        # Initialize parser
        parser = SMSTransactionParser(xml_file_path)
        
        # Parse XML file
        sms_records = parser.parse_xml()
        print(f"Parsed {len(sms_records)} SMS records")
        
        if not sms_records:
            print("No SMS records found")
            return False
        
        # Convert SMS to transactions
        transactions = parser.process_sms_to_transactions()
        print(f"Extracted {len(transactions)} transactions")
        
        if not transactions:
            print("No transactions extracted")
            return False
        
        # Save to JSON
        parser.save_to_json(output_file)
        
        # Show first few transactions
        print("\nFirst 5 transactions:")
        for i, tx in enumerate(transactions[:5]):
            print(f"  {i+1}. ID:{tx['id']} | {tx['transaction_type']} | {tx['amount']} {tx['currency']} | {tx['timestamp'][:19]}")
        
        # Show transaction type distribution
        tx_types = {}
        for tx in transactions:
            tx_type = tx['transaction_type']
            tx_types[tx_type] = tx_types.get(tx_type, 0) + 1
        
        print(f"\nTransaction Types:")
        for tx_type, count in tx_types.items():
            print(f"  {tx_type}: {count}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_parser()
    if success:
        print("\n✅ Parser test completed successfully!")
    else:
        print("\n❌ Parser test failed!")
