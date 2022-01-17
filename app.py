from flask import Flask, url_for, render_template, request, jsonify
from path_generator import PathGenerator
from road_network.base_classes import Point

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")


@app.route("/map", methods=["GET"])
def show_coords():
    print("fetch request acquired")
    lat = float(request.args["lat"])
    lon = float(request.args["lon"])
    pg = PathGenerator(Point(lat=lat, lon=lon))
    pg.generate_path(100)
    # pg.plot_path()
    res = jsonify([[p.lat, p.lon] for p in pg.cur_path.points])
    return res


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
