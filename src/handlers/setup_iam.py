import logging

import src.use_cases.setup_iam

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
    setup_iam エントリーポイント
    """
    logger.info(f"event: {event}")
    resp = src.use_cases.setup_iam.exec(event)
    return resp
