import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from folium import plugins


class NYCMapManager:
    latitude = 40.677834
    longitude = -74.012443
    crashes_filepath = "data/NYC_crashes_100000_osmid.csv"
    layer_crashes = None
    default_colors = {
        "shortest": "blue",
        "safest": "green",
        "dangerous": "red",
        "safest_streets": "orange",
        "other": "yellow",
    }

    range_of_colour = {
        10: "#FF4500",
        9: "#FF0000",
        8: "#FF6347",
        7: "#FF8C00",
        6: "#FFA500",
        5: "#FFD700",
        4: "#FFFF00",
        3: "#9ACD32",
        2: "#7FFF00",
        1: "#00FF00",
        0: "#00FF00",
    }  # red, tomate, dark orange, orange, yellow, gold, yellowgreen, reus, lim

    # def __init__(self):
    #     self.initialize_crashes_layer()

    # def initialize_crashes_layer(self):
    #     df_risk = pd.read_csv(self.crashes_filepath)
    #     geom = [Point(xy) for xy in zip(df_risk.longitude, df_risk.latitude)]
    #     gdf_risk = gpd.GeoDataFrame(df_risk, crs="EPSG:4326", geometry=geom)

    #     self.layer_crashes = folium.FeatureGroup(name="crashes")

    #     marker_cluster = plugins.MarkerCluster()
    #     self.layer_crashes.add_child(marker_cluster)
    #     for i, v in gdf_risk.iterrows():
    #         popup = """
    #         Killed : <b>%s</b><br>
    #         Injured : <b>%s</b><br>
    #         """ % (v['persons_killed'], v['persons_injured'])

    #         if v['persons_killed'] > 0:
    #             folium.CircleMarker(location=[v['latitude'], v['longitude']],
    #                                 radius=10,
    #                                 tooltip=popup,
    #                                 color='#581845',
    #                                 fill_color='#581845',
    #                                 fill_opacity=0.7,
    #                                 fill=True).add_to(marker_cluster)
    #         elif v['persons_injured'] > 0:
    #             folium.CircleMarker(location=[v['latitude'], v['longitude']],
    #                                 radius=10,
    #                                 tooltip=popup,
    #                                 color='#C70039',
    #                                 fill_color='#C70039',
    #                                 fill_opacity=0.7,
    #                                 fill=True).add_to(marker_cluster)
    #         else:
    #             folium.CircleMarker(location=[v['latitude'], v['longitude']],
    #                                 radius=10,
    #                                 tooltip=popup,
    #                                 color='#FFC300',
    #                                 fill_color='#FFC300',
    #                                 fill_opacity=0.7,
    #                                 fill=True).add_to(marker_cluster)

    def get_map(
        self, from_address: str, to_address: str, routes=None, use_gradient=True
    ):
        """Return the html code to display map

        Args:
            from_coord (tuple): location coordinates (latitude, longitude)
            to_coord (tuple): location coordinates (latitude, longitude)

        Returns:
            map_nyc._repr_html_(): the map in html format
        """
        map_nyc = folium.Map(location=[self.latitude, self.longitude], zoom_start=10)
        # self.layer_crashes.add_to(map_nyc)
        marker_added = False
        if routes is not None:

            if type(routes) is dict:
                for key in routes:
                    route = routes[key]
                    if not marker_added:
                        from_point = [
                            route.iloc[0]["geometry"].xy[1][0],
                            route.iloc[0]["geometry"].xy[0][0],
                        ]
                        to_point = [
                            route.iloc[-1]["geometry"].xy[1][-1],
                            route.iloc[-1]["geometry"].xy[0][-1],
                        ]

                        folium.Marker(
                            from_point,
                            tooltip="From : " + from_address,
                            icon=folium.Icon(color="blue"),
                        ).add_to(map_nyc)
                        folium.Marker(
                            to_point,
                            tooltip="To : " + to_address,
                            icon=folium.Icon(color="red"),
                        ).add_to(map_nyc)

                    length_km = round((route["length"].sum() / 1000), 3)

                    if use_gradient:  # Draw the path with gradient
                        # Transform the risk on a range from 0-10
                        # route["global_risk"] = round((route["global_risk"]/route["global_risk"].max())*10)
                        # for path_part, risk in zip(route["geometry"], route["global_risk"]):
                        #    choropleth = folium.Choropleth(path_part,line_weight=5, line_color=self.range_of_colour[risk], line_opacity=1)
                        #    layer_group.add_child(choropleth)
                        layer_group = folium.FeatureGroup(
                            name=f"{key} ({length_km} km) (risk view)", show=False
                        ).add_to(map_nyc)

                        def get_colour(feature):
                            """Maps low values to green and hugh values to red."""
                            if feature == 0:
                                return "#00FF00"
                            elif feature < 3:
                                return "#FFFF00"
                            elif feature < 7:
                                return "#FF8C00"
                            else:
                                return "#FF4500"

                        for path_part, risk in zip(
                            route["geometry"], route["global_risk"]
                        ):
                            choropleth = folium.Choropleth(
                                path_part,
                                line_weight=5,
                                line_color=get_colour(risk),
                                line_opacity=1,
                            )
                            layer_group.add_child(choropleth)

                    color = self.default_colors[key]
                    layer_group = folium.FeatureGroup(
                        name=f"{key} ({length_km} km) ({color})"
                    ).add_to(map_nyc)
                    choropleth = folium.Choropleth(
                        route, line_weight=5, line_color=color, line_opacity=0.7
                    )
                    layer_group.add_child(choropleth)

                    tb = route.total_bounds
                map_nyc.fit_bounds([(tb[1], tb[0]), (tb[3], tb[2])])
            else:
                folium.Choropleth(
                    routes, line_weight=5, line_color="blue", line_opacity=1
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
