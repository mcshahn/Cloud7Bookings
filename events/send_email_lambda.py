import json
import boto3

def lambda_handler(event, context):
    client = boto3.client("ses")
    booking = event['Records'][0]['Sns']['Message']
    subject = "New Booking Alert"
    body = "a new booking of " + str(booking)+ " was created"
    message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}
    response = client.send_email(Source = "mcshahn@gmail.com",
               Destination = {"ToAddresses": ["mcshahn@gmail.com"]}, Message = message)
    return response