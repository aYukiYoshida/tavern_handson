FROM python:3.8

# Install python packages
RUN set -x && \
    : Install Python libraries && \
    python -m pip install --upgrade pip && \
    python -m pip install tavern

WORKDIR /usr/local/tavern
ENV PYTHONPATH $PYTHONPATH:/usr/local/tavern/tests

# ENTRYPOINT [ "pytest" ]

# CMD [ "--help" ]