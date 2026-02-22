"""Unit tests for Reservation class."""
# pylint: disable=consider-using-with

import tempfile
import unittest
from pathlib import Path

from app.hotel import Hotel
from app.customer import Customer
from app.reservation import Reservation


class ReservationTests(unittest.TestCase):
    """Test suite for the Reservation class."""

    def setUp(self):
        """Create temporary JSON files and seed test data."""
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)

        Hotel.file_path = base / "hotels.json"
        Customer.file_path = base / "customers.json"
        Reservation.file_path = base / "reservations.json"

        # Seed: 1 hotel + 1 customer
        Hotel.create_hotel(Hotel("H1", "Hotel A", 2, 2))
        Customer.create_customer(Customer("C1", "Ana"))

    def tearDown(self):
        """Clean up temporary directory after each test."""
        self.temp_dir.cleanup()

    def test_create_reservation_decreases_availability(self):
        """Test creating a reservation decreases hotel availability."""
        Reservation.create_reservation(Reservation("R1", "H1", "C1"))
        h = Hotel.display_hotel_info("H1")
        self.assertEqual(h.available_rooms, 1)

    def test_cancel_reservation_increases_availability(self):
        """Test canceling a reservation increases hotel availability."""
        Reservation.create_reservation(Reservation("R1", "H1", "C1"))
        Reservation.cancel_reservation("R1")
        h = Hotel.display_hotel_info("H1")
        self.assertEqual(h.available_rooms, 2)

    # ---- Negative cases ----

    def test_create_duplicate_reservation_raises(self):
        """Test creating a duplicate reservation raises ValueError."""
        Reservation.create_reservation(Reservation("R1", "H1", "C1"))
        with self.assertRaises(ValueError):
            Reservation.create_reservation(Reservation("R1", "H1", "C1"))

    def test_create_reservation_missing_hotel_raises(self):
        """Test creating reservation with missing hotel raises KeyError."""
        with self.assertRaises(KeyError):
            Reservation.create_reservation(
                Reservation("R2", "NOHOTEL", "C1")
            )

    def test_create_reservation_missing_customer_raises(self):
        """Test creating reservation with missing customer raises KeyError."""
        with self.assertRaises(KeyError):
            Reservation.create_reservation(
                Reservation("R2", "H1", "NOCUST")
            )

    def test_create_reservation_no_availability_raises(self):
        """Test creating reservation with no availability raises ValueError."""
        Hotel.modify_hotel_info("H1", available_rooms=0)
        with self.assertRaises(ValueError):
            Reservation.create_reservation(
                Reservation("R2", "H1", "C1")
            )

    def test_cancel_missing_reservation_raises(self):
        """Test canceling non-existing reservation raises KeyError."""
        with self.assertRaises(KeyError):
            Reservation.cancel_reservation("NOPE")

    def test_cancel_twice_raises(self):
        """Test canceling a reservation twice raises ValueError."""
        Reservation.create_reservation(Reservation("R1", "H1", "C1"))
        Reservation.cancel_reservation("R1")
        with self.assertRaises(ValueError):
            Reservation.cancel_reservation("R1")
