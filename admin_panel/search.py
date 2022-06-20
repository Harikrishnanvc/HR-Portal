import elasticsearch
from elasticsearch_dsl import Search
from .documents import AdminUserDocument

ELASTIC_HOST = 'http://localhost:9200/'

client = elasticsearch.Elasticsearch(hosts=[ELASTIC_HOST])


def lookup(query, index='admin_user', fields=[
    'first_name',
    'designation',
    'profile_pic',
    'department',
    'email',
    'mobile_no'
]):
    if not query:
        return
    results = AdminUserDocument(index=index).search().query(
        "multi_match", fields=fields, fuzziness='AUTO', query=query)

    q_results = []

    for hit in results:
        data = {
            "first_name": hit.first_name,
            "profile_pic": hit.profile_pic,
            "designation": hit.designation,
            "department": hit.department,
            "email": hit.email,
        }
        q_results.append(data)
    return q_results