from django.http import HttpResponse
from django.template import Template, Context
from django.db import IntegrityError,  connection,  transaction
from django.core import serializers
from datetime  import datetime,  date, timedelta
import time
from django.shortcuts import render_to_response
from django.forms.models import model_to_dict
from monitor.connections.models import Item, TCPconnection, ServerConnections,  Machines
from django.db.models import Sum
from django.template import Template, Context,  RequestContext
from monitor.history_query import history_graphs_data
import simplejson as json
import calendar as calendar
from calendar import timegm
from django import forms
from django.core.context_processors import csrf
from monitor.connections.models import ContactForm,  MachinesForm
from django.shortcuts import render
from django.http import HttpResponseRedirect


def thanks(request):
    return render_to_response('contact.html')
    
def datepickerExample(request):
    return render_to_response('datepicker_template.html')

def hello(request):
    return HttpResponse("Hello world")
    
def getQueryObjects():
    my_objects = TCPconnection.objects.filter(connection_date=date.today())
    return my_objects
    
def table_main(request):
    #return HttpResponse("Hello world")
    my_objects = TCPconnection.objects.filter(connection_date=date.today())
    connections = tuple(my_objects.order_by('-connection_time')[:40])
    return render_to_response('table_template.html', {'my_list': connections})
 
def recent_query(request):
    time_now = datetime.now()
    time_thirtymin_ago = time.strftime("%Y-%m-%d %H:%M:%S", (time_now- timedelta(minutes=300)).timetuple())
    cursor = connection.cursor()
    cursor.execute('(select connection_time, server_id_id, color, lcl, rmt, rx_errno_avg, tx_errno_avg, retrans_avg  from last_five_minutes_each_machine) union (select connection_time, server_id_id, "red" as color, lcl, rmt, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  connections_serverconnections where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and rmt NOT IN (select DISTINCT(rmt) from last_five_minutes_each_machine) AND lcl NOT IN (select DISTINCT(lcl) from last_five_minutes_each_machine) group by connection_time, lcl, rmt order by connection_time desc)')
    connections = dictfetchall_django(cursor)
    graph_data = TCPconnection.objects.annotate(retrans_sum = Sum('retrans'),  tx_errno_sum=Sum('tx_errno')).filter(connection_time__range=[time_thirtymin_ago, time_now])
    all_machines = Machines.objects.all()
    return render_to_response('recent_template1.html', {'my_list': connections,  'json_graph_data': lastthirtymin_graphs_data(graph_data),  'all_machines': all_machines}, context_instance=RequestContext(request))

def recent_query_for_one_machine(request):
    machine_requested = request.GET.get('machine_requested', '')
    time_now = datetime.now()
    time_thirtymin_ago = time.strftime("%Y-%m-%d %H:%M:%S", (time_now- timedelta(minutes=300)).timetuple())
    cursor = connection.cursor()
    cursor.execute("""(select server_id_id, connection_time, color, lcl, rmt, rx_errno_avg, tx_errno_avg, retrans_avg  from last_five_minutes_each_machine where server_id_id = %s) union (select server_id_id, connection_time, "red" as color, lcl, rmt, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  connections_serverconnections where server_id_id = %s and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and lcl NOT IN (select DISTINCT(lcl) from last_five_minutes_each_machine) group by lcl, rmt order by connection_time desc)""", (machine_requested, machine_requested))
    #connections_for_one_machine = dictfetchall(cursor)
    graph_data = TCPconnection.objects.annotate(retrans_sum = Sum('retrans'),  tx_errno_sum=Sum('tx_errno')).filter(connection_time__range=[time_thirtymin_ago, time_now])
    all_machines = Machines.objects.all()
    return HttpResponse(json.dumps(dictfetchall(cursor)),  mimetype = u'application/json')

