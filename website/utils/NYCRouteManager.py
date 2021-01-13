import osmnx as ox
import networkx as nx

from os import path


def download_osm(query="New York City, New York, USA", network_type="drive"):
    """
    Create graph from OSM within the boundaries of some geocodable place(s).

    The query must be geocodable and OSM must have polygon boundaries for the
    geocode result. If OSM does not have a polygon for this place, you can
    instead get its street network using the graph_from_address function,
    which geocodes the place name to a point and gets the network within some
    distance of that point.

    If OSM does have polygon boundaries for this place but you're not finding
    it, try to vary the query string, pass in a structured query dict, or vary
    the which_result argument to use a different geocode result. If you know
    the OSM ID of the place, you can retrieve its boundary polygon using the
    geocode_to_gdf function, then pass it to the graph_from_polygon function.

    Parameters
    ----------
    query : string or dict or list
        the query or queries to geocode to get place boundary polygon(s)
        default : "drive"
    network_type : string {"all_private", "all", "bike", "drive", "drive_service", "walk"}
        what type of street network to get
        default: "drive"

    Returns
    -------
    G : networkx.MultiDiGraph
    """
    return ox.graph_from_place(query, network_type=network_type)


def save_osm(G, filepath):
    """
    Save graph to disk as GraphML file.

    Parameters
    ----------
    G : networkx.MultiDiGraph
        input graph
    filepath : string or pathlib.Path
        path to the GraphML file including extension. if None, use default
        data folder + graph.graphml

    Returns
    -------
    None
    """
    ox.save_graphml(G, filepath=filepath)


def load_osm(
    filepath, specific_dtypes={"risk": float, "global_risk": float, "length": float}
):
    """
    Load an OSMnx-saved GraphML file from disk.

    Converts the node/edge attributes to appropriate data types, which can be
    customized if needed by passing in `specific_dtypes` argument.

    Parameters
    ----------
    filepath : string or pathlib.Path
        path to the GraphML file
    specific_dtypes : dict
        dict of node attribute names:types to convert values' data types
        default: {"risk": float}

    Returns
    -------
    G : networkx.MultiDiGraph
    """
    # NOTE :
    # Use specific_dtypes to convert risk to float to avoid error as
    #   TypeError: unsupported operand type(s) for +: 'int' and 'str'
    # during the route computing on the risk attributes

    G = ox.load_graphml(
        filepath=filepath, node_dtypes=specific_dtypes, edge_dtypes=specific_dtypes
    )
    return G


def set_risk_to_graph(G, risk_path):
    """
    Append risk attributes to the nodes and the edges of a graph.

    Parameters
    ----------
    G : networkx.MultiDiGraph
        input graph
    risk_path : string or pathlib.Path
        path to the DataFrame with the crash information file including ext.

    Returns
    -------
    G : networkx.MultiDiGraph
    """
    # TODO use DF crashes to computes the risk
    nodes_proj, edges_proj = ox.graph_to_gdfs(G, nodes=True, edges=True)
    edges_proj["risk"] = edges_proj["length"] % 1
    G = ox.graph_from_gdfs(nodes_proj, edges_proj)
    return G


