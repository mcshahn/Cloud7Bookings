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

    def get_bookings(self, booking_id: str = None) -> list:
        """

        Returns booking with properties matching the values. Only non-None parameters apply to
        the filtering.

        :param booking_id: booking_id to match.
        
        :return: A list of matching JSON records.
        """
        result = []

        for b in self.bookings:

            if (booking_id is None or (b.get("booking_id", None) == booking_id)):
                result.append(b)

        return result

