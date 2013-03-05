from django.http import HttpResponse
from django.template import Template, Context
from django.db import IntegrityError
from datetime  import datetime,  date
from django.shortcuts import render_to_response
from monitor.connections.models import Item, TCPconnection
from django.template import Template, Context,  RequestContext
import simplejson as json
import calendar as calendar

    
def history_graphs_data(django_objects, param_type):
    parameter_type = param_type
    our_records = django_objects
    print type(our_records)
    final_list=[]
    final_dict = {}
    sockets_list =[]
    #for record in our_records.values('lcl').distinct('lcl').order_by('lcl'):
    for record in our_records.values('lcl').distinct().order_by('lcl'):
        sockets_list.append(record['lcl'])
    for ip_address in sockets_list:
        sockets_values_dict={}
       # print ip_address
        socket_values=None
        sockets_values_dict['label']=str(ip_address) + ' = -0.00'
        for record in our_records.values('lcl',parameter_type,'connection_time'):
            #print record['lcl'], record['connection_time'], record['unused']
            if  record['lcl']==ip_address:
                #print 'Hello'
                if socket_values is None:
                    socket_values=[]
                    socket_values.append([calendar.timegm(record['connection_time'].timetuple())*1000, int(record[parameter_type])])
                else:
                    #print 'else hello'
                    socket_values.append([calendar.timegm(record['connection_time'].timetuple())*1000, int(record[parameter_type])])
                #print record['lcl'], record['connection_time'], record['unused']
        #print socket_values
        sockets_values_dict['data']=socket_values
        final_list.append(sockets_values_dict)
        final_dict[str(ip_address)]=sockets_values_dict 
    #return final_list
    return final_dict

def historySearch(request):
    my_objects = TCPconnection.objects.filter(connection_time__range=['2012-04-26 11:17','2012-04-26 11:20'])
    graph_data = {}
    query = request.GET.get('parameter_type', '')
    if query:
        graph_data=history_graphs_data(my_objects, query)
    else:
        print 'ERROR'
    print graph_data
    return HttpResponse(json.dumps(graph_data))


    parameter_type = 'rttvar'
    our_records = my_objects
    print type(our_records)
    final_list=[]
    final_dict = {}
    sockets_list =[]
    #for record in our_records.values('lcl').distinct('lcl').order_by('lcl'):
    for record in our_records.values('lcl').distinct().order_by('lcl'):
        sockets_list.append(record['lcl'])
    print sockets_list
    for ip_address in sockets_list:
        sockets_values_dict={}
       # print ip_address
        socket_values=None
        sockets_values_dict['label']=str(ip_address) + ' = -0.00'
        for record in our_records.values('lcl',parameter_type,'connection_time'):
            #print record['lcl'], record['connection_time'], record['unused']
            if  record['lcl']==ip_address:
                #print 'Hello'
                if socket_values is None:
                    socket_values=[]
                    socket_values.append([calendar.timegm(record['connection_time'].timetuple())*1000, int(record[parameter_type])])
                else:
                    #print 'else hello'
                    socket_values.append([calendar.timegm(record['connection_time'].timetuple())*1000, int(record[parameter_type])])
                #print record['lcl'], record['connection_time'], record['unused']
        #print socket_values
        sockets_values_dict['data']=socket_values
        final_list.append(sockets_values_dict)
        final_dict[str(ip_address)]=sockets_values_dict 
    #return final_list
    return final_dict



from time import gmtime, strftime
strftime("%Y-%m-%d %H:%M", gmtime())
