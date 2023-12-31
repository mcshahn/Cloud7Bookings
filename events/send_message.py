import boto3

def publish_message_to_sns(topic_arn, message):
    # Create an SNS client
    sns_client = boto3.client('sns', region_name="us-east-2")

    # Publish a message to the specified SNS topic
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )

    # Print the MessageId of the published message
    # print(response)
    print(f"Message published to SNS. MessageId: {response['MessageId']}")

# Example usage
if __name__ == "__main__":
    # Replace 'your_topic_arn' with the ARN of your SNS topic
    topic_arn = 'arn:aws:sns:us-east-2:985087256160:bookings_changd'
    
    # Specify the message you want to publish
    message = 'Testing from post request'

    # Publish the message to the SNS topic
    publish_message_to_sns(topic_arn, message)
