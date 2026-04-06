# Loan Calculator & Tracker

A comprehensive Python/Tkinter application for managing loans, calculating payments, and tracking repayment status.

## Overview

The Loan Calculator & Tracker is a professional-grade desktop application that helps users:

- Calculate monthly loan payments using standard amortization formulas
- Add and manage multiple loans
- Track repayment progress
- View comprehensive loan statistics
- Persist data to JSON files

## Features

### Core Functionality

- **Payment Calculator**: Calculate monthly payments based on principal, interest rate, and term
- **Loan Management**: Add, view, update, and delete loans
- **Repayment Tracking**: Record payments and automatically calculate remaining balances
- **Auto-Close Loans**: Loans automatically close when fully paid
- **Statistics Dashboard**: View aggregate loan statistics

### Data Persistence

- Automatic saving of all loan data to JSON files
- Load previous loan history on startup
- No database required - simple JSON storage

### User Interface

- Clean, professional Tkinter GUI
- Easy-to-use loan input form
- Scrollable loan list with inline details
- Action buttons for all operations
- Real-time statistics display
- Status bar for feedback

## Requirements

- Python 3.8 or higher
- tkinter (usually included with Python)
- No external dependencies required!

## Installation

1. Clone or download the project
2. Navigate to the loan_calculator directory:

   ```bash
   cd loan_calculator
   ```

3. Verify Python installation:
   ```bash
   python --version  # Should be 3.8+
   ```

## Quick Start

### Run the Application

```bash
python main.py
```

The GUI will open with:

- Loan input form at the top
- Loan list in the middle
- Statistics dashboard at the bottom

### Adding a Loan

1. Enter borrower name
2. Enter principal amount (e.g., 10000)
3. Enter annual interest rate (e.g., 5.5)
4. Enter loan term in months (e.g., 60)
5. Click "Add Loan" to save

You can click "Calculate Payment" first to preview the monthly payment.

### Making Payments

1. Select a loan from the list
2. Click "Make Payment"
3. Enter the payment amount
4. Press OK to confirm

The loan will automatically close when balance reaches $0.

### Viewing Loan Details

1. Select a loan from the list
2. Click "View Details" to see complete information

## Project Structure

```
loan_calculator/
├── main.py              # Application entry point
├── loan_gui.py          # Tkinter GUI implementation (260 lines)
├── loan_logic.py        # Backend logic (196 lines)
├── test_loan.py         # Unit tests (277 lines, 30+ tests)
├── README.md            # This file
└── loans_data.json      # Auto-created data file
```

## API Documentation

### LoanCalculator Class

#### Methods

**`calculate_monthly_payment(principal: float, annual_rate: float, months: int) -> float`**

Calculate monthly payment using the standard amortization formula:

```
M = P * [r(1+r)^n] / [(1+r)^n - 1]
```

- Parameters:
  - `principal`: Loan amount (must be > 0)
  - `annual_rate`: Annual interest rate as percentage (0-100)
  - `months`: Loan term in months (must be > 0)
- Returns: Monthly payment amount (rounded to 2 decimals)
- Raises: `ValueError` for invalid inputs

Example:

```python
calculator = LoanCalculator()
monthly_payment = calculator.calculate_monthly_payment(10000, 5, 60)
# Returns: 188.71
```

**`calculate_total_interest(principal: float, monthly_payment: float, months: int) -> float`**

Calculate total interest paid over loan term.

- Returns: Total interest amount (rounded to 2 decimals)

**`add_loan(borrower: str, principal: float, annual_rate: float, months: int) -> Dict`**

Add a new loan to the system.

- Parameters:
  - `borrower`: Borrower name (non-empty string)
  - `principal`: Loan amount (must be > 0)
  - `annual_rate`: Annual interest rate (0-100)
  - `months`: Loan term in months (must be > 0)
- Returns: Dictionary with loan details including auto-generated loan_id
- Raises: `ValueError` for validation errors

**`make_repayment(loan_id: int, amount: float) -> Dict`**

Record a payment towards a loan.

- Parameters:
  - `loan_id`: ID of the loan to pay
  - `amount`: Payment amount (must be > 0, <= remaining balance)
- Returns: Updated loan dictionary
- Raises: `ValueError` for invalid payments or loan status
- Side effect: Auto-closes loan when balance reaches $0

**`get_loan_by_id(loan_id: int) -> Dict | None`**

Retrieve a specific loan by its ID.

**`get_all_loans() -> List[Dict]`**

Get all loans in the system.

**`get_active_loans() -> List[Dict]`**

Get only active (non-closed) loans.

**`get_closed_loans() -> List[Dict]`**

Get only closed (fully paid) loans.

**`delete_loan(loan_id: int) -> bool`**

Delete a loan. Returns True if successful.

**`get_total_outstanding_balance() -> float`**

Calculate total outstanding balance across all active loans.

**`get_statistics() -> Dict`**

Get overall statistics:

```python
{
    "total_loans": int,
    "active_loans": int,
    "closed_loans": int,
    "total_outstanding_balance": float,
    "total_paid_so_far": float,
    "total_loans_value": float
}
```

