from elasticsearch import Elasticsearch, helpers
from preprocessor import intent_classifier, query_preprocessor


def search(query):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    selected_intent, selected_fields = intent_classifier(query)
    new_query = query_preprocessor(selected_intent, query)
    print('NEW QUERY', new_query)
    results = es.search(index="index-actors", body={"query": {"multi_match": {
        "query": new_query,
        "type": "best_fields",
        "fields": selected_fields,
        "operator": 'or',
        "fuzziness": 'AUTO'
    }}})

    print('NO OF RESULTS ', len(results["hits"]["hits"]))
    # print(filter(results["hits"]["hits"]))
    return filter(results["hits"]["hits"])


def filter(results):
    filtered = []
    for result in results:
        filtered.append(result['_source'])
    return filtered

# queries = ["දමිතා අබේරත්න රංගනය කල නාට්ය", "දමිතා අබේරත්නගේ විස්තර", "දමිතා අබේරත්නගේ වෘත්තීය දිවිය",
#            "දමිතා අබේරත්නගේ සම්මාන", "මීහරකා චිත්රපටයේ නිළියන්", "හොඳම නිළිය සම්මානය ලබාගත් නිළියන්",
#            "හොඳම නළුවා සම්මානය ලබාගත් නළුවන්", "සඳ මඩල චිත්රපටයේ නළුවන්"]
#
# for i in queries:
#     search(i)
