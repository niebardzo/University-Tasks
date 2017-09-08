#!/usr/bin/python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import threading

def send_program():
     handle = open("program.py")			#otwieranie pliku
     return xmlrpclib.Binary(handle.read())		#odczyt pliku
     handle.close()					#zamykanie pliku

def get_compile_result(result):
	print ("wynik kompilacji: %s" % result)
	return result
	
def get_program_result(result):
	print ("wynik programu: %s" % result)
	return result

def get_program_raport(result):
	print ("Czy program juz istnieje: %s" % result)
	return result
 
def run_server (port):
	server = SimpleXMLRPCServer(("localhost", port))	#tworzenie serwera
	print ("Oczekiwanie na polaczenie, port: %s..." % port)
	server.register_function(send_program, 'send_program')	#wyslanie programu
	server.register_function(get_compile_result, 'get_compile_result')
	server.register_function(get_program_result, 'get_program_result')	
	server.register_function(get_program_raport, 'get_program_raport')
	server.serve_forever()					#utrzymanie serwera w petli
wybor=0;
print "Witaj w programie serwera"
while wybor!=1 and wybor!=2:
	print "Aby uruchomic serwer, wybierz jeden z ponizszych krokow:"
	print "1 - Wpisz porty na ktorych na ktorych ma byc uruchomiony"
	print "2 - Wczytaj skonfigurowane porty"
	wybor = int (raw_input())
#wpisywanie portow	
if wybor==1:
	print "Wpisz porty oddzielajac spacjami"
	port = raw_input().split()
	wybor =0
	#zapisywanie pliku
	while wybor!=1 and wybor !=2:
		print "Czy chcesz zapisac porty jako domyslna konfiguracje?"
		print "1 - TAK"
		print "2 - NIE"
		wybor = int (raw_input())
	if wybor==1:
		fil = open("konfiguracja_serwera", "w") 
		for a in port:
			fil.writelines(a)
			fil.write("\n")
		fil.close()
	
	port=map(int, port)
#ladowanie portow z pliku
else:
	fil = open("konfiguracja_serwera", "r") 
	port2=fil.readlines()
	fil.close()
	port=[]
	for c in range(len(port2)):
		port.append(port2[c].rstrip())
	port=map(int, port)

threads = []

for i in port:
	t = threading.Thread(target=run_server, args=(i,))
	threads.append(t)
	t.start()

