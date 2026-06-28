"""Report generation functions"""

from typing import Dict, List, Any
from functools import reduce
from datetime import datetime, timedelta


def generate_monthly_interest_report(schedule: List[Dict]) -> Dict[str, float]:
    """
    Generate interest paid by month.
    
    Args:
        schedule: Amortization schedule
    
    Returns:
        Dictionary with month as key and interest as value
    """
    return reduce(
        lambda report, month: {**report, f"Month {month['month']}": month['interest']},
        schedule,
        {}
    )


def calculate_interest_paid_till_month(schedule: List[Dict], month_num: int) -> float:
    """
    Calculate total interest paid till a specific month.
    
    Args:
        schedule: Amortization schedule
        month_num: Month number
    
    Returns:
        Total interest paid
    """
    return sum(month["interest"] for month in schedule[:month_num])


def calculate_principal_paid_till_month(schedule: List[Dict], month_num: int) -> float:
    """
    Calculate total principal paid till a specific month.
    
    Args:
        schedule: Amortization schedule
        month_num: Month number
    
    Returns:
        Total principal paid
    """
    return sum(month["principal"] for month in schedule[:month_num])


def generate_yearly_report(schedule: List[Dict]) -> List[Dict[str, Any]]:
    """
    Generate yearly breakdown of loan payments.
    
    Args:
        schedule: Amortization schedule
    
    Returns:
        List of yearly reports
    """
    def accumulate_year(yearly_data: List[Dict[str, Any]], year_months: List[Dict]) -> List[Dict[str, Any]]:
        """Accumulate data for each year."""
        if not year_months:
            return yearly_data
        
        year_num = (len(yearly_data) // 12) + 1
        total_emi = sum(m["emi"] for m in year_months)
        total_principal = sum(m["principal"] for m in year_months)
        total_interest = sum(m["interest"] for m in year_months)
        final_balance = year_months[-1]["balance"] if year_months else 0
        
        yearly_report = {
            "year": year_num,
            "total_emi": total_emi,
            "principal_paid": total_principal,
            "interest_paid": total_interest,
            "balance": final_balance
        }
        
        return yearly_data + [yearly_report]
    
    # Group schedule into chunks of 12 months
    yearly_reports = []
    for i in range(0, len(schedule), 12):
        year_chunk = schedule[i:i+12]
        accumulate_year(yearly_reports, year_chunk)
        yearly_reports = accumulate_year(yearly_reports, year_chunk)
    
    return yearly_reports


def calculate_payoff_date(schedule: List[Dict], start_date: str) -> str:
    """
    Calculate loan payoff date.
    
    Args:
        schedule: Amortization schedule
        start_date: Loan start date (YYYY-MM-DD)
    
    Returns:
        Payoff date (YYYY-MM-DD)
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    months_count = len(schedule)
    payoff = start + timedelta(days=30 * months_count)  # Approximate
    return payoff.strftime("%Y-%m-%d")
