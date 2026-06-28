"""Main entry point for EMI Management System"""

from loan_calculator import (
    calculate_emi, calculate_loan_summary, generate_amortization_schedule,
    calculate_remaining_balance, calculate_prepayment_savings
)
from utils.validation import validate_all
from utils.formatters import format_summary, format_amortization_schedule
from utils.data_handler import save_loan, load_loan, save_payment, get_payment_history
from processors.payment_tracker import record_payment, get_payment_summary
from processors.report_generator import generate_yearly_report, calculate_payoff_date
from config import DEFAULT_ANNUAL_RATE, DEFAULT_TENURE_MONTHS
from datetime import datetime
import uuid


def create_new_loan(principal: float, annual_rate: float = DEFAULT_ANNUAL_RATE, tenure_months: int = DEFAULT_TENURE_MONTHS) -> dict:
    """
    Create and save a new loan.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate
        tenure_months: Loan tenure in months
    
    Returns:
        Loan details dictionary
    """
    # Validate inputs
    is_valid, error_msg = validate_all(principal, annual_rate, tenure_months)
    if not is_valid:
        print(f"❌ Validation Error: {error_msg}")
        return {}
    
    # Generate loan ID
    loan_id = str(uuid.uuid4())[:8]
    
    # Calculate loan summary
    summary = calculate_loan_summary(principal, annual_rate, tenure_months)
    
    # Generate amortization schedule
    schedule = generate_amortization_schedule(principal, annual_rate, tenure_months)
    
    # Create loan data
    loan_data = {
        "loan_id": loan_id,
        "principal": principal,
        "annual_rate": annual_rate,
        "tenure_months": tenure_months,
        "created_date": datetime.now().strftime("%Y-%m-%d"),
        **summary,
        "schedule": schedule
    }
    
    # Save loan
    if save_loan(loan_id, loan_data):
        print(f"✅ Loan created successfully! Loan ID: {loan_id}")
        print(format_summary(summary))
        return loan_data
    else:
        print("❌ Error saving loan")
        return {}


def view_loan(loan_id: str) -> None:
    """
    Display loan details.
    
    Args:
        loan_id: Loan identifier
    """
    loan = load_loan(loan_id)
    if not loan:
        print(f"❌ Loan {loan_id} not found")
        return
    
    summary = {
        "principal": loan["principal"],
        "annual_rate": loan["annual_rate"],
        "tenure_months": loan["tenure_months"],
        "monthly_emi": loan["monthly_emi"],
        "total_interest": loan["total_interest"],
        "total_amount_payable": loan["total_amount_payable"]
    }
    
    print(format_summary(summary))


def view_amortization_schedule(loan_id: str, limit: int = None) -> None:
    """
    Display amortization schedule.
    
    Args:
        loan_id: Loan identifier
        limit: Number of months to display
    """
    loan = load_loan(loan_id)
    if not loan:
        print(f"❌ Loan {loan_id} not found")
        return
    
    schedule = loan.get("schedule", [])
    if not schedule:
        print("❌ No schedule available")
        return
    
    print(f"\n📊 AMORTIZATION SCHEDULE - Loan ID: {loan_id}")
    print(format_amortization_schedule(schedule, limit))


def record_loan_payment(loan_id: str, amount: float, payment_date: str = None) -> None:
    """
    Record a payment for a loan.
    
    Args:
        loan_id: Loan identifier
        amount: Payment amount
        payment_date: Payment date (defaults to today)
    """
    if payment_date is None:
        payment_date = datetime.now().strftime("%Y-%m-%d")
    
    payment = record_payment(payment_date, amount)
    
    if save_payment(loan_id, payment):
        print(f"✅ Payment recorded: ₹{amount:.2f} on {payment_date}")
    else:
        print("❌ Error recording payment")


def view_payment_history(loan_id: str) -> None:
    """
    Display payment history for a loan.
    
    Args:
        loan_id: Loan identifier
    """
    payments = get_payment_history(loan_id)
    
    if not payments:
        print(f"❌ No payment history for loan {loan_id}")
        return
    
    summary = get_payment_summary(payments)
    print(f"\n💳 PAYMENT HISTORY - Loan ID: {loan_id}")
    print(f"Total Payments: {summary['total_payments']}")
    print(f"Total Amount Paid: ₹{summary['total_amount']:.2f}")
    print(f"Average Payment: ₹{summary['average_payment']:.2f}")
    print(f"First Payment: {summary['first_payment_date']}")
    print(f"Last Payment: {summary['last_payment_date']}\n")


def demo():
    """
    Run demonstration of the system.
    """
    print("\n" + "="*60)
    print("EMI MANAGEMENT SYSTEM - DEMONSTRATION")
    print("="*60)
    
    # Create a sample loan
    print("\n1️⃣  Creating a sample loan...")
    loan = create_new_loan(principal=500000, annual_rate=8.5, tenure_months=60)
    
    if loan:
        loan_id = loan["loan_id"]
        
        # View loan details
        print("\n2️⃣  Viewing loan details...")
        view_loan(loan_id)
        
        # View first 6 months of schedule
        print("\n3️⃣  Viewing first 6 months of amortization schedule...")
        view_amortization_schedule(loan_id, limit=6)
        
        # Record some payments
        print("\n4️⃣  Recording payments...")
        record_loan_payment(loan_id, loan["monthly_emi"], "2024-01-15")
        record_loan_payment(loan_id, loan["monthly_emi"], "2024-02-15")
        record_loan_payment(loan_id, loan["monthly_emi"], "2024-03-15")
        
        # View payment history
        print("\n5️⃣  Viewing payment history...")
        view_payment_history(loan_id)
    
    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    demo()
