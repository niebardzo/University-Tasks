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
    
    int gniazdo, odp;
    struct sockaddr_in adres_servera;
    char wiadomosc[200], wiadomosc1[200],wiadomosc2[200],wiadomosc3[200],wiadomosc4[200], wiadomosc_servera[200];
    
    bzero(wiadomosc,200);
    bzero(wiadomosc_servera,200);
    
    gniazdo = socket(AF_INET, SOCK_STREAM, 0);
    if(gniazdo<0){
        printf("nie ma gniazda\n");
        exit(1);
    }
    
    memset(&adres_servera, 0, sizeof(adres_servera)); 
    adres_servera.sin_family = AF_INET;
    adres_servera.sin_port = htons(8888);
    adres_servera.sin_addr.s_addr = inet_addr("127.16.0.100");
    
    if(connect(gniazdo, (struct sockaddr*)&adres_servera, sizeof(adres_servera))<0){
        printf("nie ma polaczenia\n");
        exit(1);
    }
    
    //while(1){
    for(;;){
    //wysylanie
    bzero(wiadomosc,200);
    printf("co wyslac serwerowi?\n");
    fgets(wiadomosc,200,stdin);
    send(gniazdo, wiadomosc, strlen(wiadomosc),0);
    
    //odbieranie

    bzero(wiadomosc,200);
    recv(gniazdo, wiadomosc,200,0);
    printf("system: %s\n",wiadomosc);
    bzero(wiadomosc,200);
    recv(gniazdo, wiadomosc1,200,0);
    printf("nodename: %s\n",wiadomosc1);
    bzero(wiadomosc,200);
    recv(gniazdo, wiadomosc2,200,0);
    printf("release: %s\n",wiadomosc2);
    bzero(wiadomosc,200);
    recv(gniazdo, wiadomosc3,200,0);
    printf("version: %s\n",wiadomosc3);
    bzero(wiadomosc,200);
    recv(gniazdo, wiadomosc4,200,0);
    printf("machine: %s\n",wiadomosc4);
    }
    
    close(gniazdo);
    
return 0;    
}
