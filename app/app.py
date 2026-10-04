import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIGURATION
# ============================================================

# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* Main application background */
    .stApp {
        background-color: #ffffff;
    }

    /* Main content width and spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Main headings */
    h1 {
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h2 {
        font-weight: 650;
    }

    h3 {
        font-weight: 600;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f4f6f9;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 1.4rem;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e5e7eb;
        padding: 16px;
        border-radius: 10px;
    }

    /* Metric labels */
    div[data-testid="stMetricLabel"] {
        font-weight: 600;
    }

    /* Dataframes */
    div[data-testid="stDataFrame"] {
        border-radius: 8px;
    }

    /* Information boxes */
    div[data-testid="stAlert"] {
        border-radius: 8px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD PRICING DATA
# ============================================================

retail = pd.read_csv(
    "data/processed/retail_price_features.csv"
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("📊 E-Commerce Analytics")

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Select a module",
    [
        "🏠 Dashboard",
        "📤 Upload Data",
        "📦 Demand Analysis",
        "🔮 Demand Prediction",
        "💰 Pricing Analysis",
        "📉 Price Elasticity",
        "🏪 Competitor Analysis",
        "💡 Business Insights"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.info(
    "E-Commerce Pricing & Demand Analytics\n\n"
    "Data-driven analysis for demand, pricing, "
    "elasticity, competition and business decisions."
)


# ============================================================
# 🏠 DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title("📊 E-Commerce Pricing & Demand Analytics")

    st.write(
        "A data-driven dashboard for demand prediction, "
        "pricing analysis, price elasticity and competitor insights."
    )

    st.divider()

    # --------------------------------------------------------
    # REAL KPIs
    # --------------------------------------------------------

    products = retail["product_id"].nunique()

    categories = retail[
        "product_category_name"
    ].nunique()

    avg_price = retail[
        "unit_price"
    ].mean()

    avg_demand = retail[
        "qty"
    ].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Products",
        products
    )

    col2.metric(
        "Categories",
        categories
    )

    col3.metric(
        "Average Price",
        f"₹{avg_price:,.2f}"
    )

    col4.metric(
        "Average Demand",
        f"{avg_demand:,.2f}"
    )

    st.divider()

    # --------------------------------------------------------
    # PROJECT OVERVIEW
    # --------------------------------------------------------

    st.subheader("📋 Project Overview")

    st.write("""
    This application analyzes e-commerce data to understand:

    - Product demand
    - Future demand prediction
    - Pricing patterns
    - Price elasticity
    - Competitor pricing
    - Inventory planning
    - Business insights
    """)

    st.divider()

    # --------------------------------------------------------
    # CATEGORY DEMAND
    # --------------------------------------------------------

    st.subheader("📦 Demand by Product Category")

    category_demand = (
        retail
        .groupby("product_category_name")["qty"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        category_demand
    )

    st.caption(
        "Total quantity recorded across each product category."
    )

# ============================================================
# 📤 UPLOAD DATA
# ============================================================

elif page == "📤 Upload Data":

    st.title("📤 Upload Your Sales Data")

    st.write(
        "Upload a CSV file to explore sales and demand data "
        "interactively."
    )

    st.divider()

    st.subheader("📁 Upload CSV")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file is None:

        st.info(
            "Upload a CSV file to begin the analysis."
        )

        st.markdown(
            """
            ### 📋 Supported Data Format

            The application can automatically detect common column names.

            **Required information:**

            - **Date** — transaction or sales date
            - **Product** — product identifier/name
            - **Quantity** — units sold
            - **Price** — selling price

            ### Examples of accepted column names

            | Required Field | Accepted Examples |
            |---|---|
            | Date | Date, date, order_date, InvoiceDate |
            | Product | Product, product, product_name, SKU |
            | Quantity | Quantity, quantity, qty, units, units_sold |
            | Price | Price, price, unit_price, selling_price |

            Example:

            | date | product | quantity | unit_price |
            |---|---|---:|---:|
            | 2026-01-01 | Product A | 20 | 100 |
            | 2026-01-02 | Product A | 25 | 105 |
            | 2026-01-03 | Product B | 15 | 200 |
            """
        )

    else:

        try:

            uploaded_data = pd.read_csv(
                uploaded_file
            )

            st.success(
                "✅ File uploaded successfully!"
            )

            # ====================================================
            # BASIC FILE INFORMATION
            # ====================================================

            st.subheader("📊 Dataset Overview")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Rows",
                f"{uploaded_data.shape[0]:,}"
            )

            col2.metric(
                "Columns",
                f"{uploaded_data.shape[1]:,}"
            )

            col3.metric(
                "Missing Values",
                f"{uploaded_data.isna().sum().sum():,}"
            )

            st.divider()

            # ====================================================
            # DATA PREVIEW
            # ====================================================

            st.subheader("👀 Data Preview")

            st.dataframe(
                uploaded_data.head(20),
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # ====================================================
            # COLUMN INFORMATION
            # ====================================================

            st.subheader("📋 Available Columns")

            column_information = pd.DataFrame(
                {
                    "Column": uploaded_data.columns,
                    "Data Type": [
                        str(dtype)
                        for dtype in uploaded_data.dtypes
                    ],
                    "Missing Values": [
                        uploaded_data[column].isna().sum()
                        for column in uploaded_data.columns
                    ]
                }
            )

            st.dataframe(
                column_information,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # ====================================================
            # AUTOMATIC COLUMN DETECTION
            # ====================================================

            st.subheader("🔍 Automatic Column Detection")

            column_aliases = {

                "Date": [
                    "Date",
                    "date",
                    "Order_Date",
                    "order_date",
                    "Order Date",
                    "InvoiceDate",
                    "invoice_date",
                    "Transaction_Date",
                    "transaction_date"
                ],

                "Product": [
                    "Product",
                    "product",
                    "Product_ID",
                    "product_id",
                    "Product_Name",
                    "product_name",
                    "Product Name",
                    "SKU",
                    "sku"
                ],

                "Quantity": [
                    "Quantity",
                    "quantity",
                    "Qty",
                    "qty",
                    "Units",
                    "units",
                    "Units_Sold",
                    "units_sold",
                    "Units Sold",
                    "Quantity_Sold",
                    "quantity_sold"
                ],

                "Price": [
                    "Price",
                    "price",
                    "Unit_Price",
                    "unit_price",
                    "Unit Price",
                    "Selling_Price",
                    "selling_price",
                    "Selling Price",
                    "Sales_Price",
                    "sales_price"
                ]
            }

            column_mapping = {}

            for standard_name, aliases in column_aliases.items():

                for column in aliases:

                    if column in uploaded_data.columns:

                        column_mapping[standard_name] = column

                        break

            # ====================================================
            # SHOW DETECTED COLUMNS
            # ====================================================

            detected_columns = pd.DataFrame(
                {
                    "Required Field": [
                        "Date",
                        "Product",
                        "Quantity",
                        "Price"
                    ],

                    "Detected Column": [

                        column_mapping.get(
                            "Date",
                            "❌ Not detected"
                        ),

                        column_mapping.get(
                            "Product",
                            "❌ Not detected"
                        ),

                        column_mapping.get(
                            "Quantity",
                            "❌ Not detected"
                        ),

                        column_mapping.get(
                            "Price",
                            "❌ Not detected"
                        )
                    ]
                }
            )

            st.dataframe(
                detected_columns,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # ====================================================
            # CHECK REQUIRED FIELDS
            # ====================================================

            missing_fields = [
                field
                for field in [
                    "Date",
                    "Product",
                    "Quantity",
                    "Price"
                ]
                if field not in column_mapping
            ]

            if missing_fields:

                st.warning(
                    "⚠️ The application could not detect "
                    "all required sales columns."
                )

                st.write(
                    "Missing fields:",
                    missing_fields
                )

                st.info(
                    "The uploaded dataset must contain "
                    "information representing Date, Product, "
                    "Quantity and Price."
                )

            else:

                st.success(
                    "✅ All required sales columns were detected."
                )

                # ====================================================
                # STANDARDIZE COLUMN NAMES
                # ====================================================

                sales_data = uploaded_data.rename(
                    columns={
                        column_mapping["Date"]: "Date",
                        column_mapping["Product"]: "Product",
                        column_mapping["Quantity"]: "Quantity",
                        column_mapping["Price"]: "Price"
                    }
                ).copy()

                # ====================================================
                # DATA TYPE CONVERSION
                # ====================================================

                sales_data["Date"] = pd.to_datetime(
                    sales_data["Date"],
                    errors="coerce"
                )

                sales_data["Quantity"] = pd.to_numeric(
                    sales_data["Quantity"],
                    errors="coerce"
                )

                sales_data["Price"] = pd.to_numeric(
                    sales_data["Price"],
                    errors="coerce"
                )

                # ====================================================
                # REMOVE INVALID RECORDS
                # ====================================================

                valid_data = sales_data.dropna(
                    subset=[
                        "Date",
                        "Product",
                        "Quantity",
                        "Price"
                    ]
                ).copy()
                # ====================================================
                # DATA QUALITY REPORT
                # ====================================================

                st.subheader(
                    "🧹 Data Quality Report"
                )

                original_records = len(sales_data)

                valid_records = len(valid_data)

                invalid_records = (
                    original_records - valid_records
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Original Records",
                    f"{original_records:,}"
                )

                col2.metric(
                    "Valid Records",
                    f"{valid_records:,}"
                )

                col3.metric(
                    "Invalid Records",
                    f"{invalid_records:,}"
                )

                col4.metric(
                    "Missing Values",
                    f"{sales_data[['Date', 'Product', 'Quantity', 'Price']].isna().sum().sum():,}"
                )

                if invalid_records > 0:

                    st.warning(
                        f"⚠️ {invalid_records:,} records were excluded "
                        "because required sales information was missing "
                        "or invalid."
                    )

                else:

                    st.success(
                        "✅ All records contain valid Date, Product, "
                        "Quantity and Price information."
                    )

                if len(valid_data) > 0:

                    st.caption(
                        f"📅 Data range: "
                        f"{valid_data['Date'].min().strftime('%d %b %Y')} "
                        f"to "
                        f"{valid_data['Date'].max().strftime('%d %b %Y')}"
                    )

                st.divider()

                # ====================================================
                # REVENUE
                # ====================================================

                valid_data["Revenue"] = (
                    valid_data["Quantity"]
                    * valid_data["Price"]
                )

                st.divider()

                # ====================================================
                # SALES OVERVIEW
                # ====================================================

                st.subheader(
                    "📈 Sales Overview"
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Total Units",
                    f"{valid_data['Quantity'].sum():,.0f}"
                )

                col2.metric(
                    "Total Revenue",
                    f"₹{valid_data['Revenue'].sum():,.2f}"
                )

                col3.metric(
                    "Average Price",
                    f"₹{valid_data['Price'].mean():,.2f}"
                )

                col4.metric(
                    "Products",
                    f"{valid_data['Product'].nunique():,}"
                )

                st.divider()

                # ====================================================
                # MONTHLY SALES TREND
                # ====================================================

                st.subheader(
                    "📅 Monthly Sales Trend"
                )

                monthly_sales = (
                    valid_data
                    .set_index("Date")
                    .resample("ME")
                    .agg(
                        Quantity=("Quantity", "sum"),
                        Revenue=("Revenue", "sum")
                    )
                )

                st.line_chart(
                    monthly_sales
                )

                st.divider()

                # ====================================================
                # TOP PRODUCTS
                # ====================================================

                st.subheader(
                    "🏆 Top Products by Quantity"
                )

                top_products = (
                    valid_data
                    .groupby("Product")["Quantity"]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                    .head(10)
                )

                st.bar_chart(
                    top_products
                )

                # ====================================================
                # TOP PRODUCTS BY REVENUE
                # ====================================================

                st.subheader(
                    "💰 Top Products by Revenue"
                )

                top_revenue_products = (
                    valid_data
                    .groupby("Product")["Revenue"]
                    .sum()
                    .sort_values(
                        ascending=False
                    )
                    .head(10)
                )

                st.bar_chart(
                    top_revenue_products
                )

                st.divider()

                # ====================================================
                # SALES SUMMARY BY PRODUCT
                # ====================================================

                st.subheader(
                    "📋 Sales Summary by Product"
                )

                sales_summary = (
                    valid_data
                    .groupby("Product")
                    .agg(
                        Total_Units_Sold=("Quantity", "sum"),
                        Total_Revenue=("Revenue", "sum"),
                        Average_Price=("Price", "mean"),
                        Number_of_Transactions=("Product", "count")
                    )
                    .sort_values(
                        "Total_Revenue",
                        ascending=False
                    )
                    .reset_index()
                )

                sales_summary = sales_summary.round(2)

                st.dataframe(
                    sales_summary,
                    use_container_width=True,
                    hide_index=True
                )

                st.caption(
                    "Product-level summary showing total units sold, total revenue, "
                    "average selling price and number of transactions."
                )

                st.divider()

                # ====================================================
                # PRODUCT EXPLORER
                # ====================================================

                st.subheader(
                    "🔎 Product Explorer"
                )

                products = sorted(
                    valid_data["Product"]
                    .astype(str)
                    .unique()
                )

                selected_product = st.selectbox(
                    "Select a product",
                    products
                )

                selected_product_data = valid_data[
                    valid_data["Product"].astype(str)
                    == selected_product
                ].copy()

                if len(selected_product_data) > 0:

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Units Sold",
                        f"{selected_product_data['Quantity'].sum():,.0f}"
                    )

                    col2.metric(
                        "Revenue",
                        f"₹{selected_product_data['Revenue'].sum():,.2f}"
                    )

                    col3.metric(
                        "Average Price",
                        f"₹{selected_product_data['Price'].mean():,.2f}"
                    )

                    product_trend = (
                        selected_product_data
                        .set_index("Date")["Quantity"]
                        .resample("ME")
                        .sum()
                    )

                    st.line_chart(
                        product_trend
                    )

                st.divider()

                # ====================================================
                # DEMAND PREDICTION
                # ====================================================

                st.subheader(
                    "🔮 Next Month Demand Prediction"
                )

                st.write(
                    "Estimate next month's demand using the "
                    "product's historical monthly sales."
                )

                prediction_products = sorted(
                    valid_data["Product"]
                    .astype(str)
                    .unique()
                )

                prediction_product = st.selectbox(
                    "Select a product for prediction",
                    prediction_products,
                    key="upload_prediction_product"
                )

                prediction_data = valid_data[
                    valid_data["Product"].astype(str)
                    == prediction_product
                ].copy()

                monthly_demand = (
                    prediction_data
                    .set_index("Date")["Quantity"]
                    .resample("ME")
                    .sum()
                )

                if len(monthly_demand) >= 2:

                    # ------------------------------------------------
                    # SIMPLE FORECAST
                    # ------------------------------------------------

                    recent_months = monthly_demand.tail(3)

                    predicted_demand = recent_months.mean()

                    # ------------------------------------------------
                    # PREDICTION DISPLAY
                    # ------------------------------------------------

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Historical Months",
                        f"{len(monthly_demand):,}"
                    )

                    col2.metric(
                        "Recent Avg Demand",
                        f"{recent_months.mean():,.0f}"
                    )

                    col3.metric(
                        "Predicted Next Month",
                        f"{predicted_demand:,.0f}"
                    )

                    st.divider()

                    # ------------------------------------------------
                    # HISTORICAL + PREDICTED DEMAND
                    # ------------------------------------------------

                    st.subheader(
                        "📊 Historical vs Predicted Demand"
                    )

                    prediction_chart = monthly_demand.copy()

                    next_month = (
                        prediction_chart.index.max()
                        + pd.offsets.MonthEnd(1)
                    )

                    prediction_chart.loc[
                        next_month
                    ] = predicted_demand

                    st.line_chart(
                        prediction_chart
                    )

                    # ------------------------------------------------
                    # BUSINESS INTERPRETATION
                    # ------------------------------------------------

                    st.subheader(
                        "💡 Prediction Interpretation"
                    )

                    st.info(
                        f"For **{prediction_product}**, the estimated "
                        f"demand for the next month is approximately "
                        f"**{predicted_demand:,.0f} units** based on "
                        f"the average demand of the most recent "
                        f"three months."
                    )

                    # ------------------------------------------------
                    # SUGGESTED STOCK
                    # ------------------------------------------------

                    st.divider()

                    st.subheader(
                        "📦 Inventory Recommendation"
                    )

                    safety_buffer = 0.10

                    safety_stock = (
                        predicted_demand
                        * safety_buffer
                    )

                    suggested_stock = (
                        predicted_demand
                        + safety_stock
                    )

                    suggested_stock = int(
                        round(suggested_stock)
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Predicted Demand",
                        f"{predicted_demand:,.0f} units"
                    )

                    col2.metric(
                        "Safety Buffer",
                        f"{safety_stock:,.0f} units"
                    )

                    col3.metric(
                        "Suggested Stock",
                        f"{suggested_stock:,} units"
                    )

                    st.success(
                        f"📦 Recommended stock for "
                        f"**{prediction_product}**: "
                        f"**{suggested_stock:,} units"
                    )

                    st.caption(
                        "The suggested stock includes a 10% safety "
                        "buffer above the baseline demand prediction. "
                        "This is a simple inventory-planning baseline, "
                        "not a guaranteed demand level."
                    )

                    st.caption(
                        "Note: This is a baseline forecasting method "
                        "for uploaded datasets. It is not the trained "
                        "machine-learning model used in the prepared "
                        "demand prediction pipeline."
                    )

                    # ------------------------------------------------
                    # DOWNLOAD ANALYSIS RESULTS
                    # ------------------------------------------------

                    st.divider()

                    st.subheader(
                        "📥 Download Analysis Results"
                    )

                    download_data = prediction_data.copy()

                    download_data[
                        "Predicted_Next_Month_Demand"
                    ] = predicted_demand

                    download_data[
                        "Safety_Buffer"
                    ] = safety_stock

                    download_data[
                        "Suggested_Stock"
                    ] = suggested_stock

                    download_csv = download_data.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        label="📥 Download Analysis CSV",
                        data=download_csv,
                        file_name=(
                            f"{prediction_product}_analysis.csv"
                        ),
                        mime="text/csv",
                        key="download_analysis_csv"
                    )

                    st.caption(
                        "Download the selected product's historical "
                        "sales data together with the demand prediction "
                        "and inventory recommendation."
                    )

                else:

                    st.warning(
                        "⚠️ Not enough historical monthly data "
                        "to generate a demand prediction."
                    )

                    st.info(
                        "At least 2 months of historical sales "
                        "data are required."
                    )
        except Exception as e:

            st.error(
                f"Unable to process the uploaded CSV: {e}"
            )
# ============================================================
# 📦 DEMAND ANALYSIS
# ============================================================

elif page == "📦 Demand Analysis":

    st.title("📦 Demand Analysis")

    st.write(
        "Analyze historical e-commerce demand using "
        "transaction-level and monthly demand data."
    )

    st.divider()

    # --------------------------------------------------------
    # LOAD DEMAND DATA
    # --------------------------------------------------------

    demand = pd.read_csv(
        "data/processed/monthly_demand_complete.csv"
    )

    st.subheader("📋 Demand Dataset")

    st.write(
        f"Records available for analysis: **{len(demand):,}**"
    )

    # --------------------------------------------------------
    # IDENTIFY IMPORTANT COLUMNS
    # --------------------------------------------------------

    date_candidates = [
        "MonthYear",
        "month_year",
        "InvoiceDate",
        "Date",
        "date"
    ]

    quantity_candidates = [
        "Quantity",
        "quantity",
        "Qty",
        "qty",
        "Monthly_Quantity",
        "monthly_quantity"
    ]

    product_candidates = [
        "StockCode",
        "stock_code",
        "Product",
        "product_id"
    ]

    date_col = next(
        (
            col
            for col in date_candidates
            if col in demand.columns
        ),
        None
    )

    quantity_col = next(
        (
            col
            for col in quantity_candidates
            if col in demand.columns
        ),
        None
    )

    product_col = next(
        (
            col
            for col in product_candidates
            if col in demand.columns
        ),
        None
    )

    # --------------------------------------------------------
    # CHECK REQUIRED COLUMNS
    # --------------------------------------------------------

    if date_col is None or quantity_col is None:

        st.error(
            "Required demand columns could not be identified."
        )

        st.write("Available columns:")

        st.write(
            demand.columns.tolist()
        )

    else:

        # ----------------------------------------------------
        # DATA TYPE CONVERSION
        # ----------------------------------------------------

        demand[date_col] = pd.to_datetime(
            demand[date_col],
            errors="coerce"
        )

        demand[quantity_col] = pd.to_numeric(
            demand[quantity_col],
            errors="coerce"
        )

        demand = demand.dropna(
            subset=[
                date_col,
                quantity_col
            ]
        )

        # ----------------------------------------------------
        # DEMAND KPIs
        # ----------------------------------------------------

        total_demand = demand[
            quantity_col
        ].sum()

        avg_demand_value = demand[
            quantity_col
        ].mean()

        max_demand = demand[
            quantity_col
        ].max()

        if product_col is not None:

            unique_products = demand[
                product_col
            ].nunique()

        else:

            unique_products = 0

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Demand",
            f"{total_demand:,.0f}"
        )

        col2.metric(
            "Average Demand",
            f"{avg_demand_value:,.2f}"
        )

        col3.metric(
            "Maximum Demand",
            f"{max_demand:,.0f}"
        )

        col4.metric(
            "Products",
            unique_products
        )

        st.divider()

        # ----------------------------------------------------
        # MONTHLY DEMAND TREND
        # ----------------------------------------------------

        st.subheader(
            "📈 Monthly Demand Trend"
        )

        monthly_demand = (
            demand
            .groupby(date_col)[quantity_col]
            .sum()
            .sort_index()
        )

        st.line_chart(
            monthly_demand
        )

        st.caption(
            "Total quantity demanded over time."
        )

        st.divider()

        # ----------------------------------------------------
        # TOP PRODUCTS
        # ----------------------------------------------------

        if product_col is not None:

            st.subheader(
                "🏆 Top Products by Demand"
            )

            top_products = (
                demand
                .groupby(product_col)[quantity_col]
                .sum()
                .sort_values(
                    ascending=False
                )
                .head(10)
            )

            st.bar_chart(
                top_products
            )

            st.caption(
                "Top 10 products based on total historical demand."
            )

            st.divider()

            # ------------------------------------------------
            # PRODUCT DEMAND EXPLORER
            # ------------------------------------------------

            st.subheader(
                "🔎 Product Demand Explorer"
            )

            product_list = sorted(
                demand[product_col]
                .astype(str)
                .unique()
            )

            selected_product = st.selectbox(
                "Select a product",
                product_list
            )

            product_data = demand[
                demand[product_col].astype(str)
                == selected_product
            ]

            product_monthly = (
                product_data
                .groupby(date_col)[quantity_col]
                .sum()
                .sort_index()
            )

            st.line_chart(
                product_monthly
            )

            st.metric(
                "Total Historical Demand",
                f"{product_data[quantity_col].sum():,.0f}"
            )


# ============================================================
# 🔮 DEMAND PREDICTION
# ============================================================

# ============================================================
# 🔮 DEMAND PREDICTION
# ============================================================

elif page == "🔮 Demand Prediction":

    st.title("🔮 Demand Prediction")

    st.write(
        "Use the trained demand prediction results to "
        "estimate future product demand and support inventory planning."
    )

    st.divider()

    # --------------------------------------------------------
    # LOAD PREDICTION RESULTS
    # --------------------------------------------------------

    prediction = pd.read_csv(
        "data/predictions/final_decision_table.csv"
    )

    # Convert columns to appropriate data types
    prediction["StockCode"] = (
        prediction["StockCode"]
        .astype(str)
    )

    prediction["MonthYear"] = pd.to_datetime(
        prediction["MonthYear"],
        errors="coerce"
    )

    prediction["Next_Month_Quantity"] = pd.to_numeric(
        prediction["Next_Month_Quantity"],
        errors="coerce"
    )

    prediction["Predicted_Quantity"] = pd.to_numeric(
        prediction["Predicted_Quantity"],
        errors="coerce"
    )

    prediction["Suggested_Stock"] = pd.to_numeric(
        prediction["Suggested_Stock"],
        errors="coerce"
    )

    prediction = prediction.dropna(
        subset=[
            "StockCode",
            "MonthYear",
            "Predicted_Quantity"
        ]
    )

    # --------------------------------------------------------
    # PAGE KPIs
    # --------------------------------------------------------

    total_predictions = len(prediction)

    average_prediction = prediction[
        "Predicted_Quantity"
    ].mean()

    high_risk_predictions = (
        prediction["Prediction_Risk"]
        .eq("High")
        .sum()
    )

    total_suggested_stock = prediction[
        "Suggested_Stock"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Prediction Records",
        f"{total_predictions:,}"
    )

    col2.metric(
        "Average Predicted Demand",
        f"{average_prediction:,.2f}"
    )

    col3.metric(
        "High Risk Predictions",
        f"{high_risk_predictions:,}"
    )

    col4.metric(
        "Suggested Stock",
        f"{total_suggested_stock:,.0f}"
    )

    st.divider()

    # --------------------------------------------------------
    # PRODUCT SELECTOR
    # --------------------------------------------------------

    st.subheader("🔎 Product Demand Prediction")

    product_list = sorted(
        prediction["StockCode"]
        .unique()
    )

    selected_product = st.selectbox(
        "Select a product",
        product_list
    )

    product_prediction = prediction[
        prediction["StockCode"]
        == selected_product
    ].sort_values("MonthYear")

    if len(product_prediction) > 0:

        # ----------------------------------------------------
        # LATEST PREDICTION
        # ----------------------------------------------------

        latest = product_prediction.iloc[-1]

        st.subheader("📌 Latest Prediction")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Actual Demand",
            f"{latest['Next_Month_Quantity']:,.0f}"
        )

        col2.metric(
            "Predicted Demand",
            f"{latest['Predicted_Quantity']:,.2f}"
        )

        col3.metric(
            "Prediction Risk",
            str(latest["Prediction_Risk"])
        )

        col4.metric(
            "Suggested Stock",
            f"{latest['Suggested_Stock']:,.0f}"
        )

        st.caption(
            f"Prediction period: "
            f"{latest['MonthYear'].strftime('%Y-%m')}"
        )

        st.divider()

        # ----------------------------------------------------
        # ACTUAL VS PREDICTED
        # ----------------------------------------------------

        st.subheader(
            "📈 Actual vs Predicted Demand"
        )

        comparison = product_prediction[
            [
                "MonthYear",
                "Next_Month_Quantity",
                "Predicted_Quantity"
            ]
        ].copy()

        comparison = comparison.set_index(
            "MonthYear"
        )

        comparison.columns = [
            "Actual Demand",
            "Predicted Demand"
        ]

        st.line_chart(
            comparison
        )

        st.caption(
            "Comparison of actual demand and model-predicted demand "
            "for the selected product."
        )

        st.divider()

        # ----------------------------------------------------
        # PREDICTION HISTORY
        # ----------------------------------------------------

        st.subheader(
            "📋 Prediction History"
        )

        display_columns = [
            "MonthYear",
            "Next_Month_Quantity",
            "Predicted_Quantity",
            "Absolute_Error",
            "Relative_Error_Pct",
            "Prediction_Risk",
            "Suggested_Stock"
        ]

        available_columns = [
            col
            for col in display_columns
            if col in product_prediction.columns
        ]

        prediction_table = product_prediction[
            available_columns
        ].copy()

        prediction_table["MonthYear"] = (
            prediction_table["MonthYear"]
            .dt.strftime("%Y-%m")
        )

        st.dataframe(
            prediction_table,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No prediction records found for this product."
        )

    st.divider()

    # --------------------------------------------------------
    # RISK DISTRIBUTION
    # --------------------------------------------------------

    st.subheader(
        "⚠️ Prediction Risk Distribution"
    )

    risk_distribution = (
        prediction["Prediction_Risk"]
        .value_counts()
    )

    st.bar_chart(
        risk_distribution
    )

    st.caption(
        "Distribution of prediction risk levels based on "
        "relative prediction error."
    )

    st.divider()

    # --------------------------------------------------------
    # BUSINESS INTERPRETATION
    # --------------------------------------------------------

    st.subheader(
        "💡 How to Use These Predictions"
    )

    st.write("""
    **Low Risk**

    The prediction can be used with greater confidence for
    normal inventory planning.

    **Moderate Risk**

    Monitor recent demand trends and adjust inventory when necessary.

    **High Risk**

    Review the prediction carefully before making inventory decisions.

    **Suggested Stock**

    Suggested stock includes the predicted demand together with
    the safety buffer calculated during the project.
    """)
# ============================================================
# 💰 PRICING ANALYSIS
# ============================================================

# ============================================================
# 💰 PRICING ANALYSIS
# ============================================================

elif page == "💰 Pricing Analysis":

    # ============================================================
    # PRICING ANALYSIS
    # ============================================================

    st.title("💰 Pricing Analysis")

    st.write(
        "Analyze product pricing, demand patterns and "
        "pricing trends across categories and time."
    )

    st.divider()

    # ============================================================
    # PRICING KPIs
    # ============================================================

    avg_price = retail["unit_price"].mean()
    median_price = retail["unit_price"].median()
    avg_quantity = retail["qty"].mean()
    total_products = retail["product_id"].nunique()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average Price",
        f"₹{avg_price:,.2f}"
    )

    col2.metric(
        "Median Price",
        f"₹{median_price:,.2f}"
    )

    col3.metric(
        "Average Quantity",
        f"{avg_quantity:,.2f}"
    )

    col4.metric(
        "Products",
        total_products
    )

    st.divider()

    # ============================================================
    # PRICE VS DEMAND
    # ============================================================

    st.subheader("📊 Price vs Demand")

    price_demand = retail[
        ["unit_price", "qty"]
    ].dropna().copy()

    st.scatter_chart(
        price_demand,
        x="unit_price",
        y="qty"
    )

    st.caption(
        "Relationship between product unit price and recorded quantity. "
        "This is an observational relationship and does not imply causation."
    )

    st.divider()

    # ============================================================
    # CATEGORY-WISE PRICING & DEMAND
    # ============================================================

    st.subheader("📦 Category-wise Pricing & Demand")

    category_summary = (
        retail
        .groupby("product_category_name")
        .agg(
            Average_Price=("unit_price", "mean"),
            Average_Quantity=("qty", "mean"),
            Total_Quantity=("qty", "sum"),
            Products=("product_id", "nunique")
        )
        .sort_values(
            "Total_Quantity",
            ascending=False
        )
        .round(2)
    )

    st.dataframe(
        category_summary,
        use_container_width=True,
        hide_index=False
    )

    st.divider()

    # ============================================================
    # AVERAGE PRICE BY CATEGORY
    # ============================================================

    st.subheader("💰 Average Price by Category")

    category_price = (
        retail
        .groupby("product_category_name")["unit_price"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_price)

    st.caption(
        "Average product price across each category."
    )

    st.divider()

    # ============================================================
    # TOTAL DEMAND BY CATEGORY
    # ============================================================

    st.subheader("📦 Total Demand by Category")

    category_quantity = (
        retail
        .groupby("product_category_name")["qty"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_quantity)

    st.caption(
        "Total quantity recorded for each product category."
    )

    st.divider()

    # ============================================================
    # MONTHLY PRICING & DEMAND DATA
    # ============================================================

    st.subheader("📈 Monthly Pricing Trend")

    pricing_monthly = (
        retail
        .groupby("month_year")
        .agg(
            Average_Price=("unit_price", "mean"),
            Total_Quantity=("qty", "sum")
        )
        .reset_index()
    )

    # Convert date
    pricing_monthly["month_year"] = pd.to_datetime(
        pricing_monthly["month_year"],
        errors="coerce",
        dayfirst=True
    )

    pricing_monthly = (
        pricing_monthly
        .dropna(subset=["month_year"])
        .sort_values("month_year")
    )

    # Average price trend
    price_trend = (
        pricing_monthly
        .set_index("month_year")["Average_Price"]
    )

    st.line_chart(price_trend)

    st.caption(
        "Average product price over time."
    )

    st.divider()

    # ============================================================
    # MONTHLY DEMAND TREND
    # ============================================================

    st.subheader("📦 Monthly Demand Trend")

    demand_trend = (
        pricing_monthly
        .set_index("month_year")["Total_Quantity"]
    )

    st.line_chart(demand_trend)

    st.caption(
        "Total quantity recorded across all products over time."
    )

    st.divider()

    # ============================================================
    # CATEGORY EXPLORER
    # ============================================================

    st.subheader("🔎 Category Explorer")

    categories = sorted(
        retail["product_category_name"]
        .dropna()
        .unique()
    )

    selected_category = st.selectbox(
        "Select a product category",
        categories
    )

    category_data = retail[
        retail["product_category_name"]
        == selected_category
    ].copy()

    # ============================================================
    # SELECTED CATEGORY KPIs
    # ============================================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Price",
        f"₹{category_data['unit_price'].mean():,.2f}"
    )

    col2.metric(
        "Average Demand",
        f"{category_data['qty'].mean():,.2f}"
    )

    col3.metric(
        "Total Demand",
        f"{category_data['qty'].sum():,.0f}"
    )

    st.divider()

    # ============================================================
    # SELECTED CATEGORY DETAILS
    # ============================================================

    st.subheader("📋 Category Details")

    detail_columns = [
        "product_id",
        "unit_price",
        "qty",
        "total_price",
        "comp_1",
        "comp_2",
        "comp_3"
    ]

    # Keep only columns that actually exist
    available_columns = [
        col for col in detail_columns
        if col in category_data.columns
    ]

    category_details = (
        category_data[available_columns]
        .sort_values(
            "qty",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        category_details,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Top 20 records in the selected category, sorted by quantity."
    )

    st.divider()

    # ============================================================
    # PRICING INSIGHTS
    # ============================================================

    st.subheader("💡 Pricing Insights")

    highest_price_category = (
        category_summary["Average_Price"]
        .idxmax()
    )

    highest_demand_category = (
        category_summary["Total_Quantity"]
        .idxmax()
    )

    lowest_price_category = (
        category_summary["Average_Price"]
        .idxmin()
    )

    col1, col2, col3 = st.columns(3)

    col1.info(
        f"**Highest Average Price**\n\n"
        f"{highest_price_category}\n\n"
        f"₹{category_summary.loc[highest_price_category, 'Average_Price']:,.2f}"
    )

    col2.success(
        f"**Highest Total Demand**\n\n"
        f"{highest_demand_category}\n\n"
        f"{category_summary.loc[highest_demand_category, 'Total_Quantity']:,.0f} units"
    )

    col3.warning(
        f"**Lowest Average Price**\n\n"
        f"{lowest_price_category}\n\n"
        f"₹{category_summary.loc[lowest_price_category, 'Average_Price']:,.2f}"
    )

    st.caption(
        "These are descriptive observations from the pricing dataset."
    )
# ============================================================
# 📉 PRICE ELASTICITY
# ============================================================

elif page == "📉 Price Elasticity":

    # ============================================================
    # PRICE ELASTICITY
    # ============================================================

    st.title("📉 Price Elasticity Analysis")

    st.write(
        "Analyze how changes in product prices are associated "
        "with changes in demand."
    )

    st.divider()

    # ============================================================
    # LOAD ELASTICITY RESULTS
    # ============================================================

    elasticity = pd.read_csv(
        "data/processed/product_elasticity_summary.csv"
    )

    # ============================================================
    # OVERVIEW KPIs
    # ============================================================

    total_products = elasticity["product_id"].nunique()

    elastic_products = (
        elasticity["Elasticity_Type"]
        .eq("Elastic")
        .sum()
    )

    inelastic_products = (
        elasticity["Elasticity_Type"]
        .eq("Inelastic")
        .sum()
    )

    unit_elastic_products = (
        elasticity["Elasticity_Type"]
        .eq("Unit Elastic")
        .sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Products Analyzed",
        total_products
    )

    col2.metric(
        "Elastic Products",
        elastic_products
    )

    col3.metric(
        "Inelastic Products",
        inelastic_products
    )

    col4.metric(
        "Unit Elastic",
        unit_elastic_products
    )

    st.divider()

    # ============================================================
    # ELASTICITY TYPE DISTRIBUTION
    # ============================================================

    st.subheader("📊 Elasticity Type Distribution")

    elasticity_distribution = (
        elasticity["Elasticity_Type"]
        .value_counts()
    )

    st.bar_chart(
        elasticity_distribution
    )

    st.caption(
        "Classification based on the absolute value of median price elasticity."
    )

    st.divider()

    # ============================================================
    # ELASTICITY TABLE
    # ============================================================

    st.subheader("📋 Product Elasticity Summary")

    display_columns = [
        "product_id",
        "Elasticity_Observations",
        "Mean_Elasticity",
        "Median_Elasticity",
        "Min_Elasticity",
        "Max_Elasticity",
        "Abs_Median_Elasticity",
        "Elasticity_Type",
        "Reliability"
    ]

    available_columns = [
        col for col in display_columns
        if col in elasticity.columns
    ]

    st.dataframe(
        elasticity[available_columns]
        .sort_values(
            "Abs_Median_Elasticity",
            ascending=False
        )
        .round(2),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ============================================================
    # PRODUCT ELASTICITY EXPLORER
    # ============================================================

    st.subheader("🔎 Product Elasticity Explorer")

    products = sorted(
        elasticity["product_id"]
        .astype(str)
        .unique()
    )

    selected_product = st.selectbox(
        "Select a product",
        products
    )

    selected_data = elasticity[
        elasticity["product_id"].astype(str)
        == selected_product
    ].iloc[0]

    # ============================================================
    # SELECTED PRODUCT KPIs
    # ============================================================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Median Elasticity",
        f"{selected_data['Median_Elasticity']:.2f}"
    )

    col2.metric(
        "Observations",
        int(selected_data["Elasticity_Observations"])
    )

    col3.metric(
        "Elasticity Type",
        selected_data["Elasticity_Type"]
    )

    st.divider()

    # ============================================================
    # SELECTED PRODUCT DETAILS
    # ============================================================

    st.subheader("📌 Product Details")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Product:** {selected_product}"
        )

        st.write(
            f"**Mean Elasticity:** "
            f"{selected_data['Mean_Elasticity']:.2f}"
        )

        st.write(
            f"**Median Elasticity:** "
            f"{selected_data['Median_Elasticity']:.2f}"
        )

    with col2:

        st.write(
            f"**Minimum Elasticity:** "
            f"{selected_data['Min_Elasticity']:.2f}"
        )

        st.write(
            f"**Maximum Elasticity:** "
            f"{selected_data['Max_Elasticity']:.2f}"
        )

        st.write(
            f"**Reliability:** "
            f"{selected_data['Reliability']}"
        )

    st.divider()

    # ============================================================
    # HIGHEST ELASTICITY PRODUCTS
    # ============================================================

    st.subheader("📈 Products with Highest Absolute Elasticity")

    highest_elasticity = (
        elasticity[
            [
                "product_id",
                "Abs_Median_Elasticity",
                "Median_Elasticity",
                "Elasticity_Type",
                "Reliability"
            ]
        ]
        .sort_values(
            "Abs_Median_Elasticity",
            ascending=False
        )
        .head(10)
        .round(2)
    )

    st.dataframe(
        highest_elasticity,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Products are sorted by the absolute value of median elasticity."
    )

    st.divider()

    # ============================================================
    # RELIABILITY ANALYSIS
    # ============================================================

    st.subheader("🎯 Elasticity Reliability")

    reliability_summary = (
        elasticity
        .groupby("Reliability")
        .agg(
            Products=("product_id", "nunique"),
            Average_Observations=(
                "Elasticity_Observations",
                "mean"
            ),
            Median_Absolute_Elasticity=(
                "Abs_Median_Elasticity",
                "median"
            )
        )
        .round(2)
    )

    st.dataframe(
        reliability_summary,
        use_container_width=True
    )

    st.caption(
        "Reliability is based on the number of valid elasticity observations "
        "available for each product."
    )

    st.divider()

    # ============================================================
    # INTERPRETATION
    # ============================================================

    st.subheader("💡 How to Interpret Elasticity")

    st.info(
        """
        **Elastic:** Absolute elasticity greater than 1. Demand changes
        relatively more than price changes in the observed data.

        **Inelastic:** Absolute elasticity less than 1. Demand changes
        relatively less than price changes in the observed data.

        **Unit Elastic:** Absolute elasticity equal to 1.

        These elasticity values are based on historical observational data.
        They should be interpreted as associations rather than proof that
        changing the price will directly cause the observed demand change.
        """
    )


# ============================================================
# 🏪 COMPETITOR ANALYSIS
# ============================================================

# ============================================================
# 🏪 COMPETITOR ANALYSIS
# ============================================================

elif page == "🏪 Competitor Analysis":

    st.title("🏪 Competitor Price Analysis")

    st.write(
        "Compare product prices with competitor prices and "
        "understand competitive positioning."
    )

    st.divider()

    # ========================================================
    # COMPETITOR DATA
    # ========================================================

    competitor_data = retail.copy()

    # Make sure competitor columns are numeric
    numeric_columns = [
        "unit_price",
        "comp_1",
        "comp_2",
        "comp_3",
        "qty",
        "Avg_Competitor_Price",
        "Min_Competitor_Price",
        "Max_Competitor_Price",
        "Price_Difference",
        "Price_Gap_Pct"
    ]

    for column in numeric_columns:

        if column in competitor_data.columns:

            competitor_data[column] = pd.to_numeric(
                competitor_data[column],
                errors="coerce"
            )

    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    avg_product_price = (
        competitor_data["unit_price"].mean()
    )

    avg_competitor_price = (
        competitor_data["Avg_Competitor_Price"].mean()
    )

    avg_price_gap = (
        competitor_data["Price_Gap_Pct"].mean()
    )

    total_records = len(
        competitor_data
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average Product Price",
        f"₹{avg_product_price:,.2f}"
    )

    col2.metric(
        "Average Competitor Price",
        f"₹{avg_competitor_price:,.2f}"
    )

    col3.metric(
        "Average Price Gap",
        f"{avg_price_gap:,.2f}%"
    )

    col4.metric(
        "Records Analyzed",
        f"{total_records:,}"
    )

    st.divider()

    # ========================================================
    # COMPETITIVE POSITION DISTRIBUTION
    # ========================================================

    st.subheader(
        "📊 Competitive Position Distribution"
    )

    position_distribution = (
        competitor_data[
            "Competitive_Position"
        ]
        .value_counts()
    )

    st.bar_chart(
        position_distribution
    )

    st.caption(
        "Products are classified as Below, Similar to, or Above "
        "competitor prices using the project-defined price-gap thresholds."
    )

    st.divider()

    # ========================================================
    # COMPETITIVE POSITION SUMMARY
    # ========================================================

    st.subheader(
        "📋 Competitive Position Summary"
    )

    position_summary = (
        competitor_data
        .groupby("Competitive_Position")
        .agg(
            Records=("product_id", "count"),
            Products=("product_id", "nunique"),
            Average_Price=("unit_price", "mean"),
            Average_Competitor_Price=(
                "Avg_Competitor_Price",
                "mean"
            ),
            Average_Price_Gap=(
                "Price_Gap_Pct",
                "mean"
            ),
            Average_Quantity=("qty", "mean"),
            Total_Quantity=("qty", "sum")
        )
        .round(2)
    )

    st.dataframe(
        position_summary,
        use_container_width=True
    )

    st.divider()

    # ========================================================
    # OUR PRICE VS COMPETITOR PRICE
    # ========================================================

    st.subheader(
        "💰 Our Price vs Competitor Price"
    )

    price_comparison = (
        competitor_data[
            [
                "unit_price",
                "Avg_Competitor_Price"
            ]
        ]
        .dropna()
        .copy()
    )

    price_comparison.columns = [
        "Our Price",
        "Average Competitor Price"
    ]

    st.scatter_chart(
        price_comparison,
        x="Average Competitor Price",
        y="Our Price"
    )

    st.caption(
        "Each point represents a pricing observation. "
        "Points above the diagonal relationship indicate relatively higher prices."
    )

    st.divider()

    # ========================================================
    # PRICE GAP DISTRIBUTION
    # ========================================================

    st.subheader(
        "📈 Price Gap Distribution"
    )

    gap_data = (
        competitor_data[
            "Price_Gap_Pct"
        ]
        .dropna()
    )

    st.line_chart(
        gap_data.reset_index(drop=True)
    )

    st.caption(
        "Percentage difference between our product price and "
        "the average competitor price."
    )

    st.divider()

    # ========================================================
    # DEMAND BY COMPETITIVE POSITION
    # ========================================================

    st.subheader(
        "📦 Demand by Competitive Position"
    )

    demand_by_position = (
        competitor_data
        .groupby("Competitive_Position")["qty"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        demand_by_position
    )

    st.caption(
        "Total recorded quantity for each competitive pricing position."
    )

    st.divider()

    # ========================================================
    # PRODUCT EXPLORER
    # ========================================================

    st.subheader(
        "🔎 Product Competitor Explorer"
    )

    products = sorted(
        competitor_data[
            "product_id"
        ]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_product = st.selectbox(
        "Select a product",
        products
    )

    selected_product_data = competitor_data[
        competitor_data["product_id"].astype(str)
        == selected_product
    ].copy()

    if len(selected_product_data) > 0:

        latest_product = (
            selected_product_data
            .sort_values("month_year")
            .iloc[-1]
        )

        # ----------------------------------------------------
        # PRODUCT KPIs
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Our Price",
            f"₹{latest_product['unit_price']:,.2f}"
        )

        col2.metric(
            "Competitor Avg.",
            f"₹{latest_product['Avg_Competitor_Price']:,.2f}"
        )

        col3.metric(
            "Price Gap",
            f"{latest_product['Price_Gap_Pct']:,.2f}%"
        )

        col4.metric(
            "Position",
            str(
                latest_product[
                    "Competitive_Position"
                ]
            )
        )

        st.divider()

        # ----------------------------------------------------
        # COMPETITOR COMPARISON
        # ----------------------------------------------------

        st.subheader(
            "💰 Competitor Price Comparison"
        )

        competitor_prices = pd.DataFrame(
            {
                "Price": [
                    latest_product["unit_price"],
                    latest_product["comp_1"],
                    latest_product["comp_2"],
                    latest_product["comp_3"]
                ]
            },
            index=[
                "Our Price",
                "Competitor 1",
                "Competitor 2",
                "Competitor 3"
            ]
        )

        st.bar_chart(
            competitor_prices
        )

        st.divider()

        # ----------------------------------------------------
        # PRODUCT HISTORY
        # ----------------------------------------------------

        st.subheader(
            "📈 Product Price History"
        )

        product_history = (
            selected_product_data
            .sort_values("month_year")
            .copy()
        )

        product_history["month_year"] = pd.to_datetime(
            product_history["month_year"],
            errors="coerce",
            dayfirst=True
        )

        product_history = (
            product_history
            .dropna(subset=["month_year"])
            .set_index("month_year")
        )

        history_chart = product_history[
            [
                "unit_price",
                "Avg_Competitor_Price"
            ]
        ].copy()

        history_chart.columns = [
            "Our Price",
            "Average Competitor Price"
        ]

        st.line_chart(
            history_chart
        )

        st.divider()

        # ----------------------------------------------------
        # PRODUCT RECORDS
        # ----------------------------------------------------

        st.subheader(
            "📋 Product Competitor Records"
        )

        detail_columns = [
            "month_year",
            "unit_price",
            "comp_1",
            "comp_2",
            "comp_3",
            "Avg_Competitor_Price",
            "Price_Difference",
            "Price_Gap_Pct",
            "qty",
            "Competitive_Position"
        ]

        available_columns = [
            column
            for column in detail_columns
            if column in selected_product_data.columns
        ]

        product_records = (
            selected_product_data[
                available_columns
            ]
            .sort_values(
                "month_year",
                ascending=False
            )
        )

        st.dataframe(
            product_records,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ========================================================
    # BUSINESS INTERPRETATION
    # ========================================================

    st.subheader(
        "💡 Competitive Pricing Interpretation"
    )

    st.info(
        """
        **Below Competitors:** Our recorded price is more than 5%
        below the average competitor price.

        **Similar to Competitors:** Our recorded price is within
        ±5% of the average competitor price.

        **Above Competitors:** Our recorded price is more than 5%
        above the average competitor price.

        These comparisons describe historical pricing positions.
        They do not by themselves establish that price differences
        caused differences in demand.
        """
    )


# ============================================================
# 💡 BUSINESS INSIGHTS
# ============================================================

# ============================================================
# 💡 BUSINESS INSIGHTS
# ============================================================

elif page == "💡 Business Insights":

    st.title("💡 Business Insights")

    st.write(
        "Convert demand predictions, pricing analysis and risk information "
        "into practical business decisions."
    )

    st.divider()

    # ========================================================
    # LOAD BUSINESS DATA
    # ========================================================

    prediction = pd.read_csv(
        "data/predictions/final_decision_table.csv"
    )

    risk_summary = pd.read_csv(
        "data/predictions/prediction_risk_summary.csv"
    )

    recommendations = pd.read_csv(
        "data/predictions/business_action_recommendations.csv"
    )

    # ========================================================
    # CLEAN NUMERIC COLUMNS
    # ========================================================

    numeric_columns = [
        "Next_Month_Quantity",
        "Predicted_Quantity",
        "Absolute_Error",
        "Relative_Error_Pct",
        "Suggested_Stock"
    ]

    for column in numeric_columns:

        if column in prediction.columns:

            prediction[column] = pd.to_numeric(
                prediction[column],
                errors="coerce"
            )

    # ========================================================
    # KPI SECTION
    # ========================================================

    total_predictions = len(prediction)

    high_risk = (
        prediction["Prediction_Risk"]
        .eq("High")
        .sum()
    )

    moderate_risk = (
        prediction["Prediction_Risk"]
        .eq("Moderate")
        .sum()
    )

    total_suggested_stock = (
        prediction["Suggested_Stock"]
        .sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Prediction Records",
        f"{total_predictions:,}"
    )

    col2.metric(
        "High Risk Predictions",
        f"{high_risk:,}"
    )

    col3.metric(
        "Moderate Risk Predictions",
        f"{moderate_risk:,}"
    )

    col4.metric(
        "Suggested Stock",
        f"{total_suggested_stock:,.0f}"
    )

    st.divider()

    # ========================================================
    # RISK DISTRIBUTION
    # ========================================================

    st.subheader("⚠️ Prediction Risk Distribution")

    risk_order = [
        "High",
        "Moderate",
        "Low",
        "Zero Demand"
    ]

    risk_distribution = (
        prediction["Prediction_Risk"]
        .value_counts()
        .reindex(
            risk_order,
            fill_value=0
        )
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.bar(
        risk_distribution.index,
        risk_distribution.values
    )

    for bar, value in zip(
        bars,
        risk_distribution.values
    ):

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:,}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    ax.set_xlabel("Prediction Risk")
    ax.set_ylabel("Number of Predictions")
    ax.set_title("Prediction Risk Distribution")

    plt.xticks(rotation=0)

    st.pyplot(fig)

    st.divider()

    # ========================================================
    # RISK SUMMARY TABLE
    # ========================================================

    st.subheader("📋 Risk Summary")

    risk_table = pd.DataFrame(
        {
            "Risk Level": risk_distribution.index,
            "Predictions": risk_distribution.values
        }
    )

    risk_table["Percentage"] = (
        risk_table["Predictions"]
        / risk_table["Predictions"].sum()
        * 100
    )

    risk_table["Percentage"] = (
        risk_table["Percentage"]
        .round(2)
    )

    st.dataframe(
        risk_table,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ========================================================
    # HIGH RISK ANALYSIS
    # ========================================================

    st.subheader("🔴 High-Risk Prediction Analysis")

    high_risk_data = (
        prediction[
            prediction["Prediction_Risk"] == "High"
        ]
        .sort_values(
            "Relative_Error_Pct",
            ascending=False
        )
    )

    high_risk_columns = [
        "StockCode",
        "MonthYear",
        "Next_Month_Quantity",
        "Predicted_Quantity",
        "Absolute_Error",
        "Relative_Error_Pct",
        "Suggested_Stock"
    ]

    available_columns = [
        column
        for column in high_risk_columns
        if column in high_risk_data.columns
    ]

    st.dataframe(
        high_risk_data[
            available_columns
        ]
        .head(20)
        .round(2),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "High-risk predictions should be reviewed carefully before "
        "making inventory decisions."
    )

    st.divider()

    # ========================================================
    # BUSINESS ACTION RECOMMENDATIONS
    # ========================================================

    st.subheader("🎯 Business Action Recommendations")

    if len(recommendations) > 0:

        st.dataframe(
            recommendations,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No business action recommendation records were found."
        )

    st.divider()

    # ========================================================
    # INVENTORY PLANNING
    # ========================================================

    st.subheader("📦 Inventory Planning")

    inventory_columns = [
        "StockCode",
        "MonthYear",
        "Predicted_Quantity",
        "Suggested_Stock",
        "Prediction_Risk"
    ]

    available_inventory_columns = [
        column
        for column in inventory_columns
        if column in prediction.columns
    ]

    inventory_data = (
        prediction[
            available_inventory_columns
        ]
        .sort_values(
            "Suggested_Stock",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        inventory_data.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Suggested stock is based on predicted demand with the "
        "project-defined safety buffer."
    )

    st.divider()

    # ========================================================
    # PRODUCT DECISION EXPLORER
    # ========================================================

    st.subheader("🔎 Product Decision Explorer")

    products = sorted(
        prediction["StockCode"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_product = st.selectbox(
        "Select a product",
        products
    )

    product_data = prediction[
        prediction["StockCode"].astype(str)
        == selected_product
    ].copy()

    if len(product_data) > 0:

        latest_prediction = (
            product_data
            .sort_values("MonthYear")
            .iloc[-1]
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Predicted Demand",
            f"{latest_prediction['Predicted_Quantity']:,.0f}"
        )

        col2.metric(
            "Suggested Stock",
            f"{latest_prediction['Suggested_Stock']:,.0f}"
        )

        col3.metric(
            "Actual Demand",
            f"{latest_prediction['Next_Month_Quantity']:,.0f}"
        )

        col4.metric(
            "Risk",
            str(
                latest_prediction["Prediction_Risk"]
            )
        )

        st.divider()

        st.subheader("📈 Product Prediction History")

        history = (
            product_data
            .sort_values("MonthYear")
            .copy()
        )

        history_chart = history[
            [
                "Predicted_Quantity",
                "Next_Month_Quantity"
            ]
        ].copy()

        history_chart.columns = [
            "Predicted Demand",
            "Actual Demand"
        ]

        st.line_chart(
            history_chart
        )

        st.divider()

        st.subheader("📋 Product Decision History")

        history_columns = [
            "StockCode",
            "MonthYear",
            "Next_Month_Quantity",
            "Predicted_Quantity",
            "Absolute_Error",
            "Relative_Error_Pct",
            "Prediction_Risk",
            "Suggested_Stock"
        ]

        available_history_columns = [
            column
            for column in history_columns
            if column in product_data.columns
        ]

        st.dataframe(
            product_data[
                available_history_columns
            ]
            .sort_values(
                "MonthYear",
                ascending=False
            )
            .round(2),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ========================================================
    # OVERALL BUSINESS INTERPRETATION
    # ========================================================

    st.subheader("💡 Overall Business Interpretation")

    st.info(
        """
        **Demand Planning:** Use predicted demand as a reference for
        future inventory planning.

        **High-Risk Predictions:** Review these predictions carefully
        because their historical prediction error is relatively high.

        **Moderate-Risk Predictions:** Monitor demand trends and adjust
        inventory when necessary.

        **Low-Risk Predictions:** These predictions can be used as a
        stronger reference for routine inventory planning.

        **Zero-Demand Products:** Avoid unnecessary inventory buildup
        and investigate whether the product is inactive or experiencing
        very low demand.

        **Important:** These insights are based on historical data and
        model predictions. They should support business decisions rather
        than replace human review.
        """
    )