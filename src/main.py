import json
import logging
import boto3
from botocore.exceptions import ClientError

FUNCTION_NAME = 'chess-habits-level1'
logger = logging.getLogger(__name__)


def invoke_function(fen: str) -> str:
    """
    Invokes a Lambda function.

    :param fen: The FEN for the chess position.
    :return: The response from the function invocation.
    """
    try:
        boto3.setup_default_session(region_name='us-east-1')
        lambda_client = boto3.client(
            'lambda'
        )
        response = lambda_client.invoke(
            FunctionName=FUNCTION_NAME,
            Payload=json.dumps({'fen': fen}),
            LogType='Tail')
        logger.info(f"Invoked function: {FUNCTION_NAME}")
    except ClientError:
        logger.exception(f"Couldn't invoke function: {FUNCTION_NAME}")
        raise
    return json.loads(response['Payload'].read().decode())