def thirtyMinGraphsUpdate(request):
    time_now = datetime.now()
    time_onesec_ago = time.strftime("%Y-%m-%d %H:%M:%S", (time_now- timedelta(minutes=1)).timetuple())
    latest_thirtyMinGraph_array_retrans =[]
    latest_thirtyMinGraph_array_errno =[]
    latest_data = TCPconnection.objects.filter(connection_time__range=[time_onesec_ago, time_now]).annotate(retrans_sum = Sum('retrans'), tx_errno_sum = Sum('tx_errno') )
    latest_thirtyMinGraph_array_retrans.append([calendar.timegm(time_now.timetuple())*1000, latest_data['retrans_sum']])
    latest_thirtyMinGraph_array_errno.append([calendar.timegm(time_now.timetuple())*1000, latest_data['tx_errno_sum']])
    graph_update_list = [{'label': "retrans",  'data': latest_thirtyMinGraph_array_retrans}, {'label': "number_of_errors",  'data': latest_thirtyMinGraph_array_errno}]
    return HttpResponse(json.dumps(graph_update_list),  mimetype = u'application/json')

def dictfetchall_django(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def dictfetchall(cursor):
    final_list = []
    "Returns all rows from a cursor as a dict"
    desc = (('timestamp', '0'), ) + cursor.description
    new_desc =  desc[:2] + desc[3:]
    row = cursor.fetchall()
    list_with_timestamps = []
    for r in row:
       tuple0 = (time.mktime(r[1].timetuple())*1000, )
       print tuple0
       print"/n"
       print "r1"
       print r[1]
       tuple2 = tuple0+r
       tuple3 =  tuple2[:2] + tuple2[3:]
       list_with_timestamps.append(tuple3)
    for i in list_with_timestamps:
        zip_fieldname_withValue = dict(zip([col[0] for col in new_desc], i))
        final_list.append(zip_fieldname_withValue)
    return final_list

def statsUpdate(request):
    cursor = connection.cursor()
    cursor.execute('(select color, connection_time,  server_id_id, lcl, rmt, rx_errno_avg, tx_errno_avg, retrans_avg  from last_five_minutes_each_machine) union (select "red" as color, connection_time, server_id_id, lcl, rmt, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  connections_serverconnections where connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and rmt NOT IN (select rmt from last_five_minutes_each_machine) group by server_id_id, lcl, rmt order by connection_time desc)')
    return HttpResponse(json.dumps(dictfetchall(cursor)),  mimetype = u'application/json')
    #return HttpResponse(json.dumps(latest_dict_five),  mimetype = u'application/json')
    
def tableUpdate(request):
    time_now = datetime.now()
    time_onesec_ago = time.strftime("%Y-%m-%d %H:%M:%S", (time_now- timedelta(minutes=1)).timetuple())
    latest_dict ={}
    latest_data = TCPconnection.objects.filter(connection_time__range=[time_onesec_ago, time_now]).order_by('-connection_time')
    #latest('connection_time')
    for record in latest_data:
        #latest_timestamp = calendar.timegm(record.connection_time.timetuple())*1000
        latest_timestamp = time.strftime("%H:%M:%S", record.connection_time.timetuple())
        latest_connection = model_to_dict(record,  exclude=('connection_time', 'connection_date', 'flags'))
        latest_dict[latest_timestamp]=latest_connection
    #print latest_dict
       # latest_dict['data'].append(latest_connection)
    return HttpResponse(json.dumps(latest_dict),  mimetype = u'application/json')

def table_test(request):
    my_objects = TCPconnection.objects.filter(connection_date=date.today())
    connections = tuple(my_objects.order_by('-connection_time')[:200])
    return render_to_response('jqgrid_template.html', {'my_list': connections})

def graph_query(request):
    time_now = datetime.now()
    time_thirtymin_ago = time.strftime("%Y-%m-%d %H:%M:%S", (time_now - timedelta(minutes=30)).timetuple())
    my_objects = TCPconnection.objects.filter(connection_time__range=[time_thirtymin_ago, time_now]).values('lcl', 'rmt',  'rx_errno')
    connections = tuple(my_objects.exclude('connection_time')[:10])
    return HttpResponse(json.dumps(connections),  mimetype = u'application/json')

def graphs(request):
    global my_objects
    time_now = datetime.now()
    time_thirtymin_ago = time.strftime("%Y-%m-%d %H:%M:%S", (time_now- timedelta(minutes=30)).timetuple())
    my_objects = TCPconnection.objects.filter(connection_time__range=[time_thirtymin_ago, time_now])
    connections = tuple(my_objects.order_by('-connection_time')[:20])
    graph_data = graphs_data(my_objects, 'rttvar')
    #return HttpResponse(json.dumps(graph_data),  mimetype = u'application/json')
    #print graph_data
    #print str(my_objects.distinct().values_list('lcl'))
    return render_to_response('graph_template.html', {'graph_data':graph_data,'my_list': connections,  'json_graph_data':json.dumps(graph_data)}, context_instance=RequestContext(request))
    #return render_to_response('list_template.html', {'js_object':json.dumps(items),'my_list': items})

def graphs_data(django_objects, param_type):
    import calendar as calendar 
    parameter_type = param_type
    our_records = django_objects
    print type(our_records)
    final_list=[]
    final_dict = {}
    sockets_list =[]
    for record in our_records.values('lcl').distinct().order_by('lcl'):
        sockets_list.append(record['lcl'])
    for ip_address in sockets_list:
        sockets_values_dict={}
        socket_values=None
        sockets_values_dict['label']=str(ip_address) + ' = -0.00'
        for record in our_records.values('lcl',parameter_type,'connection_time'):
            if  record['lcl']==ip_address:
                if socket_values is None:
                    socket_values=[]
                    socket_values.append([calendar.timegm(record['connection_time'].timetuple())*1000, int(record[parameter_type])])
                else:
                    socket_values.append([calendar.timegm(record['connection_time'].timetuple())*1000, int(record[parameter_type])])
        sockets_values_dict['data']=socket_values
        final_list.append(sockets_values_dict)
        final_dict[str(ip_address)]=sockets_values_dict 
    return final_dict

def lastthirtymin_graphs_data(django_objects):
    our_records = django_objects
    #print type(our_records)
    errno_list =[]
    retrans_list=[]
    for record in our_records.values('connection_time', 'retrans_sum',  'tx_errno_sum'):
        retrans_list.append([calendar.timegm(record['connection_time'].timetuple())*1000, int(record['retrans_sum'])])
        errno_list.append([calendar.timegm(record['connection_time'].timetuple())*1000, int(record['tx_errno_sum'])])
    return [{'label': "retrans",  'data': retrans_list}, {'label': "number_of_errors",  'data': errno_list}]


def parameterSearch(request):
    print 'HELOOO'
    my_objects = getQueryObjects()
    graph_data = {}
    query = request.GET.get('parameter_type', '')
    if query:
        graph_data=graphs_data(my_objects, query)
    else:
        print 'ERROR'
    print graph_data
    return HttpResponse(json.dumps(graph_data))

def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['katya@pigottfamily.org']
            if cc_myself:
                recipients.append(sender)
            from django.core.mail import send_mail
            send_mail(subject, message, sender, recipients)
            form.save()
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact_template.html', {
        'form': form,
    })

def machines(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MachinesForm(request.POST) # A form bound to the POST data
        print("Machines1 form hello")
        print(form.is_valid())
        if form.is_valid(): # All validation rules pass
            server_id = form.cleaned_data['server_id']
            ip_address = form.cleaned_data['ip_address']
            print("Machines2 form hello")
            form.save()
            return HttpResponseRedirect('/machine_added/')
            #return HttpResponseRedirect('/machine_added/') # Redirect after POST
    else:
        print("Machines3 form hello")
        form = MachinesForm() # An unbound form
    all_machines = Machines.objects.all()
    return render(request, 'add_machine_template.html', {
        'form': form, 'all_machines': all_machines, 
    })
    
def machine_added(request):
    return render_to_response('machine_added.html')
 
