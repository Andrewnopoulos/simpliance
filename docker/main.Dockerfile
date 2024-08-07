FROM python:3.12

RUN apt-get update
RUN /bin/sh -c "$(curl -fsSL https://powerpipe.io/install/powerpipe.sh)"

RUN mkdir pp

WORKDIR /pp

RUN powerpipe -v
RUN powerpipe mod init
RUN powerpipe mod install github.com/turbot/steampipe-mod-aws-compliance

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./powerpipe.ppc /pp/workspaces.ppc

COPY ./app /code/app
COPY ./db_setup.sql /code/db_setup.sql

WORKDIR /code/app

CMD ["fastapi", "run", "main.py", "--port", "8000", "--proxy-headers"]