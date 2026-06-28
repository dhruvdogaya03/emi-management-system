"""Input validation functions"""

from typing import Tuple


def validate_principal(principal: float) -> Tuple[bool, str]:
    """
    Validate loan principal amount.
    
    Args:
        principal: Loan amount
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if principal <= 0:
        return False, "Principal amount must be greater than 0"
    if principal > 10_000_000:
        return False, "Principal amount exceeds reasonable limit (₹1 Cr)"
    return True, ""


def validate_interest_rate(rate: float) -> Tuple[bool, str]:
    """
    Validate annual interest rate.
    
    Args:
        rate: Annual interest rate in percentage
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if rate < 0:
        return False, "Interest rate cannot be negative"
    if rate > 50:
        return False, "Interest rate seems unreasonably high (> 50%)"
    return True, ""


def validate_tenure(months: int) -> Tuple[bool, str]:
    """
    Validate loan tenure.
    
    Args:
        months: Loan tenure in months
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if months <= 0:
        return False, "Tenure must be greater than 0 months"
    if months > 600:  # 50 years
        return False, "Tenure exceeds 600 months (50 years)"
    return True, ""


def validate_all(principal: float, rate: float, months: int) -> Tuple[bool, str]:
    """
    Validate all loan parameters at once.
    
    Args:
        principal: Loan amount
        rate: Annual interest rate
        months: Loan tenure in months
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    validators = [
        validate_principal(principal),
        validate_interest_rate(rate),
        validate_tenure(months)
    ]
    
    # Find first error, if any
    errors = [msg for is_valid, msg in validators if not is_valid]
    
    if errors:
        return False, " | ".join(errors)
    
    return True, ""
