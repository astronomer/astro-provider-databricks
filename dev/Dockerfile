FROM quay.io/astronomer/astro-runtime:7.3.0-base

USER root

# onbuild stuff
SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]
LABEL maintainer="Astronomer <humans@astronomer.io>"
LABEL io.astronomer.docker=true
LABEL io.astronomer.docker.airflow.onbuild=true

COPY dev/packages.txt .
RUN if [[ -s packages.txt ]]; then \
    apt-get update && cat packages.txt | tr '\r\n' '\n' | sed -e 's/#.*//' | xargs apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*; \
  fi

# Install python packages
COPY dev/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Install astro-sdk-template
COPY ./pyproject.toml  ${AIRFLOW_HOME}/astro_sdk_template/
# The following file are needed because version they are referenced from pyproject.toml
COPY ./README.md  ${AIRFLOW_HOME}/astro_sdk_template/
COPY ./src/astro_sdk_template/__init__.py  ${AIRFLOW_HOME}/astro_sdk_template/src/astro_sdk_template/__init__.py

RUN ls -l ${AIRFLOW_HOME}/astro_sdk_template/
RUN pip install -e "${AIRFLOW_HOME}/astro_sdk_template"


USER astro
