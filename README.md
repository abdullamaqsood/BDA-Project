# Big Data Analytics Pipeline

## Description
This project implements an end-to-end big data analytics pipeline for e-commerce data analysis. The pipeline processes, analyzes, and visualizes customer, product, and order data using a combination of big data tools and technologies. Key objectives include identifying top customers and products, analyzing sales trends by demographic factors, and computing total revenue.

### Key Features
- **Real-Time Data Ingestion**: Uses Kafka to ingest streaming data.
- **Distributed Storage**: Hadoop and HBase for scalable storage solutions.
- **ETL Processing**: MapReduce-based data cleaning and transformation.
- **Data Analysis**: Spark for exploratory and statistical data analysis.
- **Interactive Dashboards**: Built using Streamlit to present results visually.

---

## Architecture
The architecture of the pipeline follows this flow:

1. Kafka for data ingestion.
2. Hadoop and HBase for distributed storage and processing.
3. Airflow for orchestrating the workflow.
4. Spark for performing EDA and ML.
5. Streamlit dashboard for data visualization.

![Pipeline Architecture](docs/architecture_diagram.png)

---

## Data Schema

### Customer Table
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
| Field          | Data Type |
|----------------|-----------|
| product_id     | int       |
| product_name   | string    |
| category       | string    |
| price          | int       |
| stock_quantity | int       |

### Order Table
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

## Installation
Follow these steps to set up the project:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/BigDataAnalyticsPipeline.git
   cd BigDataAnalyticsPipeline
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Services**
   - Start Kafka server.
   - Start Hadoop and HBase services.

4. **Run Airflow**
   ```bash
   airflow scheduler
   airflow webserver
   ```

5. **Run the Dashboard**
   ```bash
   streamlit run dashboards/dashboard_script.py
   ```

---

## Usage

### Running the DAG
1. Open Airflow UI.
2. Trigger the `bda_pipeline` DAG.

### Viewing Results
1. Access the Streamlit dashboard at `http://localhost:8501`.
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

![Dashboard Screenshot](dashboards/dashboard_screenshot.png)

---

## Assumptions and Limitations

### Assumptions
1. Data volume is capped at 5 GB/day for processing.
2. Transaction data is streamed in real-time, while stock updates are batched.

### Limitations
1. Pipeline scalability not tested for datasets exceeding 100 million records.
2. Limited fault tolerance in Kafka brokers.
3. Results visualization is dependent on Streamlit.

---

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Submit a pull request.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

