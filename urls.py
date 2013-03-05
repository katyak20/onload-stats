from django.conf.urls.defaults import patterns, include, url
from monitor.views import graphs, graph_query, hello, table_main, recent_query, recent_query_for_one_machine,  datepickerExample, table_test,  tableUpdate,  statsUpdate, thirtyMinGraphsUpdate, machines, machine_added, contact, thanks# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.conf import settings


urlpatterns = patterns('',
    (r'^graphs/$', graphs),
    (r'^$',   recent_query), 
    (r'^hello/$',  hello), 
    (r'^table/$',  table_test), 
    (r'^stats/$', table_main),
    (r'^query_one_machine/$', recent_query_for_one_machine),
    (r'^machines/$', machines),
    (r'^machine_added/$', machine_added),
    (r'^datepicker/$', datepickerExample),
    (r'^contact/$',  contact),
    (r'^thanks/$', thanks),
    (r'^admin/', include(admin.site.urls)),
    (r'^graph_query/$', 'monitor.views.graph_query'),
    (r'^parameterSearch/$', 'monitor.views.parameterSearch'),
    (r'^statsUpdate/$', 'monitor.views.statsUpdate'),
    #(r'^statsForOneMachine/$', 'monitor.views.statsForOneMachine'),
    (r'^tableUpdate/$', 'monitor.views.tableUpdate'),
    (r'^thirtyMinGraphsUpdate/$', 'monitor.views.thirtyMinGraphsUpdate'),
    # Examples:
    # url(r'^$', 'monitor.views.home', name='home'),
    # url(r'^monitor/', include('monitor.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.STATIC_DOC_ROOT}),
   )
