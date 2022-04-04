import copy
import logging
import traceback
from typing import Dict, List, Optional

import boto3.session
from botocore.config import Config
from mypy_boto3_ec2 import EC2Client

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class EC2Service:
    def __init__(self, session: boto3.Session):
        self._session = session
        self._ec2: EC2Client = session.client("ec2")

    def describe_regions(self) -> List:
        """
        refs:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_regions
        """
        try:
            regions = list(
                map(lambda x: x["RegionName"], self._ec2.describe_regions()["Regions"])
            )
            return regions
        except Exception as e:
            logger.error(e)
            return []

    def describe_target_security_groups(self, regions) -> Dict:
        """
        refs:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Paginator.DescribeSecurityGroups
        """
        # 取得したいセキュリティグループのipadressを配列形式で指定
        # TARGET_SG_IP = [xx.xx.xx.xx, yy.yy.yy.yy]
        TARGET_SG_IP = []

        target_sg_all_regions = {}

        for region_name in regions:
            try:
                target_sg = []

                ec2 = self._session.client("ec2", region_name=region_name)
                paginator = ec2.get_paginator("describe_security_groups")
                response_iterator = paginator.paginate(
                    Filters=[
                        {
                            "Name": "ip-permission.cidr",
                            "Values": TARGET_SG_IP,
                        }
                    ]
                )
                for page in response_iterator:
                    if page["SecurityGroups"] == []:
                        continue
                    for security_group in page["SecurityGroups"]:
                        logger.info(security_group)
                        logger.info(security_group["GroupName"])
                        target_sg.append(security_group["GroupName"])

                if target_sg == []:
                    continue
                target_sg_all_regions[region_name] = copy.deepcopy(target_sg)
            except Exception as e:
                logger.error(e)
                return {}

        return target_sg_all_regions
