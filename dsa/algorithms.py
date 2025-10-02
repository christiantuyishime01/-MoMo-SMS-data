#!/usr/bin/env python3
"""
Data Structures & Algorithms (DSA) Module
MoMo SMS Data Processing System - Week 2

This module implements and compares different search algorithms:
1. Linear Search - O(n) complexity
2. Dictionary Lookup - O(1) complexity
3. Binary Search - O(log n) complexity (bonus)
4. Hash Table implementation (bonus)

Performance comparison and analysis for transaction data.
"""

import time
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Tuple
import sys
sys.path.append('.')
from etl.parse_xml import SMSTransactionParser

class DSAPerformanceAnalyzer:
    """Analyzes performance of different search algorithms"""
    
    def __init__(self, xml_file_path: str):
        self.xml_file_path = xml_file_path
        self.transactions = []
        self.transaction_dict = {}
        self.sorted_transactions = []
        self.sms_parser = SMSTransactionParser(xml_file_path)
        self.load_data()
    
    def load_data(self):
        """Load transaction data from XML file"""
        try:
            print(f"Loading SMS data for DSA analysis from: {self.xml_file_path}")
            
            # Parse SMS records and extract transactions
            self.sms_parser.parse_xml()
            self.transactions = self.sms_parser.process_sms_to_transactions()
            
            # Build dictionary for fast lookups
            for tx in self.transactions:
                self.transaction_dict[tx['id']] = tx
            
            # Create sorted list for binary search
            self.sorted_transactions = sorted(self.transactions, key=lambda x: x['id'])
            
            print(f"Loaded {len(self.transactions)} transactions for DSA analysis")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            self.transactions = []
            self.transaction_dict = {}
            self.sorted_transactions = []
    
    def linear_search(self, transaction_id: int) -> Tuple[Optional[Dict], float]:
        """
        Linear Search Algorithm - O(n) complexity
        Scans through the list sequentially until target is found
        """
        start_time = time.time()
        
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                end_time = time.time()
                return transaction, (end_time - start_time) * 1000  # Convert to milliseconds
        
        end_time = time.time()
        return None, (end_time - start_time) * 1000
    
    def dictionary_lookup(self, transaction_id: int) -> Tuple[Optional[Dict], float]:
        """
        Dictionary Lookup Algorithm - O(1) complexity
        Direct key access in hash table
        """
        start_time = time.time()
        
        result = self.transaction_dict.get(transaction_id)
        
        end_time = time.time()
        return result, (end_time - start_time) * 1000  # Convert to milliseconds
    
    def binary_search(self, transaction_id: int) -> Tuple[Optional[Dict], float]:
        """
        Binary Search Algorithm - O(log n) complexity
        Searches in sorted array by repeatedly dividing search space
        """
        start_time = time.time()
        
        left, right = 0, len(self.sorted_transactions) - 1
        
        while left <= right:
            mid = (left + right) // 2
            mid_transaction = self.sorted_transactions[mid]
            
            if mid_transaction['id'] == transaction_id:
                end_time = time.time()
                return mid_transaction, (end_time - start_time) * 1000
            
            elif mid_transaction['id'] < transaction_id:
                left = mid + 1
            else:
                right = mid - 1
        
        end_time = time.time()
        return None, (end_time - start_time) * 1000
    
    def hash_table_search(self, transaction_id: int) -> Tuple[Optional[Dict], float]:
        """
        Custom Hash Table Implementation
        Demonstrates hash table concept with collision handling
        """
        start_time = time.time()
        
        # Simple hash function
        hash_value = transaction_id % len(self.transactions) if self.transactions else 0
        
        # Linear probing for collision resolution
        for i in range(len(self.transactions)):
            index = (hash_value + i) % len(self.transactions)
            if self.transactions[index]['id'] == transaction_id:
                end_time = time.time()
                return self.transactions[index], (end_time - start_time) * 1000
        
        end_time = time.time()
        return None, (end_time - start_time) * 1000
    
    def compare_algorithms(self, test_ids: List[int]) -> Dict[str, Any]:
        """
        Compare performance of all algorithms with given test IDs
        """
        results = {
            'linear_search': {'times': [], 'total_time': 0, 'success_count': 0},
            'dictionary_lookup': {'times': [], 'total_time': 0, 'success_count': 0},
            'binary_search': {'times': [], 'total_time': 0, 'success_count': 0},
            'hash_table_search': {'times': [], 'total_time': 0, 'success_count': 0}
        }
        
        for tx_id in test_ids:
            # Test Linear Search
            result, time_taken = self.linear_search(tx_id)
            results['linear_search']['times'].append(time_taken)
            results['linear_search']['total_time'] += time_taken
            if result:
                results['linear_search']['success_count'] += 1
            
            # Test Dictionary Lookup
            result, time_taken = self.dictionary_lookup(tx_id)
            results['dictionary_lookup']['times'].append(time_taken)
            results['dictionary_lookup']['total_time'] += time_taken
            if result:
                results['dictionary_lookup']['success_count'] += 1
            
            # Test Binary Search
            result, time_taken = self.binary_search(tx_id)
            results['binary_search']['times'].append(time_taken)
            results['binary_search']['total_time'] += time_taken
            if result:
                results['binary_search']['success_count'] += 1
            
            # Test Hash Table Search
            result, time_taken = self.hash_table_search(tx_id)
            results['hash_table_search']['times'].append(time_taken)
            results['hash_table_search']['total_time'] += time_taken
            if result:
                results['hash_table_search']['success_count'] += 1
        
        # Calculate averages
        for algorithm in results:
            if results[algorithm]['times']:
                results[algorithm]['average_time'] = results[algorithm]['total_time'] / len(results[algorithm]['times'])
                results[algorithm]['min_time'] = min(results[algorithm]['times'])
                results[algorithm]['max_time'] = max(results[algorithm]['times'])
            else:
                results[algorithm]['average_time'] = 0
                results[algorithm]['min_time'] = 0
                results[algorithm]['max_time'] = 0
        
        return results
    
    def generate_performance_report(self, test_ids: List[int]) -> Dict[str, Any]:
        """
        Generate comprehensive performance analysis report
        """
        results = self.compare_algorithms(test_ids)
        
        # Find fastest algorithm
        fastest_algorithm = min(results.keys(), key=lambda k: results[k]['average_time'])
        
        # Calculate speedup ratios
        baseline_time = results['linear_search']['average_time']
        speedup_ratios = {}
        
        for algorithm in results:
            if baseline_time > 0:
                speedup_ratios[algorithm] = baseline_time / results[algorithm]['average_time']
            else:
                speedup_ratios[algorithm] = 1
        
        report = {
            'test_parameters': {
                'total_transactions': len(self.transactions),
                'test_ids': test_ids,
                'test_count': len(test_ids)
            },
            'performance_results': results,
            'analysis': {
                'fastest_algorithm': fastest_algorithm,
                'speedup_ratios': speedup_ratios,
                'recommendations': self._generate_recommendations(results, speedup_ratios)
            },
            'algorithm_complexity': {
                'linear_search': 'O(n) - Linear time complexity',
                'dictionary_lookup': 'O(1) - Constant time complexity',
                'binary_search': 'O(log n) - Logarithmic time complexity',
                'hash_table_search': 'O(1) average, O(n) worst case'
            }
        }
        
        return report
    
    def _generate_recommendations(self, results: Dict, speedup_ratios: Dict) -> List[str]:
        """Generate algorithm recommendations based on performance data"""
        recommendations = []
        
        # Dictionary lookup analysis
        if speedup_ratios.get('dictionary_lookup', 0) > 10:
            recommendations.append(
                "Dictionary lookup is significantly faster than linear search. "
                "Use for frequent lookups by ID."
            )
        
        # Binary search analysis
        if speedup_ratios.get('binary_search', 0) > 2:
            recommendations.append(
                "Binary search provides good performance for sorted data. "
                "Consider using when data is already sorted."
            )
        
        # Hash table analysis
        if speedup_ratios.get('hash_table_search', 0) > 5:
            recommendations.append(
                "Hash table search shows good performance. "
                "Consider for large datasets with frequent lookups."
            )
        
        # General recommendations
        if len(self.transactions) > 1000:
            recommendations.append(
                "For large datasets (>1000 records), avoid linear search. "
                "Use dictionary lookup or hash tables for better performance."
            )
        
        if not recommendations:
            recommendations.append("All algorithms perform similarly for small datasets.")
        
        return recommendations

