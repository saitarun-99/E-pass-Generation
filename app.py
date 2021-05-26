import requests
from flask import Flask, render_template, request
from twilio.rest import Client
import requests_cache
account_sid = "AC29d89daf4e081330767699a51a38b6fa"
auth_token = "c2415a9dd94367e2c266f8fbebe7685d"
client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')
@app.route('/')
def registration_form():
    return render_template('test_page.html')

@app.route('/login_page', methods=['POST','GET'])
def login_reg_details():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source-state']
    source_dt = request.form['source-dt']
    dest_st = request.form['dest-st']
    dest_dt = request.form['dest-dt']
    pno = request.form['pno']
    #id_proof = request.form['id-proof']
    date = request.form['trip']
    full_name = first_name+" "+last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[dest_st]['districts'][dest_dt]['total']['confirmed']
    pop = json_data[dest_st]['districts'][dest_dt]['meta']['population']
    travel_pass = ((cnt/pop)*100)
    if(travel_pass< 45) and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to="whatsapp:+91"+pno,
                               from_="whatsapp:+14155238886",
                               body="Hello "+full_name+" "+"Your Travel From "+" "+source_dt+" To "+dest_dt+" is "+ status+" "+" "+date+",")
        return render_template('user_reg_details.html', var=full_name , var1=email_id,
                                var3=source_st,var4=source_dt,var5=dest_st,var6=dest_dt,
                               var7=pno,var8=date,var9=status) #var2=id_proof,
    else:
        status="Not Confirmed"
        client.messages.create(to="whatsapp:+919177289491",
                               from_="whatsapp:+14155238886",
                               body="Hello " + full_name + " " + "Your")
        return render_template('user_reg_details.html', var=full_name, var1=email_id,
                                var3=source_st, var4=source_dt, var5=dest_st, var6=dest_dt,
                               var7=pno, var8=date, var9=status) #var2=id_proof,





if __name__ == '__main__':
    app.run(port=3011,debug=True)