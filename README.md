# MoMo SMS Data Processing System

An enterprise-level system designed to process and manage Mobile Money (MoMo) transaction data received via SMS in XML format. This comprehensive solution includes database implementation, REST API with authentication, and performance analysis using Data Structures & Algorithms (DSA).

## 🚀 Project Overview

This system enables efficient storage, querying, and analysis of transaction data while maintaining data integrity and supporting future scalability. The project spans multiple weeks of development, from database design to API implementation.

## ✨ Features

### Database Foundation (Week 2)
- **MySQL Database**: Robust schema with proper relationships and constraints
- **Entity Relationship Design**: Clear ERD with transaction, user, and category entities
- **Data Integrity**: Foreign key constraints and validation rules
- **JSON Serialization**: Structured data modeling for API responses

### API Implementation (Current)
- **SMS Data Parsing**: Extracts transaction information from real SMS messages
- **REST API**: Complete CRUD operations for transaction management  
- **Authentication**: Basic Authentication with multiple user credentials
- **DSA Integration**: Performance comparison of search algorithms
- **Real Data Processing**: Works with actual MoMo SMS data (1,693 transactions)
- **Security Analysis**: Comprehensive documentation of authentication limitations

## Our Team
- Kevin Nizeyimana
- Arnaud Manzi Ineza
- Tuyishime Christian
- Katsia Teta
- Karigirwa Ange

## 📁 Project Structure

```
MoMo-SMS-data/
├── api/                    # REST API implementation
│   ├── app.py
│   ├── rest_api.py        # Main API server with authentication
│   ├── db.py              # Database connection utilities
│   └── schemas.py         # Data validation schemas
├── data/
│   ├── raw/               # Input data files
│   │   └── modified_sms_v2.xml    # Real SMS data (1,693 transactions)
│   └── processed/         # Processed JSON data
│       ├── transactions.json      # Parsed transaction data
│       └── dashboard.json         # Dashboard data
├── database/              # Database implementation
│   └── database_setup.sql # MySQL schema with sample data
├── docs/                  # Comprehensive documentation
│   ├── api_docs.md        # Complete API documentation
│   ├── database_design_document.md
│   ├── erd_diagram.md     # Entity Relationship Documentation
│   └── README.md
├── dsa/                   # Data Structures & Algorithms
│   ├── algorithms.py      # Performance analysis & comparisons
│   └── performance_report.json
├── etl/                   # Extract, Transform, Load
│   ├── parse_xml.py       # SMS parser for real data
│   ├── clean_normalize.py # Data cleaning utilities
│   ├── categorize.py      # Transaction categorization
│   └── run.py             # ETL pipeline runner
├── examples/              # Data examples and schemas
│   └── json_schemas.json  # JSON structure examples
├── scripts/               # Utility and testing scripts
│   ├── test_api.py        # Comprehensive API testing
│   ├── init_db.sh         # Database initialization
│   └── run_etl.sh         # ETL execution script
├── tests/                 # Test suites
│   ├── test_api.py        # API endpoint tests
│   ├── test_parse_xml.py  # XML parsing tests
│   └── test_categorize.py # Categorization tests
├── web/                   # Frontend dashboard
│   ├── dashboard.js       # Interactive dashboard
│   ├── chart_handler.js   # Data visualization
│   └── styles.css         # Dashboard styling
├── TESTING_COMMANDS.md    # Complete testing guide
├── start_api.bat         # Windows API starter
├── test_api.bat          # Windows API tester
└── index.html            # Main dashboard page
```

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- curl (for API testing)

### Installation

1. **Clone or download the project**
   ```bash
   cd MoMo-SMS-data-1
   ```

2. **Install dependencies** (if requirements.txt is populated)
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify data files**
   - Ensure `data/raw/modified_sms_v2.xml` contains your SMS data
   - Check that `data/processed/transactions.json` exists (sample data provided)

## Quick Start

> **Need Screenshots for Assignment?** 
> **Go directly to [TESTING_COMMANDS.md](TESTING_COMMANDS.md) for all required screenshot commands!**

### Option 1: Windows (Batch Files)

1. **Start the API server**
   ```cmd
   start_api.bat
   ```

2. **Test the API** (in a new terminal)
   ```cmd
   test_api.bat
   ```

### Option 2: Manual Python Execution

1. **Start the API server**
   ```bash
   python api/rest_api.py
   ```

2. **Test with curl**
   ```bash
   # Test authentication and get all transactions
   curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" http://localhost:8000/transactions
   ```

