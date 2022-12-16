from flask import Flask, request, jsonify, render_template,url_for
from flask_cors import CORS
import sqlite3
app = Flask(__name__)

DB_PATH = "network_visualizer.db"


@app.route("/update", methods=['POST'])
def new_entry():
    netname = request.values.get("netname")
    numpresent = request.values.get("numpresent")
    zone = request.values.get("zone")
    # if color is not None and color != "":
    update_db((netname,numpresent,zone))
    # unread = get_unread(msg_from)
    # ids = unread.keys()
    # read_ids(ids)
    # return jsonify(unread)

@app.route("/view", methods=['GET'])
def view_updates():
    url_for('static', filename='rect.css')
    zones = {"z1a": False, "z2a": False, "z3a": False, "z1b": False, "z2b": False, "z3b": False}
    db_vals = read_db()
    for net in db_vals:
        if net[0] == 1:
            zoneName = "a"
        else:
            zoneName = "b"
        for znum in net[2]:
            key = "z"+znum+zoneName
            zones[key] = True
    print(zones)
    return render_template("vis.html", **zones)

def read_db():
    conn, c = connect()
    c.execute(
        "SELECT * FROM {tn}".format(tn="occupancy_map"))
    unread_messages = c.fetchall()
    disconnect(conn)
    return unread_messages

def connect():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    return conn, c


def disconnect(conn):
    conn.close()

def update_db(content):
    conn, c = connect()
    nn,np,z = (content)

    c.execute(
        "UPDATE {tn} SET ({np},{z})=(?,?) WHERE {nn}=(?)".format(tn="occupancy_map",nn="netname",
                                 np='numpresent',
                                 z='zone'), [np,z,nn])
    conn.commit()
    disconnect(conn)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5002)
