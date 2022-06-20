from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry

from .models import Product, AdminUser

@registry.register_document
class AdminUserDocument(Document):
    class Index:
        name = 'admin_user'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    url = fields.TextField(attr='get_absolute_url')

    class Django:
        model = AdminUser
        fields = [
            'first_name',
            'designation',
            'profile_pic',
            'department',
            'email'
                  ]