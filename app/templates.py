
from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

aws_template = f"""
[cli_user]
aws_access_key_id = {AWS_ACCESS_KEY_ID}
aws_secret_access_key = {AWS_SECRET_ACCESS_KEY}

[<ACCOUNT_NAME>]
role_arn = <ROLE_ARN>
source_profile = cli_user
external_id = <EXTERNAL_ID>
"""

steampipe_config_template = """
connection "aws_raw_connection" {
  plugin  = "aws"
  profile = "cli_user"
  regions = ["ap-southeast-2"]
}

connection "aws_client_connection" {
  plugin  = "aws"
  profile = "<ACCOUNT_NAME>"
  regions = ["ap-southeast-2"]
}
"""

if __name__ == '__main__':

    a = steampipe_config_template.replace('<ACCOUNT_NAME>', "Andrew's account")

    with open('test.txt', 'w') as f:
        f.write(a)
