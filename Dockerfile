FROM python:3.6
LABEL maintainer="wilddeej@gmail.com"

ARG GIT_REPO=https://github.com/ellisonleao/pyshorteners.git
ARG GIT_REPO_REV=master
RUN \
  git clone $GIT_REPO \
  && cd pyshorteners \
  && git checkout $GIT_REPO_REV \
  && pip install -r requirements_test.txt \
  && python setup.py install

WORKDIR pyshorteners
