#!/usr/bin/python
import xmlrpclib
import os
import shlex
import subprocess
import threading
import datetime
import time
import filecmp
import glob
import RestrictedPython
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins




wybor=0;
print "Witaj w programie klienta"
while wybor!=1 and wybor!=2:
	print "Aby uruchomic klient, wybierz jeden z ponizszych krokow:"
	print "1 - Wpisz adres i porty na ktorych na ktorych ma byc uruchomiony"
	print "2 - Wczytaj skonfigurowane adres i porty "
	wybor = int (raw_input())
if wybor==1:
	print "Wpisz adres IP serwera"
	IP =raw_input().split()
	print "Wpisz porty oddzielajac spacjami"
	port = raw_input().split()
	wybor =0
	while wybor!=1 and wybor !=2:
		print "Czy chcesz zapisac jako domyslna konfiguracje?"
		print "1 - TAK"
		print "2 - NIE"
		wybor = int (raw_input())
	if wybor==1:
		fil = open("konfiguracja_klienta_PORTY", "w") 
		for a in port:
			fil.write(a)
			fil.write("\n")
		fil.close()
		fil = open("konfiguracja_klienta_IP", "w") 
		fil.writelines(IP)
		fil.close()
	port=map(int, port)
else:
	fil = open("konfiguracja_klienta_IP", "r") 
	IP =fil.readlines()
	fil.close()
	fil = open("konfiguracja_klienta_PORTY", "r") 
	port2=fil.readlines()
	fil.close()
	port=[]
	adres=[]
	for c in range(len(port2)):
		port.append(port2[c].rstrip())
	port=map(int, port)

if not os.path.isdir("program"):
	os.system("mkdir program")

def get_program():

	#
	# Skladowanie do pliku
	#
	name="program/p"+unicode(datetime.datetime.now().time())+".py"		
	handle = open(name, "w") 						
	adres=[]
	for x in port:
		adres.append(IP[0].rstrip()+":"+str(x)+"/")
	for g in adres:
		proxy = xmlrpclib.ServerProxy(g)
		try:
			handle.write(proxy.send_program().data)	
			break
		except:
			print ("Adres %s jest niedostepny" %g)
	handle.close()	

	#
	#
	#
	os.system('sudo chmod -R 777 program/')	
	if (os.system('python -m compileall -l %s'% name))==0:
		proxy.get_compile_result("true")
	else:
		proxy.get_compile_result("false")
	print "Uruchomienie w bezpiecznym watku"
	source_code="""
import os
import subprocess
file_list =  glob.glob("program/*.py")
i=0;
i2=0
for j in file_list:
	k=os.path.getctime("program/"+j)
	if k>i:
		i=k
		i2="program/"+j;
subprocess.Popen(i2, stdout=subprocess.PIPE)

"""
        byte_code=compile_restricted(source_code, '<inline>', 'exec')
	print "Uruchomienie w bezpiecznym watku zakonczono"
	p=subprocess.Popen(name, stdout=subprocess.PIPE)	
	result=p.communicate()[0]
	proxy.get_program_result(result)
	print  	result
	
	#
	# Porownanie pod wzgledem podobienstwa programow i przesylanie zwrotnych raportow.
	#
	exist="false"
	file_list =  glob.glob("program/*.py")
	#libka glob szuka paternu zgodnie z unixowymi zasadami, nie regular expressions
	for j in file_list:
		if filecmp.cmp(j, name):
			exist = "true";						
			break;
	proxy.get_program_raport(exist)

get_program()





#bezpieczenstwo









