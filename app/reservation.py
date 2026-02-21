"""Reservation Module"""


import json
from pathlib import Path

from app.hotel import Hotel
from app.customer import Customer


class Reservation:
    """Represents a reservation linking a customer to a hotel."""

    file_path = Path("data/reservations.json")

    STATUS_ACTIVE = "ACTIVE"
    STATUS_CANCELLED = "CANCELLED"

    def __init__(
        self,
        reservation_id,
        hotel_id,
        customer_id,
        status=STATUS_ACTIVE,
    ):
        if not reservation_id:
            raise ValueError("reservation_id cannot be empty")
        if not hotel_id:
            raise ValueError("hotel_id cannot be empty")
        if not customer_id:
            raise ValueError("customer_id cannot be empty")
        if status not in (self.STATUS_ACTIVE, self.STATUS_CANCELLED):
            raise ValueError("Invalid reservation status")

        self.reservation_id = reservation_id
        self.hotel_id = hotel_id
        self.customer_id = customer_id
        self.status = status

    def to_dict(self):
        """Convert object to dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "hotel_id": self.hotel_id,
            "customer_id": self.customer_id,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Reservation from dictionary."""
        return cls(
            data["reservation_id"],
            data["hotel_id"],
            data["customer_id"],
            data.get("status", cls.STATUS_ACTIVE),
        )

    @classmethod
    def _load_all(cls):
        """Load all reservations from JSON file."""
        if not cls.file_path.exists():
            return []

        try:
            with open(cls.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print("Invalid JSON file")
            return []

        if not isinstance(data, list):
            print("Invalid JSON structure: expected a list")
            return []

        reservations = []
        for item in data:
            try:
                reservations.append(cls.from_dict(item))
            except (KeyError, TypeError, ValueError):
                print(f"Invalid record skipped: {item}")

        return reservations

    @classmethod
    def _save_all(cls, reservations):
        """Save all reservations to JSON file."""
        cls.file_path.parent.mkdir(parents=True,
                                   exist_ok=True)

        with open(cls.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [reservation.to_dict() for reservation in reservations],
                file,
                indent=2,
            )

    @classmethod
    def create_reservation(cls, reservation):
        """
        Create a reservation (Customer, Hotel).
        """
        reservations = cls._load_all()

        if any(
            r.reservation_id == reservation.reservation_id
            for r in reservations
                ):
            raise ValueError("Reservation already exists")

        # Validate existence of hotel & customer
        Hotel.display_hotel_info(reservation.hotel_id)
        Customer.display_customer_info(reservation.customer_id)

        # Reserve one room (may raise KeyError/ValueError)
        Hotel.reserve_room(reservation.hotel_id)

        reservations.append(reservation)
        cls._save_all(reservations)

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """
        Cancel a reservation by id and persist changes.
        """
        reservations = cls._load_all()
        found = False

        for reservation in reservations:
            if reservation.reservation_id == reservation_id:
                found = True

                if reservation.status == cls.STATUS_CANCELLED:
                    raise ValueError("Reservation already cancelled")

                reservation.status = cls.STATUS_CANCELLED
                cls._save_all(reservations)

                # Release one room back to the hotel
                Hotel.cancel_reservation(reservation.hotel_id)
                return

        if not found:
            raise KeyError("Reservation not found")
