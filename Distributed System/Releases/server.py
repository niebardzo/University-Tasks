#!/usr/bin/python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import threading

def send_program():
	"""Funkcja otwiera plik zwierający kod programu do przesłania, po czym zwraca otwarty plik używając funkcji biblioteki RPC, 
	a następnie zamyka plik."""
     handle = open("program.py")			#otwieranie pliku
     return xmlrpclib.Binary(handle.read())		#odczyt pliku
     handle.close()					#zamykanie pliku

def get_compile_result(result):
	"""Wypisuje na ekranie odebraną zmienną, zawierajcą wynik kompilacji programu na komputerze 2. """
	print ("wynik kompilacji: %s" % result)
	return result
	
def get_program_result(result):
	"""Wypisuje na ekranie odebraną zmienną, zawierajcą wynik uruchomienia programu programu na komputerze 2. """
	print ("wynik programu: %s" % result)
	return result

def get_program_raport(result):
	"""Wypisuje na ekranie odebraną zmienną, opisującą istnienie pliku programu na komputerze 2. """
	print ("Czy program juz istnieje: %s" % result)
	return result
 
def run_server (port):
	"""Funkcja wykorzystuje bibliotekę XMLRPCServer w celu stworzenia serwera, 
	następnie wywołując utworzone wcześniej funkcje wysyła dane programu i oczekuje na odpowiedź,
	która zawiera rezultat kompilacji, rezultata wywołania i czy program nie został wysłany już wcześniej.
	na końcu program jest zapętlany aby działął w trybie ciągłym."""
	server = SimpleXMLRPCServer(("localhost", port))	#tworzenie serwera
	print ("Oczekiwanie na polaczenie, port: %s..." % port)
	server.register_function(send_program, 'send_program')	#wyslanie programu
	server.register_function(get_compile_result, 'get_compile_result')
	server.register_function(get_program_result, 'get_program_result')	
	server.register_function(get_program_raport, 'get_program_raport')
	server.serve_forever()					#utrzymanie serwera w petli


port = [8004, 8005, 8006]
threads = []
"""Program głwny tworzy pętlę, która uruchamia wątki, ktore po kolejnych portach, zamieszczonych w tablicy uruchamia serwer. """
for i in port:
	t = threading.Thread(target=run_server, args=(i,))
	threads.append(t)
	t.start()

