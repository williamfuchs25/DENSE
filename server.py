# flask --app data_server run
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import json


app = Flask(__name__, static_url_path="", static_folder="static")


@app.route("/")
def index():
    return redirect("/about", code=302)




@app.route("/about")
def about():
    f = open("data/data.json", "r")
    data = json.load(f)
    f.close()
    states = []
    for st in data.keys():
        if st != "US-TOTAL":
            states.append(st)
    return render_template("about.html", states=states)

@app.route("/macro")
def macro():
    dict = {}
    f = open("data/data.json", "r")
    data = json.load(f)
    f.close()
    min = 10000000000
    for key in data.keys():
        if len(key) == 2:
            dict[key] = data[key]["Total"]
            if data[key]["Total"] < min:
                min = data[key]["Total"]
    states = []
    for st in data.keys():
        if st != "US-TOTAL":
            states.append(st)
            
    return render_template("macro.html", states=states, dict=dict)

@app.route("/micro")
def micro():
    f = open("data/data.json", "r")
    data = json.load(f)
    f.close()
    state = request.args.get("state")
    types = data[state].keys()
    sources = []
    vals = []
    for key in types:
        if key != "Total":
            vals.append(data[state][key])
            sources.append(key)
    total = data[state]["Total"]
    usTypes = data["US-TOTAL"].keys()
    usSources = []
    usVals = []
    states = []
    for st in data.keys():
        if st != "US-TOTAL":
            states.append(st)
    for key in usTypes:
        if key != "Total":
            usVals.append(data["US-TOTAL"][key] / 50)
            usSources.append(key)
    usTotal = data["US-TOTAL"]["Total"] / 50
    comp = ""
    if total < usTotal:
        comp = "less"
    else:
        comp = "more"
    return render_template("micro.html", sources=sources, vals=vals, state=state, total=total, usTypes=usTypes, usSources = usSources, usVals=usVals, usTotal=usTotal, states=states, comp=comp)

app.run(debug=True)
