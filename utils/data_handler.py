"""File I/O and data persistence functions"""

import json
from typing import Dict, List, Any
from pathlib import Path
from config import LOAN_DATA_FILE, PAYMENT_HISTORY_FILE


def read_json_file(filepath: str) -> Dict[str, Any]:
    """
    Read JSON file safely.
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Dictionary from JSON file or empty dict if file doesn't exist
    """
    try:
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def write_json_file(filepath: str, data: Dict[str, Any]) -> bool:
    """
    Write data to JSON file.
    
    Args:
        filepath: Path to JSON file
        data: Dictionary to write
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError:
        return False


def save_loan(loan_id: str, loan_data: Dict[str, Any]) -> bool:
    """
    Save loan data to file.
    
    Args:
        loan_id: Unique loan identifier
        loan_data: Loan information dictionary
    
    Returns:
        True if successful
    """
    loans = read_json_file(LOAN_DATA_FILE)
    loans[loan_id] = loan_data
    return write_json_file(LOAN_DATA_FILE, loans)


def load_loan(loan_id: str) -> Dict[str, Any]:
    """
    Load loan data from file.
    
    Args:
        loan_id: Unique loan identifier
    
    Returns:
        Loan information dictionary or empty dict if not found
    """
    loans = read_json_file(LOAN_DATA_FILE)
    return loans.get(loan_id, {})


def save_payment(loan_id: str, payment_data: Dict[str, Any]) -> bool:
    """
    Record a payment for a loan.
    
    Args:
        loan_id: Unique loan identifier
        payment_data: Payment information
    
    Returns:
        True if successful
    """
    history = read_json_file(PAYMENT_HISTORY_FILE)
    
    if loan_id not in history:
        history[loan_id] = []
    
    history[loan_id].append(payment_data)
    return write_json_file(PAYMENT_HISTORY_FILE, history)


def get_payment_history(loan_id: str) -> List[Dict[str, Any]]:
    """
    Get all payments for a loan.
    
    Args:
        loan_id: Unique loan identifier
    
    Returns:
        List of payment records
    """
    history = read_json_file(PAYMENT_HISTORY_FILE)
    return history.get(loan_id, [])
