#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <time.h>
#include <sys/utsname.h>
#define _POSIX_SOURCE

int main(){
    
   int gniazdo,gniazdo_klienta,dl_adresu,odczyt;
   struct sockaddr_in adres_servera, adres_clienta;
   char wiadomosc[200],wiadomosc1[200],wiadomosc2[200],wiadomosc3[200],wiadomosc4[200];
   
   bzero(wiadomosc,200);
   
   gniazdo = socket(AF_INET,SOCK_STREAM,0);
   if(gniazdo<0){
       printf("gniazdko nam nie powstalo\n");
       exit(1);
   }
    
    memset(&adres_servera, 0, sizeof(adres_servera));
    adres_servera.sin_family = AF_INET;
    adres_servera.sin_port = htons(8888);
    adres_servera.sin_addr.s_addr = htonl(INADDR_ANY);
    
    if(bind(gniazdo, (struct sockaddr*)&adres_servera, sizeof(adres_servera))<0){
        printf("nie zbindowalo sie\n");
        exit(1);
    }
    
    listen(gniazdo,5);
    
    dl_adresu = sizeof(adres_clienta);
    gniazdo_klienta = accept(gniazdo, (struct sockaddr*)&adres_clienta, &dl_adresu);
    if(gniazdo_klienta<0){
        printf("nie ma akceptacji");
        exit(1);
    }
    
    for(;;){
    //while(1){
    //odczyt wiadomosci klienta
    bzero(wiadomosc,200);
    recv(gniazdo_klienta,wiadomosc,200,0);
    printf("klient pyta: %s\n", wiadomosc);
    bzero(wiadomosc,200);

    struct utsname uts;
    uname(&uts);
    sprintf(wiadomosc, "%s", uts.sysname);
    send(gniazdo_klienta,wiadomosc,strlen(wiadomosc),0);
    sprintf(wiadomosc1, "%s", uts.nodename);
    send(gniazdo_klienta,wiadomosc1,strlen(wiadomosc1),0);
    sprintf(wiadomosc2, "%s", uts.release);
    send(gniazdo_klienta,wiadomosc2,strlen(wiadomosc2),0);
    sprintf(wiadomosc3, "%s", uts.version);
    send(gniazdo_klienta,wiadomosc3,strlen(wiadomosc3),0);
    sprintf(wiadomosc4, "%s", uts.machine);
    send(gniazdo_klienta,wiadomosc4,strlen(wiadomosc4),0);
    
    }
    close(gniazdo);
    close(gniazdo_klienta);

return 0;    
}
