(select 'red' as color, rmt, connection_time,  avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) group by rmt order by connection_time desc)  union ( select 'green' as color, rmt, connection_time, avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by rmt order by connection_time DESC)



(select 'green' as color, rmt, connection_time, avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by rmt order by connection_time DESC) union (select 'red' as color, rmt, connection_time,  avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and rmt NOT IN 
(select rmt from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by rmt) group by rmt order by connection_time desc)


create view last_five_minutes as select 'green' as color, rmt, connection_time, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by rmt order by connection_time DESC



(select color, rmt, rx_errno_avg, tx_errno_avg, retrans_avg  from last_five_minutes) union (select "red" as color, rmt, avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and rmt NOT IN (select rmt from last_five_minutes) group by rmt order by connection_time desc)
