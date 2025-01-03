import happybase
import pandas as pd
import streamlit as st
import plotly.express as px

# Product ID to Product Name mapping
PRODUCT_MAPPING = {
    1: "Ultraboost 22",
    2: "R.Y.V. Crossbody Bag",
    3: "Adilette Slides",
    4: "Trefoil Hoodie",
    5: "4D Fusio",
    6: "Forum Low Shoes",
    7: "AEROREADY Backpack",
    8: "Primeblue Shorts",
    9: "ZX 2K Boost Shoes",
    10: "Alphaskin Tights",
}

# Function to create and test HBase connection
@st.cache_resource
def get_hbase_connection():
    try:
        connection = happybase.Connection(host='hbasebda', port=9090, transport="buffered", protocol="binary")  # Update host/port if necessary
        connection.tables()  # Test connection by listing tables
        return connection
    except Exception as e:
        st.error(f"Failed to connect to HBase: {e}")
        return None

# Function to fetch data from HBase
@st.cache_data
def fetch_data(table_name, column_family):
    try:
        connection = get_hbase_connection()
        if connection is None:
            raise Exception("No active HBase connection.")

        table = connection.table(table_name)
        rows = table.scan()
        data = []

        for key, value in rows:
            record = {}
            for col, val in value.items():
                if col.startswith(f"{column_family}:".encode("utf-8")):  # Convert string to bytes
                    col_name = col.split(b":")[1].decode("utf-8")  # Extract the column name
                    record[col_name] = val.decode("utf-8") if isinstance(val, bytes) else val

            data.append(record)  # Exclude row_key column

        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error fetching data from {table_name}: {e}")
        return pd.DataFrame()

# Streamlit App
def main():
    st.set_page_config(page_title="HBase EDA", layout="wide", initial_sidebar_state="expanded")
    st.title("HBase EDA with Streamlit")

    # Sidebar selection
    st.sidebar.title("Options")
    selected_table = st.sidebar.selectbox("Select a table for EDA", ["CustomerTable", "ProductTable", "OrderTable"])

    # Fetch data based on selected table
    if selected_table == "CustomerTable":
        data = fetch_data("CustomerTable", "info")
        if data.empty:
            st.warning(f"No data available for {selected_table}.")
        else:
            st.write("### Customer Table Data (First 100 Rows)")
            data = data.head(100)  # Limit to the first 100 rows
            st.dataframe(data)

            # EDA for CustomerTable
            st.write("#### Age Distribution (Grouped in 10s)")

            # Ensure 'age' is numeric and handle invalid data
            data['age'] = pd.to_numeric(data['age'], errors='coerce')  # Convert age to numeric, replacing invalid data with NaN
            data = data.dropna(subset=['age'])  # Drop rows where age is NaN

            # Create age groups in intervals of 10
            data['age_group'] = pd.cut(
                data['age'].astype(int),  # Ensure 'age' is treated as an integer
                bins=range(0, int(data['age'].max()) + 10, 10),  # Bins for 10-year intervals
                right=False,  # Exclude the right edge of the interval
                labels=[f"{i}-{i+9}" for i in range(0, int(data['age'].max()), 10)]  # Create labels for the intervals
            )

            # Count and sort age groups
            age_group_counts = data['age_group'].value_counts().reset_index()
            age_group_counts.columns = ['age_group', 'count']  # Rename columns for clarity
            age_group_counts = age_group_counts.sort_values('age_group')  # Sort by age_group

            # Plot the age group distribution
            fig_age_group = px.bar(
                age_group_counts,
                x="age_group",  # The age group labels
                y="count",  # The counts for each group
                # title="Age Group Distribution (Grouped in 10s)",
                labels={"age_group": "Age Group", "count": "Count"},  # Labels for the axes
                template="plotly_dark",
            )
            st.plotly_chart(fig_age_group)



            st.write("#### Gender Distribution")
            fig_gender = px.pie(data, names="gender", title="Gender Distribution", template="plotly_dark")
            st.plotly_chart(fig_gender)

            st.write("#### Location Distribution")
            location_counts = data["location"].value_counts().reset_index()
            location_counts.columns = ["location", "count"]  # Rename columns for clarity

            fig_location = px.bar(
                location_counts,
                x="location",
                y="count",
                title="Top 10 Locations",
                template="plotly_dark",
            )
            st.plotly_chart(fig_location)

    elif selected_table == "ProductTable":
        data_details = fetch_data("ProductTable", "details")
        data_inventory = fetch_data("ProductTable", "inventory")

        if data_details.empty and data_inventory.empty:
            st.warning(f"No data available for {selected_table}.")
        else:
            st.write("### Product Table Data")
            st.write("#### Details Column Family")
            st.dataframe(data_details)
            st.write("#### Inventory Column Family")
            st.dataframe(data_inventory)

            # Map product IDs to product names
            if "product_id" in data_inventory:
                data_inventory["product_name"] = data_inventory["product_id"].astype(int).map(PRODUCT_MAPPING)

            # EDA for ProductTable
            st.write("#### Price Distribution")
            fig_price = px.histogram(data_inventory, x="price", title="Price Distribution", template="plotly_dark")
            st.plotly_chart(fig_price)

            st.write("#### Stock Quantity Distribution")
            stock_counts = data_inventory["stock_quantity"].value_counts().reset_index()
            stock_counts.columns = ["stock_quantity", "count"]  # Rename columns for clarity

            fig_stock = px.bar(
                stock_counts,
                x="stock_quantity",
                y="count",
                title="Stock Quantity Distribution",
                template="plotly_dark",
            )
            st.plotly_chart(fig_stock)

            st.write("#### Category Distribution")
            fig_category = px.pie(
                data_details,
                names="category",
                title="Category Distribution",
                template="plotly_dark",
            )
            st.plotly_chart(fig_category)

    elif selected_table == "OrderTable":
        data = fetch_data("OrderTable", "info")
        if data.empty:
            st.warning(f"No data available for {selected_table}.")
        else:
            st.write("### Order Table Data (First 100 Rows)")
            data = data.head(100)  # Limit to the first 100 rows
            st.dataframe(data)

            # Map product IDs to product names
            if "product_id" in data:
                data["product_name"] = data["product_id"].astype(int).map(PRODUCT_MAPPING)

            # EDA for OrderTable
            st.write("#### Total Amount Distribution")
            fig_total = px.histogram(
                data, x="total_amount", title="Total Amount Distribution", template="plotly_dark"
            )
            st.plotly_chart(fig_total)

            st.write("#### Payment Method Distribution")
            fig_payment = px.pie(data, names="payment_method", title="Payment Method Distribution", template="plotly_dark")
            st.plotly_chart(fig_payment)

            st.write("#### Quantity Distribution")
            quantity_counts = data["quantity"].value_counts().reset_index()
            quantity_counts.columns = ["quantity", "count"]  # Rename columns for clarity

            fig_quantity = px.bar(
                quantity_counts,
                x="quantity",
                y="count",
                title="Quantity Distribution",
                template="plotly_dark",
            )
            st.plotly_chart(fig_quantity)

if __name__ == "__main__":
    main()
