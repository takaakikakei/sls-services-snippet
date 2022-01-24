import logging
import traceback

import src.services.iam_env
from src.services.iam import IAMService

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _format_traceback_str(exception: Exception) -> str:
    tb = traceback.TracebackException.from_exception(exception)
    return "".join(list(tb.format()))


class IAMSetUpUseCase:
    def __init__(self, iam_service):
        self.iam_service = iam_service

    def exec(self, event: str) -> None:
        role_name = "test_role"

        CONFIG_ROLE_ALL_REGIONS_ASSUME_ROLE_POLICY = (
            src.services.iam_env.CONFIG_ROLE_ALL_REGIONS_ASSUME_ROLE_POLICY
        )
        self.iam_service.create_role(
            role_name, CONFIG_ROLE_ALL_REGIONS_ASSUME_ROLE_POLICY
        )

        self.iam_service.waiter_role_exist(role_name)

        READ_ONLY_ACCESS_ARN = src.services.iam_env.READ_ONLY_ACCESS_ARN
        self.iam_service.attach_role_policy(
            role_name,
            READ_ONLY_ACCESS_ARN,
        )

        VIEW_BILLING_POLICY = src.services.iam_env.VIEW_BILLING_POLICY
        self.iam_service.put_role_policy(
            role_name,
            "ViewBillingPolicy",
            VIEW_BILLING_POLICY,
        )

        return


def _use_case_init() -> IAMSetUpUseCase:
    """
    Usecase初期化（Mock差込易くする用)
    """
    iam_service = IAMService()
    return IAMSetUpUseCase(iam_service)


def exec(event):
    logger.info(f"event: {event}")
    use_case = _use_case_init()
    try:
        use_case.exec(event)
        return "OK"
    except Exception as e:
        logger.exception(f"{_format_traceback_str(e)}")
    return "NG"
