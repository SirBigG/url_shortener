FROM python:3.8.5-slim

ENV PYTHONUNBUFFERED 1

ARG REQUIREMENTS_FILE=requirements.txt

ENV PROJECT_DIR /app

RUN mkdir $PROJECT_DIR

ADD requirements*.txt $PROJECT_DIR/

#RUN apt-get update && \
#    apt-get install -y --no-install-recommends apt-utils && \
#    apt-get install -y --no-install-recommends gcc \
#                                               build-essential \
#                                               && \
#    apt-get clean && \
RUN pip --no-cache-dir install -r $PROJECT_DIR/$REQUIREMENTS_FILE

ADD . $PROJECT_DIR/

WORKDIR $PROJECT_DIR
