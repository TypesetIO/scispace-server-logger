"""
    Client for pushing the events into AWS KINESIS through boto3
"""
import json
import boto3


class KinesisFirehoseClient(object):
    """
        Client to connect to Kinesis Firehose service in AWS
    """

    def __init__(self) -> None:
        self._cli = boto3.client('firehose')

    def push_record(self, **kwargs):
        """
            Push the record to delivery stream provided
        """
        delivery_stream_name = kwargs.get('delivery_stream_name')
        data = kwargs.get('data')
        response = self._cli.put_record(
            DeliveryStreamName=delivery_stream_name,
            Record={
                'Data': json.dumps(data)
            }
        )
        return response.get('RecordId')
