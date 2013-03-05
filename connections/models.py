from django.db import models 
from django.forms import ModelForm
from django import forms

TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)

class Item(models.Model):
    row_id = models.IntegerField()
    data = models.CharField(max_length=40)
    
class Contact(models.Model):
    topic = models.CharField(max_length=30,  choices=TOPIC_CHOICES)
    sender = models.EmailField()
    message = models.CharField(max_length=30)
    cc_myself = models.BooleanField()

class ContactForm(ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows':'4'}))
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Contact

class Machines(models.Model):
    server_id =  models.CharField(max_length=30,  primary_key=True)
    ip_address =models.GenericIPAddressField()
    

class MachinesForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Machines

class TCPconnection(models.Model):
    connection_time = models.DateTimeField(primary_key=True)
    connection_date = models.DateField(db_index=True)
    lcl = models.CharField(max_length=30)
    rmt = models.CharField(max_length=30)
    rx_wake = models.CharField(max_length=30)
    tx_wake = models.CharField(max_length=30)
    rcvbuf = models.IntegerField()
    sndbuf = models.IntegerField()
    bindtodev = models.CharField(max_length=20)
    ttl = models.IntegerField()
    rcvtimeo_ms = models.IntegerField()
    sndtimeo_ms = models.IntegerField()
    rx_errno = models.IntegerField()
    tx_errno = models.IntegerField()
    so_errno = models.IntegerField()
    up = models.CharField(max_length=8)
    una_nxt_max = models.CharField(max_length=40)
    enq = models.CharField(max_length=8)
    send = models.CharField(max_length=10)
    send_pre = models.IntegerField()
    inflight = models.CharField(max_length=10)
    wnd = models.IntegerField()
    unused = models.IntegerField()
    cwnd_0 = models.CharField(max_length=15)
    used = models.IntegerField()
    ssthresh = models.IntegerField()
    bytes_acked = models.IntegerField()
    iff = models.IntegerField()
    mtu = models.IntegerField()
    intf_i = models.IntegerField()
    vlan = models.IntegerField()
    encap = models.IntegerField()
    rwnd = models.IntegerField()
    cwnd = models.IntegerField()
    nagle = models.IntegerField()
    more = models.IntegerField()
    app = models.IntegerField()
    nxt_max = models.CharField(max_length=20)
    current = models.CharField(max_length=9)
    rob_n = models.IntegerField()
    recv1_n = models.IntegerField()
    recv2_n = models.IntegerField()
    adv = models.IntegerField()
    cur = models.IntegerField()
    usr = models.IntegerField()
    eff_mss = models.IntegerField()
    smss = models.IntegerField()
    amss = models.IntegerField()
    used_bufs = models.SmallIntegerField()
    uid = models.IntegerField()
    sss = models.IntegerField()
    rrr = models.IntegerField()
    srtt = models.IntegerField()
    rttvar = models.IntegerField()
    rto = models.IntegerField()
    zwins = models.CharField(max_length=10)
    retrans =  models.SmallIntegerField()
    dupacks = models.IntegerField()
    rtos = models.IntegerField()
    frecs = models.IntegerField()
    seqerr = models.CharField(max_length=10)
    ooo_pkts = models.IntegerField()
    ooo = models.IntegerField()
    flags = models.CharField(max_length=400)
    
class ServerConnections(models.Model):
    server_id = models.ForeignKey(Machines, to_field = 'server_id')
    connection_time = models.DateTimeField()
    connection_date = models.DateField()
    lcl = models.CharField(max_length=30)
    rmt = models.CharField(max_length=30)
    rx_wake = models.CharField(max_length=30)
    tx_wake = models.CharField(max_length=30)
    rcvbuf = models.IntegerField()
    sndbuf = models.IntegerField()
    bindtodev = models.CharField(max_length=20)
    ttl = models.IntegerField()
    rcvtimeo_ms = models.IntegerField()
    sndtimeo_ms = models.IntegerField()
    rx_errno = models.IntegerField()
    tx_errno = models.IntegerField()
    so_errno = models.IntegerField()
    up = models.CharField(max_length=8)
    una_nxt_max = models.CharField(max_length=40)
    enq = models.CharField(max_length=8)
    send = models.CharField(max_length=10)
    send_pre = models.IntegerField()
    inflight = models.CharField(max_length=10)
    wnd = models.IntegerField()
    unused = models.IntegerField()
    cwnd_0 = models.CharField(max_length=15)
    used = models.IntegerField()
    ssthresh = models.IntegerField()
    bytes_acked = models.IntegerField()
    iff = models.IntegerField()
    mtu = models.IntegerField()
    intf_i = models.IntegerField()
    vlan = models.IntegerField()
    encap = models.IntegerField()
    rwnd = models.IntegerField()
    cwnd = models.IntegerField()
    nagle = models.IntegerField()
    more = models.IntegerField()
    app = models.IntegerField()
    nxt_max = models.CharField(max_length=20)
    current = models.CharField(max_length=9)
    rob_n = models.IntegerField()
    recv1_n = models.IntegerField()
    recv2_n = models.IntegerField()
    adv = models.IntegerField()
    cur = models.IntegerField()
    usr = models.IntegerField()
    eff_mss = models.IntegerField()
    smss = models.IntegerField()
    amss = models.IntegerField()
    used_bufs = models.SmallIntegerField()
    uid = models.IntegerField()
    sss = models.IntegerField()
    rrr = models.IntegerField()
    srtt = models.IntegerField()
    rttvar = models.IntegerField()
    rto = models.IntegerField()
    zwins = models.CharField(max_length=10)
    retrans =  models.SmallIntegerField()
    dupacks = models.IntegerField()
    rtos = models.IntegerField()
    frecs = models.IntegerField()
    seqerr = models.CharField(max_length=10)
    ooo_pkts = models.IntegerField()
    ooo = models.IntegerField()
    flags = models.CharField(max_length=400)

# Create your models here.