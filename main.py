import time
from requests import get
from datetime import datetime
import math

def normal_round(n, decimals=0):
    expoN = n * 10 ** decimals
    if abs(expoN) - abs(math.floor(expoN)) < 0.5:
        return math.floor(expoN) / 10 ** decimals
    return math.ceil(expoN) / 10 ** decimals


def get_data(day):
    try:
        html = get(url=f"https://www.cboe.com/us/options/market_statistics/daily/?dt={day}")
    except:
        print("access site error!!!")

    time.sleep(5)

    htmltext = html.text
    htmlpoint = htmltext.find("<td>TOTAL PUT/CALL RATIO</td>")
    return htmltext[htmlpoint+  58 : htmlpoint + 62]
    
def get_values():
    fin = open("calendar.csv", "r")
    days = fin.readlines()
    fin.close()

    today = days.index(list(filter(lambda x: datetime.today().strftime("%Y-%m-%d") in x, days))[0])

    fout = open("putcallratio.txt", "a")

    for i in range(1, 227, 1):
        fout.write(get_data(list(days[i].split(";"))[1]) + ", " + str(days[i]))
        print(i)
    fout.close()

def yesterdays_value():
    today = datetime.today().strftime("%Y-%m-%d")
    f1 = open("putcallratio.txt", "r")
    f2 = open("calendar.csv", "r")
    f3 = open("all dates calendar.csv", "r")
    putcallratios = f1.readlines()
    tradingkalender = f2.readlines()
    kalender = f3.readlines()
    daybefore = list(kalender[kalender.index(list(filter(lambda x: today in x, kalender))[0]) - 1].split("\n"))[0]
    print(daybefore)
    if list(filter(lambda x: daybefore in x, tradingkalender)) == []:
        f1.close()
        f2.close()
        f3.close()
        print("1. case")
        return 0

    if len(list(filter(lambda x: daybefore in x, putcallratios))) > 0 or not list(filter(lambda x: today in x, putcallratios)) == []:
        print("already done!")
        f1.close()
        f2.close()
        f3.close()

    else:
        f1.close()
        f1 = open("putcallratio.txt", "a")
        f1.write("\n" + get_data(daybefore) + ", " + daybefore)
        f1.close()
        f2.close()
        f3.close()

def get_200_day_average():
    fin = open("putcallratio.txt", "r")
    fout = open("200_day_averages.txt", "a")
    putcallratioswdate = fin.readlines()
    fin.close()

    allratios = []
    for i in range(len(putcallratioswdate) - 1, len(putcallratioswdate) - 201, -1):
        allratios.append(float(list(putcallratioswdate[i].split(","))[0]))

    average = sum(allratios) / len(allratios)
    average = normal_round(average, 2)
    fout.write(str(average) + ", " + datetime.today().strftime("%Y-%m-%d") + "\n")
    fout.close()

def buy_sell():
    fbuyhold = open("buyholdsell.txt", "a")
    fvalue = open("putcallratio.txt", "r")
    faverage = open("200_day_averages.txt", "r")

    values = fvalue.readlines()
    averages = faverage.readlines()

    value1 = float(values[-1].split(",")[0])
    value2 = float(values[-2].split(",")[0])

    average = float(list(averages[-1].split(","))[0])

    day = datetime.today().strftime("%Y-%m-%d")

    if average * 1.15 <= value1:
        if average * 1.15 <= value2:
            fbuyhold.write(f"Buy: {average}: {value1}, {value2}; {day}")
            fbuyhold.close()
            fvalue.close()
            faverage.close()
            return f"Buy: {average}: {value1}, {value2}; {day}"
        else:
            fbuyhold.write(f"Watch tomorrow: {average}: {value1}, {value2}; {day}")
            fbuyhold.close()
            fvalue.close()
            faverage.close()
            return f"Watch tomorrow: {average}: {value1}, {value2}; {day}"

    elif average * 0.85 >= value1:
        if average * 0.85 >= value2:
            fbuyhold.write(f"Sell: {average}: {value1}, {value2}; {day}")
            fbuyhold.close()
            fvalue.close()
            faverage.close()
            return f"Sell: {average}: {value1}, {value2}; {day}"
        else:
            fbuyhold.write(f"Watch tomorow: {average}: {value1}, {value2}; {day}")
            fbuyhold.close()
            fvalue.close()
            faverage.close()
            return f"Watch tomorow: {average}: {value1}, {value2}; {day}"
    else:
        fbuyhold.write(f"Hold: {average}: {value1}, {value2}; {day}")
        fbuyhold.close()
        fvalue.close()
        faverage.close()
        return f"Hold: {average}: {value1}, {value2}; {day}"


def htmlout():
    fout = open("anlage.html", "w")
    action = buy_sell()
    print(action)
    fout.write(f"<!DOCTYPE html><body><h1>{action}</h1></body></html>")
    fout.close()

yesterdays_value()
get_200_day_average()
htmlout()