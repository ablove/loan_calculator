import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from loan_logic import LoanCalculator
from typing import Optional


class LoanCalculatorGUI:
    """Tkinter GUI for Loan Calculator & Tracker."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the GUI."""
        self.root: tk.Tk = root
        self.root.title("Loan Calculator & Tracker")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Initialize backend
        self.calculator: LoanCalculator = LoanCalculator()
        
        # Setup GUI
        self._setup_styles()
        self._create_widgets()
        self._refresh_loan_list()

    def _setup_styles(self) -> None:
        """Setup Tkinter styles and colors."""
        self.root.configure(bg="#f0f0f0")
        
        # Configure styles
        style: ttk.Style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', background='#f0f0f0', font=('Arial', 14, 'bold'))
        style.configure('TButton', font=('Arial', 10))

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Main container
        main_frame: ttk.Frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        title_label: ttk.Label = ttk.Label(main_frame, text="Loan Calculator & Tracker", style='Title.TLabel')
        title_label.pack(pady=10)

        # Input frame
        input_frame: ttk.LabelFrame = ttk.LabelFrame(main_frame, text="Add New Loan", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Borrower name
        ttk.Label(input_frame, text="Borrower Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.borrower_entry: ttk.Entry = ttk.Entry(input_frame, width=25)
        self.borrower_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # Principal amount
        ttk.Label(input_frame, text="Principal Amount ($):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.principal_entry: ttk.Entry = ttk.Entry(input_frame, width=25)
        self.principal_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # Annual interest rate
        ttk.Label(input_frame, text="Annual Interest Rate (%):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.rate_entry: ttk.Entry = ttk.Entry(input_frame, width=25)
        self.rate_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

        # Loan term in months
        ttk.Label(input_frame, text="Loan Term (months):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.months_entry: ttk.Entry = ttk.Entry(input_frame, width=25)
        self.months_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

        # Buttons for input
        button_frame: ttk.Frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=10)

        ttk.Button(button_frame, text="Calculate Payment", command=self._calculate_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Add Loan", command=self._add_loan).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self._clear_fields).pack(side=tk.LEFT, padx=5)

        input_frame.columnconfigure(1, weight=1)

        # Loans list frame
        list_frame: ttk.LabelFrame = ttk.LabelFrame(main_frame, text="All Loans", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbar and listbox
        scrollbar: ttk.Scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.loans_listbox: tk.Listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=('Courier', 9),
            height=12
        )
        self.loans_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.config(command=self.loans_listbox.yview)
        self.loans_listbox.bind('<<ListboxSelect>>', self._on_loan_select)

        # Actions frame for loans
        actions_frame: ttk.Frame = ttk.Frame(list_frame)
        actions_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(actions_frame, text="Make Payment", command=self._make_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Delete Loan", command=self._delete_loan).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="View Details", command=self._view_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions_frame, text="Refresh", command=self._refresh_loan_list).pack(side=tk.LEFT, padx=5)

        # Statistics frame
        stats_frame: ttk.LabelFrame = ttk.LabelFrame(main_frame, text="Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)

        self.stats_label: ttk.Label = ttk.Label(stats_frame, text="", justify=tk.LEFT)
        self.stats_label.pack(fill=tk.X)

        # Status bar
        self.status_var: tk.StringVar = tk.StringVar(value="Ready")
        status_bar: ttk.Label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=5)

    def _calculate_payment(self) -> None:
        """Calculate monthly payment based on input."""
        try:
            principal: float = float(self.principal_entry.get())
            rate: float = float(self.rate_entry.get())
            months: int = int(self.months_entry.get())

            monthly_payment: float = self.calculator.calculate_monthly_payment(principal, rate, months)
            total_interest: float = self.calculator.calculate_total_interest(principal, monthly_payment, months)
            total_paid: float = round(monthly_payment * months, 2)

            message: str = f"""
Monthly Payment: ${monthly_payment:.2f}
Total Interest: ${total_interest:.2f}
Total Amount Paid: ${total_paid:.2f}
            """
            messagebox.showinfo("Payment Calculation", message)
            self.status_var.set(f"Calculated: Monthly Payment ${monthly_payment:.2f}")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
            self.status_var.set("Error calculating payment")

    def _add_loan(self) -> None:
        """Add a new loan."""
        try:
            borrower: str = self.borrower_entry.get()
            principal: float = float(self.principal_entry.get())
            rate: float = float(self.rate_entry.get())
            months: int = int(self.months_entry.get())

            loan: dict = self.calculator.add_loan(borrower, principal, rate, months)
            messagebox.showinfo("Success", f"Loan added successfully!\nLoan ID: {loan['loan_id']}\nMonthly Payment: ${loan['monthly_payment']:.2f}")
            self._clear_fields()
            self._refresh_loan_list()
            self.status_var.set(f"Loan added for {borrower}")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
            self.status_var.set("Error adding loan")

    def _make_payment(self) -> None:
        """Make a payment on selected loan."""
        selection: tuple = self.loans_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a loan first")
            return

        loan: dict = self.calculator.get_all_loans()[selection[0]]
        
        # Ask for payment amount
        amount_str: Optional[str] = simpledialog.askstring(
            "Make Payment",
            f"Enter payment amount (Max: ${loan['balance']:.2f}):"
        )
        
        if not amount_str:
            return

        try:
            amount: float = float(amount_str)
            updated_loan: dict = self.calculator.make_repayment(loan["loan_id"], amount)
            messagebox.showinfo(
                "Payment Successful",
                f"Payment of ${amount:.2f} made\nRemaining Balance: ${updated_loan['balance']:.2f}"
            )
            self._refresh_loan_list()
            self.status_var.set(f"Payment of ${amount:.2f} made for loan {loan['loan_id']}")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
            self.status_var.set("Error making payment")

    def _delete_loan(self) -> None:
        """Delete selected loan."""
        selection: tuple = self.loans_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a loan first")
            return

        loan: dict = self.calculator.get_all_loans()[selection[0]]
        
        if messagebox.askyesno("Confirm Delete", f"Delete loan {loan['loan_id']} for {loan['borrower']}?"):
            self.calculator.delete_loan(loan["loan_id"])
            self._refresh_loan_list()
            self.status_var.set(f"Loan {loan['loan_id']} deleted")
            messagebox.showinfo("Success", "Loan deleted successfully")

    def _view_details(self) -> None:
        """View detailed information about selected loan."""
        selection: tuple = self.loans_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a loan first")
            return

        loan: dict = self.calculator.get_all_loans()[selection[0]]
        
        details: str = f"""
Loan ID: {loan['loan_id']}
Borrower: {loan['borrower']}
Principal: ${loan['principal']:.2f}
Annual Interest Rate: {loan['annual_rate']:.2f}%
Loan Term: {loan['months']} months
Monthly Payment: ${loan['monthly_payment']:.2f}
Total Interest: ${loan['total_interest']:.2f}
Remaining Balance: ${loan['balance']:.2f}
Payments Made: {loan['payments_made']}
Status: {loan['status']}
Created: {loan['created_date'][:10]}
        """
        messagebox.showinfo("Loan Details", details)

    def _on_loan_select(self, event: tk.Event) -> None:
        """Handle loan selection."""
        selection: tuple = self.loans_listbox.curselection()
        if selection:
            self.status_var.set(f"Selected loan {selection[0] + 1}")

    def _refresh_loan_list(self) -> None:
        """Refresh the loans listbox and statistics."""
        self.loans_listbox.delete(0, tk.END)
        
        loans: list = self.calculator.get_all_loans()
        if not loans:
            self.loans_listbox.insert(tk.END, "No loans in the system")
        else:
            for i, loan in enumerate(loans, 1):
                status_icon: str = "✓" if loan["status"] == "Closed" else "→"
                line: str = f"{status_icon} #{loan['loan_id']} {loan['borrower'][:15]:15} | Balance: ${loan['balance']:>10.2f} | Monthly: ${loan['monthly_payment']:>8.2f}"
                self.loans_listbox.insert(tk.END, line)

        # Update statistics
        stats: dict = self.calculator.get_statistics()
        stats_text: str = f"Total Loans: {stats['total_loans']} | Active: {stats['active_loans']} | Closed: {stats['closed_loans']} | Total Outstanding: ${stats['total_outstanding_balance']:.2f} | Total Paid: ${stats['total_paid_so_far']:.2f}"
        self.stats_label.config(text=stats_text)

    def _clear_fields(self) -> None:
        """Clear all input fields."""
        self.borrower_entry.delete(0, tk.END)
        self.principal_entry.delete(0, tk.END)
        self.rate_entry.delete(0, tk.END)
        self.months_entry.delete(0, tk.END)
        self.status_var.set("Fields cleared")