3. **Run Python tests**
   ```bash
   python scripts/test_api.py
   ```

## Authentication

The API uses Basic Authentication with these credentials:

| Username | Password     | Base64 Encoded                |
|----------|-------------|-------------------------------|
| admin    | password123 | YWRtaW46cGFzc3dvcmQxMjM=     |
| user     | momo2024    | dXNlcjptb21vMjAyNA==         |
| api      | sms_data    | YXBpOnNtc19kYXRh             |

## API Endpoints

| Method | Endpoint             | Description                    |
|--------|---------------------|--------------------------------|
| GET    | `/transactions`     | List all transactions         |
| GET    | `/transactions/{id}`| Get specific transaction      |
| POST   | `/transactions`     | Create new transaction        |
| PUT    | `/transactions/{id}`| Update transaction            |
| DELETE | `/transactions/{id}`| Delete transaction            |
| GET    | `/performance`      | DSA performance comparison    |

## Testing & Screenshots
<img width="1059" height="549" alt="Screenshot from 2025-10-02 17-59-07" src="https://github.com/user-attachments/assets/0adf0087-75ba-4922-8d0c-62f7d0e04039" />

### **For Assignment Screenshots**
**See [TESTING_COMMANDS.md](TESTING_COMMANDS.md) for complete testing instructions and all required screenshot commands!**

This file contains:
- Step-by-step setup instructions
- All 8 required screenshot commands with expected results
- Authentication details and troubleshooting
- Alternative testing methods (Postman, Browser, Python)

### Quick Testing Examples

### 1. Get All Transactions
```bash
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     http://localhost:8000/transactions
```

### 2. Get Specific Transaction
```bash
curl -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     http://localhost:8000/transactions/1
```

### 3. Create New Transaction
```bash
curl -X POST \
     -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
     -H "Content-Type: application/json" \
     -d '{"transaction_type":"send","amount":1500,"currency":"RWF","sender":"Test User","receiver":"Jane Doe"}' \
     http://localhost:8000/transactions
```

### 4. Test Invalid Credentials (should return 401)
```bash
curl -H "Authorization: Basic aW52YWxpZDpjcmVkZW50aWFscw==" \
     http://localhost:8000/transactions
```

## Data Structures & Algorithms (DSA)

This system implements and compares multiple search algorithms:

### Algorithms Implemented

1. **Linear Search - O(n)**
   - Sequential scan through all transactions
   - Simple but inefficient for large datasets

2. **Dictionary Lookup - O(1)**
   - Direct key access using Python dictionary
   - Fastest for frequent lookups

3. **Binary Search - O(log n)**
   - Divide and conquer on sorted data
   - Good balance between speed and memory

4. **Hash Table Search - O(1) average**
   - Custom implementation with collision resolution
   - Demonstrates hash table concepts

### Performance Comparison

The `/performance` endpoint provides real-time comparison of these algorithms on your transaction data.

## Security Analysis

### Basic Authentication Limitations

**Why Basic Auth is Weak:**
- Credentials are only base64 encoded, not encrypted
- No expiration mechanism
- Single factor authentication only
- Vulnerable to replay attacks
- No session management

**Better Alternatives:**
- **JWT (JSON Web Tokens)**: Stateless with built-in expiration
- **OAuth 2.0**: Industry standard with scoped permissions
- **API Keys**: Simple but more secure than Basic Auth
- **Multi-Factor Authentication**: Additional security layer

## SMS Data Processing

The system processes various types of MoMo SMS messages:

- **Money Received**: "You have received X RWF from..."
- **Payments**: "TxId: X. Your payment of Y RWF to..."
- **Money Transfers**: "*165*S*X RWF transferred to..."
- **Bank Deposits**: "*113*R*A bank deposit of X RWF..."
- **Airtime Purchases**: "*162*TxId:X*S*Your payment of Y RWF to Airtime..."

## 🎯 Project Milestones

### Week 2: Database Foundation ✅
**Objective**: Design and implement robust database schema

**Completed Deliverables:**
- ✅ **Entity Relationship Diagram (ERD)** - Complete database design
- ✅ **MySQL Database Schema** - Full DDL with constraints and relationships
- ✅ **JSON Data Modeling** - Structured serialization for API responses
- ✅ **Sample Data Population** - 5+ records per main table
- ✅ **Database Documentation** - Complete design rationale and data dictionary
- ✅ **CRUD Operations Testing** - Validated database functionality

**Database Architecture Features:**
- Primary and foreign key relationships
- CHECK constraints for data validation
- Indexes for performance optimization
- Referential integrity enforcement
- Comprehensive audit trails

