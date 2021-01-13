from flask import Flask, request, render_template
from utils.coordinates import (
    get_coordinates,
    LocationUnknownException,
    LocationNotInNyException,
)
from utils.NYCMapManager import NYCMapManager
from utils.NYCRouteManager import NYCRouteManager
import os


app = Flask(__name__, template_folder=".")
route_manager = NYCRouteManager()
map_manager = NYCMapManager()


@app.route("/")
def hello():
    """Display the home page"""
    return render_template("default.html", title="Home")


@app.route("/navigate", methods=["POST"])
def login():
    """Get the coordinates from adrress"""

    from_address = request.form["from_address"]
    to_address = request.form["to_address"]
    route_types = ["safest"]
    route_types.extend(request.form.getlist("type"))

    try:
        start_location = get_coordinates(from_address)
        end_location = get_coordinates(to_address)

        routes = route_manager.get_routes(start_location, end_location, route_types)
        data = map_manager.get_map(from_address, to_address, routes=routes)

        return render_template("default.html", title="Navigation", data=data)
        # return render_template("default.html", title="Navigation", start_location=start_location, end_location=end_location)
    except LocationUnknownException:
        return render_template(
            "default.html", title="Navigation : Error", data="Unknown address"
        )
    except LocationNotInNyException:
        return render_template(
            "default.html", title="Navigation : Error", data="Address not in New York"
        )
    except Exception as err:
        msg = f"Error : {err}"
        return render_template("default.html", title="Navigation : Error", data=msg)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
