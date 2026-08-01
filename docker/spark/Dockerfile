FROM apache/spark:3.5.6

USER root

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/ivy

RUN /opt/spark/bin/spark-submit \
    --conf spark.jars.ivy=/tmp/ivy \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
    --class org.apache.spark.examples.SparkPi \
    /opt/spark/examples/jars/spark-examples_2.12-3.5.6.jar 1 || true

RUN find /tmp/ivy -name "*.jar" -exec cp {} /opt/spark/jars/ \;

RUN rm -rf /tmp/ivy

USER spark