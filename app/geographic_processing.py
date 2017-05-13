# Reference: https://github.com/gboeing/urban-data-science/blob/master/19-Spatial-Analysis-and-Cartography/rtree-spatial-indexing.ipynb
# Reference: http://geoffboeing.com/2016/10/r-tree-spatial-index-python/

import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
import osmnx as ox

def contains(x_list,y_list):
    """
    This method passes in all the points from the database and then checks for 
    """
    #our bounding box defined here...
    gdf = ox.gdf_from_place('Walnut Creek, California, USA')
    gdf_nodes = gpd.GeoDataFrame(data={'x':x_list, 'y':y_list})
    gdf_nodes.crs = gdf.crs
    gdf_nodes.name = 'nodes'
    gdf_nodes['geometry'] = gdf_nodes.apply(lambda row: Point((row['x'], row['y'])), axis=1)

    # make the geometry a multipolygon if it's not already
    geometry = gdf['geometry'].iloc[0]
    if isinstance(geometry, Polygon):
        geometry = MultiPolygon([geometry])

    import code
    code.interact(local=locals())

    sindex = gdf_nodes.sindex
    possible_matches_index = list(sindex.intersection(geometry.bounds))
    possible_matches = gdf_nodes.iloc[possible_matches_index]
    return possible_matches[possible_matches.intersects(geometry)]
    
