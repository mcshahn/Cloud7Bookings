from resources.abstract_base_data_service import BaseDataService
import json


class BookingDataService(BaseDataService):

    def __init__(self, config: dict):
        """

        :param config: A dictionary of configuration parameters.
        """
        super().__init__()

        self.data_dir = config['data_directory']
        self.data_file = config["data_file"]
        self.bookings = []

        self._load()

    def _get_data_file_name(self):
        # DFF TODO Using os.path is better than string concat
        result = self.data_dir + "/" + self.data_file
        return result

    def _load(self):

        fn = self._get_data_file_name()
        with open(fn, "r") as in_file:
            self.bookings = json.load(in_file)

    def _save(self):
        fn = self._get_data_file_name()
        with open(fn, "w") as out_file:
            json.dump(self.bookings, out_file)


    def get_bookings(self) -> list:       
        """

        Returns booking with properties matching the values. Only non-None parameters apply to
        the filtering.

        :param booking_id: booking_id to match.
        
        :return: A list of matching JSON records.
        """
        result = []

        for b in self.bookings:
            result.append(b)

        return result

    def get_bookings_by_booking_id(self, booking_id: str = None) -> list:
        """

        Returns booking with properties matching the values. Only non-None parameters apply to
        the filtering.

        :param booking_id: booking_id to match.
        
        :return: A list of matching JSON records.
        """
        result = []
        # print("bookings", self.bookings)

        for b in self.bookings:

            if (booking_id is None or (b.get("booking_id", None) == booking_id)):
                result.append(b)

        return result
    
    
    def get_bookings_by_space_id(self, space_id: str = None) -> list:
        """

        Returns booking with properties matching the values. Only non-None parameters apply to
        the filtering.

        :param space_id: space_id to match.
        
        :return: A list of matching JSON records.
        """
        result = []

        for b in self.bookings:

            if (space_id is None or (b.get("space_id", None) == space_id)):
                result.append(b)

        return result

    def create_booking(self, booking):
        new_booking = booking.dict()
        new_booking.pop("links")
        self.bookings.append(new_booking)
        return new_booking
    
    def update_booking(self, booking):
        new_booking = booking.dict()
        new_booking.pop("links")
        for b in self.bookings:
            if new_booking["booking_id"] == b["booking_id"]:
                self.bookings.remove(b)
                self.bookings.append(new_booking)
                break
        return new_booking

    def delete_booking(self, booking):
        booking_dict = booking.dict()
        removed= None
        for b in self.bookings:
            if booking_dict["booking_id"] == b["booking_id"]:
                self.bookings.remove(b)
                removed=b
                break
        
        return removed
