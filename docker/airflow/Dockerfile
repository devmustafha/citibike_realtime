FROM apache/spark:3.5.6 AS spark

FROM apache/airflow:2.10.5

# COPY airflow/requirements.txt /requirements.txt

# RUN pip install --no-cache-dir -r /requirements.txt

USER root
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

COPY --from=spark /opt/spark /opt/spark

RUN /opt/spark/bin/spark-submit \
    --conf spark.jars.ivy=/tmp/ivy \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
    --class org.apache.spark.examples.SparkPi \
    /opt/spark/examples/jars/spark-examples_2.12-3.5.6.jar 1 || true

RUN find /tmp/ivy -name "*.jar" -exec cp {} /opt/spark/jars/ \;

RUN rm -rf /tmp/ivy

ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${PATH}"

USER airflow