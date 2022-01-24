import logging
from typing import Dict, List

import boto3.session
from botocore.config import Config
from mypy_boto3_iam.client import IAMClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class IAMService:
    def __init__(self):
        self.session = boto3.session.Session()
        self.client: IAMClient = self.session.client("iam", config=Config())

    def create_role(self, role_name: str, assume_role_policy_document: str) -> bool:
        """
        ロール作成。信頼関係のポリシードキュメントもあわせて設定。
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_role
        """
        try:
            self.client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=assume_role_policy_document,
            )
            return True
        except Exception as e:
            if e.response["Error"]["Code"] == "EntityAlreadyExists":
                return True
            else:
                logger.error(e)
                return False

    def waiter_role_exist(self, role_name: str) -> None:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_waiter
        """
        waiter = self.client.get_waiter("role_exists")
        waiter.wait(RoleName=role_name)

    def attach_role_policy(self, role_name: str, policy_arn: str) -> bool:
        """
        AWS管理ポリシーの付与
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.attach_role_policy
        """
        try:
            self.client.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def put_role_policy(
        self, role_name: str, policy_name: str, policy_document: str
    ) -> bool:
        """
        インラインポリシーの付与
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.put_role_policy
        """
        try:
            self.client.put_role_policy(
                RoleName=role_name,
                PolicyName=policy_name,
                PolicyDocument=policy_document,
            )
            return True
        except Exception as e:
            logger.error(e)
            return False

    def update_account_password_policy(self) -> bool:
        """
        パスワードポリシー内容はサンプル
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.update_account_password_policy
        """
        try:
            self.client.update_account_password_policy(
                MinimumPasswordLength=10,
                RequireSymbols=True,
                RequireNumbers=True,
                RequireUppercaseCharacters=True,
                RequireLowercaseCharacters=True,
                AllowUsersToChangePassword=True,
            )
            return True
        except Exception as e:
            logger.error(e)
            return False

    def get_account_password_policy(self) -> Dict:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_account_password_policy
        """
        try:
            resp = self.client.get_account_password_policy()
            return resp["PasswordPolicy"]
        except Exception as e:
            logger.error(e)
            return {}

    def equals_password_policy(self) -> bool:
        """
        パスワードポリシー内容はサンプル
        """
        password_policy = self.get_account_password_policy(self)
        if password_policy is None:
            return False
        if (
            password_policy["MinimumPasswordLength"] == 10
            and password_policy["RequireSymbols"] == True
            and password_policy["RequireNumbers"] == True
            and password_policy["RequireUppercaseCharacters"] == True
            and password_policy["RequireLowercaseCharacters"] == True
            and password_policy["AllowUsersToChangePassword"] == True
        ):
            return True
        else:
            return False

    def delete_role_policy(self, role_name: str, policy_name: str) -> bool:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role_policy
        """
        try:
            self.client.delete_role_policy(RoleName=role_name, PolicyName=policy_name)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def delete_role(self, role_name: str) -> bool:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.delete_role
        """
        try:
            self.client.delete_role(RoleName=role_name)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def list_roles(self) -> List:
        """
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles
        """
        try:
            resp = self.client.list_roles()
            return resp["Roles"]
        except Exception as e:
            logger.error(e)
            return []

    def list_attached_role_policies(self, role_name: str) -> List:
        """
        AWS管理ポリシーの確認
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_attached_role_policies
        """
        try:
            resp = self.client.list_attached_role_policies(RoleName=str(role_name))
            return resp["AttachedPolicies"]
        except Exception as e:
            logger.error(e)
            return []

    def list_role_policies(self, role_name: str) -> List:
        """
        インラインポリシーの確認
        refs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_role_policies
        """
        try:
            resp = self.client.list_role_policies(RoleName=str(role_name))
            return resp["PolicyNames"]
        except Exception as e:
            logger.error(e)
            return []
