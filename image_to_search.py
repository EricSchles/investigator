from elasticsearch import Elasticsearch
from app.models import ImageToText


host = "http://localhost:9200"
es = Elasticsearch(host)


def db_to_elasticsearch(index_name):
    for elem in ImageToText.query.all():
        data = {}
        for label in elem.labels.rstrip("}").lstrip("}").split(","):
            data["label"] = label
            data["file"] = elem.file_name
        es.index(index=index_name, doc_type="txt", body=data)


if __name__ == '__main__':
    index_name = "image_search_index"
    db_to_elasticsearch(index_name)