class NYCRouteManager:
    """
    The NYC Route manager class allows you to manipulate a MultiDiGraph
    and find a way between 2 points in the NYC streets network.

    The computed way can be :
        - the shortest
        - the safest
        - the more dangerous
    """

    # OSM files
    osm_filepath = "data/NYC_drive.osm"
    osm_risk_filepath = "data/NYC_drive_risk.osm"
    # Crashes statistics data
    crash_weight_filepath = "data/NYC_crashes.csv"
    # Map networkx including risk
    G_risk = None

    def __init__(self, reload_data=False):
        """
        Initialize the NYCRouteManager

        Parameters
        ----------
        reload_data : boolean
            If True, the OSM information and the risk associated to the Graph
            will be be reloaded
            Otherwhise, it will try load the saved Graph or create it if the
            OSM file is missing.
        """
        self.load_risk_graph(reload_data)

    def load_risk_graph(self, reload_data=False):
        """
        Load the NYC streets network graph including risk into G_risk

        Parameters
        ----------
        reload_data : boolean
            If True, the OSM information and the risk associated to the Graph
            will be be reloaded
            Otherwhise, it will try load the saved Graph or create it if the
            OSM file is missing.
        """
        G = None
        # Download the NYC_Network Graph with OSMNX
        if not path.isfile(self.osm_filepath) or reload_data:
            G = download_osm()
            save_osm(G, self.osm_filepath)
        # Load the NYC_Network Graph with risk
        if not path.isfile(self.osm_risk_filepath) or reload_data:
            if G is None:
                G = load_osm(self.osm_filepath)
            # create file with risk
            self.G_risk = set_risk_to_graph(G, self.crash_weight_filepath)
            # Save file for a future usage
            save_osm(self.G_risk, self.osm_risk_filepath)
        else:
            self.G_risk = load_osm(self.osm_risk_filepath)

    def get_nearest_node(self, point, return_dist=False):
        """
        Find the nearest node to a point.

        Return the graph node nearest to some (lat, lng) or (y, x) point and
        optionally the distance between the node and the point.

        Parameters
        ----------
        G : networkx.MultiDiGraph
            input graph
        point : tuple
            The (lat, lng) or (y, x) point for which we will find
            the nearest node in the graph
        return_dist : bool
            Optionally also return the distance (in meters)
            between the point and the nearest node

        Returns
        -------
        int or tuple of (int, float)
            Nearest node ID or optionally a tuple of (node ID, dist),
            where dist is the distance (in meters) between the point
            and nearest node
        """
        return ox.get_nearest_node(self.G_risk, point, return_dist=return_dist)

    def convert_route_to_gdf(self, route):
        """
        Convert a route to a geopandas.GeoDataFrame

        Parameters
        ----------
        G : networkx.MultiDiGraph
            input graph
        route : list
            List of nodes in a route.

        Returns
        -------
        geopandas.GeoDataFrame
            List of the edges defined in the route
        """
        # Extracted from ox.plot_route_folium()
        node_pairs = zip(route[:-1], route[1:])
        uvk = (
            (
                u,
                v,
                min(self.G_risk[u][v], key=lambda k: self.G_risk[u][v][k]["length"]),
            )
            for u, v in node_pairs
        )
        gdf_edges = ox.graph_to_gdfs(self.G_risk.subgraph(route), nodes=False).loc[uvk]

        return gdf_edges

    def get_route(self, point_from, point_to, weight="length"):
        """
        Returns the shortest weighted path from point_from to point_to in
        the NYC streets network.
        The point_from and point_to will be computed to be the nearest node
        in the NYC streets network based on the longitude and latitude of
        these geographic points.

        Uses Dijkstra's Method to compute the shortest weighted path
        between two nodes in a graph.

        Parameters
        ----------
        point_from : tuple(latitude, longitude)
            Starting point

        point_to : tuple(latitude, longitude)
            Destination point

        weight : string or function
            If this is a string, then edge weights will be accessed via the
            edge attribute with this key (that is, the weight of the edge
            joining `u` to `v` will be ``G.edges[u, v][weight]``). If no
            such edge attribute exists, the weight of the edge is assumed to
            be one.

            If this is a function, the weight of an edge is the value
            returned by the function. The function must accept exactly three
            positional arguments: the two endpoints of an edge and the
            dictionary of edge attributes for that edge. The function must
            return a number.

        Returns
        -------
        geopandas.GeoDataFrame
            List of the edges defined in the route

        Raises
        ------
        NodeNotFound
            If `point_from` is not in NYC streets network.

        NetworkXNoPath
            If no path exists between point_from and point_to.
        """
        # Search the nodes from and to
        node_from = self.get_nearest_node(point_from)
        node_to = self.get_nearest_node(point_to)

        # Compute the shortest weigthed way
        route = nx.dijkstra_path(self.G_risk, node_from, node_to, weight=weight)

        return self.convert_route_to_gdf(route)

    def get_safest_route(self, point_from, point_to):
        """
        Returns the safest path from point_from to point_to in
        the NYC streets network.

        Call `get_route` using `risk` as weigth

        See get_route(self, point_from, point_to, weight=weight) for more information.

        """
        return self.get_route(point_from, point_to, weight="global_risk")

    def get_safest_streets_route(self, point_from, point_to):
        """
        Returns the safest path from point_from to point_to in
        the NYC streets network by looking for a short disance.

        Call `get_route` using `custom_value` as weight

        See get_route(self, point_from, point_to, weight=weight)
        for more information.
        """

        def safest_street_weight(u, v, d):
            length = d[0].get("length", 0)
            global_risk = d[0].get("global_risk", 0)
            return length * (global_risk + 1)

        return self.get_route(point_from, point_to, weight=safest_street_weight)

    def get_shortest_route(self, point_from, point_to):
        """
        Returns the shortest path from point_from to point_to in
        the NYC streets network.

        Call `get_route` using `length` as weight

        See get_route(self, point_from, point_to, weight=weight)
        for more information.
        """
        return self.get_route(point_from, point_to, weight="length")

    # Sample to compute weigth with function
    # Source : https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html?highlight=dijkstra_path#networkx.algorithms.shortest_paths.weighted.dijkstra_path
    # def func(u, v, d):
    #   node_u_wt = G.nodes[u].get("node_weight", 1)
    #   node_v_wt = G.nodes[v].get("node_weight", 1)
    #   edge_wt = d.get("weight", 1)
    #   return node_u_wt / 2 + node_v_wt / 2 + edge_wt

    def get_most_dangerous_route(self, point_from, point_to):
        """
        Returns the dangerous path from point_from to point_to in
        the NYC streets network.

        Call `get_route` using `global_risk * -1` as weight

        See get_route(self, point_from, point_to, weight=weight)
        for more information.
        """

        def most_dangerous_weight(u, v, d):
            edge_risk = d[0].get("global_risk", 0)
            edge_length = d[0].get("length", 1)
            if edge_risk == 0:
                edge_risk = 1000
            elif edge_risk < 3:
                edge_risk = 500
            elif edge_risk < 7:
                edge_risk = 250
            elif edge_risk < 10:
                edge_risk = 100
            else:
                edge_risk = 1
            return edge_length * edge_risk

        return self.get_route(point_from, point_to, weight=most_dangerous_weight)

    def get_routes(self, point_from: tuple, point_to: tuple, route_types: list):
        routes = {}
        for route_type in route_types:
            route = None
            if route_type == "safest":
                route = self.get_safest_route(point_from, point_to)
            elif route_type == "shortest":
                route = self.get_shortest_route(point_from, point_to)
            elif route_type == "dangerous":
                route = self.get_most_dangerous_route(point_from, point_to)
            elif route_type == "safest_streets":
                route = self.get_safest_streets_route(point_from, point_to)
            if route is not None:
                routes[route_type] = route
        return routes


