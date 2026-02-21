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
    
    @classmethod
    def _save_all(cls, customers):
        """Save all customers to JSON file."""
        cls.file_path.parent.mkdir(exist_ok=True)

        with open(cls.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [customer.to_dict() for customer in customers],
                file,
                indent=2,
            )

    @classmethod
    def create_customer(cls, customer):
        """Create a customer and persist it."""
        customers = cls._load_all()

        if any(c.customer_id == customer.customer_id for c in customers):
            raise ValueError("Customer already exists")

        customers.append(customer)
        cls._save_all(customers)

    @classmethod
    def delete_customer(cls, customer_id):
        """Delete a customer by id."""
        customers = cls._load_all()
        filtered = [c for c in customers if c.customer_id != customer_id]

        if len(filtered) == len(customers):
            raise KeyError("Customer not found")

        cls._save_all(filtered)

    @classmethod
    def display_customer_info(cls, customer_id):
        """Return a customer by id."""
        customers = cls._load_all()

        for customer in customers:
            if customer.customer_id == customer_id:
                return customer

        raise KeyError("Customer not found")

    @classmethod
    def modify_customer_info(cls, customer_id, **kwargs):
        """Modify fields of an existing customer."""
        customers = cls._load_all()
        found = False

        for customer in customers:
            if customer.customer_id == customer_id:
                for key, value in kwargs.items():
                    if hasattr(customer, key):
                        setattr(customer, key, value)

                if not customer.customer_id:
                    raise ValueError("customer_id cannot be empty")
                if not customer.customer_name:
                    raise ValueError("customer_name cannot be empty")

                found = True

        if not found:
            raise KeyError("Customer not found")

        cls._save_all(customers)