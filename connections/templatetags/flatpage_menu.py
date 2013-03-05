from django.template import Library, Node
register = Library()
import itertools
import collections

def flatpage_menu():
    # Create an unordered list of all flatpages
    #pages = FlatPage.objects.all()
    pages = {}
    pages['Realtime performance'] = '/'
    pages['Onload stats'] = '/stats/'
    pages['Graphs'] = '/graphs/'
    pages['Machines'] = '/machines/'
    pages['Contact'] ='/contact/'
    d = collections.OrderedDict((('Realtime performance','/'),  ('Onload stats','/stats/'), ('Graphs',  '/graphs/'), ('Machines','/machines/'), ('Contact','/contact/'))) 
    x = itertools.islice(d.items(), 0, 5)

    menu =    menu = '<div class="navbar navbar-fixed-top"> <div class="navbar-inner"> <div class="container"> <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse"> <span class="icon-bar"></span> <span class="icon-bar"></span> <span class="icon-bar"></span> </a> <div class="nav-collapse"> <ul class="nav">'
    for k,  v in x:
        menu += '<li>'+'<a href="'+ v +'" title="'+k+'">'+k+'</a></li>'
    menu += '</ul> </div><!--/.nav-collapse --> </div> </div> </div>'
    return menu 

register.simple_tag(flatpage_menu)
