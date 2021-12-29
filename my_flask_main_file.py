"""
    Homyzz (Home Inventory Management)

    author: Gurleen Kaur Jhajj
    date: 14th Sep,21

    [Includes Templates directory having html files]
    [Uses mongoDB database and data science.]
"""

from flask import *
from my_mongoDB_database import DB
import hashlib
import os
import data_science_homyzz

email = ""

app = Flask(__name__)
my_db = DB()

app.secret_key = os.urandom(24)


@app.route("/")
def index():
    return render_template("index_.html")


@app.route("/about_")
def about():
    return render_template("about_.html")


@app.route("/contact_")
def contact():
    return render_template("contact_.html")


@app.route("/about2_")
def about2():
    return render_template("about2_.html")


@app.route("/contact2_")
def contact2():
    return render_template("contact2_.html")


@app.route("/register_")
def register():
    return render_template("register_.html")


@app.route("/register_and_save_", methods=["POST"])
def register_user_and_save_in_db():
    my_user = {
        "name": request.form['uname'],
        "email": request.form['email'],
        "password": request.form['password'],
        "income details": []
    }
    my_user['password'] = hashlib.sha256(my_user['password'].encode()).hexdigest()
    print(my_user)
    my_db.insert_operation(collection="my_app", document=my_user)
    return render_template("success_.html", message="Registered Successfully")


@app.route("/login_")
def login():
    return render_template("login_.html")


@app.route("/auth_", methods=["POST"])
def authenticate_user():
    user = {
        "email": request.form['email'],
        "password": request.form['password']
    }
    global email
    email = user['email']
    user['password'] = hashlib.sha256(user['password'].encode()).hexdigest()
    query = {"email": user['email'], "password": user['password']}
    documents = my_db.validate_document_in_collection('my_app', query=query)
    print(documents.count())

    if documents.count() == 1:
        return render_template("home_.html", email=user["email"])
    else:
        return render_template("error_.html", message="Invalid Credentials")


@app.route("/manage_transactions_")
def manage_transactions():
    return render_template("manage_transactions_.html")


@app.route("/information_")
def information():
    return render_template("information_.html")


@app.route("/saving_income_", methods=["POST"])
def saving_income():
    income_details = {
        "income": request.form['income'],
        "source": request.form['source'],
        "savings": request.form['savings'],
        "emergency": request.form['emergency'],
        "date": request.form['date']
    }
    my_query = {"email": email}

    print(my_query)
    documents = my_db.fetch_document_for_my_app(collection_name="my_app", query=my_query)
    for doc in documents:
        result_dict = doc
    print(result_dict)
    income_list_temp = []
    if len(result_dict["income details"]) != 0:
        for dictionaries in result_dict["income details"]:
            income_list_temp.append(dictionaries)
    income_list_temp.append(income_details)
    print("result_dict[income details]:", result_dict["income details"])
    result_dict["income details"] = income_list_temp
    my_db.update_document_for_my_app(collection_name="my_app", email=email, document=result_dict)

    return render_template("success2_.html", message="Income Details saved successfully.")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.route('/logout_')
def logout():
    session.pop('user', None)
    return render_template("index_.html")


@app.route("/user_")
def fetch_user():
    my_query = {"email": email}
    user = my_db.fetch_document_for_my_app(collection_name="my_app", query=my_query)
    for info in user:
        user_info = info
    print(user_info)
    income_list = []
    if len(user_info["income details"]) != 0:
        for dictionaries in user_info["income details"]:
            income_list.append(dictionaries)
    print("result_dict[income details]:", user_info["income details"])

    return render_template("user_.html", user_info=user_info["income details"])


@app.route("/expenditure_")
def expenditure():
    my_query = {"email": email}
    user = my_db.fetch_document_for_my_app(collection_name="my_app", query=my_query)
    for info in user:
        user_info = info
    print(user_info)
    income_list = []
    income = []
    savings = []
    emergency = []
    date = []
    if len(user_info["income details"]) != 0:
        for dictionaries in user_info["income details"]:
            income_list.append(dictionaries)
    print("result_dict[income details]:", user_info["income details"])
    for info in user_info["income details"]:
        for key, value in info.items():
            if key == "income":
                print(value)
                if "," in value:
                    value = value.replace(",", "")
                income.append(int(value))
            elif key == "savings":
                if "," in value:
                    value = value.replace(",", "")
                savings.append(int(value))
            elif key == "emergency":
                if "," in value:
                    value = value.replace(",", "")
                emergency.append(int(value))
            elif key == "date":
                date.append(value)
    expenditure = []
    for i in range(len(income)):
        expend = income[i] - (savings[i] + emergency[i])
        expenditure.append(expend)

    data_science_homyzz.plot_expenditure(expenditure, date)

    return render_template("expenditure_.html", user_info_expend=expenditure, user_info_date=date, num=len(income))


@app.route("/data_science_homyzz_")
def data_science():
    my_query = {"email": email}
    user = my_db.fetch_document_for_my_app(collection_name="my_app", query=my_query)
    for info in user:
        user_info = info
    print(user_info)
    income_list = []
    if len(user_info["income details"]) != 0:
        for dictionaries in user_info["income details"]:
            income_list.append(dictionaries)
    print("result_dict[income details]:", user_info["income details"])
    data_science_homyzz.data_science(user_info["income details"])

    return render_template("data_science_homyzz_.html")


def main():
    app.run()


if __name__ == '__main__':
    main()
