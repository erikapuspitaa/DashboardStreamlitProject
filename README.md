# DashboardStreamlitProject

# E-Commerce Public Dashboard🛒


## About Dataset
The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allows viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, product attributes and payment.

## About Project
Simple dashboard using streamlit to deliver analysis results from public ecommerce public dataset.

## Installation Anaconda
1. Go to anaconda.com/download.
2. Install Anaconda Distribution for your OS.

## Setting Path Environtment 
1. Go to Edit the System Environtment Variables
2. Select Environtment Variable, then select Path and Edit
3. Add below :
```sh
C:\Users\Lenovo\anaconda3\Scripts\
C:\Users\Lenovo\anaconda3
```
4. Click OK

## Create an environment using Anaconda Navigato
1. Open Anaconda Navigator (the graphical interface included with Anaconda Distribution).
2. You can decline signing in to Anaconda if prompted.
3. In the left menu, click "Environments".
4. Enter "streamlitenv" for the name of your environment.
5. Click "Create."

## Activate your environment
1. Click the green play icon (play_circle) next to your environment.
2. Click "Open Terminal."

Detail information :  https://docs.streamlit.io/get-started/installation/anaconda-distribution

## Install Streamlit and setup environment 
```sh
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel
```

## Run steamlit app
```sh
streamlit run dashboard.py
```
## Quickstart Streamlit Community Cloud
Follow the tutorial below: https://docs.streamlit.io/streamlit-community-cloud/get-started/quickstart








