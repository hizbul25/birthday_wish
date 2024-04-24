FROM python:3.10-slim

WORKDIR /home/user/app/

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off 

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

# Install system dependencies
RUN apt-get update && apt-get install python3-dev gcc build-essential libpq-dev -y

# install python dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt /home/user/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /home/user/app/

USER user
