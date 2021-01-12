import folium
import geopy
from geopy import distance
from xxx import gdf
loc = [(40.798504, -73.967125),(40.731167, -73.709940),(40.700108,-73.953830),(40.701527,-73.989570),(40.798504, -73.967125)]


class Path_tracing:

    def creat_map(self):
        """ creat folium map, location is New-York"""
        m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

        return m

    def trace_the_path(self, segments : list, m):
        range_of_coluor = {10:"#FF4500",
                9:"#FF0000",
                8:"#FF6347",
                7:"#FF8C00",
                6:"#FFA500",
                5:"#FFD700",
                4:"#FFFF00",
                3:"#9ACD32",
                2:"#7FFF00",
                1:"#00FF00",
                0:"#00FF00"} # red, tomate, dark orange, orange, yellow, gold, yellowgreen, reus, lim
        
        gdf["risk"] = (gdf["risk"]-gdf["risk"].min()) / (gdf["risk"].max() - gdf["risk"].min()) # normalaized the risk columns
        for i, ii in zip(gdf["geometry"], gdf["risk"]):
            path = folium.Choropleth(i,line_weight=5, line_color=range_of_coluor[round(ii*10)], line_opacity=1).add_to(m)
        return path
