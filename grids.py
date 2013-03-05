from monitor.connections.models import Item, TCPconnection
from django.conf.urls import url
from monitor.jqgrid import JqGrid 
from django.core.urlresolvers import reverse_lazy


class ExampleGrid(JqGrid):
    model = Item
    #model = TCPconnection.objects.filter(connection_date='2012-04-27').order_by('-connection_time')[:200] # could also be a queryset
    fields = ['id', 'row_id', 'data'] # optional 
    url = reverse_lazy('grid_handler')
    caption = 'My First Grid' # optional
    colmodel_overrides = {
        'id': { 'editable': False, 'width':10 },
    }
