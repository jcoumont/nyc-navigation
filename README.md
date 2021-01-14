# Find a path through New York City

Challenge realized @BeCode
- Type of Challenge: `Consolidation`
- Duration: `4 days (variable)`
- Deadline: `12/01/2020 - 13h30`
- Deployment strategy : `Github page`
- Team challenge : `5`

### Team Members
- [Axelle Paquet](https://github.com/GodIsADJ)
- [Imad Haj Rashid](https://github.com/hajrashidimad)
- [Jérôme Coumont](https://github.com/jcoumont)
- [Ousmane Diop](https://github.com/Nooreyni)
- [Reza Nasrollahrikaran](https://github.com/RezaNasrollahi)

## Summary
### Mission objectives
- Learn and apply graph theory
- Learn and apply graph traversal algorithms
- Apply basic statistics on a dataset
- Work with geolocalized data
- Work in a dev-client relationship

### The mission

xyz blablabla xyz

### Must-have features
- [x] Create a graph of edges and vertices mapping to roads and intersections
- [x] Apply an algorithm to find the *least dangerous path* between two streets and/or coordinates.
- [x] Build a graphical interface that shows the *least dangerous path* on a map of New York.

  It does not have to be interactive, e.g. you can just get the street names/coordinates as arguments to a function, and show the result on a map.
- [x] Code is PEP8 compliant
- [x] Code is formatted using `Black`
- [x] Code duplication is reduced.
- [x] Functions and objects have been used.

### Nice-to-have features
- [x] Create different algorithms e.g. one for the *most dangerous path*. Be creative.
- [x] Make an interactive version of this where the user can add the streets/coordinates in the browser.
- [x] Deploy your app on the platform of your choice.
## Usage
Launch the API : `python route.py`  
Access the API by using this url : http://localhost:5000/  
## Installation
The needed libraries are in the requirement.txt. To install it, use the command below:  
  
``` sh
python -m pip install -r requirements.txt
```  
### *Links to documentation :*
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) : To display the website
- [Docker](https://docs.docker.com/) : to run the code int a container and deploy it on Azure
- [Networkx](https://networkx.org/documentation/stable/) : To create and manipulate a graph
- [Osmnx](https://osmnx.readthedocs.io/en/stable/osmnx.html) : to manipulate coordinates
- [Folium](https://python-visualization.github.io/folium/) : to diplay a map of New York
## Live version
The live version is [here](https://nyc-navigation.azurewebsites.net/)
