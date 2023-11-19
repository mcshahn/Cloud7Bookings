# from flask import Flask
# app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'docker Test Worked for AWS (Cloud 7) (it better work...))'


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000)


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


from resources.students.students_resource import StudentsResource
from resources.students.students_data_service import StudentDataService
from resources.students.student_models import StudentModel, StudentRspModel
from resources.schools.school_models import SchoolRspModel, SchoolModel
from resources.schools.schools_resource import SchoolsResource
from resources.bookings.booking_models import BookingRspModel, BookingModel
from resources.bookings.bookings_data_service import BookingDataService
from resources.bookings.bookings_resource import BookingsResource



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


# ******************************
#
# DFF TODO Show the class how to do this with a service factory instead of hard code.


def get_data_service():

    config = {
        "data_directory": "/Users/michelle/Desktop/Cloud Computing/Cloud7Booking/data",
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
    print("in /bookings", result)
    return result
@app.get("/bookings/{booking_id}", response_model=Union[BookingRspModel, None])
async def get_booking(booking_id: str):
    """
    Return a booking based on booking_id.

    - **booking_id**: booking's id
    """
    result = None
    
    result = bookings_resource.get_bookings(booking_id)
    print(result)
    if len(result) == 1:
        result = result[0]
    else:
        raise HTTPException(status_code=404, detail="Not found")

    return result

@app.get("/students/{uni}", response_model=Union[StudentRspModel, None])
async def get_student(uni: str):
    """
    Return a student based on UNI.

    - **uni**: student's UNI
    """
    result = None
    result = students_resource.get_students(uni)
    if len(result) == 1:
        result = result[0]
    else:
        raise HTTPException(status_code=404, detail="Not found")

    return result


# @app.get("/schools", response_model=List[SchoolRspModel])
# async def get_schools():
#     """
#     Return a list of schools.
#     """
#     result = schools_resource.get_schools()
#     return result


# @app.get("/schools/{school_code}/students", response_model=List[StudentRspModel])
# async def get_schools_students(school_code, uni=None, last_name=None):
#     """
#     Return a list of schools.
#     """
#     result = schools_resource.get_schools_students(school_code, uni, last_name)
#     return result




# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8011)


# from fastapi import FastAPI
# from fastapi.responses import JSONResponse, HTMLResponse
# from pydantic import BaseModel
# import asyncio
# import uvicorn
# from resources.students.students_resource import StudentsResource

# app = FastAPI()


# # example_instance = StudentsResource(config)


# @app.get("/")
# async def home_page():
#     home_page = \
#         """
#         <!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Simple Composite Service Example</title>
#         </head>
#         <body>
        
#             <header>
#                 <h1>Welcome to Simple Composite Example</h1>
#             </header>
        
#             <section>
#                 <h2>Usage</h2>
#                 <p>Please go to <a href="/docs">the OpenAPI docs page for this app.</a>
#             </section>
        
#             <footer>
#                 <p>&copy; 2023 Donald Ferguson. All rights reserved.</p>
#             </footer>
        
#         </body>
#         </html>
#         """
#     return HTMLResponse(home_page)


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
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")