# app/utils/validators.py
from pydantic import constr

def non_empty_str(x: str) -> str:
    if not x or not x.strip():
        raise ValueError("Value cannot be empty")
    return x.strip()
