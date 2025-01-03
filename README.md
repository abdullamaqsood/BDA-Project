# E-Commerce Big Data Processing and Analysis Pipeline

## Description
This project implements an end-to-end big data analytics pipeline for e-commerce data analysis. The pipeline processes, analyzes, and visualizes customer, product, and order data using a combination of big data tools and technologies. Key objectives include identifying top customers and products, analyzing sales trends by demographic factors, and computing total revenue.

### Key Features
- **Real-Time Data Ingestion**: Uses Kafka to ingest streaming data.
- **Distributed Storage**: Hadoop and HBase for scalable storage solutions.
- **ETL Processing**: MapReduce-based data cleaning and transformation.
- **Data Analysis**: Python is used for exploratory and Spark is used for statistical data analysis.
- **Interactive Dashboards**: Built using Streamlit to present results visually.

---

## Architecture
The architecture of the pipeline follows this flow:

1. Kafka for data ingestion.
2. Hadoop and HBase for distributed storage and processing.
3. Airflow for orchestrating the workflow.
4. Spark for performing EDA and ML.
5. Streamlit dashboard for data visualization.

![Pipeline Architecture](Images/architecture_diagram.jpg)

---

## Data Schema

### Customer Table

Column Family: info

| Field        | Data Type |
|--------------|-----------|
| customer_id  | int       |
| name         | string    |
| email        | string    |
| phone        | int       |
| age          | int       |
| gender       | char      |
| location     | string    |

### Product Table

Column Family: details

| Field          | Data Type |
|----------------|-----------|
| product_id     | int       |
| product_name   | string    |
| category       | string    |

Column Family: inventory

| Field          | Data Type |
|----------------|-----------|
| product_id     | int       |
| price          | int       |
| stock_quantity | int       |

### Order Table

Column Family: info

| Field            | Data Type |
|------------------|-----------|
| order_id         | int       |
| customer_id      | int       |
| product_id       | int       |
| quantity         | int       |
| total_amount     | int       |
| transaction_date | date      |
| payment_method   | int       |

---

## Exploratory Data Analysis (EDA)
The following visualizations provide insights into customer demographics and behavior:

### Age Distribution
![Age Distribution](Images/EDA1.png)

### Location Distribution
![Location Distribution](Images/EDA2.png)

### Category Distribution
![Category Distribution](Images/EDA3.png)

### Payment Method Distribution
![Payment Method Distribution](Images/EDA4.png)

---

## Analysis
The following visualizations provide insights based on data analysis:

### Highest Monthly Sale and Total Revenue
![Highest Monthly Sale and Total Revenue](Images/Analysis1.png)

### Age Distribution of Customers
![Age Distribution Analysis](Images/Analysis2.png)

### Gender-wise Sales Distribution
![Gender Sales Analysis](Images/Analysis3.png)

### Customer Count by Location
![Customer Count by Location](Images/Analysis4.png)

### Top Products by Quantity and Revenue
![Top Products Analysis](Images/Analysis5.png)

---

## Usage

### Running the DAG
1. Open Airflow UI.
2. Trigger the `bda_pipeline` DAG.

### Viewing Results
1. Access the Streamlit dashboards at `http://localhost:8501` and `http://localhost:8502`.
2. Explore key metrics such as:
   - Top customers by revenue.
   - Top-selling products.
   - Sales trends by age, gender, location, and month.

---

## Results
The project provides insights into:
- **Top Customers**: Highest revenue generators.
- **Top Products**: Best-selling products.
- **Demographic Insights**: Sales distribution by age, gender, and location.
- **Revenue Analysis**: Total revenue over time.

![Dashboard Screenshot](Images/Dashboard.png)

---

## Setup Instructions
For detailed step-by-step setup instructions, please refer to the [Setup Guide](Code_Files/README.md).

---

## Demo Video
Watch the complete demo of the project in this [video demo](https://www.youtube.com/watch?v=wp9aBacO-QM).

---

## Assumptions and Limitations

### Assumptions
1. Data volume is capped at 5 GB/day for processing.
2. Transaction data is streamed in real-time, while stock updates are batched.

### Limitations
1. Pipeline scalability not tested for datasets exceeding 10GB.
2. Results visualization is dependent on Streamlit.

