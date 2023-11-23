#
# FastAPI is a framework and library for implementing REST web services in Python.
# https://fastapi.tiangolo.com/
#
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
from typing import List, Union

# I like to launch directly and not use the standard FastAPI startup process.
# So, I include uvicorn
import uvicorn


from resources.bookings.booking_models import BookingRspModel, BookingModel
from resources.bookings.bookings_data_service import BookingDataService
from resources.bookings.bookings_resource import BookingsResource

import boto3
from events.send_message import publish_message_to_sns




app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


# ******************************
#
# DFF TODO Show the class how to do this with a service factory instead of hard code.


def get_data_service():

    config = {
        "data_directory": "./data",
        "data_file": "bookings.json"
    }

    ds = BookingDataService(config)
    return ds


def get_bookings_resource():
    ds = get_data_service()
    config = {
        "data_service": ds
    }
    res = BookingsResource(config)
    return res


bookings_resource = get_bookings_resource()

# schools_resource = SchoolsResource(config={"students_resource": students_resource})


#
# END TODO
# **************************************


@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")


@app.get("/bookings", response_model=List[BookingRspModel])
async def get_bookings():
    """
    Return a list of bookings matching a query string.

    - **booking_id**: booking's id
   
    """
    result = bookings_resource.get_bookings()
    # print("in /bookings", result)
    return result
@app.get("/bookings/booking_id/{booking_id}", response_model=Union[BookingRspModel, None])
async def get_booking_by_booking_id(booking_id: str):
    """
    Return a booking based on booking_id.

    - **booking_id**: booking's id
    """
    result = None
    
    result = bookings_resource.get_bookings_by_booking_id(booking_id)
    # print(result)
    if len(result) == 1:
        result = result[0]
    else:
        raise HTTPException(status_code=404, detail="Not found")

    return result

@app.get("/bookings/space_id/{space_id}", response_model=Union[BookingRspModel, None])
async def get_booking_by_space_id(space_id: str):
    """
    Return a booking based on booking_id.

    - **booking_id**: booking's id
    """
    result = None
    
    result = bookings_resource.get_bookings_by_space_id(space_id)
    # print(result)
    if len(result) == 1:
        result = result[0]
    else:
        raise HTTPException(status_code=404, detail="Not found")

    return result

@app.post("/bookings/") #append/create a new one; if something exists-->append
async def create_item(item: BookingRspModel):
    bookings_resource.create_booking(item)
    topic_arn = 'arn:aws:sns:us-east-2:985087256160:bookings_changd'
    
    # Specify the message you want to publish
    # message = 'Testing from post request'

    # Publish the message to the SNS topic
    publish_message_to_sns(topic_arn, str(item))
    return item

@app.put("/bookings/") #update and create(but not append,just return  ) new one if instance doesn't exist
async def update_item(item: BookingRspModel):
    bookings_resource.update_booking(item)
    return item

@app.delete("/bookings/")
async def delete_item(item: BookingRspModel):
    bookings_resource.delete_booking(item)
    return item




# @app.get("/get_item")
# async def async_call(item_name: str = None):
#     result = await example_instance.get_item(item_name)
#     return JSONResponse(content={"message": result})


# @app.get("/get_student_async")
# async def async_call():
#     result = await example_instance.get_student_async()
#     return JSONResponse(content={"students": result})


# @app.get("/get_student_sync")
# async def async_call():
#     result = await example_instance.get_student_sync()
#     return JSONResponse(content={"students": result})


if __name__ == "__main__":
    import uvicorn
    # session = boto3.Session(
    #     aws_access_key_id=ACCESS_KEY,
    #     aws_secret_access_key=SECRET_KEY,
    #     )
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
