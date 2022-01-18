from flask import Flask, render_template, request, jsonify
from path_generator import PathGenerator
from road_network.base_classes import Point
import os

app = Flask(__name__)
pg = PathGenerator()


@app.route("/", methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")


@app.route("/map", methods=["GET"])
def show_coords():
    lat = float(request.args["lat"])
    lon = float(request.args["lon"])
    pg.generate_path(200, Point(lon, lat))
    # pg.plot_path()
    res = jsonify([[p.lat, p.lng] for p in pg.cur_path.points])
    return res


if __name__ == "__main__":
    app.run(port=os.environ.get("PORT", 80))
