# Reference: https://github.com/gboeing/urban-data-science/blob/master/19-Spatial-Analysis-and-Cartography/rtree-spatial-indexing.ipynb
# Reference: http://geoffboeing.com/2016/10/r-tree-spatial-index-python/
        
def contains(latitude_bounds,longitude_bounds,point_to_check):
    """
    This method passes in all the points from the database and then checks for containment in an area.
    @latitude_bounds - the latitudes of the bounding box
    @longitude - the longitudes of the bounding box
    @point_to_check - the point to check.  

    This function answers the question, is the point_to_check inside the polygon we pass in?
    """
    #our bounding box defined here...
    max_lat, min_lat = max(latitude_bounds), min(latitude_bounds)
    max_long, min_long = max(longitude_bounds), min(longitude_bounds)

    if point_to_check[0] < max_lat and point_to_check[0] > min_lat:
        if point_to_check[1] < max_long and point_to_check[1] > min_long:
            return True
    return False


