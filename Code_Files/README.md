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
############################# Server Basics #############################
broker.id=1

############################# Socket Server Settings #############################
listeners=PLAINTEXT://:9092
advertised.listeners=PLAINTEXT://kafka:9092
listener.security.protocol.map=PLAINTEXT:PLAINTEXT

num.network.threads=3
num.io.threads=8
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

############################# Log Basics #############################
log.dirs=/bitnami/kafka/data
num.partitions=1
num.recovery.threads.per.data.dir=1

############################# Internal Topic Settings #############################
offsets.topic.replication.factor=1
transaction.state.log.replication.factor=1
transaction.state.log.min.isr=1

############################# Log Retention Policy #############################
log.retention.hours=168
log.retention.check.interval.ms=300000

############################# Zookeeper #############################
zookeeper.connect=zookeeperbda:2181

sasl.enabled.mechanisms=PLAIN,SCRAM-SHA-256,SCRAM-SHA-512
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

If the above command doesn't work:
```bash
export HADOOP_CLASSPATH=$(find $HADOOP_HOME/share/hadoop -name "*.jar" | tr '\n' ':')
javac -d classes -cp $HADOOP_CLASSPATH CustomerDataMapper.java CustomerDataReducer.java CustomerDataDriver.java
```

### **Generate JAR File**
```bash
jar -cvf customer-data-cleaner.jar -C classes .
jar -tf customer-data-cleaner.jar
```

### **Extract HBase Tar File**
```bash
tar -xzvf hbase.tar.gz
echo "export HBASE_HOME=/hbase/hbase-1.2.6" >> ~/.bashrc
echo "export HADOOP_CLASSPATH=$(find $HADOOP_HOME/share/hadoop -name \"*.jar\" | tr '\n' ':'):$HBASE_HOME/lib/*" >> ~/.bashrc
echo "export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HBASE_HOME/bin" >> ~/.bashrc
source ~/.bashrc
```

### **Create HDFS Directories**
```bash
hdfs dfs -mkdir -p /user/airflow
hdfs dfs -chown airflow:supergroup /user/airflow
hdfs dfs -chmod 775 /user/airflow
```

---

## **Airflow Container Setup**

### **Access Airflow Container**
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

### **Install Java**
```bash
apt-get install -y openjdk-11-jdk
mkdir -p /usr/share/man/man1
dpkg --configure -a
apt-get install -y openjdk-11-jdk
```

To remove Java if needed:
```bash
apt-get remove --purge openjdk-11-jdk openjdk-11-jre-headless ca-certificates-java
```

### **Extract HBase Files**
```bash
tar -xzvf hbase-2.4.13-bin.tar.gz
export HBASE_HOME=/usr/local/airflow/hbase/hbase-2.4.13
export PATH=$PATH:$HBASE_HOME/bin
echo "export HBASE_HOME=/usr/local/airflow/hbase/hbase-2.4.13" >> ~/.bashrc
echo "export PATH=$PATH:$HBASE_HOME/bin" >> ~/.bashrc
source ~/.bashrc
```

### **HDFS Configuration**
```bash
hdfs dfs -mkdir /airflow
hdfs dfs -chown airflow:supergroup /airflow
hdfs dfs -chmod 775 /airflow
```

### **Run Hadoop Jobs**
```bash
hadoop jar /usr/local/airflow/CustomerCleaner/customer-data-cleaner.jar CustomerDataDriver /airflow/customer_data_raw /airflow/customer_data_cleaned
hdfs dfs -ls /airflow/customer_data_cleaned
hdfs dfs -cat /airflow/customer_data_cleaned/part-00000
```

---

## **HBase Container Setup**

### **Create Tables**
```bash
create 'CustomerTable', 'info'
create 'ProductTable', 'details', 'inventory'
create 'OrderTable', 'info'
```

### **HDFS and HFiles Setup**
```bash
hdfs dfs -mkdir /hfiles
hdfs dfs -chown hbase:supergroup /hfiles
hdfs dfs -chmod 775 /hfiles
```

### **Generate HFiles**
```bash
hadoop jar /usr/local/airflow/CustomerHFile/customer-hfile-generator.jar CustomerHFileDriver /airflow/customer_data_cleaned/part-r-00000 /hfiles/customer CustomerTable
```

### **Load HFiles into HBase**
```bash
hbase org.apache.hadoop.hbase.mapreduce.LoadIncrementalHFiles /hfiles/customer CustomerTable
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
spark-submit --master spark://spark-master-bda:7077 --deploy-mode client --executor-memory 4G --total-executor-cores 4 --conf "spark.executor.heartbeatInterval=120s" --conf "spark.network.timeout=300s" /usr/local/airflow/sparkanalysis/customerAnalysis.py
```

---

## **Zookeeper Setup**

### **Enable Zookeeper Commands**
Edit `/opt/bitnami/zookeeper/conf/zoo.cfg`:
```properties
4lw.commands.whitelist=ruok,stat,conf,isro
```

Test Zookeeper:
```bash
echo "ruok" | nc localhost 2181
```

---

## **Dashboard Container Setup**

### **Run Streamlit Dashboard**
```bash
streamlit run EDA.py --server.port 8501
```

---

## **Extra Utility Commands**

### **Remove HDFS Directories**
```bash
hdfs dfs -rm -r -skipTrash <directory-path>
```

### **Find Airflow Database**
```bash
find / -type f -name "airflow.db" 2>/dev/null
```

### **Connect Docker Network**
```bash
docker network connect bda_network custom_airflow
```

---