"""Hotel module"""

import json
from pathlib import Path

JSON_FILE = Path("A00828432_6.2\data\hotels.json")

class Hotel:
    """This class represents a hotel and its operations"""
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

    def create_hotel():
        return
    def delete_hotel():
        return
    def display_hotel_info():
        return
    def modify_hotel_info():
        return
    def reserve_room():
        return
    def cancel_reservation():
        return
