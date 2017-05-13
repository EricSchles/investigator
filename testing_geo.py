from app.geographic_processing import contains
from app.models import BackpageAdInfo as B

latlongs = [(elem.latitude,elem.longitude)
            for elem in B.query.all() if "no" not in elem.latitude]
latlongs = [(float(elem[0]), float(elem[1]))
            for elem in latlongs if elem[0] != '']
xs = [elem[0] for elem in latlongs]
ys = [elem[1] for elem in latlongs]
contains(xs,ys)


