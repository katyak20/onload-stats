CREATE INDEX connections_serverconnections_server_time_index ON connections_serverconnections(server_id, connection_time);


alter table connections_serverconnections modify id INT not null;
alter table connections_serverconnections drop primary key;
alter table connections_serverconnections add primary key(server_id_id, connection_time, rmt, lcl);
alter table connections_serverconnections drop id;



create index txerrno_rxerrno_retrans_index on connections_serverconnections(server_id_id, tx_errno, rx_errno, retrans);
create index machine_id_index on connections_serverconnections(server_id_id);
drop index machine_id_index on connections_serverconnections;


create TABLE serverconnections_new LIKE connections_serverconnections;


INSERT serverconnections_new SELECT * FROM connections_serverconnections;

alter table serverconnections_new ADD id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

INSERT INTO serverconnections_new(server_id_id, connection_time, connection_date, lcl, rmt, rx_wake, tx_wake, rcvbuf, sndbuf, bindtodev, ttl, rcvtimeo_ms, sndtimeo_ms, rx_errno, tx_errno, so_errno, up, una_nxt_max, enq, send, send_pre, inflight, wnd, unused, cwnd_0, used, ssthresh, bytes_acked, iff, mtu, intf_i, vlan, encap, rwnd, cwnd, nagle, more, app, nxt_max, current, rob_n, recv1_n, recv2_n, adv, cur, usr, eff_mss, smss, amss, used_bufs, uid, sss, rrr, srtt, rttvar, rto, zwins, retrans, dupacks, rtos, frecs, seqerr, ooo_pkts, ooo, flags) 
SELECT server_id_id, connection_time, connection_date, lcl, rmt, rx_wake, tx_wake, rcvbuf, sndbuf, bindtodev, ttl, rcvtimeo_ms, sndtimeo_ms, rx_errno, tx_errno, so_errno, up, una_nxt_max, enq, send, send_pre, inflight, wnd, unused, cwnd_0, used, ssthresh, bytes_acked, iff, mtu, intf_i, vlan, encap, rwnd, cwnd, nagle, more, app, nxt_max, current, rob_n, recv1_n, recv2_n, adv, cur, usr, eff_mss, smss, amss, used_bufs, uid, sss, rrr, srtt, rttvar, rto, zwins, retrans, dupacks, rtos, frecs, seqerr, ooo_pkts, ooo, flags FROM connections_serverconnections;


(select server_id_id, connection_time, color, lcl, rmt, rx_errno_avg, tx_errno_avg, retrans_avg  from last_five_minutes_each_machine_new where server_id_id = '2') union (select server_id_id, connection_time, "red" as color, lcl, rmt, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  serverconnections_new where server_id_id = '2' and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and lcl NOT IN (select DISTINCT(lcl) from last_five_minutes_each_machine) group by lcl, rmt order by connection_time desc);


create index txerrno_rxerrno_retrans_index_new on serverconnections_new(server_id_id, connection_time, lcl, rmt, rx_errno, tx_errno, retrans);

create index txerrno_rxerrno_retrans_index_new on serverconnections_new(server_id_id, connection_time, lcl, rmt, rx_errno, tx_errno, retrans);
create index machine_id_index_new on serverconnections_new(server_id_id);
create index lcl_index_new on serverconnections_new(lcl);


(select server_id_id, connection_time, color, lcl, rmt, rx_errno_avg, tx_errno_avg, retrans_avg  from last_five_minutes_each_machine_new where server_id_id = '2') union (select server_id_id, connection_time, "red" as color, lcl, rmt, avg(rx_errno) as rx_errno_avg, avg(tx_errno) as tx_errno_avg, avg(retrans) as retrans_avg from  serverconnections_new where server_id_id = '2' and connection_time BETWEEN TIMESTAMPADD(minute, -30, now()) AND TIMESTAMPADD(minute, -5, now()) and lcl NOT IN (select DISTINCT(lcl) from last_five_minutes_each_machine_new) group by lcl, rmt order by connection_time desc);
