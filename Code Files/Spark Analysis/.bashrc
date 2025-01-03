export SPARK_HOME=/spark
export PATH=$PATH:$SPARK_HOME/bin
export HBASE_HOME=/opt/hbase-1.2.6
export PATH=$PATH:$HBASE_HOME/bin
export HADOOP_HOME=/opt/hadoop-3.2.1
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export SPARK_CLASSPATH=$SPARK_HOME/jars/*:$HBASE_HOME/lib/*:$HBASE_HOME/conf:/spark/jars/spark-hbase-connector_2.10-1.0.3.jar:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/*
export JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_DIST_CLASSPATH=$($HADOOP_HOME/bin/hadoop classpath)

