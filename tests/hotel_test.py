import tempfile
import unittest
from pathlib import Path

from app.hotel import Hotel


class HotelTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        Hotel.file_path = Path(self.temp_dir.name) / "hotels.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_display_hotel(self):
        Hotel.create_hotel(Hotel("H1", "Hotel A", 10, 10))
        h = Hotel.display_hotel_info("H1")
        self.assertEqual(h.hotel_name, "Hotel A")
        self.assertEqual(h.total_rooms, 10)
        self.assertEqual(h.available_rooms, 10)

    def test_delete_hotel(self):
        Hotel.create_hotel(Hotel("H1", "Hotel A", 10, 10))
        Hotel.delete_hotel("H1")
        with self.assertRaises(KeyError):
            Hotel.display_hotel_info("H1")

    def test_modify_hotel_info(self):
        Hotel.create_hotel(Hotel("H1", "Hotel A", 10, 10))
        Hotel.modify_hotel_info("H1", hotel_name="Hotel B")
        h = Hotel.display_hotel_info("H1")
        self.assertEqual(h.hotel_name, "Hotel B")

    # ---- Negative cases ----

    def test_create_duplicate_hotel_raises(self):
        Hotel.create_hotel(Hotel("H1", "Hotel A", 10, 10))
        with self.assertRaises(ValueError):
            Hotel.create_hotel(Hotel("H1", "Hotel X", 5, 5))

    def test_delete_missing_hotel_raises(self):
        with self.assertRaises(KeyError):
            Hotel.delete_hotel("NOPE")

    def test_reserve_room_no_availability_raises(self):
        Hotel.create_hotel(Hotel("H1", "Hotel A", 1, 0))
        with self.assertRaises(ValueError):
            Hotel.reserve_room("H1")

    def test_cancel_reservation_when_all_available_raises(self):
        Hotel.create_hotel(Hotel("H1", "Hotel A", 2, 2))
        with self.assertRaises(ValueError):
            Hotel.cancel_reservation("H1")

    def test_invalid_json_returns_empty_list(self):
        # Create invalid JSON file
        Hotel.file_path.write_text("{not json", encoding="utf-8")

        # Should not crash; should behave as empty database
        with self.assertRaises(KeyError):
            Hotel.display_hotel_info("H1")