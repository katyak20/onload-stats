import sys
import os

from django.core.management import setup_environ
import settings
setup_environ(settings)

from monitor.tcp_parameters import data_save

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    data_save()

if __name__ == '__main__':
    main()
