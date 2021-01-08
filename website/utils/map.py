import folium


def get_map():
    latitude = 40.677834
    longitude = -74.012443
    map_nyc = folium.Map(location=[latitude, longitude], zoom_start=10)

    # folium.Marker([G.nodes[origin_node]['y'], G.nodes[origin_node]['x']],
    #             popup="<i>From</i>", icon=folium.Icon(color="green")).add_to(map_nyc)
    # folium.Marker([G.nodes[destination_node]['y'], G.nodes[destination_node]['x']],
    #             popup="<i>To</i>", icon=folium.Icon(color="red")).add_to(map_nyc)
    # folium.Choropleth(get_route_detail(G_weight, route), line_weight=5,
    #                 line_color='blue', line_opacity=0.5).add_to(map_nyc)
    # folium.Choropleth(get_route_detail(G_weight, route_weigth),
    #                 line_weight=5, line_color='red', line_opacity=0.5).add_to(map_nyc)

    return map_nyc


if __name__ == "__main__":
    print(get_map())
