"""Core EMI calculation functions using functional programming"""

from math import pow
from functools import reduce
from typing import Tuple, List, Dict


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    Calculate monthly EMI using the standard formula.
    EMI = P * r * (1+r)^n / ((1+r)^n - 1)
    where r = monthly rate, n = number of months
    
    Args:
        principal: Loan amount in currency
        annual_rate: Annual interest rate in percentage
        tenure_months: Loan tenure in months
    
    Returns:
        Monthly EMI amount
    """
    monthly_rate = annual_rate / (12 * 100)
    
    # Handle edge case: 0% interest
    if monthly_rate == 0:
        return principal / tenure_months
    
    numerator = principal * monthly_rate * pow(1 + monthly_rate, tenure_months)
    denominator = pow(1 + monthly_rate, tenure_months) - 1
    
    return numerator / denominator


def calculate_total_interest(emi: float, tenure_months: int, principal: float) -> float:
    """
    Calculate total interest paid over the loan tenure.
    
    Args:
        emi: Monthly EMI amount
        tenure_months: Number of months
        principal: Original loan amount
    
    Returns:
        Total interest amount
    """
    total_paid = emi * tenure_months
    return total_paid - principal


def calculate_monthly_interest(outstanding_balance: float, annual_rate: float) -> float:
    """
    Calculate interest for a specific month.
    
    Args:
        outstanding_balance: Current loan balance
        annual_rate: Annual interest rate in percentage
    
    Returns:
        Interest amount for that month
    """
    monthly_rate = annual_rate / (12 * 100)
    return outstanding_balance * monthly_rate


def calculate_principal_component(emi: float, monthly_interest: float) -> float:
    """
    Calculate principal portion of EMI.
    
    Args:
        emi: Monthly EMI amount
        monthly_interest: Interest portion of that month
    
    Returns:
        Principal portion of EMI
    """
    return emi - monthly_interest


def generate_amortization_schedule(principal: float, annual_rate: float, tenure_months: int) -> List[Dict[str, float]]:
    """
    Generate complete amortization schedule for the loan.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate in percentage
        tenure_months: Loan tenure in months
    
    Returns:
        List of dictionaries containing month-wise breakdown
    """
    emi = calculate_emi(principal, annual_rate, tenure_months)
    
    def calculate_month(accumulator: Tuple[List[Dict], float], month_num: int) -> Tuple[List[Dict], float]:
        """Higher-order function to calculate each month's details."""
        schedule, balance = accumulator
        
        monthly_interest = calculate_monthly_interest(balance, annual_rate)
        principal_paid = calculate_principal_component(emi, monthly_interest)
        new_balance = balance - principal_paid
        
        month_data = {
            "month": month_num,
            "emi": emi,
            "principal": principal_paid,
            "interest": monthly_interest,
            "balance": max(0, new_balance)  # Avoid negative balance due to rounding
        }
        
        return (schedule + [month_data], max(0, new_balance))
    
    # Use reduce to build amortization schedule
    schedule, _ = reduce(
        calculate_month,
        range(1, tenure_months + 1),
        ([], principal)
    )
    
    return schedule


def calculate_loan_summary(principal: float, annual_rate: float, tenure_months: int) -> Dict[str, float]:
    """
    Generate a summary of loan details.
    
    Args:
        principal: Loan amount
        annual_rate: Annual interest rate in percentage
        tenure_months: Loan tenure in months
    
    Returns:
        Dictionary with loan summary
    """
    emi = calculate_emi(principal, annual_rate, tenure_months)
    total_interest = calculate_total_interest(emi, tenure_months, principal)
    total_amount = principal + total_interest
    
    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "tenure_months": tenure_months,
        "monthly_emi": emi,
        "total_interest": total_interest,
        "total_amount_payable": total_amount
    }


def calculate_remaining_balance(schedule: List[Dict], paid_months: int) -> float:
    """
    Get remaining balance after a certain number of payments.
    
    Args:
        schedule: Amortization schedule
        paid_months: Number of months paid
    
    Returns:
        Remaining balance
    """
    if paid_months >= len(schedule):
        return 0.0
    return schedule[paid_months]["balance"]


def calculate_prepayment_savings(schedule: List[Dict], prepayment_month: int, prepayment_amount: float) -> Dict[str, float]:
    """
    Calculate savings from early loan repayment.
    
    Args:
        schedule: Original amortization schedule
        prepayment_month: Month in which prepayment is made
        prepayment_amount: Amount to prepay
    
    Returns:
        Dictionary with savings details
    """
    remaining_balance = schedule[prepayment_month - 1]["balance"]
    
    if prepayment_amount > remaining_balance:
        return {"status": "error", "message": "Prepayment amount exceeds remaining balance"}
    
    new_balance = remaining_balance - prepayment_amount
    
    # Calculate interest saved
    total_future_interest = sum(
        month["interest"] for month in schedule[prepayment_month:]
    )
    
    return {
        "prepayment_amount": prepayment_amount,
        "remaining_balance_before": remaining_balance,
        "remaining_balance_after": new_balance,
        "interest_saved": total_future_interest  # Approximate saving
    }
