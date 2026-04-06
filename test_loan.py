import unittest
import os
from loan_logic import LoanCalculator
from typing import Dict, List


class TestLoanCalculator(unittest.TestCase):
    """Test cases for LoanCalculator class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.calculator = LoanCalculator("test_loans.json")
        self.calculator.clear_all_loans()

    def tearDown(self) -> None:
        """Clean up after tests."""
        self.calculator.clear_all_loans()
        if os.path.exists("test_loans.json"):
            os.remove("test_loans.json")

    # Tests for calculate_monthly_payment
    def test_calculate_monthly_payment_valid(self) -> None:
        """Test monthly payment calculation with valid inputs."""
        # $10,000 loan at 5% for 60 months should be ~$188.71
        payment: float = self.calculator.calculate_monthly_payment(10000, 5, 60)
        self.assertAlmostEqual(payment, 188.71, places=1)

    def test_calculate_monthly_payment_zero_interest(self) -> None:
        """Test monthly payment with 0% interest."""
        # $12,000 at 0% for 12 months = $1,000/month
        payment: float = self.calculator.calculate_monthly_payment(12000, 0, 12)
        self.assertEqual(payment, 1000.0)

    def test_calculate_monthly_payment_invalid_months(self) -> None:
        """Test monthly payment with invalid months."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_monthly_payment(10000, 5, 0)

    def test_calculate_monthly_payment_negative_rate(self) -> None:
        """Test monthly payment with negative interest rate."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_monthly_payment(10000, -5, 60)

    def test_calculate_monthly_payment_invalid_principal(self) -> None:
        """Test monthly payment with invalid principal."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_monthly_payment(0, 5, 60)

    # Tests for calculate_total_interest
    def test_calculate_total_interest(self) -> None:
        """Test total interest calculation."""
        monthly_payment: float = 188.71
        months: int = 60
        principal: float = 10000
        
        total_interest: float = self.calculator.calculate_total_interest(principal, monthly_payment, months)
        expected: float = (monthly_payment * months) - principal
        self.assertAlmostEqual(total_interest, expected, places=1)

    # Tests for add_loan
    def test_add_loan_valid(self) -> None:
        """Test adding a valid loan."""
        loan: Dict = self.calculator.add_loan("John Doe", 15000, 4.5, 48)
        
        self.assertEqual(loan["loan_id"], 1)
        self.assertEqual(loan["borrower"], "John Doe")
        self.assertEqual(loan["principal"], 15000.0)
        self.assertEqual(loan["annual_rate"], 4.5)
        self.assertEqual(loan["months"], 48)
        self.assertEqual(loan["balance"], 15000.0)
        self.assertEqual(loan["status"], "Active")
        self.assertTrue(loan["monthly_payment"] > 0)

    def test_add_loan_empty_borrower(self) -> None:
        """Test adding loan with empty borrower name."""
        with self.assertRaises(ValueError):
            self.calculator.add_loan("", 10000, 5, 60)

    def test_add_loan_invalid_principal(self) -> None:
        """Test adding loan with invalid principal."""
        with self.assertRaises(ValueError):
            self.calculator.add_loan("John Doe", -5000, 5, 60)

    def test_add_loan_invalid_months(self) -> None:
        """Test adding loan with invalid months."""
        with self.assertRaises(ValueError):
            self.calculator.add_loan("John Doe", 10000, 5, 0)

    def test_add_loan_incremental_ids(self) -> None:
        """Test that loan IDs increment correctly."""
        loan1: Dict = self.calculator.add_loan("Alice", 10000, 5, 60)
        loan2: Dict = self.calculator.add_loan("Bob", 20000, 6, 48)
        loan3: Dict = self.calculator.add_loan("Charlie", 15000, 4, 36)
        
        self.assertEqual(loan1["loan_id"], 1)
        self.assertEqual(loan2["loan_id"], 2)
        self.assertEqual(loan3["loan_id"], 3)

    # Tests for make_repayment
    def test_make_repayment_valid(self) -> None:
        """Test making a valid repayment."""
        loan: Dict = self.calculator.add_loan("John Doe", 10000, 5, 60)
        original_balance: float = loan["balance"]
        
        updated_loan: Dict = self.calculator.make_repayment(loan["loan_id"], 1000)
        
        self.assertEqual(updated_loan["balance"], original_balance - 1000)
        self.assertEqual(updated_loan["payments_made"], 1)
        self.assertEqual(updated_loan["status"], "Active")

    def test_make_repayment_exceeds_balance(self) -> None:
        """Test repayment exceeding remaining balance."""
        loan: Dict = self.calculator.add_loan("John Doe", 5000, 5, 60)
        
        with self.assertRaises(ValueError):
            self.calculator.make_repayment(loan["loan_id"], 10000)

    def test_make_repayment_closes_loan(self) -> None:
        """Test that loan is closed when fully paid."""
        loan: Dict = self.calculator.add_loan("John Doe", 1000, 0, 12)
        
        updated_loan: Dict = self.calculator.make_repayment(loan["loan_id"], 1000)
        
        self.assertEqual(updated_loan["balance"], 0)
        self.assertEqual(updated_loan["status"], "Closed")

    def test_make_repayment_invalid_loan_id(self) -> None:
        """Test repayment on non-existent loan."""
        with self.assertRaises(ValueError):
            self.calculator.make_repayment(999, 500)

    def test_make_repayment_invalid_amount(self) -> None:
        """Test repayment with invalid amount."""
        loan: Dict = self.calculator.add_loan("John Doe", 10000, 5, 60)
        
        with self.assertRaises(ValueError):
            self.calculator.make_repayment(loan["loan_id"], -100)

    def test_make_repayment_multiple_payments(self) -> None:
        """Test multiple repayments on same loan."""
        loan: Dict = self.calculator.add_loan("John Doe", 10000, 5, 60)
        
        self.calculator.make_repayment(loan["loan_id"], 2000)
        self.calculator.make_repayment(loan["loan_id"], 3000)
        updated_loan: Dict = self.calculator.get_loan_by_id(loan["loan_id"])
        
        self.assertEqual(updated_loan["balance"], 5000)
        self.assertEqual(updated_loan["payments_made"], 2)

    # Tests for get_loan_by_id
    def test_get_loan_by_id_found(self) -> None:
        """Test retrieving an existing loan."""
        loan: Dict = self.calculator.add_loan("John Doe", 10000, 5, 60)
        retrieved: Dict | None = self.calculator.get_loan_by_id(loan["loan_id"])
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["borrower"], "John Doe")

    def test_get_loan_by_id_not_found(self) -> None:
        """Test retrieving a non-existent loan."""
        result: Dict | None = self.calculator.get_loan_by_id(999)
        self.assertIsNone(result)

    # Tests for get_all_loans
    def test_get_all_loans_empty(self) -> None:
        """Test getting loans when none exist."""
        loans: List[Dict] = self.calculator.get_all_loans()
        self.assertEqual(len(loans), 0)

    def test_get_all_loans_multiple(self) -> None:
        """Test getting multiple loans."""
        self.calculator.add_loan("Alice", 10000, 5, 60)
        self.calculator.add_loan("Bob", 20000, 6, 48)
        self.calculator.add_loan("Charlie", 15000, 4, 36)
        
        loans: List[Dict] = self.calculator.get_all_loans()
        self.assertEqual(len(loans), 3)

    # Tests for active/closed loans
    def test_get_active_loans(self) -> None:
        """Test retrieving active loans."""
        loan1: Dict = self.calculator.add_loan("Alice", 10000, 5, 60)
        loan2: Dict = self.calculator.add_loan("Bob", 5000, 0, 10)
        
        self.calculator.make_repayment(loan2["loan_id"], 5000)  # Close loan2
        
        active: List[Dict] = self.calculator.get_active_loans()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["loan_id"], loan1["loan_id"])

    def test_get_closed_loans(self) -> None:
        """Test retrieving closed loans."""
        loan: Dict = self.calculator.add_loan("John Doe", 1000, 0, 1)
        self.calculator.make_repayment(loan["loan_id"], 1000)
        
        closed: List[Dict] = self.calculator.get_closed_loans()
        self.assertEqual(len(closed), 1)

    # Tests for delete_loan
    def test_delete_loan_existing(self) -> None:
        """Test deleting an existing loan."""
        loan: Dict = self.calculator.add_loan("John Doe", 10000, 5, 60)
        
        result: bool = self.calculator.delete_loan(loan["loan_id"])
        
        self.assertTrue(result)
        self.assertIsNone(self.calculator.get_loan_by_id(loan["loan_id"]))

    def test_delete_loan_non_existing(self) -> None:
        """Test deleting a non-existent loan."""
        result: bool = self.calculator.delete_loan(999)
        self.assertFalse(result)

    # Tests for statistics
    def test_get_statistics_empty(self) -> None:
        """Test statistics with no loans."""
        stats: Dict = self.calculator.get_statistics()
        
        self.assertEqual(stats["total_loans"], 0)
        self.assertEqual(stats["active_loans"], 0)
        self.assertEqual(stats["closed_loans"], 0)
        self.assertEqual(stats["total_outstanding_balance"], 0)

    def test_get_statistics_with_loans(self) -> None:
        """Test statistics with multiple loans."""
        loan1: Dict = self.calculator.add_loan("Alice", 10000, 5, 60)
        loan2: Dict = self.calculator.add_loan("Bob", 5000, 0, 10)
        
        self.calculator.make_repayment(loan2["loan_id"], 2000)
        
        stats: Dict = self.calculator.get_statistics()
        
        self.assertEqual(stats["total_loans"], 2)
        self.assertEqual(stats["active_loans"], 2)
        self.assertEqual(stats["closed_loans"], 0)
        self.assertGreater(stats["total_outstanding_balance"], 0)

    def test_get_total_outstanding_balance(self) -> None:
        """Test calculating total outstanding balance."""
        loan1: Dict = self.calculator.add_loan("Alice", 10000, 5, 60)
        loan2: Dict = self.calculator.add_loan("Bob", 5000, 0, 10)
        
        self.calculator.make_repayment(loan1["loan_id"], 1000)
        self.calculator.make_repayment(loan2["loan_id"], 1000)
        
        total: float = self.calculator.get_total_outstanding_balance()
        expected: float = (10000 - 1000) + (5000 - 1000)
        self.assertEqual(total, expected)

    # Tests for file persistence
    def test_save_and_load(self) -> None:
        """Test saving and loading loans from file."""
        loan1: Dict = self.calculator.add_loan("Alice", 10000, 5, 60)
        loan2: Dict = self.calculator.add_loan("Bob", 5000, 4, 48)
        
        # Create new calculator instance to test loading
        calculator2: LoanCalculator = LoanCalculator("test_loans.json")
        loans: List[Dict] = calculator2.get_all_loans()
        
        self.assertEqual(len(loans), 2)
        self.assertEqual(loans[0]["borrower"], "Alice")
        self.assertEqual(loans[1]["borrower"], "Bob")

    def test_clear_all_loans(self) -> None:
        """Test clearing all loans."""
        self.calculator.add_loan("Alice", 10000, 5, 60)
        self.calculator.add_loan("Bob", 5000, 4, 48)
        
        self.calculator.clear_all_loans()
        loans: List[Dict] = self.calculator.get_all_loans()
        
        self.assertEqual(len(loans), 0)


if __name__ == '__main__':
    unittest.main()