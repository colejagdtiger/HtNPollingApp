# main app file

from flask import Flask, render_template, request, jsonify, make_response, redirect
from database import create_connection, select_all_items, update_item
from flask_cors import CORS, cross_origin
from pusher import Pusher
import simplejson
import os
import string
import random

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# configure pusher object
pusher = Pusher(
    app_id="1139320",
    key="4ac52c799ded4e369788",
    secret=os.getenv("PUSHER_SECRET"),
    cluster="us2",
    ssl=True,
)

database = "./pythonsqlite.db"
conn = create_connection(database)
c = conn.cursor()


def main():
    global conn, c


@app.route("/")
def index():
    poll_id = request.args.get("pollid")
    if not poll_id:
        # generate a new poll ID
        new_poll_id = "".join(random.choice(string.ascii_letters) for _ in range(8))
        print("New poll ID: ", new_poll_id)
        return redirect("/?pollid={0}".format(new_poll_id))

    return render_template("index.html")


@app.route("/polls", methods=["POST"])
def publish():
    data = simplejson.loads(request.data)
    print(data)
    return jsonify({"pollurl": "/polls/{0}".format(data["poll_id"])})


@app.route("/polls/<pollid>", methods=["GET"])
def poll(pollid):
    return render_template("poll.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/vote", methods=["POST"])
def vote():
    data = simplejson.loads(request.data)
    update_item(c, [data["member"]])
    output = select_all_items(c, [data["member"]])
    pusher.trigger(u"poll", u"vote", output)
    return request.data


if __name__ == "__main__":
    main()
    app.run(debug=True)
