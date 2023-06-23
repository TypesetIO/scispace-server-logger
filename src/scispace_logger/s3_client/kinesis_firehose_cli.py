"""
    Client for pushing the events into AWS KINESIS through boto3
"""
import json
import boto3

from ..constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME


class KinesisFirehoseClient(object):
    """
        Client to connect to Kinesis Firehose service in AWS
    """

    def __init__(self) -> None:
        try:
            self._cli = boto3.client(
                'firehose', aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION_NAME)
        except Exception as e:
            print('Exception while establishing boto3 connection: ', str(e))
            self._cli = None

    def push_record(self, **kwargs):
        """
            Push the record to delivery stream provided
        """
        delivery_stream_name = kwargs.get('delivery_stream_name')
        data = kwargs.get('data')
        if not self._cli:
            print('Boto3 Client connection is not established.')
            return None

        response = self._cli.put_record(
            DeliveryStreamName=delivery_stream_name,
            Record={
                'Data': json.dumps(data)
            }
        )
        return response.get('RecordId')
