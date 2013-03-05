from django.db import IntegrityError
import subprocess
import datetime
from itertools import dropwhile, islice
import MySQLdb
from monitor.connections.models import Item, TCPconnection,  ServerConnections, Machines
from datetime import datetime, date
import os

def ParcedTCP(output):
    str_list = []
    my_str = []
    new_str = []
    temporary_list = []
    TCP_lcl = 0
    table_index = 0  
    row_index = 0
    TCP_parameter_number = 0
    number_of_TCP_connections = 0
    row_dict = {}
    for i, line in enumerate(output, 1):
      #print i,  line  
      if i == 1:
        str_list = line.splitlines()
    for i, line in enumerate(str_list, 1):
      #Goes through stuckdamp_output line_by_line
      #print i,  line
      if 'lcl' in line:
        TCP_lcl = i
        my_str.append(line) 
      line_difference = i - TCP_lcl  
      if 0 < line_difference < 20:
        my_str.append(line)
    new_str = list(islice(my_str, 19, None))
    connection_id = 0
    for i, line in enumerate(new_str):
      #print 'the row to be processed',  i,  line  
      if 'TCP ' in line:
          connection_id +=1 
      element = line.split(' ')
      for y, x in enumerate(element):
        if x == 'TCP':
            #print 'i+y', i+y, '    x',  x
            temporary_list = list(x)
            #print temporary_list
        else:
            #print '   x',  x
            #row_dict[connection_id].append(x)
            temporary_list.append(x)
            #print'else ',  temporary_list
      row_dict[connection_id] = temporary_list
      print connection_id
    #for key in row_dict:
     #   print key,  row_dict[key]
    return row_dict 

def data_save():
    onload_process = subprocess.Popen(['onload_stackdump','lots'], stdout = subprocess.PIPE)
    out = onload_process.communicate()
    #print out
    TCP_splitted = ParcedTCP(out) #.split('TCP')
    database_insert(TCP_splitted)
    database_insert_new(TCP_splitted, 1)
    database_insert_new(TCP_splitted, 2)
    database_insert_new(TCP_splitted, 23)
    database_insert_new(TCP_splitted, 3)
    
