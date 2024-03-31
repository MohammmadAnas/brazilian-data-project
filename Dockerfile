# First-time build can take upto 10 mins.

FROM apache/airflow:2.2.3

ENV AIRFLOW_HOME=/opt/airflow

USER root

RUN apt-get update -qq \
    && apt-get install firefox-esr -y -qq \
    && apt-get install wget -y -qq

COPY requirements.txt .

RUN pip install -q -r requirements.txt
USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
RUN pip install apache-airflow-providers-apache-spark==2.1.1


# workaround to fix selenium module not found
# RUN curl -sSLf "https://files.pythonhosted.org/packages/b4/f9/e9ac5e4c5d84b07c7d117d67b2c84be221bcb9e62ff31fd0a1bbc06099c0/selenium-4.19.0-py3-none-any.whl" > ~/selenium-4.1.0-py3-none-any.whl \
#     && chmod +x ~/selenium-4.1.0-py3-none-any.whl \
#     && sudo pip install -q ~/selenium-4.1.0-py3-none-any.whl webdriver_manager

WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID