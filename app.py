from flask import Flask , render_template,request,redirect, url_for,send_file,session
from sample import *
import secrets
import string

        
app = Flask("__name__")

users = {
    'paresh': 'paresh03',
    'pareshjaiswal': 'paresh2002',
}


@app.route('/')
def index():
    return render_template("event_selection.html")

@app.route('/login_authentication',methods=['GET','POST'])
def login_authentication():
    error=None
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            return render_template("attributes.html")
        else:
            return 'Login failed. Invalid username or password.' 
               
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user', None)
    return render_template("event_selection.html")


@app.route('/attributes')
def attributes():
    return render_template("attributes.html")

@app.route('/donation_section')
def donation_section():
    return render_template("donations_section.html")

@app.route('/expense_section')
def expense_section():
    return render_template("expense_section.html")

@app.route('/expense', methods=['GET', 'POST'])
def expense():
    error = None
    if request.method == 'POST':
        ex_date=request.form['expense_date']
        details=request.form['item_name']
        qty=request.form['item_qty']
        expense_type=request.form['expense_type']
        amount=request.form['expense_amount']
        bill=request.form['bill_num']
        helper.insert_expenenditure(ex_date,details,qty,expense_type,amount, bill)
        print("done")
        return render_template("expense_reg.html",error=error)
    return render_template("expense_reg.html",error=error)
    
@app.route('/expense_list', methods=['GET', 'POST'])
def expense_list():
    data=helper.total_expenditure()
    return render_template("expense_table_show.html",data=data)


@app.route('/donation', methods=['GET', 'POST'])
def donation():
    error = None
    if request.method == 'POST':
        receipt_date = request.form['receipt_date']
        u_name = request.form['u_name']
        d_amount=request.form['d_amount']
        payment_type=request.form['payment_type']
        status=request.form['status']
        payment_date=request.form['payment_date']
        helper.insert_donation(receipt_date, u_name,d_amount,payment_type,status,payment_date)
        print('done')
        return render_template("donation_reg.html",error=error)
    return render_template("donation_reg.html",error=error)

@app.route('/summary_section', methods=['GET', 'POST'])
def summary_section():
    return render_template("summary.html")

@app.route('/summaryexpense', methods=['GET', 'POST'])
def summaryexpense():
    return render_template("sum_expense.html")

@app.route('/summarydonation', methods=['GET', 'POST'])
def summarydonation():
    return render_template("sum_donation.html")

@app.route('/donation_list', methods=['GET', 'POST'])
def donation_list():
    data=helper.total_donation()
    return render_template("table_show.html",data=data)
    
    
@app.route('/donation_cash', methods=['GET', 'POST'])
def donation_cash():
    data=helper.cash_paid()
    return render_template("table_show.html",data=data)
    

@app.route('/donation_upi', methods=['GET', 'POST'])
def donation_upi():
    data=helper.upi_paid()
    return render_template("table_show.html",data=data)
    

@app.route('/update_donation_table', methods=['GET', 'POST'])
def update_donation_table():
    data=helper.total_donation()
    return render_template("update_donation_table.html",data=data)

@app.route('/updateDonation', methods=['GET','POST'])
def updateDonation():
    receipt_number = request.args.get('receiptNumber')
    data=helper.get_update_donation(receipt_number)
    return render_template("update_donation_temp.html",data=data)

@app.route('/put_update_donation', methods=['GET', 'POST'])
def put_update_donation():
    error = None
    if request.method == 'POST':
        rece_num = request.form['rece_num']
        u_name = request.form['u_name']
        d_amount=request.form['d_amount']
        payment_type=request.form['payment_type']
        status=request.form['status']
        payment_date=request.form['payment_date']
        helper.put_update_donation(rece_num,u_name,d_amount,payment_type,status,payment_date)
        print('done')
        return render_template("update_donation_temp.html",error=error)
    return render_template("update_donation_temp.html",error=error)


@app.route('/donation_balance', methods=['GET', 'POST'])
def donation_balance():
    data=helper.balance()
    return render_template("table_show.html",data=data)
    
@app.route('/amount_available', methods=['GET', 'POST'])
def amount_available():
    data=helper.amount_paid()
    return render_template("amount_display.html",data=data)

@app.route('/amount_expended', methods=['GET', 'POST'])
def amount_expended():
    data=helper.amount_expended()
    return render_template("amount_display.html",data=data)

@app.route('/funds_details', methods=['GET', 'POST'])
def funds_details():
    data1=helper.amount_paid()
    data2=helper.amount_expended()
    r=data1[0]
    r=int(r[0])
    e=data2[0]
    e=int(e[0])
    a=r-e
    data=(e,r,a)
    return render_template("funds_display.html",data=data)

@app.route('/database_view', methods=['GET', 'POST'])
def database_view():
    data1=helper.total_donation()
    data2=helper.total_expenditure()
    data=(data1,data2)
    return render_template("database_view.html",data=data)

@app.route('/download_excel', methods=['GET', 'POST'])
def download_excel():
    helper.convert_to_excel()
    return render_template("download_excel.html")

@app.route('/convert_excel')
def convert_excel():
    excel_file = 'static/event_database.xlsx'
    return send_file(excel_file, as_attachment=True)

@app.route('/donation_table_download')
def donation_table_download():
    helper.download_specific_table('donations')
    return render_template("download_donation_table.html")

@app.route('/expense_table_download')
def expense_table_download():
    helper.download_specific_table('expenditure')
    return render_template("download_expense_table.html")

@app.route('/convert_excel_expenditure')
def convert_excel_expenditure():
    excel_file = 'static/expenditure.xlsx'
    return send_file(excel_file, as_attachment=True)

@app.route('/convert_excel_donation')
def convert_excel_donation():
    excel_file = 'static/donations.xlsx'
    return send_file(excel_file, as_attachment=True)

@app.route('/category_display')
def category_display():
    return render_template("expense_category.html")

@app.route('/maintainance_expense_list', methods=['GET', 'POST'])
def maintainance_expense_list():
    data=helper.maintenance_expense()
    return render_template("expense_table_show.html",data=data)

@app.route('/pooja_expense_list', methods=['GET', 'POST'])
def pooja_expense_list():
    data=helper.pooja_expense()
    return render_template("expense_table_show.html",data=data)

@app.route('/decoration_expense_list', methods=['GET', 'POST'])
def decoration_expense_list():
    data=helper.decoration_expense()
    return render_template("expense_table_show.html",data=data)

@app.route('/cultural_expense_list', methods=['GET', 'POST'])
def cultural_expense_list():
    data=helper.cultural_expense()
    return render_template("expense_table_show.html",data=data)

@app.route('/procession_expense_list', methods=['GET', 'POST'])
def procession_expense_list():
    data=helper.procession_expense()
    return render_template("expense_table_show.html",data=data)

@app.route('/other_expense_list', methods=['GET', 'POST'])
def other_expense_list():
    data=helper.other_expense()
    return render_template("expense_table_show.html",data=data)

@app.route('/home_page')
def home_page():
    return render_template("attributes.html")

@app.route('/category_expense_download')
def category_expense_download():
    #helper.download_specific_table_data('expenditure','maintenance_expense')
    helper.download_specific_table_data('expenditure','pooja_expense')
    helper.download_specific_table_data('expenditure','decoration_expense')
    helper.download_specific_table_data('expenditure','cultural_expense')
    helper.download_specific_table_data('expenditure','procession_expense')
    helper.download_specific_table_data('expenditure','other_expense')
    return render_template("expense_categories_download.html")

@app.route('/maintainance_expense_table_download')
def maintainance_expense_table_download():
    excel_file = 'static/maintenance_expense.xlsx'
    return send_file(excel_file, as_attachment=True)

@app.route('/pooja_expense_table_download')
def pooja_expense_table_download():
    excel_file = 'static/pooja_expense.xlsx'
    return send_file(excel_file, as_attachment=True)

@app.route('/decoration_expense_table_download')
def decoration_expense_table_download():
    excel_file = 'static/decoration_expense.xlsx'
    return send_file(excel_file, as_attachment=True)

@app.route('/cultural_expense_table_download')
def cultural_expense_table_download():
    excel_file = 'static/cultural_expense.xlsx'
    return send_file(excel_file, as_attachment=True)

@app.route('/procession_expense_table_download')
def procession_expense_table_download():
    excel_file = 'static/procession_expense.xlsx'
    return send_file(excel_file, as_attachment=True)

@app.route('/other_expense_table_download')
def other_expense_table_download():
    excel_file = 'static/other_expense.xlsx'
    return send_file(excel_file, as_attachment=True)

if __name__ == '__main__':
    secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
    app.secret_key = secret_key
    app.debug = True
    app.run()