def run_dsa_analysis(xml_file_path: str, test_ids: List[int] = None) -> Dict[str, Any]:
    """
    Run complete DSA analysis on SMS transaction data
    
    Args:
        xml_file_path: Path to the XML data file
        test_ids: List of transaction IDs to test (default: random selection)
    
    Returns:
        Complete performance analysis report
    """
    analyzer = DSAPerformanceAnalyzer(xml_file_path)
    
    if not test_ids:
        # Default test IDs (first 10 transaction IDs from actual data)
        test_ids = [tx['id'] for tx in analyzer.transactions[:10]] if analyzer.transactions else []
    
    return analyzer.generate_performance_report(test_ids)

def main():
    """Main function to run DSA analysis"""
    xml_file_path = 'data/raw/modified_sms_v2.xml'
    
    print("DSA Performance Analysis Starting...")
    print(f"Analyzing data from: {xml_file_path}")
    
    # Run analysis
    report = run_dsa_analysis(xml_file_path)
    
    # Display results
    print("\nPERFORMANCE ANALYSIS RESULTS")
    print("=" * 50)
    
    print(f"\nTest Parameters:")
    print(f"   Total Transactions: {report['test_parameters']['total_transactions']}")
    print(f"   Test IDs: {report['test_parameters']['test_ids']}")
    print(f"   Test Count: {report['test_parameters']['test_count']}")
    
    print(f"\nPerformance Results (Average Time in ms):")
    for algorithm, data in report['performance_results'].items():
        print(f"   {algorithm.replace('_', ' ').title()}: {data['average_time']:.4f}ms")
    
    print(f"\nFastest Algorithm: {report['analysis']['fastest_algorithm'].replace('_', ' ').title()}")
    
    print(f"\nSpeedup Ratios (vs Linear Search):")
    for algorithm, ratio in report['analysis']['speedup_ratios'].items():
        print(f"   {algorithm.replace('_', ' ').title()}: {ratio:.2f}x")
    
    print(f"\nRecommendations:")
    for i, recommendation in enumerate(report['analysis']['recommendations'], 1):
        print(f"   {i}. {recommendation}")
    
    print(f"\nAlgorithm Complexity:")
    for algorithm, complexity in report['algorithm_complexity'].items():
        print(f"   {algorithm.replace('_', ' ').title()}: {complexity}")
    
    # Save detailed report
    report_file = 'dsa/performance_report.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed report saved to: {report_file}")
    
    return report

if __name__ == '__main__':
    main()
