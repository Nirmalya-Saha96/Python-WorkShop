from flask import Flask, request
from uuid import uuid1,uuid4
import os,json,pytz
from datetime import date,datetime

db={}
db_filename = "db.json"

#Check whether db.json exists in the directory or not

if os.path.exists(db_filename):
    with open(db_filename,'r') as f:
        db = json.load(f)
else:
    accessKey = str(uuid1())
    secretKey = str(uuid4())

    item_types = [
        "Food","Beverages","Clothing","Stationaries",
        "Wearables","Electronics Accessories"
    ]

    db={
        "accessKey": accessKey,
        "secretKey": secretKey,
        "item_types": item_types,
        "users": []
    }

    with open(db_filename,"w+") as f:
        json.dump(db,f,indent=4)

app = Flask(__name__)


#User sign up
@app.route('/signup',methods = ['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        user = {
            "name": name,
            "email": email,
            "password": password,
            "username": username,
            "purchases":{}
        }

        emailList = []
        for item in db['users']:
            emailList.append(item['email'])

        if(len(db['users'])==0 or user not in db['users']):
            if(user['email'] not in emailList):
                db['users'].append(user)
                with open(db_filename,"r+") as f:
                    f.seek(0)
                    json.dump(db,f,indent=4)

                return {
                        "status": "success",
                        "msg": "User created successfully",
                        "user": user
                    }
            else:
                return {
                    "status": "fail",
                    "error_code": 404,
                    "error_message": "User already exists"
                }  
        return {
                    "status": "fail",
                    "error_code": 404,
                    "error_message": "User already exists"
                }

    else:
        return {
            "status": "fail",
            "error_code": 500,
            "error_message": "Error: Trying to access endpoint with wrong method"
        }

#User login
@app.route('/login', methods=['POST'])
def login():
    if(request.method == 'POST'):
        email = request.form['email']
        password = request.form['password']
        err_msg = ""
        response = {}

        for user in db['users']: 
            if(user['email'] == email and user['password'] == password):
                current_user = user
                response = {
                    "status": "success",
                    "msg": "User Logged In Successfuly",
                    "user": current_user,
                    "user_idx": db['users'].index(current_user) 
                }
                return response
            elif(user['email'] != email and user['password'] == password):
                err_msg = "Email incorrect"
            elif(user['email'] == email and user['password'] != password):
                err_msg = "Password incorrect"
            else: 
                err_msg = "Incorrect credentials"

        response = {
            "status": "fail",
            "error_code": 404,
            "error_message": err_msg
        }
        return response
    else:
        return {
            "status": "fail",
            "error_code": 500,
            "error_message": "Error: Trying to access endpoint with wrong method"
        }

#User purchase add
@app.route('/user/purchase', methods=['POST'])
def addPurchase():
    if(request.method == 'POST'):
        user_idx = int(request.form['user_idx'])
        item_type = request.form['item_type']
        item_name = request.form['item_name']
        item_price = request.form['item_price']
        user = db['users'][user_idx]
        curr_date = str(date.today())
        curr_time = str(datetime.now(pytz.timezone("Asia/Kolkata")))

        purchase_dates = list(db['users'][user_idx]['purchases'].keys())

        purchaseObj = {
            "item_type": item_type,
            "item_name": item_name,
            "item_price": item_price,
            "purchase_time": curr_time
        }

        if(curr_date in purchase_dates):
            db['users'][user_idx]['purchases'][curr_date].append(purchaseObj)
            with open(db_filename, 'r+') as f:
                f.seek(0)
                json.dump(db, f, indent=4)

            return {
                "status": "success",
                "status_code": 200, 
                "user": db['users'][user_idx],
                "msg": "Purchase added successfully"
            }  
        else:
            db['users'][user_idx]['purchases'][curr_date] = []
            db['users'][user_idx]['purchases'][curr_date].append(purchaseObj)
            with open(db_filename, 'r+') as f:
                f.seek(0)
                json.dump(db, f, indent=4)

            return {
                "status": "success",
                "status_code": 200, 
                "user": db['users'][user_idx],
                "msg": "Purchase added successfully"
            }  

    else:
        return {
            "status": "fail",
            "error_code": 500,
            "error_message": "Error: Trying to access endpoint with wrong method"
        }      






if __name__ == "__main__":
    app.run(host='127.0.0.1',port='3000',debug = True)