### Current: API Implementation & DSA Analysis ✅
**Objective**: Build secure REST API with performance analysis

**Completed Deliverables:**

1. **Data Parsing & ETL**
   - ✅ Real SMS XML parsing (1,693 transactions)
   - ✅ Transaction extraction using regex patterns
   - ✅ JSON conversion with proper data types
   - ✅ Data cleaning and normalization

2. **REST API Implementation**  
   - ✅ All CRUD endpoints (GET, POST, PUT, DELETE)
   - ✅ Proper HTTP status codes and error handling
   - ✅ JSON request/response format
   - ✅ Performance monitoring endpoint

3. **Authentication & Security**
   - ✅ Basic Authentication implementation
   - ✅ Multiple valid credentials
   - ✅ 401 Unauthorized for invalid access
   - ✅ Comprehensive security analysis and recommendations

4. **API Documentation**
   - ✅ Complete endpoint documentation (`docs/api_docs.md`)
   - ✅ Request/response examples
   - ✅ Error codes and troubleshooting
   - ✅ Setup and testing instructions

5. **Data Structures & Algorithms (DSA)**
   - ✅ Linear search implementation - O(n)
   - ✅ Dictionary lookup implementation - O(1)
   - ✅ Binary search implementation - O(log n)
   - ✅ Hash table search with collision resolution
   - ✅ Performance comparison endpoint with real-time analysis
   - ✅ Efficiency analysis and recommendations

6. **Testing & Validation**
   - ✅ Automated test scripts (Python and Windows batch)
   - ✅ Manual testing examples with curl
   - ✅ Screenshot testing guide (`TESTING_COMMANDS.md`)
   - ✅ Comprehensive test coverage for all endpoints

## 📊 Technical Specifications

### Database Requirements Met:
- ✅ **MySQL Data Types**: Appropriate VARCHAR, INT, DECIMAL, DATETIME usage
- ✅ **Referential Integrity**: FOREIGN KEY constraints implementation
- ✅ **Data Validation**: CHECK constraints for business rules
- ✅ **Performance**: Indexes for optimized queries
- ✅ **Documentation**: Comprehensive table and column comments

### API Security Enhancements:
- ✅ **Authentication**: Multi-user Basic Auth with validation
- ✅ **Data Validation**: Input sanitization and type checking
- ✅ **Error Handling**: Proper HTTP status codes and messages
- ✅ **Security Analysis**: Documented limitations and improvements

### DSA Performance Metrics:
- **Linear Search**: O(n) - Average 0.045ms per search
- **Dictionary Lookup**: O(1) - Average 0.001ms per search  
- **Binary Search**: O(log n) - Average 0.009ms per search
- **Hash Table**: O(1) average - Custom implementation with collision handling

## 🔗 Project Resources

- **Architecture Diagram**: [System Design](https://drive.google.com/file/d/1Xa7DOjepNgDx9xvPfTrK3o_vju3nNNQe/view?usp=sharing)
- **Progress Board**: [GitHub Project](https://github.com/users/christiantuyishime01/projects/3/views/1)
- **Repository**: [GitHub Repository](https://github.com/christiantuyishime01/-MoMo-SMS-data.git)

## 🎓 Academic Context

This project demonstrates enterprise-level software development practices including:
- **Database Design**: Professional ERD and schema implementation
- **API Development**: RESTful services with proper authentication
- **Algorithm Analysis**: Practical DSA implementation and performance comparison
- **Testing Methodology**: Comprehensive validation and documentation
- **Team Collaboration**: GitHub workflow and project management

## 📞 Support & Documentation

For technical issues or questions:
1. **API Documentation**: Complete guide in `docs/api_docs.md`
2. **Testing Guide**: Step-by-step instructions in `TESTING_COMMANDS.md`
3. **Database Documentation**: Schema details in `database/database_setup.sql`
4. **Error Resolution**: Check server console and documentation

## 🚀 Quality Assurance

### Testing Performed:
- ✅ **Schema Validation**: Database constraints and relationships
- ✅ **API Endpoint Testing**: All CRUD operations validated
- ✅ **Authentication Testing**: Valid and invalid credential scenarios
- ✅ **Performance Testing**: DSA algorithm comparison and analysis
- ✅ **Integration Testing**: End-to-end workflow validation

---

**System Status**: ✅ **Production Ready** - This system successfully processes real MoMo SMS data (1,693 transactions) and provides a secure, efficient API for transaction management with comprehensive database foundation and DSA performance analysis.
