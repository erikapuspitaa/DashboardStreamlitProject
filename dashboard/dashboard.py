import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import csv

st.set_option('deprecation.showPyplotGlobalUse', False)

current_directory = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_directory, "..", "data") 

# Membaca dataset
customers_df = pd.read_csv(os.path.join(data_path, "customers_dataset.csv"))
order_item_df = pd.read_csv(os.path.join(data_path, "order_items_dataset.csv"))
order_payment_df = pd.read_csv(os.path.join(data_path, "order_payments_dataset.csv"))
orders_df = pd.read_csv(os.path.join(data_path, "orders_dataset.csv"))
product_df = pd.read_csv(os.path.join(data_path, "products_dataset.csv"))

# Menangani missing value pada orders_df
orders_df['order_approved_at'] = pd.to_datetime(orders_df['order_approved_at'], errors='coerce')
orders_df['order_delivered_carrier_date'] = pd.to_datetime(orders_df['order_delivered_carrier_date'], errors='coerce')
orders_df['order_delivered_customer_date'] = pd.to_datetime(orders_df['order_delivered_customer_date'], errors='coerce')

mean_order_approved_at = orders_df['order_approved_at'].mean()
mean_order_delivered_carrier_date = orders_df['order_delivered_carrier_date'].mean()
mean_order_delivered_customer_date = orders_df['order_delivered_customer_date'].mean()

orders_df['order_approved_at'].fillna(mean_order_approved_at, inplace=True)
orders_df['order_delivered_carrier_date'].fillna(mean_order_delivered_carrier_date, inplace=True)
orders_df['order_delivered_customer_date'].fillna(mean_order_delivered_customer_date, inplace=True)

# Menangani missing value pada product_df
product_df['product_category_name'].fillna(product_df['product_category_name'].mode()[0], inplace=True)
product_df['product_name_lenght'].fillna(product_df['product_name_lenght'].mean(), inplace=True)
product_df['product_description_lenght'].fillna(product_df['product_description_lenght'].mean(), inplace=True)
product_df['product_photos_qty'].fillna(product_df['product_photos_qty'].mean(), inplace=True)
product_df['product_weight_g'].fillna(product_df['product_weight_g'].mean(), inplace=True)
product_df['product_length_cm'].fillna(product_df['product_length_cm'].mean(), inplace=True)
product_df['product_height_cm'].fillna(product_df['product_height_cm'].mean(), inplace=True)
product_df['product_width_cm'].fillna(product_df['product_width_cm'].mean(), inplace=True)

# Menggabungkan data orders dan customer
merged_df = pd.merge(customers_df, orders_df, on='customer_id', how='inner')

# Menggabungkan data product dan order payment
merged_df2 = pd.merge(order_item_df, product_df[['product_id', 'product_weight_g']], on='product_id', how='left')
merged_df2 = pd.merge(merged_df2, order_payment_df[['order_id', 'payment_value']], on='order_id', how='left')
final_merged_df = pd.merge(merged_df, merged_df2, on='order_id', how='inner')

# Menyiapkan data untuk visualisasi tren jumlah pembelian per bulan
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
orders_df['order_purchase_month'] = orders_df['order_purchase_timestamp'].dt.to_period('M')
tren_monthly_orders = orders_df.groupby('order_purchase_month').size()

st.title('🛍️E-Commerce Public Dataset🛒')
st.write('Oleh : Erika Dwi Puspitasari')

st.sidebar.image('logo-modified.png', width=250)

# Sidebar
st.sidebar.title('E-Commerce Dashboard')
menu = st.sidebar.selectbox('Pilih Menu:', ['Dashboard', 'Dataset',])

# Visualisasi sesuai pilihan menu
if menu == 'Dashboard':
    
     # 10 Kota dengan Jumlah Pelanggan Terbanyak
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('10 Kota dengan Jumlah Pelanggan Terbanyak')
        city_counts = customers_df['customer_city'].value_counts().head(10)
        plt.figure(figsize=(9, 6))
        city_counts.plot(kind='bar', color='skyblue')
        plt.title('Top 10 Kota by Number of Customers')
        plt.xlabel('City')
        plt.ylabel('Number of Customers')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot()
        
    # Perbandingan Pengiriman Terlambat vs Tepat Waktu
    with col2:
        st.subheader('Perbandingan Pengiriman Terlambat vs Tepat Waktu')
        late_deliveries_count = orders_df['order_delivered_customer_date'] > orders_df['order_estimated_delivery_date']
        late_deliveries_count = late_deliveries_count.sum()
        on_time_deliveries_count = len(orders_df) - late_deliveries_count
        sizes = [late_deliveries_count, on_time_deliveries_count]
        labels = ['Terlambat', 'Tepat Waktu']
        colors = ['#ff9999', '#66b3ff']
        explode = (0.1, 0)
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda p: '{:.0f} ({:.0f}%)'.format(p * sum(sizes) / 100, p),
                shadow=True, startangle=140)
        plt.title('Perbandingan Pengiriman Terlambat vs Tepat Waktu')
        plt.axis('equal')
        st.pyplot()
    
    st.subheader('Korelasi Berat Produk dengan Biaya Pengiriman')
    plt.figure(figsize=(10, 6))
    sns.regplot(x='product_weight_g', y='payment_value', data=final_merged_df, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
    plt.title('Korelasi Berat Produk dan Biaya Pengiriman')
    plt.xlabel('Berat Produk')
    plt.ylabel('Biaya Pengiriman')
    plt.grid(True)
    correlation_coefficient = final_merged_df['product_weight_g'].corr(final_merged_df['payment_value'])
    plt.text(0.2, 5000, f"Korelasi: {correlation_coefficient:.2f}", fontsize=12)
    st.pyplot()
    
    st.subheader('Trend Jumlah Pembelian per Bulan')
    plt.figure(figsize=(10, 6))
    tren_monthly_orders.plot(marker='o')
    plt.title('Trend Jumlah Pembelian per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Pembelian')
    plt.xticks(rotation=45)
    plt.grid(True)
    st.pyplot()

if menu == 'Dataset':
    st.write("Tabel Dataset Customers:")
st.dataframe(customers_df)

st.write("Tabel Dataset Orders:")
st.dataframe(orders_df)

st.write("Tabel Dataset Products:")
st.dataframe(product_df)

st.write("Tabel Dataset Order Items:")
st.dataframe(order_item_df)

st.write("Tabel Dataset Order Payments:")
st.dataframe(order_payment_df)

