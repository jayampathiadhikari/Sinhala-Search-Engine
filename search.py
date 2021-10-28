from elasticsearch import Elasticsearch, helpers
from preprocessor import intent_classifier, query_preprocessor


def search(query):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    selected_intent, selected_fields = intent_classifier(query)
    new_query = query_preprocessor(selected_intent, query)
    print('NEW QUERY', new_query)
    results = es.search(index="index-test-actors", body={"query": {"multi_match": {
        "query": new_query,
        "type": "best_fields",
        "fields": selected_fields
    }}})
    print('NO OF RESULTS ', len(results["hits"]["hits"]))
    print(filter(results["hits"]["hits"]))
    return filter(results["hits"]["hits"])

def filter(results):
    filtered = []
    for result in results:
        filtered.append(result['_source'])
    return filtered

# query = "හොඳම නිළිය සම්මානය ලබා ගත් නිළියන්"
# search(query)

