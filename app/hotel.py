"""Hotel module"""

import json
from pathlib import Path


class Hotel:
    """This class represents a hotel and its operations"""

    file_path = Path(r"A00828432_6.2\data\hotels.json")

    def __init__(self, hotel_id, hotel_name,
                 total_rooms, available_rooms):
        if not hotel_id:
            raise ValueError("hotel_id is empty")
        if not hotel_name:
            raise ValueError("hotel_id is empty")
        if not total_rooms:
            raise ValueError("total_rooms is empty")
        if not available_rooms:
            raise ValueError("available_rooms is empty")

        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.total_rooms = total_rooms
        self.available_rooms = available_rooms

    def to_dict(self):
        """Convert object to dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "hotel_name": self.hotel_name,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
        }

    @classmethod
    def from_dict(cls, data):
        """Create Hotel from dictionary."""
        return cls(
            data["hotel_id"],
            data["hotel_name"],
            data["total_rooms"],
            data["available_rooms"],
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

        hotels = []
        for item in data:
            try:
                hotels.append(cls.from_dict(item))
            except (KeyError, TypeError, ValueError):
                print(f"Invalid record skipped: {item}")
        return hotels

    @classmethod
    def _save_all(cls, hotels):
        """Saves the JSON File  in file_path"""
        cls.file_path.parent.mkdir(exist_ok=True)

        with open(cls.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [hotel.to_dict() for hotel in hotels],
                file,
                indent=2
            )

    @classmethod
    def create_hotel(cls, hotel):
        """Creates new hotel register"""
        hotels = cls._load_all()

        if any(h.hotel_id == hotel.hotel_id for h in hotels):
            raise ValueError("Hotel already exists")

        hotels.append(hotel)

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Deletes existing hotel register"""
        hotels = cls._load_all()

        filtered = [h for h in hotels if h.hotel_id != hotel_id]

        if len(filtered) == len(hotels):
            raise KeyError("Hotel not found")

        cls._save_all(filtered)

    @classmethod
    def display_hotel_info(cls, hotel_id):
        """Displays information from a selected hotel"""
        hotels = cls._load_all()

        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                return hotel

        raise KeyError("Hotel not found")

    @classmethod
    def modify_hotel_info(cls, hotel_id, **kwargs):
        """Modifies information from a selected hotel"""
        hotels = cls._load_all()
        found = False

        for hotel in hotels:
            if hotel.hotel_id == hotel_id:

                # actualizar solo atributos existentes
                for key, value in kwargs.items():
                    if hasattr(hotel, key):
                        setattr(hotel, key, value)

                # validar coherencia después de cambios
                if hotel.total_rooms <= 0:
                    raise ValueError("total_rooms must be positive")

                if (hotel.available_rooms < 0 or
                        hotel.available_rooms > hotel.total_rooms):
                    raise ValueError("Invalid available_rooms value")

                found = True

        if not found:
            raise KeyError("Hotel not found")

        cls._save_all(hotels)

    @classmethod
    def reserve_room(cls, hotel_id):
        """Creates a reservation for a selected hotel"""
        hotels = cls._load_all()

        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                if hotel.available_rooms <= 0:
                    raise ValueError("No available rooms")

                hotel.available_rooms -= 1
                cls._save_all(hotels)
                return

        raise KeyError("Hotel not found")

    @classmethod
    def cancel_reservation(cls, hotel_id):
        """Cancels a reservation for a selected hotel"""
        hotels = cls._load_all()

        for hotel in hotels:
            if hotel.hotel_id == hotel_id:
                if hotel.available_rooms >= hotel.total_rooms:
                    raise ValueError("All rooms already available")

                hotel.available_rooms += 1
                cls._save_all(hotels)
                return

        raise KeyError("Hotel not found")
