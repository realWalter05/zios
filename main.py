from flask import Flask, render_template, request
from scraper import Scraper
import json

app = Flask(__name__)

@app.route("/",)
def index():
    print("here")   

    json_file = read_json("links.json")
    spoje = get_spoje()

    for spoj in spoje:
        if spoj[0][1] not in json_file:
            spoje.remove(spoj)
        
    return render_template("index.html", spoje=spoje, details=json_file)

def read_json(file):
    with open(file, "r", encoding="utf-8") as json_text:
        return json.load(json_text)

def get_spoje():
    spoje = []
    links = open('links.txt', 'r')
    lines = links.readlines()

    for line in lines:
        spoj = Scraper(line).data
        spoje.append(spoj)

    return spoje

if __name__ == "__main__":
    app.run(debug=True)
