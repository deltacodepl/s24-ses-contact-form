import boto3
from botocore.exceptions import ClientError
import json
import os
from datetime import datetime
import uuid
import decimal

sender = os.environ['SENDER_EMAIL']
info_email = os.environ['INFO_EMAIL']
subject = os.environ['EMAIL_SUBJECT']
dbtable = os.environ['DYNAMODB_TABLE']
charset = 'UTF-8'

client = boto3.client('ses')
dynamodb = boto3.resource('dynamodb')

def sendEmail(event, context):
    print(event)
    try:
        data = event['body']
        content = f"New message from {data['email']} " + data['senderName'] + ' phone ' + data['phone'] + ',\n: ' + data['message']
        saveToDynamoDB(data)
        response = sendEmailToUser(data, content)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Message:"),
        print(response)
    return f"Email sent: {response}"

def list(event, context):
    table = dynamodb.Table(dbtable)
    result = table.scan()
    return {
        "statusCode": 200,
        "body": result['Items']
    }

def saveToDynamoDB(data):
    timestamp = int(datetime.timestamp(datetime.now()))
    
    table = dynamodb.Table(dbtable)
    item = {
        'id': str(uuid.uuid1()),
        'senderName': data['senderName'],
        'phone': data['phone'],
        'email': data['email'],
        'message': data['message'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }
    table.put_item(Item=item)
    return

def sendEmailToUser(data, content):

    return client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': [
                info_email,
            ],
        },
        Message={
            'Subject': {
                'Charset': charset,
                'Data': subject
            },
            'Body': {
                'Html': {
                    'Charset': charset,
                    'Data': content
                },
                'Text': {
                    'Charset': charset,
                    'Data': content
                }
            }
        }
    )
