import copy
import folium


class NYCMapManager:
    default_map = None

    def __init__(self):
        latitude = 40.677834
        longitude = -74.012443
        self.default_map = folium.Map(location=[latitude, longitude], zoom_start=10)

    def get_map(self, from_coord: tuple, to_coord: tuple, routes=None):
        """Return the html code to display map

        Args:
            from_coord (tuple): location coordinates (latitude, longitude)
            to_coord (tuple): location coordinates (latitude, longitude)

        Returns:
            map_nyc._repr_html_(): the map in html format
        """
        map_nyc = copy.copy(self.default_map)

        if routes is not None:
            if type(routes) is dict:
                for key in routes:
                    choropleth = folium.Choropleth(
                                        routes[key], line_weight=5, line_color="blue", line_opacity=0.5
                                    )
                    layer_group = folium.FeatureGroup(name=key).add_to(map_nyc)
                    layer_group.add_child(choropleth)
                    tb = routes[key].total_bounds
                    map_nyc.fit_bounds([(tb[1], tb[0]), (tb[3], tb[2])])
            else:
                folium.Choropleth(
                    routes, line_weight=5, line_color="blue", line_opacity=0.5
                ).add_to(map_nyc)
                tb = routes.total_bounds
                map_nyc.fit_bounds([(tb[1], tb[0]), (tb[3], tb[2])])
            folium.LayerControl().add_to(map_nyc)
        # folium.Marker([G.nodes[origin_node]['y'], G.nodes[origin_node]['x']],
        #             popup="<i>From</i>", icon=folium.Icon(color="green")).add_to(map_nyc)
        # folium.Marker([G.nodes[destination_node]['y'], G.nodes[destination_node]['x']],
        #             popup="<i>To</i>", icon=folium.Icon(color="red")).add_to(map_nyc)

        # folium.Choropleth(get_route_detail(G_weight, route_weigth),
        #                 line_weight=5, line_color='red', line_opacity=0.5).add_to(map_nyc)

        return map_nyc._repr_html_()
