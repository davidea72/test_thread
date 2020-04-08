import subprocess
import time
import threading
import concurrent.futures

'''

 sudo getcap /bin/ping
 sudo setcap cap_net_raw=ep /bin/ping
 sudo getcap /bin/ping
/bin/ping = cap_net_raw+ep


'''
def ping(id,host):
    command = ['ping', '-c', '1',"-W","1", host]
    valore=subprocess.run(command,capture_output=True)
    return id,host,valore


elenco_host={
1:"8.8.8.8",
2:"4.4.4.4",
3:"1.1.1.1",
4:"fisso",
5:"216.58.205.67",      # www.google.it
6:"31.13.86.36",        # www.facebook.com
7:"104.244.42.65",      # www.twitter.com
8:"31.13.86.174",       # www.instagram.com
9:"104.17.61.22",       # www.ilfattoquotidiano.it
10:"92.122.247.92",     # www.repubblica.it
11:"104.26.14.239",     # realpython.com
12:"104.106.84.116",    # www.ebay.it
13:"104.17.122.180",    # www.mitnicksecurity.com
14:"212.224.123.69",    # www.proxmox.com
15:"95.101.71.241",     # www.aliexpress.com
16:"89.40.173.155",     # www.davidea.it
17:"92.122.35.239",     # www.banggood.com
18:"5.144.168.131",     # www.cisco.it
19:"159.148.147.196",   # www.mikrotik.com
20:"140.82.118.3",      # www.github.com
21:"96.30.24.64",       # www.ubiquiti.com
22:"172.65.251.78",     # www.gitlab.com 
23:"64.170.98.42",      # tools.ietf.org
24:"104.106.125.40",    # www.amazon.it
25:"151.101.112.223",   # www.python.org
26:"216.58.208.142",    # www.youtube.it
27:"64.91.226.82",      # www.whois.com
28:"104.27.15.91"       # 33hops.com

}

'''
**************************** sequenziale ******************************
'''


inizio = time.time()
for id in elenco_host.keys():
    
    ritorno=ping(id,elenco_host[id])
    print(ritorno[0],end="\t")
    print(ritorno[1],end="\t")
    if len(ritorno[1]) < 8:
        print("\t",end="")
    print(str(ritorno[2].returncode==0))
    #print(a.stdout)
fine = time.time()
print(fine-inizio)



'''
**************************** threading ******************************
'''



thread_local = threading.local()

def ping_threaded(id,host):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        valori_di_ritorno=zip(executor.map(ping, id,host))
        return valori_di_ritorno


inizio = time.time()
ids=[]
hosts=[]
for id in elenco_host.keys():
    host=elenco_host[id]
    ids.append(id)
    hosts.append(host)

zippato=ping_threaded(ids,hosts)


for istanza in zippato:
    print("istanza",end="\t")
    print(istanza[0][0],end="\t")
    print(istanza[0][1],end="\t")
    if len(istanza[0][1]) < 8:
        print("\t",end="")
    print(istanza[0][2].returncode==0)

#zippato è stato consumato da istanza ma in modo ordinato
#se viene consumato da set è disordinato

unzippato=set(zippato)

for elemento in unzippato:
    print("unzippato",end="\t")
    print(elemento[0][0],end="\t")
    print(elemento[0][1],end="\t")
    if len(elemento[0][1]) < 8:
        print("\t",end="")
    print(elemento[0][2].returncode==0)

fine = time.time()
print(fine-inizio)
