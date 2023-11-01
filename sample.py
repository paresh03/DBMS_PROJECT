import mysql.connector as connector
import pandas as pd
import os
from openpyxl import Workbook
class dbhelp:
    def __init__(self):
        self.con=connector.connect(host='localhost', port='3306', user='root',password='root',database='dbms_project',auth_plugin='mysql_native_password')

    def create_table(self,query):
        
        cur=self.con.cursor()
        cur.execute(query)
        print('created')

   
    def insert_donation(self, receipt_date, u_name,amount,payment_type,status,payment_date):
        query="insert into donations(receipt_date, u_name,amount,payment_type,status,payment_date) values('{}','{}',{},'{}','{}','{}')".format( receipt_date, u_name,amount,payment_type,status,payment_date)
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
    
    def insert_expenenditure(self,ex_date,details,qty,expense_type,amount, bill):
        query="insert into expenditure(ex_date,details,qty,expense_type, amount, bill) values('{}','{}','{}','{}',{},'{}')".format(ex_date,details,qty,expense_type,amount, bill)
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        
    def total_donation(self):
        cur=self.con.cursor()
        cur.execute("select * from donations")
        data = cur.fetchall()
        return data
        
    def upi_paid(self):
        cur=self.con.cursor()
        cur.execute("select * from donations where payment_type='UPI' AND status='PAID'")
        data = cur.fetchall()
        return data
            
    def cash_paid(self):
        
            cur=self.con.cursor()
            cur.execute("select * from donations where payment_type='CASH' AND status='PAID'")
            data = cur.fetchall()
            return data
    
    def balance(self):   
        
            cur=self.con.cursor()
            cur.execute("select * from donations where status='BALANCE'")
            data = cur.fetchall()
            return data
    
    def amount_paid(self):
        
            cur=self.con.cursor()
            cur.execute("select sum(amount) from donations where status='PAID'")
            data = cur.fetchall()
            return data
        
    def amount_expended(self):
            cur=self.con.cursor()
            cur.execute("select sum(amount) from expenditure")
            data = cur.fetchall()
            return data
        
    """ def funds_details(self):
            cur=self.con.cursor()
            cur.execute("select sum(amount) from donations where status='PAID'")
            received= cur.fetchall()
            cur.execute("select sum(amount) from expenditure")
            expended = cur.fetchall()
            data=1
            return [received,expended,data]"""
        
    def convert_to_excel(self):
        cur=self.con.cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        wb=Workbook()
        excel_writer = pd.ExcelWriter("static/event_database.xlsx", engine="openpyxl")
        for table in tables:
            table_name = table[0]
            # Fetch data from the table into a DataFrame
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.con)
            # Write the DataFrame to the Excel file
            df.to_excel(excel_writer, sheet_name=table_name, index=False)

        #Save the Excel file
        wb.save(filename="event_database.xlsx")

    def download_specific_table(self,table_name):
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, self.con)
        static_folder='static'
        excel_file_path = os.path.join(static_folder, f'{table_name}.xlsx')
        df.to_excel(excel_file_path, index=False)
        print(f"Data from '{table_name}' table has been exported to '{excel_file_path}'")
        
    def download_specific_table_data(self,table_name,Expense_type):
        query = f"SELECT * FROM {table_name} where expense_type = '{Expense_type}'"
        df = pd.read_sql(query, self.con)
        static_folder='static'
        excel_file_path = os.path.join(static_folder, f'{Expense_type}.xlsx')
        df.to_excel(excel_file_path, index=False)
        print(f"Data from '{Expense_type}' table has been exported to '{excel_file_path}'")
        
    def total_expenditure(self):
            cur=self.con.cursor()
            cur.execute("select * from expenditure" )
            data = cur.fetchall()
            return data
    
          
    def maintenance_expense(self):
            cur=self.con.cursor()
            cur.execute("select * from expenditure where expense_type='maintenance_expense'" )
            data = cur.fetchall()
            return data
        
    def pooja_expense(self):
            cur=self.con.cursor()
            cur.execute("select * from expenditure where expense_type='pooja_expense'" )
            data = cur.fetchall()
            return data
        
    def decoration_expense(self):
            cur=self.con.cursor()
            cur.execute("select * from expenditure where expense_type='decoration_expense'" )
            data = cur.fetchall()
            return data
    
    def cultural_expense(self):
            cur=self.con.cursor()
            cur.execute("select * from expenditure where expense_type='cultural_expense'" )
            data = cur.fetchall()
            return data  
        
    def procession_expense(self):
            cur=self.con.cursor()
            cur.execute('select * from expenditure where expense_type="procession_expense"' )
            data = cur.fetchall()
            return data  
        
    def other_expense(self):
            cur=self.con.cursor()
            cur.execute("select * from expenditure where expense_type='other_expense'" )
            data = cur.fetchall()
            return data
    
    def get_update_donation(self,receipt_num):
            cur=self.con.cursor()
            cur.execute(f"select * from donations where receipt_number = {receipt_num}")
            data = cur.fetchall()
            return data
    
    def put_update_donation(self,rece_num,u_name,d_amount,payment_type,status,payment_date):
            cur=self.con.cursor()
            cur.execute(f"UPDATE donations SET u_name = '{u_name}', amount = {d_amount}, payment_type = '{payment_type}' , status='{status}',payment_date='{payment_date}' WHERE receipt_number={rece_num} ")
            self.con.commit()
            
            """def truncate(self):
        query="truncate table donations"
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()"""
        
#main coding

helper=dbhelp()
query1='create table if not exists donations(receipt_number int NOT NULL AUTO_INCREMENT primary key,receipt_date date, u_name varchar(255),amount int,payment_type varchar(255),status varchar(255),payment_date date)'
 
query2='create table if not exists expenditure(sr_no int NOT NULL AUTO_INCREMENT primary key,ex_date date,details varchar(255),qty varchar(25), expense_type varchar(255),amount int , bill varchar(255))'
helper.create_table(query1)
helper.create_table(query2)
#helper.truncate()

