from resources.abstract_base_resource import BaseResource
from resources.bookings.booking_models import BookingRspModel, BookingModel
from resources.rest_models import Link
from typing import List


class BookingsResource(BaseResource):
    #
    # This code is just to get us started.
    # It is also pretty sloppy code.
    #

    def __init__(self, config):
        super().__init__()

        self.data_service = config["data_service"]

    @staticmethod
    def _generate_links(b: dict) -> BookingRspModel:

        self_link = Link(**{
            "rel": "self",
            "href": "/booking/" + b['booking_id']
        })
        # school_link = Link(**{
        #     "rel": "school",
        #     "href": "/schools/" + s['school_code']
        # })

        links = [
            self_link,
            # school_link
        ]
        rsp = BookingRspModel(**b, links=links)
        return rsp

    def get_bookings(self) -> List[BookingRspModel]:

        result = self.data_service.get_bookings()
        final_result = []

        for b in result:
            m = self._generate_links(b)
            final_result.append(m)

        return final_result


    def get_bookings_by_booking_id(self, booking_id: str = None) -> List[BookingRspModel]:

        result = self.data_service.get_bookings_by_booking_id(booking_id)
        final_result = []

        for b in result:
            m = self._generate_links(b)
            final_result.append(m)

        return final_result
    
    def get_bookings_by_space_id(self, space_id: str = None) -> List[BookingRspModel]:

        result = self.data_service.get_bookings_by_space_id(space_id)
        final_result = []

        for b in result:
            m = self._generate_links(b)
            final_result.append(m)

        return final_result


    def create_booking(self, item):
        result = self.data_service.create_booking(item)
        return result
    
    def update_booking(self, item):
        result = self.data_service.update_booking(item)
        return result
    
    def delete_booking(self, item):
        result = self.data_service.delete_booking(item)
        return result

