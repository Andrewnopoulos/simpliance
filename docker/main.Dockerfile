FROM python:3.12-slim

RUN apt-get update
RUN /bin/sh -c "$(curl -fsSL https://powerpipe.io/install/powerpipe.sh)"

RUN mkdir pp

WORKDIR /pp
RUN powerpipe mod init
RUN powerpipe mod install github.com/turbot/steampipe-mod-aws-compliance

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
WORKDIR /code/app

CMD ["fastapi", "run", "main.py", "--port", "8000", "--proxy-headers"]