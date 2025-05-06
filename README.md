Inventory Management System

A simple inventory tracking web application built using Flask and MySQL.

Features

- Manage products, stock, and locations
- Track inventory movements
- Dashboard UI with HTML templates
- Flask backend with MySQL database

## Tech Stack

- Python 3
- Flask
- MySQL
- HTML 

## Project Structure

inventory-system/
├── app.py
├── templates/
│ ├── dashboard.html
│ ├── locations.html
│ ├── movements.html
│ ├── products.html
│ └── stock.html


Local Setup

1. Clone the Repository
   
git clone https://github.com/your-username/inventory-system.git

cd inventory-system

2. Create Virtual Environment
   
python -m venv venv

venv\Scripts\activate

3. Install Dependencies

pip install flask mysql-connector-python

4.Set Up MySQL

CREATE DATABASE inventory_db;
CREATE USER 'root'@'localhost' IDENTIFIED BY 'mani';
GRANT ALL PRIVILEGES ON inventory_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

5. Run the Application

python app.py


Visit http://localhost:5000 to access the app.

ScreenShots
1.
![image](https://github.com/user-attachments/assets/cab221fc-91a5-437d-b370-8faf7d62c006)
2.
![image](https://github.com/user-attachments/assets/e0ef6cb1-50c1-4458-b8ee-3bed9b3b97b5)
3.
![image](https://github.com/user-attachments/assets/701d3002-976c-437f-865e-0552b50aebd8)
4.
![image](https://github.com/user-attachments/assets/bc28a83d-d89a-4335-8e57-3713c8f8c5aa)
5.
![image](https://github.com/user-attachments/assets/69796f6a-6e3b-4e9c-a843-f52097b762f3)


