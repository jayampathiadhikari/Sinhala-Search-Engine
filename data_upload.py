from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def data_upload():
    with open('./corpus/actor_corpus.json', encoding="utf8") as f:
        data = json.loads(f.read())
    helpers.bulk(es, data, index='index-actors')


if __name__ == "__main__":
    data_upload()
