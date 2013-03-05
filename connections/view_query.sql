(select 'red' as color, rmt, connection_time,  avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) group by rmt order by connection_time desc)  union ( select 'green' as color, rmt, connection_time, avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by rmt order by connection_time DESC)



(select 'green' as color, rmt, connection_time, avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by rmt order by connection_time DESC) union (select 'red' as color, rmt, connection_time,  avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and rmt NOT IN 
(select rmt from  connections_tcpconnection where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by rmt) group by rmt order by connection_time desc)

create view last_five_minutes as select 'green' as color, lcl, rmt, connection_time, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  connections_serverconnections where connection_date=curdate() and connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by rmt order by connection_time DESC

create view last_five_minutes_each_machine as select 'green' as color, server_id_id, lcl, rmt, connection_time, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  connections_serverconnections where connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by server_id_id, lcl, rmt  order by connection_time DESC

create view last_five_minutes_each_machine_new as select 'green' as color, server_id_id, lcl, rmt, connection_time, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  serverconnections_new where connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by server_id_id, lcl, rmt  order by connection_time DESC


(select color, rmt, rx_errno_avg, tx_errno_avg, retrans_avg  from last_five_minutes) union (select "red" as color, rmt, avg(rx_errno), avg(tx_errno), avg(retrans) from  connections_tcpconnection where connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and rmt NOT IN (select rmt from last_five_minutes) group by rmt order by connection_time desc)


(select server_id_id, connection_time, color, lcl, rmt, rx_errno_avg, tx_errno_avg, retrans_avg  from last_five_minutes_each_machine where server_id_id = %s) union (select server_id_id, connection_time, "red" as color, lcl, rmt, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  connections_serverconnections where server_id_id = %s and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and lcl NOT IN (select DISTINCT(lcl) from last_five_minutes_each_machine) group by lcl, rmt order by connection_time desc)



select 'green' as color, server_id_id, lcl, rmt, connection_time, rx_errno, 
tx_errno, retrans from  connections_serverconnections 
where connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() connection_time DESC

 select 'green' as color, server_id_id, lcl, rmt, connection_time, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  connections_serverconnections where connection_time BETWEEN TIMESTAMPADD(minute, -5, now()) AND now() group by server_id_id, lcl, rmt  order by connection_time DESC