def database_insert(tcp_parameters):
    for key, socket_value in tcp_parameters.items():
        par_dict = {}
        par_dict[62]= []
        for element in socket_value:
          if element == '':
            continue
          elif '=' in element:
            splitted_el = element.split('=')
            if splitted_el[0] =='lcl':
              par_dict[1] = splitted_el[1]
            elif splitted_el[0] =='rmt':
              par_dict[2] = splitted_el[1]
            elif splitted_el[0] =='rx_wake':
              par_dict[3] = splitted_el[1]
            elif splitted_el[0] =='tx_wake':
              par_dict[4] = splitted_el[1]
            elif splitted_el[0] =='rcvbuf':
              par_dict[5] = splitted_el[1]
            elif splitted_el[0] =='sndbuf':
              par_dict[6] = splitted_el[1]
            elif splitted_el[0] =='bindtodev':
              par_dict[7] = splitted_el[1]
            elif splitted_el[0] =='ttl':
              par_dict[8] = splitted_el[1]
            elif splitted_el[0] =='rcvtime0_ms':
              par_dict[9] = splitted_el[1]
            elif splitted_el[0] =='sndtimeo_ms':
              par_dict[10] = splitted_el[1]
            elif splitted_el[0] =='rx_errno':
              par_dict[11] = splitted_el[1]
            elif splitted_el[0] =='tx_errno':
              par_dict[12] = splitted_el[1]
            elif splitted_el[0] =='so_error':
              par_dict[13] = splitted_el[1]
            elif splitted_el[0] =='up':
              par_dict[14] = splitted_el[1]
            elif splitted_el[0] =='una-nxt-max':
              par_dict[15] = splitted_el[1]
            elif splitted_el[0] =='enq':
              par_dict[16] = splitted_el[1]
            elif splitted_el[0] =='send':
              par_dict[17] = splitted_el[1]
            elif splitted_el[0] =='send+pre':
              par_dict[18] = splitted_el[1]
            elif splitted_el[0] =='inflight':
              par_dict[19] = splitted_el[1]
            elif splitted_el[0] =='wnd':
              par_dict[20] = splitted_el[1]
            elif splitted_el[0] =='unused':
              par_dict[21] = splitted_el[1]
            elif splitted_el[0] =='cwnd':
              par_dict[22] = splitted_el[1]
            elif splitted_el[0] =='used':
              par_dict[23] = splitted_el[1]
            elif splitted_el[0] =='ssthresh':
              par_dict[24] = splitted_el[1]
            elif splitted_el[0] =='bytes_acked':
              par_dict[25] = splitted_el[1]
            elif splitted_el[0] =='if':
              par_dict[26] = splitted_el[1] 
            elif splitted_el[0] =='mtu':
              par_dict[27] = splitted_el[1]
            elif splitted_el[0] =='intf_i':
              par_dict[28] = splitted_el[1]
            elif splitted_el[0] =='vlan':
              par_dict[29] = splitted_el[1]  
            elif splitted_el[0] =='encap':
              par_dict[30] = splitted_el[1]
            elif splitted_el[0] =='rwnd':
              par_dict[31] = splitted_el[1]
            elif splitted_el[0] =='cwnd':
              par_dict[32] = splitted_el[1]
            elif splitted_el[0] =='nagle':
              par_dict[33] = splitted_el[1]
            elif splitted_el[0] =='more':
              par_dict[34] = splitted_el[1]
            elif splitted_el[0] =='app':
              par_dict[35] = splitted_el[1]
            elif splitted_el[0] =='nxt-max':
              par_dict[36] = splitted_el[1]
            elif splitted_el[0] =='current':
              par_dict[37] = splitted_el[1]
            elif splitted_el[0] =='rob_n':
              par_dict[38] = splitted_el[1]
            elif splitted_el[0] =='recv1_n':
              par_dict[39] = splitted_el[1]
            elif splitted_el[0] =='recv2_n':
              par_dict[40] = splitted_el[1]
            elif splitted_el[0] =='adv':
              par_dict[41] = splitted_el[1]
            elif splitted_el[0] =='cur':
              par_dict[42] = splitted_el[1]
            elif splitted_el[0] =='usr':
              par_dict[43] = splitted_el[1]
            elif splitted_el[0] =='eff_mss':
              par_dict[44] = splitted_el[1]
            elif splitted_el[0] =='smss':
              par_dict[45] = splitted_el[1]
            elif splitted_el[0] =='amss':
              par_dict[46] = splitted_el[1]
            elif splitted_el[0] =='used_bufs':
              par_dict[47] = splitted_el[1]
            elif splitted_el[0] =='uid':
              par_dict[48] = splitted_el[1]
            elif splitted_el[0] =='s':
              par_dict[49] = splitted_el[1]
            elif splitted_el[0] =='r':
              par_dict[50] = splitted_el[1]
            elif splitted_el[0] =='srtt':
              par_dict[51] = splitted_el[1]
            elif splitted_el[0] =='rttvar':
              par_dict[52] = splitted_el[1]
            elif splitted_el[0] =='rto':
              par_dict[53] = splitted_el[1]
            elif splitted_el[0] =='zwins':
              par_dict[54] = splitted_el[1]
            elif splitted_el[0] =='retrans':
              par_dict[55] = splitted_el[1]
            elif splitted_el[0] =='dupacks':
              par_dict[56] = splitted_el[1]
            elif splitted_el[0] =='rtos':
              par_dict[57] = splitted_el[1]
            elif splitted_el[0] =='frecs':
              par_dict[58] = splitted_el[1]
            elif splitted_el[0] =='seqerr':
              par_dict[59] = splitted_el[1]
            elif splitted_el[0] =='ooo_pkts':
              par_dict[60] = splitted_el[1]
            elif splitted_el[0] =='ooo':
              par_dict[61] = splitted_el[1]       
          else:
            par_dict[62].append(element)
   # tcp = Item(row_id = 1, data = par_dict[2])
        tcp = TCPconnection(connection_time=datetime.now(), connection_date=date.today(), lcl=par_dict[1], rmt=par_dict[2], rx_wake=par_dict[3], tx_wake=par_dict[4], rcvbuf=par_dict[5], sndbuf=par_dict[6], bindtodev=par_dict[7], ttl=par_dict[8], rcvtimeo_ms=1000, sndtimeo_ms=1000, rx_errno=par_dict[11], tx_errno=par_dict[12], so_errno=par_dict[13], up=par_dict[14], una_nxt_max=par_dict[15], enq=par_dict[16], send=par_dict[17], send_pre=par_dict[18], inflight=par_dict[19], wnd=par_dict[20], unused=par_dict[21], cwnd_0=par_dict[22], used=par_dict[23], ssthresh=par_dict[24], bytes_acked=par_dict[25], iff=par_dict[26], mtu=par_dict[27], intf_i=par_dict[28], vlan=par_dict[29], encap=par_dict[30], rwnd=par_dict[31], cwnd=9, nagle=par_dict[33], more=par_dict[34], app=par_dict[35], nxt_max=par_dict[36], current=par_dict[37], rob_n=par_dict[38], recv1_n=par_dict[39], recv2_n=par_dict[40], adv=par_dict[41], cur=par_dict[42], usr=par_dict[43], eff_mss=par_dict[44], smss=par_dict[45], amss=par_dict[46], used_bufs=par_dict[47], uid=par_dict[48], sss=par_dict[49], rrr=par_dict[50], srtt=par_dict[51], rttvar=par_dict[52], rto=par_dict[53], zwins=par_dict[54], retrans=par_dict[55], dupacks=par_dict[56], rtos=par_dict[57], frecs=par_dict[58], seqerr=par_dict[59], ooo_pkts=par_dict[60], ooo=par_dict[61], flags=par_dict[62])
        try:
            tcp.save()
            print 'Insert successful'
        except MySQLdb.IntegrityError, message:
            errorcode = message[0]
            return render_to_response('500.html', {'my_list': errorcode})
            
