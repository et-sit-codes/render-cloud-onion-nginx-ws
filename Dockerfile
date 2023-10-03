FROM python:3.10-alpine
WORKDIR /
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

## Install build dependencies for docker-gen
RUN apk add --update \
        curl \
        gcc \
        git \
        make \
        musl-dev


RUN apk -U --no-progress upgrade \
 && apk -U --no-progress add tor supervisor

## Install Nginx
RUN apk add nginx

EXPOSE 3030
COPY . .

CMD python3 main.py & python3 checker.py && chmod 700 /tor_server/hidden_service && tor -f /tor_server/torrc.in
