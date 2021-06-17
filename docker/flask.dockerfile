FROM python:3.8-alpine

# Install python packages
RUN set -x && \
    : Install Python libraries && \
    python -m pip install --upgrade pip && \
    python -m pip install flask pyjwt pyyaml

COPY tests/components/authentication.yaml /usr/local