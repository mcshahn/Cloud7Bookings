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

import os
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth

# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


from starlette.middleware.sessions import SessionMiddleware
SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


from fastapi import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError

@app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the url for the /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    # user_data = await oauth.google.parse_id_token(request, access_token)
    user_data = access_token["userinfo"]
    request.session['user'] = dict(user_data)
    return RedirectResponse(url='/')

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

from starlette.responses import HTMLResponse
@app.get('/')
def public(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
    return HTMLResponse('<p> Please log in to access the bookings microservice<p> <a href=/login>Login</a>')


@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@app.get("/homepage")
async def root():
    return RedirectResponse("/static/index.html")


@app.get("/bookings", response_model=List[BookingRspModel])
async def get_bookings(request: Request):
    """
    Return a list of bookings matching a query string.

    - **booking_id**: booking's id
   
    """

    user = request.session.get('user')
    if user:
        result = bookings_resource.get_bookings()
        return result
    return RedirectResponse(url='/')

@app.get("/bookings/booking_id/{booking_id}", response_model=Union[BookingRspModel, None])
async def get_booking_by_booking_id(booking_id: str, request: Request):
    """
    Return a booking based on booking_id.

    - **booking_id**: booking's id
    """
    user = request.session.get('user')
    if user:
        result = bookings_resource.get_bookings_by_booking_id(booking_id)
        # print(result)
        if len(result) == 1:
            result = result[0]
        else:
            raise HTTPException(status_code=404, detail="Not found")

        return result
    return RedirectResponse(url='/')

@app.get("/bookings/space_id/{space_id}", response_model=Union[BookingRspModel, None])
async def get_booking_by_space_id(space_id: str, request: Request):
    """
    Return a booking based on booking_id.

    - **booking_id**: booking's id
    """
    user = request.session.get('user')
    if user:
        result = bookings_resource.get_bookings_by_space_id(space_id)
        # print(result)
        if len(result) == 1:
            result = result[0]
        else:
            raise HTTPException(status_code=404, detail="Not found")

        return result
    return RedirectResponse(url='/')


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
