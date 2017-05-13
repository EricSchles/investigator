from app.geographic_processing import contains
from app.models import BackpageAdInfo as B

latlongs = [(elem.latitude,elem.longitude)
            for elem in B.query.all() if "no" not in elem.latitude]
latlongs = [(float(elem[0]), float(elem[1]))
            for elem in latlongs if elem[0] != '']
xs = [elem[0] for elem in latlongs]
ys = [elem[1] for elem in latlongs]
box = [(40.775329,-73.753134),
       (40.777100, -73.746568),
       (40.768537, -73.741225),
       (40.767740,-73.751504)]

result = contains(xs,ys,(xs[0],ys[0]))
import code
code.interact(local=locals())
