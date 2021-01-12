import folium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from folium import plugins


class NYCMapManager:
    latitude = 40.677834
    longitude = -74.012443
    crashes_filepath = 'data/NYC_crashes_100000_osmid.csv'
    layer_crashes = None
    default_colors = {
                        "shortest": "blue",
                        "safest": "green",
                        "dangerous": "red",
                        "other": "yellow"
                     }

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

    def get_map(self, from_coord: tuple, to_coord: tuple, routes=None):
        """Return the html code to display map

        Args:
            from_coord (tuple): location coordinates (latitude, longitude)
            to_coord (tuple): location coordinates (latitude, longitude)

        Returns:
            map_nyc._repr_html_(): the map in html format
        """
        map_nyc = folium.Map(location=[self.latitude, self.longitude], zoom_start=10)
        #self.layer_crashes.add_to(map_nyc)

        if routes is not None:
            if type(routes) is dict:
                for key in routes:
                    choropleth = folium.Choropleth(
                                        routes[key], line_weight=5, line_color=self.default_colors[key], line_opacity=0.5
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
