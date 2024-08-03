FROM python:3.12

RUN apt-get update
RUN /bin/sh -c "$(curl -fsSL https://steampipe.io/install/steampipe.sh)"

RUN useradd -ms /bin/bash andrew

USER andrew
RUN steampipe plugin install aws
RUN steampipe plugin install steampipe

CMD ["steampipe", "service", "start", "--foreground", "--database-listen", "network", "--database-password", "password"]