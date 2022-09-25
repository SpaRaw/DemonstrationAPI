from flask import Flask, render_template, request, redirect, flash
from flask_cors import CORS
import sqlite3
import secrets



app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret
CORS(app)

IN_MEMORY_ORDER = 1
IN_MEMORY_ORDER_OPTIONS_COLOUMS ={
    1: "ORDER BY id",
    2: "ORDER BY prio",
    3: "ORDER BY time"
}
IN_MEMORY_ORDER_OPTIONS_DIR = " ASC"


@app.route('/')
def main():
    print(IN_MEMORY_ORDER)
    connection = sqlite3.connect("ticket.db")
    cursor = connection.cursor()
    all_elements_open = cursor.execute("SELECT * FROM ticket where status = 0 " + IN_MEMORY_ORDER_OPTIONS_COLOUMS[IN_MEMORY_ORDER] + IN_MEMORY_ORDER_OPTIONS_DIR)
    tuple_of_open_elements = all_elements_open.fetchall()
    connection.commit()
    all_elements_closed = cursor.execute("SELECT * FROM ticket where status = 1 "+ IN_MEMORY_ORDER_OPTIONS_COLOUMS[IN_MEMORY_ORDER] + IN_MEMORY_ORDER_OPTIONS_DIR)
    tuple_of_closed_elements = all_elements_closed.fetchall()

    list_of_closed_elements = []
    list_of_open_elements = []

    for element in tuple_of_closed_elements:
        list_of_closed_elements.append(list(element))

    for element in tuple_of_open_elements:
        list_of_open_elements.append(list(element))

    connection.close()
    return render_template('demo.html', list_of_open=list_of_open_elements, list_of_close=list_of_closed_elements)


@app.route("/api/endpoints/", methods=["POST"])
def api_endpoints():
    connection = sqlite3.connect("ticket.db")
    cursor = connection.cursor()

    print(request.form.get('button'))
    if request.form.get('button') == 'POST-Request':
        prio = request.form.get('prio')
        data = request.form.get('data')
        time = request.form.get('time')

        if prio == "":
            prio = 10
        if data == "":
            data = "No data available, POST request was empty"
        if time == "":
            time = 999

        information = (prio, data, time, 0)

        cursor.execute("insert into ticket (prio, data, time, status) values (?, ?, ?, ?)", information)

    elif request.form.get('button') == "GET-Request":
        print("get")
        element = cursor.execute("SELECT * FROM ticket where status = 0")
        id = -1
        response = ""
        try:
            index, prio, data, zeit, status, time = element.fetchone()
        except TypeError:
            index, prio, data, zeit, status, time=(-1, -1, "NO OPEN TASK", -1, -1, -1)

        cursor.execute("update ticket set status = 1 where id = "+str(index))

        return_json = {
            "index": index,
            "prio": prio,
            "data": data,
            "zeit": zeit,
            "status": status,
            "time": time
        }


        flash(return_json)


    connection.commit()
    connection.close()

    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True)