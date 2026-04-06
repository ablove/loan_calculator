#!/usr/bin/env python3
"""
Loan Calculator & Tracker - Main Entry Point
Run this file to launch the application.
"""

import tkinter as tk
from loan_gui import LoanCalculatorGUI


def main() -> None:
    """Main entry point for the application."""
    root: tk.Tk = tk.Tk()
    app: LoanCalculatorGUI = LoanCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()