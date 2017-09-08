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

if not os.path.isdir("program"):
	os.system("mkdir program")

proxy = xmlrpclib.ServerProxy("http://localhost:8004/")				#polaczenie z serverem
def get_program():
	"""Funckja pobierająca program 
	używając odczytu z zegara nazywamy plik do którego wpisany zostanie kod przesłanego programu, 
	nastpenie łączymy się z serwerem i odebrane dane zapisujemy do utworzonego pliku.
	Potem plik jest zamykany oraz nadawane mu są odpowiednie uprawnienia. Kolejnie program jest kompilowany 
	i uruchomiony, a rezultat jest wypisany na ekranie."""
	name="program/p"+unicode(datetime.datetime.now().time())+".py"		#tworzenie nazwy pliku
	handle = open(name, "w") 						#utworzenie pliku
	try:
		handle.write(proxy.send_program().data)					#zapisanie do pliku
	except:
		proxy = xmlrpclib.ServerProxy("http://localhost:8005/")			#polaczenie z serverem
		try:
			handle.write(proxy.send_program().data)					#zapisanie do pliku
		except:
			proxy = xmlrpclib.ServerProxy("http://localhost:8006/")			#polaczenie z serverem
			handle.write(proxy.send_program().data)	



	handle.close()								#zamkniecie pliku
	os.system('sudo chmod -R 777 program/')					#nadanie uprawniej 

	#kompilacja programu
	if (os.system('python -m compileall -l %s'% name))==0:
		proxy.get_compile_result("true")
	else:
		proxy.get_compile_result("false")				

	#uruchomienie programu 
	p=subprocess.Popen(name, stdout=subprocess.PIPE)	
	result=p.communicate()[0]
	proxy.get_program_result(result)
	print  	result								#wypisanie wyniku
	
	#porownywanie plikow
	exist="false"
	file_list =  glob.glob("program/*.py")
	for j in file_list:
		if filecmp.cmp(j, name):
			exist = "true";						# jesli istnieje exist=true
			break;

	proxy.get_program_raport(exist)


threads = []
"""W petli uruchamiamy kilka wątków, gdzie każdy wątek uruchamia funckję 'get_program' """
for i in range (1):
	t = threading.Thread(target=get_program)
	threads.append(t)
	t.start()
	print ("watek: %d" % i)




#bezpieczenstwo









