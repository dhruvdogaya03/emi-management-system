"""Formatting and display functions"""

from config import CURRENCY_SYMBOL, DECIMAL_PLACES
from typing import Dict, List


def format_currency(amount: float) -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Numerical amount
    
    Returns:
        Formatted currency string
    """
    return f"{CURRENCY_SYMBOL}{amount:,.{DECIMAL_PLACES}f}"


def format_percentage(rate: float) -> str:
    """
    Format rate as percentage string.
    
    Args:
        rate: Percentage value
    
    Returns:
        Formatted percentage string
    """
    return f"{rate:.{DECIMAL_PLACES}f}%"


def format_summary(summary: Dict[str, float]) -> str:
    """
    Format loan summary for display.
    
    Args:
        summary: Loan summary dictionary
    
    Returns:
        Formatted summary string
    """
    lines = [
        "\n" + "="*50,
        "LOAN SUMMARY",
        "="*50,
        f"Principal Amount:        {format_currency(summary['principal'])}",
        f"Annual Interest Rate:    {format_percentage(summary['annual_rate'])}",
        f"Loan Tenure:             {int(summary['tenure_months'])} months",
        "-"*50,
        f"Monthly EMI:             {format_currency(summary['monthly_emi'])}",
        f"Total Interest:          {format_currency(summary['total_interest'])}",
        f"Total Amount Payable:    {format_currency(summary['total_amount_payable'])}",
        "="*50 + "\n"
    ]
    return "\n".join(lines)


def format_amortization_schedule(schedule: List[Dict], limit: int = None) -> str:
    """
    Format amortization schedule for display.
    
    Args:
        schedule: Amortization schedule list
        limit: Show only first N months (None = all)
    
    Returns:
        Formatted schedule string
    """
    items = schedule[:limit] if limit else schedule
    
    header = f"{'Month':<8} {'EMI':<15} {'Principal':<15} {'Interest':<15} {'Balance':<15}"
    separator = "-" * 68
    
    rows = [header, separator]
    
    for month in items:
        row = (
            f"{int(month['month']):<8} "
            f"{format_currency(month['emi']):<15} "
            f"{format_currency(month['principal']):<15} "
            f"{format_currency(month['interest']):<15} "
            f"{format_currency(month['balance']):<15}"
        )
        rows.append(row)
    
    rows.append(separator)
    if limit and limit < len(schedule):
        rows.append(f"... ({len(schedule) - limit} more months)\n")
    
    return "\n".join(rows)
