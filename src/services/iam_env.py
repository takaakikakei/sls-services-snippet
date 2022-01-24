import json

# Trust Relationship Policy Document

CONFIG_ROLE_ALL_REGIONS_ASSUME_ROLE_POLICY = json.dumps(
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {"Service": "config.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }
)

# Permissions policies ARN（AWS managed policy）

READ_ONLY_ACCESS_ARN = "arn:aws:iam::aws:policy/ReadOnlyAccess"
AWS_SUPPORT_ACCESS_ARN = "arn:aws:iam::aws:policy/AWSSupportAccess"
AWS_CONFIG_ROLE_ARN = "arn:aws:iam::aws:policy/service-role/AWS_ConfigRole"

# Permissions policies Document（Inline policy）

VIEW_BILLING_POLICY = json.dumps(
    {
        "Version": "2012-10-17",
        "Statement": [
            {"Action": "aws-portal:ViewBilling", "Effect": "Allow", "Resource": "*"}
        ],
    }
)
