# EMI Management System

A functional programming-based EMI (Equated Monthly Installment) tracking system for loan management in Python. This project demonstrates pure functional programming principles without using Object-Oriented Programming.

## Features

### Core Calculations
- ✅ **EMI Calculation** - Calculate monthly EMI using the standard formula
- ✅ **Amortization Schedule** - Generate complete month-by-month loan breakdown
- ✅ **Interest Calculations** - Track monthly and total interest
- ✅ **Prepayment Analysis** - Calculate savings from early repayment
- ✅ **Loan Summary** - Get comprehensive loan overview

### Payment Tracking
- 📊 **Payment Recording** - Record individual loan payments
- 📈 **Payment History** - View complete payment history
- 💰 **Balance Calculation** - Track remaining loan balance
- 📅 **Payment Summary** - Aggregate payment statistics

### Reports
- 📋 **Yearly Report** - Annual breakdown of payments
- 📆 **Payoff Date Calculation** - Estimate loan completion date
- 🔍 **Payment Filtering** - Filter payments by date range

### Data Persistence
- 💾 **JSON Storage** - Save and load loan data
- 📝 **Payment History** - Persistent payment records
- 🔄 **Data Management** - Easy data retrieval and updates

## Project Structure

```
emi-management-system/
├── main.py                  # Entry point and demo
├── loan_calculator.py       # Core EMI calculation functions
├── config.py               # Configuration constants
├── utils/
│   ├── __init__.py
│   ├── validation.py       # Input validation functions
│   ├── formatters.py       # Display formatting functions
│   └── data_handler.py     # File I/O functions
├── processors/
│   ├── __init__.py
│   ├── payment_tracker.py  # Payment tracking functions
│   └── report_generator.py # Report generation functions
└── README.md
```

## Functional Programming Concepts Used

### 1. **Pure Functions**
Functions with no side effects that return the same output for the same input.
```python
def calculate_emi(principal, annual_rate, tenure_months) -> float:
    # No state modification, deterministic output
    ...
```

### 2. **Higher-Order Functions**
Functions that take or return other functions.
```python
def calculate_month(accumulator, month_num):
    # Inner function used with reduce
    ...
```

### 3. **Function Composition**
Combining functions to create new functionality.
```python
# Calculate total from payments using composition
total = calculate_total_paid(payments)
balance = calculate_balance_after_payments(principal, payments)
```

### 4. **Immutability & Reduce**
Using `reduce()` to accumulate results without state mutation.
```python
schedule = reduce(
    calculate_month,
    range(1, tenure_months + 1),
    ([], principal)
)
```

### 5. **Filter & Map**
Functional data transformation.
```python
errors = [msg for is_valid, msg in validators if not is_valid]
filtered_payments = list(filter(
    lambda p: start_date <= p["date"] <= end_date,
    payments
))
```

### 6. **First-Class Functions**
Passing functions as arguments and returning them.
```python
validators = [
    validate_principal(principal),
    validate_interest_rate(rate),
    validate_tenure(months)
]
```

## Installation

```bash
# Clone the repository
git clone https://github.com/dhruvdogaya03/emi-management-system.git

# Navigate to directory
cd emi-management-system

# No external dependencies required! Uses only Python standard library.
```

## Usage

### Run the Demo
```bash
python main.py
```

### Create a New Loan
```python
from main import create_new_loan

loan = create_new_loan(
    principal=500000,
    annual_rate=8.5,
    tenure_months=60
)
```

### View Loan Details
```python
from main import view_loan

view_loan(loan_id="a1b2c3d4")
```

### View Amortization Schedule
```python
from main import view_amortization_schedule

# View first 6 months
view_amortization_schedule(loan_id="a1b2c3d4", limit=6)

# View all months
view_amortization_schedule(loan_id="a1b2c3d4")
```

### Record a Payment
```python
from main import record_loan_payment

record_loan_payment(
    loan_id="a1b2c3d4",
    amount=10000,
    payment_date="2024-01-15"
)
```

### View Payment History
```python
from main import view_payment_history

view_payment_history(loan_id="a1b2c3d4")
```

## Key Functions

### Loan Calculation Module

| Function | Purpose |
|----------|----------|
| `calculate_emi()` | Calculate monthly EMI |
| `calculate_total_interest()` | Calculate total interest payable |
| `calculate_monthly_interest()` | Calculate interest for a month |
| `calculate_principal_component()` | Get principal portion of EMI |
| `generate_amortization_schedule()` | Create complete payment schedule |
| `calculate_loan_summary()` | Get loan overview |
| `calculate_prepayment_savings()` | Calculate early repayment benefits |

### Validation Module

| Function | Purpose |
|----------|----------|
| `validate_principal()` | Validate loan amount |
| `validate_interest_rate()` | Validate interest rate |
| `validate_tenure()` | Validate loan tenure |
| `validate_all()` | Validate all parameters |

### Data Handler Module

| Function | Purpose |
|----------|----------|
| `read_json_file()` | Read JSON safely |
| `write_json_file()` | Write JSON safely |
| `save_loan()` | Persist loan data |
| `load_loan()` | Retrieve loan data |
| `save_payment()` | Record payment |
| `get_payment_history()` | Retrieve payment records |

## Example Output

```
==================================================
LOAN SUMMARY
==================================================
Principal Amount:        ₹500,000.00
Annual Interest Rate:    8.50%
Loan Tenure:             60 months
--------------------------------------------------
Monthly EMI:             ₹10,036.13
Total Interest:          ₹102,167.78
Total Amount Payable:    ₹602,167.78
==================================================

Month    EMI             Principal       Interest        Balance
------- -------- -------- -------- -------- --------
1        ₹10,036.13  ₹6,481.13    ₹3,555.00    ₹493,518.87
2        ₹10,036.13  ₹6,532.82    ₹3,503.31    ₹486,986.05
...
```

## Configuration

Edit `config.py` to customize:
- Default interest rate
- Default loan tenure
- Currency symbol
- Decimal places for display
- File paths for data storage

## Testing

Run the demo to test all functionality:
```bash
python main.py
```

## No External Dependencies

This project uses only Python standard library:
- `math` - Mathematical calculations
- `json` - Data persistence
- `functools` - Functional utilities (reduce)
- `pathlib` - File path handling
- `datetime` - Date/time operations
- `uuid` - Unique ID generation

## Why Functional Programming?

### Advantages
- ✅ **Predictability** - Pure functions always produce same output
- ✅ **Testability** - Easy to unit test without mocking state
- ✅ **Reusability** - Functions can be composed easily
- ✅ **Maintainability** - Less complexity, easier to reason about
- ✅ **Concurrency** - No shared state issues
- ✅ **Debugging** - Easier to trace execution path

### When to Use
- Data transformation pipelines
- Mathematical calculations (like EMI)
- Report generation
- Data validation
- Stateless operations

## Future Enhancements

- [ ] CLI interface for interactive usage
- [ ] Support for floating-rate loans
- [ ] Comparison tools for different loan options
- [ ] EMI reduction calculator
- [ ] Loan comparison matrix
- [ ] Export to CSV/PDF
- [ ] Web API using Flask/FastAPI
- [ ] Database integration

## License

MIT License - Feel free to use and modify

## Author

Created by [dhruvdogaya03](https://github.com/dhruvdogaya03)

---

**Made with ❤️ using Functional Programming**
