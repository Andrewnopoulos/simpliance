# simpliance
making compliance simple

## Notes

- use ClassVar to set the table name

## Pushing creds to steampipe

`~/.aws/credentials`
Defines credentials to accounts
```
# This user must have sts:AssumeRole permission for arn:aws:iam::*:role/spc_role
[cli_user]
aws_access_key_id = AKIA4YFAKEKEYXTDS252
aws_secret_access_key = SH42YMW5p3EThisIsNotRealzTiEUwXN8BOIOF5J8m

[account_a_role_without_mfa]
role_arn = arn:aws:iam::111111111111:role/spc_role
source_profile = cli_user
external_id = xxxxx

[account_b_role_without_mfa]
role_arn = arn:aws:iam::222222222222:role/spc_role
source_profile = cli_user
external_id = yyyyy
```

`~/.steampipe/config/aws.spc`

Defines connections
```
connection "aws_account_a" {
  plugin  = "aws"
  profile = "account_a_role_without_mfa"
  regions = ["us-east-1", "us-east-2"]
}

connection "aws_account_b" {
  plugin  = "aws"
  profile = "account_b_role_without_mfa"
  regions = ["us-east-1", "us-east-2"]
}
```

Need to have both files as volumes. Read/write can be done by the python app.

## TODO

- Push the aws credentials to the steampipe container during build
- Implementation for adding/removing linked AWS profiles

## How's it gonna go?

- Benchmark request from a client comes in
- `powerpipe benchmark run cis_v150 --search-path-prefix aws_connection_2`
- What information do we need?
  - Which Benchmark?
  - Which connection -> search-path-prefix
  - Who to return the data to?
  - search-path-prefix and data destination are connected = user information (fetch from db?)
  - return as html and/or downloadable pdf
  - when request is made: generate an ID
  - request to that ID will return differently depending on the request state
  - ultimately it'll return the report

  - Probably gonna want to put steampipe and powerpipe into its own container
  - managing them plus an api server is a pita
  
  SOLUTION:
  - One container runs steampipe
  - other container runs powerpipe + fastapi
  - Docker compose for deployment


## Connect to host

```
ssh -i my-key.pem admin@ec2-3-27-14-73.ap-southeast-2.compute.amazonaws.com
```

## Stack

sudo apt install nginx -y
