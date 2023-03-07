import json
import logging
import boto3
from botocore.exceptions import ClientError

FUNCTION_NAME = 'chess-habits-level1'
logger = logging.getLogger(__name__)


def invoke_function(fen: str):
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
        logger.info("Invoked function %s.", FUNCTION_NAME)
    except ClientError:
        logger.exception("Couldn't invoke function %s.", FUNCTION_NAME)
        raise
    return response
