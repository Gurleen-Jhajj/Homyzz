"""
    Data Science code for Homyzz

    author: Gurleen Kaur Jhajj
    date: 14th Sep,21

"""
import matplotlib.pyplot as plt

income = []
savings = []
emergency = []
date = []


def data_science(user_info):
    for info in user_info:
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

    plt.bar(date, income)
    plt.xlabel("Dates")
    plt.ylabel("Income")
    plt.show()
    plt.bar(date, savings)
    plt.xlabel("Dates")
    plt.ylabel("Savings")
    plt.show()
    plt.bar(date, emergency)
    plt.xlabel("Dates")
    plt.ylabel("Emergency")
    plt.show()


def plot_expenditure(expend, date):
    plt.bar(date, expend)
    plt.xlabel("Dates")
    plt.ylabel("Expenditure")
    plt.show()
