# simpliance
making compliance simple

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
