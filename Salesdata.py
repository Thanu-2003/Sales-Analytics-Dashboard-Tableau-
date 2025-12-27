import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# MySQL connection settings
# --------------------------
user = 'root'
password = 'root'
host = 'localhost'  # MySQL host
port = 3306
database = 'sales_db'

# Create SQLAlchemy engine
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')


path = r"C:\Users\thanu\Downloads\Sales analytics\Sales_Data.xlsx"
df = pd.ExcelFile(path)
# df = pd.read_excel("C:\\Users\\thanu\\Downloads\\Sales analytics\\Sales_Data.xlsx")
# df = pd.read_excel("C:/Users/thanu/Downloads/Sales analytics/Sales_Data.xlsx")
# df = pd.read_excel('sales_Data.xlsx')

print(df.sheet_names)
# data = pd.DataFrame(df)
# print(data)
# print(data.head())
# print(data.shape)
# print(data.info)
# for sheet in data:
#     print(sheet)
# print(data['Product_Info'])

#  -----------------------------------------------------------Sales_Transactions ----------------------------------------------

# --- ['Sales_Transactions', 'Sales_by_Month_Wide', 'Inventory_Log', 'Regional_Performance', 'Customer_Feedback', 'Supplier_Data', 'Employee_Performance', 'Campaign_Metrics', 'Customer_Accounts', 'Purchase_History'] ---
data_Sales_Transactions = pd.read_excel(path,sheet_name='Sales_Transactions')
print(data_Sales_Transactions)
print(data_Sales_Transactions.shape)
print(data_Sales_Transactions.describe())
print(data_Sales_Transactions.info())
print(data_Sales_Transactions['Date'])

data_Sales_Transactions['Date_fy'] = pd.to_datetime(data_Sales_Transactions['Date'],errors = 'ignore')
data_Sales_Transactions['Date_fy'] = pd.to_datetime(data_Sales_Transactions['Date'], dayfirst=True, errors='coerce')

print(data_Sales_Transactions['Date_fy'])
print(data_Sales_Transactions.info())

data_Sales_Transactions['Date_fy'].isna().sum()
print(data_Sales_Transactions['Date_fy'].isna().sum())

# -----date-------
mask = data_Sales_Transactions['Date'].astype(str).str.contains(r'[A-Za-z]', na=False)
data_Sales_Transactions.loc[mask, 'Date'] = pd.to_datetime(
    data_Sales_Transactions.loc[mask, 'Date'],
    format='%d-%b-%Y',
    errors='coerce'
)
data_Sales_Transactions['Date'] =pd.to_datetime(data_Sales_Transactions['Date'], errors='coerce')
# print(data_Sales_Transactions['Date'])
print(data_Sales_Transactions['Date'].isna().sum())
data_Sales_Transactions['Date'] = pd.to_datetime(data_Sales_Transactions['Date'].fillna(method = 'bfill'))
print(data_Sales_Transactions['Date'].isna().sum())
print(data_Sales_Transactions['Date'].unique)
# ------Transaction_ID------
for columns in data_Sales_Transactions:
    print(columns)
print(data_Sales_Transactions['Transaction_ID'])
print(data_Sales_Transactions['Transaction_ID'].unique())


#  ------- Product_Info -- ------
for columns in data_Sales_Transactions:
    print(columns)
print(data_Sales_Transactions['Product_Info'])
data_Sales_Transactions[['Alpa_code','Product_code','Product_name','Product_value']] = data_Sales_Transactions['Product_Info'].str.split('[-|]',expand=True)
print(data_Sales_Transactions[['Alpa_code','Product_code','Product_name','Product_value']])

print(data_Sales_Transactions['Alpa_code'].is_unique)
print(data_Sales_Transactions['Product_code'].info)
print(data_Sales_Transactions['Product_name'].info)
print(data_Sales_Transactions['Product_value'].is_unique)
data_Sales_Transactions['Product_value'] = pd.to_numeric(data_Sales_Transactions['Product_value'])
data_Sales_Transactions.drop(columns='Product_Info',inplace= True)
print(data_Sales_Transactions.info())


#  ------- Location -- ------
# for columns in data_Sales_Transactions:
#     print(columns)

print(data_Sales_Transactions['Location'].unique)
data_Sales_Transactions[['Region','Country_code']] = data_Sales_Transactions['Location'].str.split('[ |/-]' ,n=2,expand=True)
print(data_Sales_Transactions[['Region','Country_code']])

# print(data_Sales_Transactions['Region'].unique())

# print(data_Sales_Transactions.info())

#  -------  Quantity --------
for columns in data_Sales_Transactions:
    print(columns)

# data_Sales_Transactions['Quantity'].info()
# for i in data_Sales_Transactions['Quantity']:
#     if i <= -1:
#         print(i)
data_Sales_Transactions['Quantity'] = data_Sales_Transactions['Quantity'].abs()

print(data_Sales_Transactions['Quantity'].unique())

#  ------Unit_Price ------
print(data_Sales_Transactions['Unit_Price'].info())

#  -------Total_Amount ------
print(data_Sales_Transactions['Total_Amount'].info())

#  ------- Customer_ID --------
print(data_Sales_Transactions['Customer_ID'].info())
print(data_Sales_Transactions['Customer_ID'])

