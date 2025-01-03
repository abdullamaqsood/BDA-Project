import streamlit as st
import pandas as pd
import os

def read_local_file(file_path):
    return pd.read_csv(file_path)

def main():
    st.title("Local Data Visualization")

    # Base directory for data
    base_dir = "./csvfiles"
    directories = [
        "age_distribution",
        "gender_sales",
        "high_value_customers",
        "location_sales",
        "monthly_order_trends",
        "monthly_sales",
        "payment_method_distribution",
        "top_products",
        "total_revenue",
    ]

    # Product mapping dictionary
    product_mapping = {
        1: "Ultraboost 22",
        2: "Adilette Slides",
        3: "Trefoil Hoodie",
        4: "4D Fusio",
        5: "Forum Low Shoes",
        6: "AEROREADY Backpack",
        7: "Primeblue Shorts",
        8: "ZX 2K Boost Shoes",
        9: "Alphaskin Tights",
        10: "R.Y.V. Crossbody Bag"
    }

    # Show Monthly Sales and Total Revenue at the top
    try:
        # Monthly Sales
        monthly_sales_path = os.path.join(base_dir, "monthly_sales")
        monthly_sales_file = next((f for f in os.listdir(monthly_sales_path) if f.endswith('.csv')), None)
        if not monthly_sales_file:
            raise FileNotFoundError(f"No CSV file found in {monthly_sales_path}")
        monthly_sales_df = read_local_file(os.path.join(monthly_sales_path, monthly_sales_file))
        
        # Total Revenue
        total_revenue_path = os.path.join(base_dir, "total_revenue")
        total_revenue_file = next((f for f in os.listdir(total_revenue_path) if f.endswith('.csv')), None)
        if not total_revenue_file:
            raise FileNotFoundError(f"No CSV file found in {total_revenue_path}")
        total_revenue_df = read_local_file(os.path.join(total_revenue_path, total_revenue_file))
        
        # Display side by side
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Monthly Sales", value=monthly_sales_df.iloc[0]["Monthly Revenue"])
        with col2:
            st.metric(label="Total Revenue", value=total_revenue_df.iloc[0][0])
    except Exception as e:
        st.error(f"Failed to load Monthly Sales or Total Revenue: {e}")

    for directory in directories:
        if directory in ["monthly_sales", "total_revenue"]:
            continue

        dir_path = os.path.join(base_dir, directory)

        try:
            # Find the first CSV file in the directory
            file_name = next((f for f in os.listdir(dir_path) if f.endswith('.csv')), None)
            if not file_name:
                raise FileNotFoundError(f"No CSV file found in {dir_path}")

            file_path = os.path.join(dir_path, file_name)
            df = read_local_file(file_path)
            
            # Visualize the data
            if directory == "age_distribution":
                st.subheader("Age Distribution")
                st.bar_chart(data=df.set_index("age_group"), use_container_width=True)

            elif directory == "gender_sales":
                st.subheader("Gender Sales")
                st.bar_chart(data=df.set_index("gender"), use_container_width=True)

            elif directory == "high_value_customers":
                st.subheader("High Value Customers")
                st.write(df)

            elif directory == "location_sales":
                st.subheader("Customer Count by Location")
                st.line_chart(data=df.set_index("location"))

            elif directory == "monthly_order_trends":
                st.subheader("Monthly Order Trends")
                st.line_chart(data=df.set_index("Month"))

            elif directory == "payment_method_distribution":
                st.subheader("Payment Method Distribution")
                st.bar_chart(data=df.set_index("payment_method"))

            elif directory == "top_products":
                st.subheader("Top Products")
                # Replace product IDs with product names
                df["product_id"] = df["product_id"].map(product_mapping)
                st.bar_chart(data=df.set_index("product_id"), use_container_width=True)

        except Exception as e:
            st.error(f"Failed to read data from {directory}: {e}")

if __name__ == "__main__":
    main()
