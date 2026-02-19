"""Customer module"""

import json
from pathlib import Path

class Customer:
    
    file_path = Path(r"A00828432_6.2\data\customers.json")

    def __init__(self, customer_id, customer_name):
        if not customer_id:
            raise ValueError("customer_id is empty")
        if not customer_name:
            raise ValueError("customer_name is empty")

        self.customer_id = customer_id
        self.customer_name = customer_name

    def to_dict(self):
        """Convert object to dictionary."""
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Hotel from dictionary."""
        return cls(
            data["customer_id"],
            data["customer_name"],
        )

    @classmethod
    def _load_all(cls):
        """Load all Hotel information from JSON file"""
        if not cls.file_path.exists():
            return []

        try:
            with open(cls.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print("Invalid JSON file")
            return []

        customers = []
        for item in data:
            try:
                customers.append(cls.from_dict(item))
            except (KeyError, TypeError, ValueError):
                print(f"Invalid record skipped: {item}")
        return customers
