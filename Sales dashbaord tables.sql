-- create table Sales_all_details as
select * from data_sales_transactions;
alter table data_sales_transactions
drop column Customer_Contact,
drop column Date_fy;
alter table data_sales_transactions
drop column Location;
select * from data_sales_transactions;
select * from data_sales_by_month_wide_;
select * from data_regional_performance;
SELECT * FROM data_customer_feedback;
-- select * from data_inventory_log;
USE sales_db;
create TABLE ALL_SALES_DATA AS (
select sales_transactions.*,customer_feedback.Customer_ID AS CUSTOMER_ID, customer_feedback.Feedback_Date,
customer_feedback.Rating,customer_feedback.Rating,
customer_feedback.Product_code,
customer_feedback.Product_name,
customer_feedback.Product_buy_Category
FROM data_sales_transactions AS sales_transactions
LEFT JOIN data_customer_feedback AS customer_feedback
ON sales_transactions.Customer_ID = customer_feedback.Customer_ID);


SELECT data_sales_by_month_wide_.*,data_regional_performance.* FROM data_sales_by_month_wide_
INNER JOIN data_regional_performance
ON data_sales_by_month_wide_.Region = data_regional_performance.RegionName;


SELECT 
    data_sales_by_month_wide_.*,
    data_regional_performance.*,
    QUARTER(data_sales_by_month_wide_.Date) AS Quarter
FROM data_sales_by_month_wide_ 
INNER JOIN data_regional_performance 
    ON data_sales_by_month_wide_.Region = data_regional_performance.RegionName;
    
select sum(Quantity) from data_sales_transactions
where year(date)= 2024 and month(date) = 12;


