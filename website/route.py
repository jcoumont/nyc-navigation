from flask import Flask, request, render_template
from utils.coordinates import get_coordinates, LocationUnknownException, LocationNotInNyException
from utils.map import get_map
from utils.NYCRouteManager import NYCRouteManager
import os


app = Flask(__name__, template_folder=".")
route_manager = NYCRouteManager()

@app.route("/")
def hello():
    """Display the home page
    """
    return render_template("default.html", title="Home")



@app.route("/navigate", methods=["POST"])
def login():
    """Get the coordinates from adrress
    """

    from_address = request.form['from_address']
    to_address = request.form['to_address']

    try:
        start_location = get_coordinates(from_address)
        end_location = get_coordinates(to_address)

        route = route_manager.get_safest_route(start_location, end_location)
        data = get_map(start_location, end_location, route=route)
        return render_template("default.html", title="Navigation",data=data)
        # return render_template("default.html", title="Navigation", start_location=start_location, end_location=end_location)
    except LocationUnknownException:
        return render_template("default.html", title="Navigation : Error", data="Unknown address")
    except LocationNotInNyException:
        return render_template("default.html", title="Navigation : Error", data="Address not in New York")
    except Exception:
        return render_template("default.html", title="Navigation : Error", data="Error!")



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
