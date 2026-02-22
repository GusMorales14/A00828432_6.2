"""Unit tests for Customer class."""
# pylint: disable=consider-using-with

import tempfile
import unittest
from pathlib import Path

from app.customer import Customer


class CustomerTests(unittest.TestCase):
    """Test suite for the Customer class."""

    def setUp(self):
        """Create temporary JSON file for customer tests."""
        self.temp_dir = tempfile.TemporaryDirectory()
        Customer.file_path = Path(self.temp_dir.name) / "customers.json"

    def tearDown(self):
        """Clean up temporary directory after each test."""
        self.temp_dir.cleanup()

    def test_create_and_display_customer(self):
        """Test creating and retrieving a customer."""
        Customer.create_customer(Customer("C1", "Ana"))
        c = Customer.display_customer_info("C1")
        self.assertEqual(c.customer_name, "Ana")

    def test_delete_customer(self):
        """Test deleting an existing customer."""
        Customer.create_customer(Customer("C1", "Ana"))
        Customer.delete_customer("C1")
        with self.assertRaises(KeyError):
            Customer.display_customer_info("C1")

    def test_modify_customer_info(self):
        """Test modifying customer information."""
        Customer.create_customer(Customer("C1", "Ana"))
        Customer.modify_customer_info("C1", customer_name="Ana Maria")
        c = Customer.display_customer_info("C1")
        self.assertEqual(c.customer_name, "Ana Maria")

    # ---- Negative cases ----

    def test_create_duplicate_customer_raises(self):
        """Test creating a duplicate customer raises ValueError."""
        Customer.create_customer(Customer("C1", "Ana"))
        with self.assertRaises(ValueError):
            Customer.create_customer(Customer("C1", "Ana 2"))

    def test_delete_missing_customer_raises(self):
        """Test deleting a non-existing customer raises KeyError."""
        with self.assertRaises(KeyError):
            Customer.delete_customer("NOPE")

    def test_invalid_json_returns_empty_list(self):
        """Test handling of invalid JSON file without crashing."""
        Customer.file_path.write_text("{not json", encoding="utf-8")
        with self.assertRaises(KeyError):
            Customer.display_customer_info("C1")
