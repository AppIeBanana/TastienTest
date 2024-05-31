'''
题目一
假设我们有一个名为 Sales 的表，它记录了一家公司的产品销售数据。表的结构如下：
SaleID | ProductID | CustomerID | SaleDate   | Quantity | UnitPrice | Region
-------|-----------|------------|------------|----------|-----------|-------
1      | 101       | 1001       | 2024-04-01 | 2        | 50        | North
2      | 102       | 1002       | 2024-04-01 | 1        | 80        | South
3      | 103       | 1003       | 2024-04-02 | 5        | 20        | North
4      | 101       | 1002       | 2024-04-03 | 3        | 50        | West
5      | 102       | 1001       | 2024-04-03 | 2        | 80        | East
6      | 103       | 1002       | 2024-04-03 | 1        | 20        | South
7      | 101       | 1003       | 2024-04-04 | 1        | 50        | East
8      | 102       | 1001       | 2024-04-04 | 4        | 80        | North

使用SQL、Python、R等任一方式回答以下问题(提供代码和结果)
问题 1: 查找每个区域(Region)最畅销的产品ID。
问题 2: 计算每个产品的累积销售总额，并显示每个产品的累积销售额在所有产品销售额中的百分比。
问题 3: 找出每个客户连续两天购买的产品，并列出这些产品的详细信息。
'''

# !/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql

if __name__ == "__main__":
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='plk741023',
                         database='Tastien',
                         charset="utf8")
    cursor = db.cursor()

    # cursor.execute("""
    # CREATE DATABASE IF NOT EXISTS Tastien
    # """)

    # 创建表，插入数据
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales (
        SaleID INT AUTO_INCREMENT PRIMARY KEY,
        ProductID VARCHAR(255) NOT NULL,
        CustomerID VARCHAR(255) NOT NULL,
        SaleDate DATE NOT NULL,
        Quantity INT NOT NULL,
        UnitPrice FLOAT NOT NULL,
        Region ENUM('North','South','East','West') NOT NULL                                             
    )
    ''')

    # 插入数据
    cursor.execute('''
    INSERT INTO Sales (ProductID, CustomerID, SaleDate, Quantity, UnitPrice, Region) 
    VALUES 
    (101, 1001, '2024-04-01', 2, 50, 'North'),
    (102, 1002, '2024-04-01', 1, 80, 'South'),
    (103, 1003, '2024-04-02', 5, 20, 'North'),
    (101, 1002, '2024-04-03', 3, 50, 'West'),
    (102, 1001, '2024-04-03', 2, 80, 'East'),
    (103, 1002, '2024-04-03', 1, 20, 'South'),
    (101, 1003, '2024-04-04', 1, 50, 'East'),
    (102, 1001, '2024-04-04', 4, 80, 'North')
    ''')

    db.commit()

    # Q1:查找每个区域(Region)最畅销的产品ID
    cursor.execute("""
    SELECT 
        Region, ProductID, MAX(Quantity)
    FROM 
        Sales
    GROUP BY
        Region, ProductID
    ORDER BY 
        Region, MAX(Quantity) DESC
    """)

    result = cursor.fetchall()
    for row in result:
        print(f"区域{row[0]}最畅销的产品ID为{row[1]}\n")

    # Q2:计算每个产品的累积销售总额，并显示每个产品的累积销售额在所有产品销售额中的百分比。
    cursor.execute("""
    SELECT 
        ProductID, 
        SUM(Quantity * UnitPrice) AS TotalSales, 
        ROUND(SUM(Quantity * UnitPrice) * 100.0 / (SELECT SUM(Quantity * UnitPrice) FROM Sales),2) AS Percentage
    FROM 
        Sales
    GROUP BY
        ProductID
    ORDER BY
        TotalSales DESC
    """)

    result = cursor.fetchall()
    for row in result:
        print(f"产品{row[0]}的累计销售总额为{row[1]}, 在所有产品销售额中的百分比为{row[2]}%\n")


    #Q3:找出每个客户连续两天购买的产品，并列出这些产品的详细信息。
    cursor.execute("""
    SELECT DISTINCT
        s1.CustomerID, s1.SaleDate AS SaleDate1, s2.SaleDate AS SaleDate2, s1.ProductID, s1.UnitPrice, s1.Region
    FROM 
        Sales s1
    JOIN
        Sales s2 ON s1.CustomerID=s2.CustomerID AND s1.ProductID=s2.ProductID AND DATE_ADD(s1.SaleDate, INTERVAL 1 DAY)=s2.SaleDate
    ORDER BY 
        s1.CustomerID, s1.SaleDate
    """)

    result = cursor.fetchall()
    for row in result:
        print(f"客户{row[0]}在{row[1]}和{row[2]}内连续两天购买{row[3]},其单价{row[4]}，区域{row[5]}\n")

    db.close()