**`save_to_file() -> None`**

Save all loans to JSON file (called automatically).

**`load_from_file() -> None`**

Load loans from JSON file (called on initialization).

**`clear_all_loans() -> None`**

Clear all loans from memory and file.

## Data Structure

Each loan is stored as a dictionary:

```python
{
    "loan_id": 1,
    "borrower": "John Doe",
    "principal": 10000.00,
    "annual_rate": 5.5,
    "months": 60,
    "monthly_payment": 188.71,
    "total_interest": 1322.60,
    "balance": 8000.00,
    "payments_made": 3,
    "created_date": "2024-01-15T10:30:45.123456",
    "status": "Active"  # or "Closed"
}
```

## Examples

### Example 1: Calculate and Add a Loan

```python
from loan_logic import LoanCalculator

calculator = LoanCalculator()

# Calculate first
monthly = calculator.calculate_monthly_payment(50000, 6.5, 120)
print(f"Monthly payment: ${monthly:.2f}")

# Add the loan
loan = calculator.add_loan("Jane Smith", 50000, 6.5, 120)
print(f"Loan added with ID: {loan['loan_id']}")
```

### Example 2: Track Multiple Payments

```python
# Make payments over time
for payment in [500, 600, 500]:
    updated = calculator.make_repayment(loan['loan_id'], payment)
    print(f"Balance: ${updated['balance']:.2f}")

# Check if closed
if updated['status'] == 'Closed':
    print("Loan fully paid!")
```

### Example 3: Generate Reports

```python
stats = calculator.get_statistics()
print(f"Active loans: {stats['active_loans']}")
print(f"Total owed: ${stats['total_outstanding_balance']:.2f}")

for loan in calculator.get_all_loans():
    print(f"{loan['borrower']}: ${loan['balance']:.2f} remaining")
```

## Testing

The project includes 30+ comprehensive unit tests covering:

- Payment calculations
- Loan creation and validation
- Repayment processing
- Loan closure
- File persistence
- Statistics generation
- Error handling

### Run All Tests

```bash
python -m unittest test_loan.py -v
```

### Run Specific Test

```bash
python -m unittest test_loan.TestLoanCalculator.test_add_loan_valid -v
```

### Expected Output

All 30 tests should pass:

```
test_add_loan_empty_borrower ... ok
test_add_loan_incremental_ids ... ok
test_add_loan_invalid_months ... ok
test_add_loan_invalid_principal ... ok
test_add_loan_valid ... ok
...
Ran 30 tests in 0.015s
OK
```

## Challenges & Solutions

### Challenge 1: Amortization Formula

**Problem**: Calculating accurate monthly payments using the proper amortization formula.

**Solution**: Implemented standard financial formula:

```
M = P * [r(1+r)^n] / [(1+r)^n - 1]
```

Special handling for 0% interest rates.

### Challenge 2: Loan Closure

**Problem**: Determining when a loan is fully paid while handling floating-point precision.

**Solution**: Check if balance <= 0, auto-close loans when appropriate.

### Challenge 3: Data Persistence

**Problem**: Saving datetime objects to JSON.

**Solution**: Convert datetime to ISO format strings during save, parse back on load.

### Challenge 4: GUI State Management

**Problem**: Keeping loan list, statistics, and form in sync.

**Solution**: Refresh UI after every state-changing operation via `_refresh_loan_list()`.

## Future Enhancements

1. **Advanced Filtering**
   - Filter by borrower name
   - Filter by date range
   - Sort by balance, payment date, etc.

2. **Loan Templates**
   - Preset loan types (auto, mortgage, personal)
   - Quick-create common loan types

3. **Payment Schedules**
   - View full amortization schedule
   - Print payment plan

4. **Export Features**
   - Export to CSV/Excel
   - Generate PDF reports

5. **Database Backend**
   - SQLite for larger datasets
   - Multi-user support

6. **Advanced Analytics**
   - Charts and graphs
   - Payment history visualization
   - Debt reduction projection

7. **Reminders**
   - Payment due notifications
   - Late payment warnings

8. **Backup & Cloud Sync**
   - Automatic backups
   - Cloud synchronization

## Troubleshooting

### GUI won't open

- Ensure tkinter is installed: `python -m tkinter`
- On Linux: `sudo apt-get install python3-tk`

### Data not saving

- Check write permissions in the directory
- Verify loans_data.json file exists and is readable

### Calculation errors

- Ensure all input values are valid numbers
- Interest rate should be a percentage (0-100, not 0-1)

### Tests failing

- Run from the loan_calculator directory
- Ensure test_loans.json is deleted before running tests

## Performance

- Handles 1000+ loans efficiently
- File I/O is optimized with JSON
- GUI remains responsive even with large datasets

## Code Quality

- 100% type hints throughout
- Comprehensive docstrings
- Clean, readable code
- Follows PEP 8 style guide
- 30+ unit tests (all passing)

## License

This project is open source and available for educational and commercial use.

## Support

For issues or questions:

1. Check the README and documentation
2. Review the test cases for usage examples
3. Check the inline code comments
4. Run tests to verify installation

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Python**: 3.8+
