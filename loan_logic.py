import json
import os
from typing import List, Dict, Tuple
from datetime import datetime


class LoanCalculator:
    """Backend logic for loan calculator and tracker."""

    def __init__(self, data_file: str = "loans_data.json") -> None:
        """Initialize the loan calculator with data file path."""
        self.data_file: str = data_file
        self.loans: List[Dict] = []
        self.load_from_file()

    def calculate_monthly_payment(self, principal: float, annual_rate: float, months: int) -> float:
        """
        Calculate monthly payment using standard amortization formula.

        Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        Where:
            M = Monthly payment
            P = Principal amount
            r = Monthly interest rate (annual_rate / 12 / 100)
            n = Number of months
        """
        if months <= 0:
            raise ValueError("Months must be greater than 0")
        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if principal <= 0:
            raise ValueError("Principal must be greater than 0")

        monthly_rate: float = annual_rate / 12 / 100
        
        # If no interest, simple division
        if monthly_rate == 0:
            return principal / months
        
        # Standard amortization formula
        numerator: float = monthly_rate * ((1 + monthly_rate) ** months)
        denominator: float = ((1 + monthly_rate) ** months) - 1
        monthly_payment: float = principal * (numerator / denominator)
        
        return round(monthly_payment, 2)

    def calculate_total_interest(self, principal: float, monthly_payment: float, months: int) -> float:
        """Calculate total interest paid over the loan period."""
        total_paid: float = monthly_payment * months
        total_interest: float = total_paid - principal
        return round(total_interest, 2)

    def add_loan(self, borrower: str, principal: float, annual_rate: float, months: int) -> Dict:
        """
        Add a new loan to the system.
        
        Returns the loan dictionary with calculated monthly payment and ID.
        """
        if not borrower or not borrower.strip():
            raise ValueError("Borrower name cannot be empty")
        if principal <= 0:
            raise ValueError("Principal must be greater than 0")
        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if months <= 0:
            raise ValueError("Months must be greater than 0")

        # Generate loan ID (simple incrementing ID based on existing loans)
        loan_id: int = max([loan["loan_id"] for loan in self.loans], default=0) + 1

        # Calculate monthly payment
        monthly_payment: float = self.calculate_monthly_payment(principal, annual_rate, months)
        total_interest: float = self.calculate_total_interest(principal, monthly_payment, months)

        loan: Dict = {
            "loan_id": loan_id,
            "borrower": borrower.strip(),
            "principal": round(principal, 2),
            "annual_rate": round(annual_rate, 2),
            "months": months,
            "monthly_payment": monthly_payment,
            "total_interest": total_interest,
            "balance": round(principal, 2),
            "payments_made": 0,
            "created_date": datetime.now().isoformat(),
            "status": "Active"
        }

        self.loans.append(loan)
        self.save_to_file()
        return loan

    def make_repayment(self, loan_id: int, amount: float) -> Dict:
        """
        Make a repayment towards a loan.
        
        Returns updated loan dictionary.
        """
        loan: Dict | None = self.get_loan_by_id(loan_id)
        if not loan:
            raise ValueError(f"Loan with ID {loan_id} not found")
        
        if amount <= 0:
            raise ValueError("Payment amount must be greater than 0")
        
        if loan["status"] == "Closed":
            raise ValueError("Cannot make payment on a closed loan")
        
        if amount > loan["balance"]:
            raise ValueError(f"Payment exceeds remaining balance of {loan['balance']}")

        loan["balance"] = round(loan["balance"] - amount, 2)
        loan["payments_made"] += 1

        # Auto-close loan if fully paid
        if loan["balance"] <= 0:
            loan["status"] = "Closed"
            loan["balance"] = 0

        self.save_to_file()
        return loan

    def get_loan_by_id(self, loan_id: int) -> Dict | None:
        """Get a loan by its ID."""
        for loan in self.loans:
            if loan["loan_id"] == loan_id:
                return loan
        return None

    def get_all_loans(self) -> List[Dict]:
        """Get all loans."""
        return self.loans

    def get_active_loans(self) -> List[Dict]:
        """Get all active loans."""
        return [loan for loan in self.loans if loan["status"] == "Active"]

    def get_closed_loans(self) -> List[Dict]:
        """Get all closed loans."""
        return [loan for loan in self.loans if loan["status"] == "Closed"]

    def delete_loan(self, loan_id: int) -> bool:
        """Delete a loan by ID."""
        for i, loan in enumerate(self.loans):
            if loan["loan_id"] == loan_id:
                self.loans.pop(i)
                self.save_to_file()
                return True
        return False

    def get_total_outstanding_balance(self) -> float:
        """Calculate total outstanding balance across all active loans."""
        total: float = sum(loan["balance"] for loan in self.get_active_loans())
        return round(total, 2)

    def get_statistics(self) -> Dict:
        """Get overall loan statistics."""
        total_loans: int = len(self.loans)
        active_loans: int = len(self.get_active_loans())
        closed_loans: int = len(self.get_closed_loans())
        total_outstanding: float = self.get_total_outstanding_balance()
        total_paid: float = round(sum(loan["monthly_payment"] * loan["payments_made"] for loan in self.loans), 2)

        return {
            "total_loans": total_loans,
            "active_loans": active_loans,
            "closed_loans": closed_loans,
            "total_outstanding_balance": total_outstanding,
            "total_paid_so_far": total_paid,
            "total_loans_value": round(sum(loan["principal"] for loan in self.loans), 2)
        }

    def save_to_file(self) -> None:
        """Save all loans to JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.loans, f, indent=2)
        except IOError as e:
            raise IOError(f"Failed to save loans data: {e}")

    def load_from_file(self) -> None:
        """Load loans from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.loans = json.load(f)
            except (IOError, json.JSONDecodeError):
                self.loans = []
        else:
            self.loans = []

    def clear_all_loans(self) -> None:
        """Clear all loans (for testing/reset)."""
        self.loans = []
        self.save_to_file()