if __name__ == "__main__":
    from datetime import datetime

    # LOADING
    print(f"[!] Start Loading: {datetime.now()}")
    nyc_manager = NYCRouteManager()
    print(f"[!] End Loading: {datetime.now()}")

    from_point = (40.533187572963215, -74.20338996809984)
    to_point = (40.7678192111937, -73.77352502200928)

    # POINTS SEARCH
    print(f"[!] Start Node Search: {datetime.now()}")
    print("FROM")
    node = nyc_manager.get_nearest_node(from_point, return_dist=True)
    print("Point : ", from_point, " -> Node ID : ", node)
    # print(nyc_manager.G_risk.nodes[node])

    print("TO")
    node = nyc_manager.get_nearest_node(to_point)
    print("Point : ", to_point, " -> Node ID : ", node)
    print(nyc_manager.G_risk.nodes[node])
    print(f"[!] End Node Search: {datetime.now()}")

    # ROUTE SEARCH
    print(f"[!] Start Shortest Route Search: {datetime.now()}")
    route = nyc_manager.get_shortest_route(from_point, to_point)
    print("Shape : ", route.shape)
    print(route.head())
    print(route.columns)
    print(f"[!] End Shortest Route Search: {datetime.now()}")

    print(f"[!] Start Safest Route Search: {datetime.now()}")
    route = nyc_manager.get_safest_route(from_point, to_point)
    print("Shape : ", route.shape)
    print(route.head())
    print(route.columns)
    print(f"[!] End Safest Route Search: {datetime.now()}")

    print(f"[!] Start Dangerous Route Search: {datetime.now()}")
    route = nyc_manager.get_most_dangerous_route(from_point, to_point)
    print("Shape : ", route.shape)
    print(route.head())
    print(route.columns)
    print(f"[!] End Dangerous Route Search: {datetime.now()}")