def database_insert_new(tcp_parameters, machine_id):
    for key, socket_value in tcp_parameters.items():
        par_dict = {}
        par_dict[62]= []
        for element in socket_value:
          if element == '':
            continue
          elif '=' in element:
            splitted_el = element.split('=')
            if splitted_el[0] =='lcl':
              par_dict[1] = splitted_el[1]
            elif splitted_el[0] =='rmt':
              par_dict[2] = splitted_el[1]
            elif splitted_el[0] =='rx_wake':
              par_dict[3] = splitted_el[1]
            elif splitted_el[0] =='tx_wake':
              par_dict[4] = splitted_el[1]
            elif splitted_el[0] =='rcvbuf':
              par_dict[5] = splitted_el[1]
            elif splitted_el[0] =='sndbuf':
              par_dict[6] = splitted_el[1]
            elif splitted_el[0] =='bindtodev':
              par_dict[7] = splitted_el[1]
            elif splitted_el[0] =='ttl':
              par_dict[8] = splitted_el[1]
            elif splitted_el[0] =='rcvtime0_ms':
              par_dict[9] = splitted_el[1]
            elif splitted_el[0] =='sndtimeo_ms':
              par_dict[10] = splitted_el[1]
            elif splitted_el[0] =='rx_errno':
              par_dict[11] = splitted_el[1]
            elif splitted_el[0] =='tx_errno':
              par_dict[12] = splitted_el[1]
            elif splitted_el[0] =='so_error':
              par_dict[13] = splitted_el[1]
            elif splitted_el[0] =='up':
              par_dict[14] = splitted_el[1]
            elif splitted_el[0] =='una-nxt-max':
              par_dict[15] = splitted_el[1]
            elif splitted_el[0] =='enq':
              par_dict[16] = splitted_el[1]
            elif splitted_el[0] =='send':
              par_dict[17] = splitted_el[1]
            elif splitted_el[0] =='send+pre':
              par_dict[18] = splitted_el[1]
            elif splitted_el[0] =='inflight':
              par_dict[19] = splitted_el[1]
            elif splitted_el[0] =='wnd':
              par_dict[20] = splitted_el[1]
            elif splitted_el[0] =='unused':
              par_dict[21] = splitted_el[1]
            elif splitted_el[0] =='cwnd':
              par_dict[22] = splitted_el[1]
            elif splitted_el[0] =='used':
              par_dict[23] = splitted_el[1]
            elif splitted_el[0] =='ssthresh':
              par_dict[24] = splitted_el[1]
            elif splitted_el[0] =='bytes_acked':
              par_dict[25] = splitted_el[1]
            elif splitted_el[0] =='if':
              par_dict[26] = splitted_el[1] 
            elif splitted_el[0] =='mtu':
              par_dict[27] = splitted_el[1]
            elif splitted_el[0] =='intf_i':
              par_dict[28] = splitted_el[1]
            elif splitted_el[0] =='vlan':
              par_dict[29] = splitted_el[1]  
            elif splitted_el[0] =='encap':
              par_dict[30] = splitted_el[1]
            elif splitted_el[0] =='rwnd':
              par_dict[31] = splitted_el[1]
            elif splitted_el[0] =='cwnd':
              par_dict[32] = splitted_el[1]
            elif splitted_el[0] =='nagle':
              par_dict[33] = splitted_el[1]
            elif splitted_el[0] =='more':
              par_dict[34] = splitted_el[1]
            elif splitted_el[0] =='app':
              par_dict[35] = splitted_el[1]
            elif splitted_el[0] =='nxt-max':
              par_dict[36] = splitted_el[1]
            elif splitted_el[0] =='current':
              par_dict[37] = splitted_el[1]
            elif splitted_el[0] =='rob_n':
              par_dict[38] = splitted_el[1]
            elif splitted_el[0] =='recv1_n':
              par_dict[39] = splitted_el[1]
            elif splitted_el[0] =='recv2_n':
              par_dict[40] = splitted_el[1]
            elif splitted_el[0] =='adv':
              par_dict[41] = splitted_el[1]
            elif splitted_el[0] =='cur':
              par_dict[42] = splitted_el[1]
            elif splitted_el[0] =='usr':
              par_dict[43] = splitted_el[1]
            elif splitted_el[0] =='eff_mss':
              par_dict[44] = splitted_el[1]
            elif splitted_el[0] =='smss':
              par_dict[45] = splitted_el[1]
            elif splitted_el[0] =='amss':
              par_dict[46] = splitted_el[1]
            elif splitted_el[0] =='used_bufs':
              par_dict[47] = splitted_el[1]
            elif splitted_el[0] =='uid':
              par_dict[48] = splitted_el[1]
            elif splitted_el[0] =='s':
              par_dict[49] = splitted_el[1]
            elif splitted_el[0] =='r':
              par_dict[50] = splitted_el[1]
            elif splitted_el[0] =='srtt':
              par_dict[51] = splitted_el[1]
            elif splitted_el[0] =='rttvar':
              par_dict[52] = splitted_el[1]
            elif splitted_el[0] =='rto':
              par_dict[53] = splitted_el[1]
            elif splitted_el[0] =='zwins':
              par_dict[54] = splitted_el[1]
            elif splitted_el[0] =='retrans':
              par_dict[55] = splitted_el[1]
            elif splitted_el[0] =='dupacks':
              par_dict[56] = splitted_el[1]
            elif splitted_el[0] =='rtos':
              par_dict[57] = splitted_el[1]
            elif splitted_el[0] =='frecs':
              par_dict[58] = splitted_el[1]
            elif splitted_el[0] =='seqerr':
              par_dict[59] = splitted_el[1]
            elif splitted_el[0] =='ooo_pkts':
              par_dict[60] = splitted_el[1]
            elif splitted_el[0] =='ooo':
              par_dict[61] = splitted_el[1]       
          else:
            par_dict[62].append(element)
        #print(socket_value)
        #print(machine_id,  datetime.now(),  par_dict[1])
        machine = Machines.objects.get(server_id=machine_id)
        tcp = ServerConnections(server_id=machine, connection_time=datetime.now(), connection_date=date.today(), lcl=par_dict[1], rmt=par_dict[2], rx_wake=par_dict[3], tx_wake=par_dict[4], rcvbuf=par_dict[5], sndbuf=par_dict[6], bindtodev=par_dict[7], ttl=par_dict[8], rcvtimeo_ms=1000, sndtimeo_ms=1000, rx_errno=par_dict[11], tx_errno=par_dict[12], so_errno=par_dict[13], up=par_dict[14], una_nxt_max=par_dict[15], enq=par_dict[16], send=par_dict[17], send_pre=par_dict[18], inflight=par_dict[19], wnd=par_dict[20], unused=par_dict[21], cwnd_0=par_dict[22], used=par_dict[23], ssthresh=par_dict[24], bytes_acked=par_dict[25], iff=par_dict[26], mtu=par_dict[27], intf_i=par_dict[28], vlan=par_dict[29], encap=par_dict[30], rwnd=par_dict[31], cwnd=9, nagle=par_dict[33], more=par_dict[34], app=par_dict[35], nxt_max=par_dict[36], current=par_dict[37], rob_n=par_dict[38], recv1_n=par_dict[39], recv2_n=par_dict[40], adv=par_dict[41], cur=par_dict[42], usr=par_dict[43], eff_mss=par_dict[44], smss=par_dict[45], amss=par_dict[46], used_bufs=par_dict[47], uid=par_dict[48], sss=par_dict[49], rrr=par_dict[50], srtt=par_dict[51], rttvar=par_dict[52], rto=par_dict[53], zwins=par_dict[54], retrans=par_dict[55], dupacks=par_dict[56], rtos=par_dict[57], frecs=par_dict[58], seqerr=par_dict[59], ooo_pkts=par_dict[60], ooo=par_dict[61], flags=par_dict[62])
        try:
            tcp.save()
            print 'ServerConnections Insert successful'
        except MySQLdb.IntegrityError, message:
            errorcode = message[0]
            return render_to_response('500.html', {'my_list': errorcode})
            
