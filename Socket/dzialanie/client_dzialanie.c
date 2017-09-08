#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>

int main(){
    
    int gniazdo, odp;
    struct sockaddr_in adres_servera;
    char wiadomosc[200], wiadomosc_servera[200];
    
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
    adres_servera.sin_addr.s_addr = inet_addr("127.0.0.1");
    
    if(connect(gniazdo, (struct sockaddr*)&adres_servera, sizeof(adres_servera))<0){
        printf("nie ma polaczenia\n");
        exit(1);
    }
    
    //while(1){
    for(;;){
    //wysylanie
    bzero(wiadomosc,200);
    printf("podaj dzialanie:\n");
    fgets(wiadomosc,200,stdin);
    send(gniazdo, wiadomosc, strlen(wiadomosc),0);
    
    //odbieranie
    bzero(wiadomosc,200);
    recv(gniazdo, wiadomosc,200,0);
    printf("wynik: %s\n",wiadomosc);
    }
    
    close(gniazdo);
    
return 0;    
}
