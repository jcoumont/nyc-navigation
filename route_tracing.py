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
        list_of_colors = ["#799351", "#ebdc87", "#ffa36c," "#d54062"] #Green , Yellow, Orange, red

        for i, ii in zip(gdf["geometry"], gdf["dangerosity"]):
            if ii <= 0.3:
                path = folium.Choropleth(i,line_weight=5, line_color='#799351', line_opacity=1).add_to(m)
        
            elif 0.3 < ii <= 0.6:
                path = folium.Choropleth(i,line_weight=5, line_color='#ffa36c', line_opacity=1).add_to(m)
        
            else:
                path = folium.Choropleth(i,line_weight=5, line_color='#FF0000', line_opacity=1).add_to(m)
        return path

    def calculate_distance(self, segments):
        distance = geopy.distance.distance(segments[0], segments[-1])
m = Path_tracing().creat_map()
Path_tracing().trace_the_path(loc,m)