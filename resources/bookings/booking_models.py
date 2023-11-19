from __future__ import annotations
from pydantic import BaseModel
from typing import List

from resources.rest_models import Link


class BookingModel(BaseModel):
    booking_id: str
    space_id: str
    student_uni: str
    admin_uni: str
    start_time: str
    end_time: str   
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "booking_id": "1",
                    "space_id": "4",
                    "student_uni": "cl9731",
                    "admin_uni": "li8739",
                    "start_time": "5/26/2023",
                    "end_time": "12/16/2022"
                }
            ]
        }
    }


class BookingRspModel(BookingModel):
    links: List[Link] = None



