from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def data_upload():
    with open('si_actors_sinhala_name1.json', encoding="utf8") as f:
        data = json.loads(f.read())
    helpers.bulk(es, data, index='index-test-actors')


if __name__ == "__main__":
    data_upload()
