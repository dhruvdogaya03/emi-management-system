"""Payment tracking and balance calculation functions"""

from typing import Dict, List, Any
from datetime import datetime
from functools import reduce


def record_payment(payment_date: str, amount: float, payment_method: str = "Online") -> Dict[str, Any]:
    """
    Create a payment record.
    
    Args:
        payment_date: Date of payment (YYYY-MM-DD)
        amount: Payment amount
        payment_method: Method of payment
    
    Returns:
        Payment record dictionary
    """
    return {
        "date": payment_date,
        "amount": amount,
        "method": payment_method,
        "timestamp": datetime.now().isoformat()
    }


def calculate_total_paid(payments: List[Dict[str, Any]]) -> float:
    """
    Calculate total amount paid from payment list.
    
    Args:
        payments: List of payment records
    
    Returns:
        Total amount paid
    """
    return reduce(lambda total, payment: total + payment["amount"], payments, 0.0)


def calculate_balance_after_payments(principal: float, payments: List[Dict[str, Any]]) -> float:
    """
    Calculate remaining balance after payments.
    
    Args:
        principal: Original loan amount
        payments: List of payment records
    
    Returns:
        Remaining balance
    """
    total_paid = calculate_total_paid(payments)
    return max(0, principal - total_paid)


def get_payment_summary(payments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate summary of all payments.
    
    Args:
        payments: List of payment records
    
    Returns:
        Payment summary dictionary
    """
    if not payments:
        return {
            "total_payments": 0,
            "total_amount": 0.0,
            "average_payment": 0.0,
            "last_payment_date": None
        }
    
    total_amount = calculate_total_paid(payments)
    
    return {
        "total_payments": len(payments),
        "total_amount": total_amount,
        "average_payment": total_amount / len(payments),
        "last_payment_date": payments[-1]["date"],
        "first_payment_date": payments[0]["date"]
    }


def filter_payments_by_date(payments: List[Dict[str, Any]], start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    Filter payments within a date range.
    
    Args:
        payments: List of payment records
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        Filtered payment list
    """
    return list(filter(
        lambda p: start_date <= p["date"] <= end_date,
        payments
    ))