#  -------- Customer_Contact----------
print(data_Sales_Transactions['Customer_Contact'].info())
data_Sales_Transactions[['Customer_it','Customer_Number','Customer_Mailid']] = data_Sales_Transactions['Customer_Contact'].str.split('[|]',expand=True)
print(data_Sales_Transactions[['Customer_it','Customer_Number','Customer_Mailid']])
print(data_Sales_Transactions[['Customer_it','Customer_ID']])
data_Sales_Transactions.drop(columns=['Customer_it'])
data_Sales_Transactions.drop(columns='Customer_it',inplace= True)

print(data_Sales_Transactions.info())

#  --------- Sales_Rep_ID -----------

print(data_Sales_Transactions['Sales_Rep_ID'].info())
print(data_Sales_Transactions['Sales_Rep_ID'].head(20))
data_Sales_Transactions['Sales_Rep_ID'].fillna('id_not_available')
print(data_Sales_Transactions['Sales_Rep_ID'].fillna('id_not_available',inplace=True))
print(data_Sales_Transactions['Sales_Rep_ID'].info())

#  ------- Payment_Method ------
print(data_Sales_Transactions['Payment_Method'].info())
data_Sales_Transactions['Payment_Method'].fillna('Blank',inplace=True)
print(data_Sales_Transactions['Payment_Method'].info())
print(data_Sales_Transactions['Payment_Method'].unique())
#  --------- Order_Status -------

print(data_Sales_Transactions['Order_Status'].unique())
print(data_Sales_Transactions['Order_Status'].info())


#  ------------------------------------------------------Sales_by_Month_Wide----------------------------------------------------
data_Sales_by_Month_Wide = pd.read_excel(path,sheet_name='Sales_by_Month_Wide')

print(data_Sales_by_Month_Wide.head(30))

df_long = data_Sales_by_Month_Wide.melt(
    id_vars=['Region','Category'],
    var_name='Month',
    value_name='Sales'
)

df_long['Date'] = pd.to_datetime(
    df_long['Month'] + '-2024',
    format='%b-%Y'
)
data_Sales_by_Month_Wide_ = df_long[['Region','Category','Date','Sales']]
print(data_Sales_by_Month_Wide_.head(50))

print(data_Sales_by_Month_Wide_.info())
print(data_Sales_by_Month_Wide_)
# fact_sales.drop_duplicates()
print(data_Sales_by_Month_Wide_['Region'].isna().sum())

print(data_Sales_by_Month_Wide_.dropna(inplace=True))
print(data_Sales_by_Month_Wide_)
print(data_Sales_by_Month_Wide_.info())



#  -------------------------------     Inventory_Log --------------------------
# print(df.sheet_names)
data_Inventory_Log = pd.read_excel(path,sheet_name='Inventory_Log')
print(data_Inventory_Log)
print(data_Inventory_Log.info())
data_Inventory_Log['Log_Date'] = pd.to_datetime(data_Inventory_Log['Log_Date'])
print(data_Inventory_Log)
print(data_Inventory_Log.info())
print(data_Inventory_Log['Notes'].isna().sum())
data_Inventory_Log['Notes'].fillna('blank_value',inplace=True)
print(data_Inventory_Log.info())

# ----------------------------------Customer_Feedback------------------------------------------
data_Customer_Feedback = pd.read_excel(path,sheet_name='Customer_Feedback')

print(data_Customer_Feedback.head(10))

print(data_Customer_Feedback.info())
print(data_Customer_Feedback['Customer_ID'].head(10))
data_Customer_Feedback['Feedback_Date'] = pd.to_datetime(data_Customer_Feedback['Feedback_Date'])
print(data_Customer_Feedback['Feedback_Date'].head(10))
data_Customer_Feedback[['Product_code','Product_name','Product_buy_Category']] = data_Customer_Feedback['Product_Info'].str.split('[|]',expand=True)
print(data_Customer_Feedback[['Product_code','Product_name','Product_buy_Category']].head(10))
data_Customer_Feedback.drop('Product_Info',axis=1,inplace=True)
print(data_Customer_Feedback.info())

print(data_Customer_Feedback['Feedback_Text'].info())
print(data_Customer_Feedback['Feedback_Text'].head(10))

print(data_Customer_Feedback['Tags'].head(10))
#  -----------------------------------  Regional_Performance ----------------------------------------------
print(df.sheet_names)
data_Regional_Performance = pd.read_excel(path,sheet_name='Regional_Performance')
print(data_Regional_Performance)
print(data_Regional_Performance.info())
data_Regional_Performance['Sales'] = (
    data_Regional_Performance['Sales']
    .fillna(data_Regional_Performance['Sales'].mean())
)
print(data_Regional_Performance)
print(data_Regional_Performance.info())


# ------------ MYSQL ETL (FINAL) -----------------
data_Sales_Transactions.to_sql("data_Sales_Transactions", con=engine, if_exists="replace", index=False)
data_Sales_by_Month_Wide_.to_sql("data_Sales_by_Month_Wide_", con=engine, if_exists="replace", index=False)
data_Inventory_Log.to_sql("data_Inventory_Log", con=engine, if_exists="replace", index=False)
data_Customer_Feedback.to_sql("data_Customer_Feedback", con=engine, if_exists="replace", index=False)
data_Regional_Performance.to_sql("data_Regional_Performance", con=engine, if_exists="replace", index=False)



