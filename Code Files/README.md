# Project Setup Instructions

This document provides step-by-step instructions to set up and run the project using Docker containers for Kafka, Hadoop, Airflow, HBase, and Spark.

---

## **Kafka Container Setup**

### **Create Topics**
Run the following commands to create the required topics:
```bash
/opt/bitnami/kafka/bin/kafka-topics.sh --create --topic ProductTopic --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1
/opt/bitnami/kafka/bin/kafka-topics.sh --create --topic OrderTopic --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1
/opt/bitnami/kafka/bin/kafka-topics.sh --create --topic CustomerTopic --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1
```

### **List Topics**
```bash
/opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### **Delete Topics**
```bash
kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic OrderTopic
kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic ProductTopic
kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic CustomerTopic
```

### **View Topic Data**
```bash
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic ProductTopic --from-beginning
```

### **Edit Server Properties**
Update the following files:
- `/opt/bitnami/kafka/config/kraft/server.properties`
- `/opt/bitnami/kafka/config/server.properties`

Ensure the following configurations:
```properties
broker.id=1
listeners=PLAINTEXT://:9092
advertised.listeners=PLAINTEXT://kafka:9092
listener.security.protocol.map=PLAINTEXT:PLAINTEXT
log.dirs=/bitnami/kafka/data
num.partitions=1
offsets.topic.replication.factor=1
zookeeper.connect=zookeeperbda:2181
```

---

## **Hadoop-Namenode Container Setup**

### **Create Hadoop Tar File**
```bash
cd /opt
tar -czvf hadoop-3.2.1.tar.gz hadoop-3.2.1/
```

### **Compile Java Files and Create JAR**
```bash
echo $JAVA_HOME
export PATH=$JAVA_HOME/bin:$PATH
export HADOOP_HOME=/opt/hadoop-3.2.1
export PATH=$HADOOP_HOME/bin:$PATH
mkdir -p classes
hadoop com.sun.tools.javac.Main -d classes /tmp/*.java
```

### **Generate JAR File**
```bash
export HADOOP_CLASSPATH=$(find $HADOOP_HOME/share/hadoop -name "*.jar" | tr '\n' ':')
javac -d classes -cp $HADOOP_CLASSPATH CustomerDataMapper.java CustomerDataReducer.java CustomerDataDriver.java
jar -cvf customer-data-cleaner.jar -C classes .
jar -tf customer-data-cleaner.jar
```

---

## **Airflow Container Setup**

### **Prepare Airflow Container**
```bash
docker exec -it --user root custom_airflow /bin/bash
chmod 666 /var/run/docker.sock
docker exec -it custom_airflow /bin/bash
```

### **Install Dependencies**
```bash
export FERNET_KEY=RP9QND5O48Du6-_W5lKvwI-NarPSZyZmTs9IfcMDork=
pip install kafka-python pyspark
```

### **Unpack Hadoop Files**
```bash
mkdir /usr/local/airflow/hadoop
tar -xzvf hadoop-3.2.1.tar.gz -C /usr/local/airflow/hadoop
```

### **Set Environment Variables**
```bash
export HADOOP_HOME=/usr/local/airflow/hadoop/hadoop-3.2.1/
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

---

## **HBase Container Setup**

### **Start HBase**
```bash
/hbase-2.1.3/bin/start-hbase.sh
```

### **Update HBase Configuration (`hbase-site.xml`)**
```xml
<configuration>
  <property>
    <name>hbase.rootdir</name>
    <value>hdfs://hadoop-namenode-bda:9000/hbase</value>
  </property>
  <property>
    <name>hbase.zookeeper.quorum</name>
    <value>zookeeperbda</value>
  </property>
  <property>
    <name>hbase.regionserver.thrift.port</name>
    <value>9090</value>
  </property>
</configuration>
```

---

## **Spark Setup**

### **Install Spark and Verify**
```bash
mkdir /usr/local/airflow/spark
tar -xzvf spark.tar.gz -C /usr/local/airflow/spark
export SPARK_HOME=/usr/local/airflow/spark
export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
spark-submit --version
```

### **Run Spark Jobs**
```bash
spark-submit --master spark://spark-master-bda:7077 --deploy-mode client /usr/local/airflow/sparkanalysis/customerAnalysis.py
```

---

## **HDFS Configuration**

### **Create HDFS Directories**
```bash
hdfs dfs -mkdir /airflow
hdfs dfs -chown airflow:supergroup /airflow
hdfs dfs -chmod 775 /airflow
```

---

## **HBase Table Creation**

### **Create Tables**
```bash
create 'CustomerTable', 'info'
create 'ProductTable', 'details', 'inventory'
create 'OrderTable', 'info'
```

---

## **Dashboard Container Setup**

### **Run Streamlit Dashboard**
```bash
streamlit run EDA.py --server.port 8501
```

---

## **Zookeeper Setup**

### **Enable Zookeeper Commands**
Edit `/opt/bitnami/zookeeper/conf/zoo.cfg`:
```properties
4lw.commands.whitelist=ruok,stat,conf,isro
```

---

## **Utility Commands**

### **Remove HDFS Directories**
```bash
hdfs dfs -rm -r -skipTrash <directory-path>
```

### **Truncate HBase Tables**
```bash
truncate 'CustomerTable'
truncate 'OrderTable'
truncate 'ProductTable'
```

---


