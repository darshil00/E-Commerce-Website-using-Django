import django_tables2 as tables
from sellinghub.models import Customer, Users

class SimpleTable(tables.Table):
    class Meta:
        model = Users
        attrs = {"class": "table thead-light table-striped table-hover"}