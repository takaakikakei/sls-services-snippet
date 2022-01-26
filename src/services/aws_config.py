import logging
import re
from typing import Dict, List

import boto3.session
from botocore.config import Config
from mypy_boto3_config.client import ConfigServiceClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConfigService:
    def __init__(self):
        self.session = boto3.session.Session()

    def put_configuration_recorder(
        self,
        role_arn: str,
        resource_types: List,
        region_name: str,
        name="default",
        all_supported=False,
        include_global_resource_types=False,
    ) -> None:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_configuration_recorder
        """
        try:
            client: ConfigServiceClient = self.session.client(
                "config",
                region_name=str(region_name),
                config=Config(),
            )
            client.put_configuration_recorder(
                ConfigurationRecorder={
                    "name": name,
                    "roleARN": role_arn,
                    "recordingGroup": {
                        "allSupported": all_supported,
                        "includeGlobalResourceTypes": include_global_resource_types,
                        "resourceTypes": resource_types,
                    },
                }
            )
        except Exception as e:
            logger.error(e)
            return
        else:
            return

    def put_delivery_channel(
        self,
        region_name: str,
        bucket_name: str,
        name="default",
    ) -> None:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.put_delivery_channel
        """
        try:
            client: ConfigServiceClient = self.session.client(
                "config",
                region_name=str(region_name),
                config=Config(),
            )
            client.put_delivery_channel(
                DeliveryChannel={
                    "name": str(name),
                    "s3BucketName": str(bucket_name),
                }
            )
        except Exception as e:
            logger.error(e)
            return
        else:
            return

    def start_configuration_recorder(
        self,
        region_name: str,
        config_recorder_name: str,
    ) -> None:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.start_configuration_recorder
        """
        try:
            client: ConfigServiceClient = self.session.client(
                "config",
                region_name=str(region_name),
                config=Config(),
            )
            client.start_configuration_recorder(
                ConfigurationRecorderName=config_recorder_name
            )
        except Exception as e:
            logger.error(e)
            return
        else:
            return

    def describe_configuration_recorders(
        self,
        region_name: str,
        recorder_name: str,
    ) -> bool:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_configuration_recorders
        """
        try:
            client: ConfigServiceClient = self.session.client(
                "config",
                region_name=str(region_name),
                config=Config(),
            )
            client.describe_configuration_recorders(
                ConfigurationRecorderNames=[str(recorder_name)]
            )
        except Exception as e:
            logger.error(e)
            return False
        else:
            return True

    def describe_delivery_channels(
        self,
        region_name: str,
        recorder_name: str,
    ) -> bool:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_delivery_channels
        """
        try:
            client: ConfigServiceClient = self.session.client(
                "config",
                region_name=str(region_name),
                config=Config(),
            )
            client.describe_delivery_channels(
                DeliveryChannelNames=[str(recorder_name)],
            )
        except Exception as e:
            logger.error(e)
            return False
        else:
            return True

    def is_configuration_recorder_status(
        self,
        region_name: str,
        recorder_name: str,
    ) -> bool:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.describe_configuration_recorder_status
        """
        try:
            client: ConfigServiceClient = self.session.client(
                "config",
                region_name=str(region_name),
                config=Config(),
            )
            resp = client.describe_configuration_recorder_status(
                ConfigurationRecorderNames=[recorder_name]
            )
        except Exception as e:
            logger.error(e)
            return False
        else:
            if resp["ConfigurationRecordersStatus"][0]["recording"]:
                return True
            return False
