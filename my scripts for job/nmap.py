#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
import nmap
import sqlite3
import subprocess
from ipaddress import IPv4Network as net
from ipaddress import IPv4Address as addr
from tabulate import tabulate
from pdb import set_trace as bt
import socket
from slacker import Slacker

SLACK_CHANEL = ''
SLACK_TOKEN = ''
NOTFICATIONS_SLACK = 1

class DB:
    def __init__(self,name):
        self.name = name
        self.conn = None

    def connect(self):
        if not self.conn:
            try:
                self.conn = sqlite3.connect(self.name)
            except Exception as e:
                print("DB error: {0}".format(e))
                sys.exit()

    def close(self):
        self.conn.close()

    def query(self, sql, values=()):
        self.connect()
        c = self.conn.cursor()
        c.execute(sql, values)
        self.conn.commit()
        return c.fetchall()

    def schema(self):
        sql = "CREATE TABLE IF NOT EXISTS now( \
               host INTEGER UNIQUE NOT NULL, state INTEGER DEFAULT 0, \
               udp TEXT, tcp TEXT);"
        self.query(' '.join(sql.split()))
        sql = "CREATE TABLE IF NOT EXISTS last( \
               host INTEGER UNIQUE NOT NULL, state INTEGER DEFAULT 0, \
               udp TEXT, tcp TEXT);"
        self.query(' '.join(sql.split()))


def getHosts(file):
    hosts = []
    try:
        with codecs.open(file, encoding='utf8') as f:
            targets = f.readlines()
    except:
        print('Error in reading a Hosts File')
        sys.exit(1)
    for target in targets:
#        bt()
        t = target.strip()
        try:
            net(t)
        except Exception as e:
            t= socket.gethostbyname(t).strip()

        if not t.startswith("#"):
            hosts += [str(addr) for addr in net(t) if 
                      (addr != net(t).network_address and 
                        addr != net(t).broadcast_address) or
                      net(t).prefixlen == 32]
    return hosts

def ping(host):
    #print("ping of {0}".format(host))
    #ping = subprocess.Popen('/bin/ping -q -c3 -W1 {0} >/dev/null'.format(host)
    #               ,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # for LINUX
    ping = subprocess.Popen('ping -w 1 -n 3 '+host,stdout=subprocess.PIPE) # for WINDOWS
    ping.wait()
    print(str(not ping.poll()))
    return not ping.poll() # for WINDOWS
    #return not ping.returncode # for LINUX

def scan(host):
    
    #print("scan of {0}".format(host))
    try:
        nm = nmap.PortScanner()         # instantiate nmap.PortScanner object
    except nmap.PortScannerError:
        print('Nmap not found', sys.exc_info()[0])
        sys.exit(1)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(1)
    #nm.scan(hosts=host, arguments='-sT -sU -Pn -p U:22-443,T:22-443')
    #nm.scan(host, '22-25')
    nm.scan(hosts=host, arguments='-sT -sU')
    #nm.scan(hosts=host, arguments='-sT -sU -Pn')
    #nm.scan(host, arguments='-sS -sU -T4 -A -v -p U:22-443,T:22-443')
    #nm.scan(host, '22-443')
    if not nm.all_hosts():
        print('scan of {0} is failed'.format(host))
        return None
    
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        if 'tcp' in nm[host].keys():
            tcp = [str(port) for port in nm[host]['tcp'].keys()
                  if nm[host]['tcp'][port]['state'] == 'open']
        else:
            tcp = []
        if 'udp' in nm[host].keys():
            udp = [str(port) for port in nm[host]['udp'].keys()
                  if nm[host]['udp'][port]['state'] == 'open']
        else:
            udp = []
    #print(udp)
    return tcp, udp

def process(hosts, scan, db):
    sql = 'INSERT OR REPLACE INTO last(host,state,udp,tcp)\
           SELECT host,state,udp,tcp FROM now'
    db.query(sql)

    for host in hosts:
        if ping(host):
            tcp, udp = scan(host)
            h = int(addr(str(host)))
            sql = 'INSERT OR REPLACE INTO now (host,state,udp,tcp) \
                                      VALUES (?,?,?,?)'
            db.query(sql, (int(addr(str(host))), 
                                    1, ','.join(udp), ','.join(tcp)))
        else:
            sql = 'INSERT OR REPLACE INTO now (host,state,udp,tcp) \
                                      VALUES (?,?,?,?)'
            db.query(sql, (int(addr(str(host))), 0, '', ''))

def report(db):
    msg = []
    sql = "select host,state,udp,tcp from ( select * from now union all \
                           select * from last ) t \
                           group by host,state,udp,tcp having count(*)=1;"
    result = db.query(sql)
    if not result:
        msg.append('Changes in infrastructure perimeter are not found')
        msg.append('')
    else:
        skip = False
        msg.append('Found next Changes in infrastructure perimeter:\n')
        rows = []
        h = len(result)
        for i in range(h):
            rec = []
            if skip:
                skip = False
                continue
            if i < h-1 and result[i][0] == result[i+1][0]:
                skip = True
                rec.append(str(addr(result[i][0])))
#                bt()
                for n in range(1, len(result[i])):
                    if result[i][n] != result[i+1][n]:
                        last = result[i][n] if result[i][n] != "" else "-"
                        now = result[i+1][n] if result[i+1][n] != "" else "-"
                    else:
                        last = result[i][n]
                        now = result[i+1][n]
                    rec.append("{0}|{1}".format(now, last))
            else:
                skip = False
                rec.append('new: {0}'.format(str(addr(result[i][0]))))
                rec.append(result[i][1])
                rec.append(result[i][2])
                rec.append(result[i][3])
            rows.append(rec)
        title = ['host', 'state: last|now','open udp: last|now',
                                                  'open tcp: last|now']
        msg.append(tabulate(rows, headers=title, tablefmt='orgtbl'))
        msg.append('')
    print('\n'.join(msg))

    if NOTFICATIONS_SLACK == 1:
        slack = Slacker(SLACK_TOKEN)
        print(msg)
        print()
        msg_str = ''.join(msg)
        msg_str=msg_str.strip()
        slack.chat.post_message(SLACK_CHANEL, '```'+'...\n' + msg_str+'```')




if __name__ == "__main__":
    if len(sys.argv) > 1:
        hosts = getHosts(sys.argv[1])
    else:
        print('Hosts list is requred as 1st argument')
        sys.exit(1)

    db_name = "{0}.db".format(sys.argv[0])
    db = DB(db_name)
    db.schema()
    process(hosts, scan, db)

    report(db)
    db.close()

