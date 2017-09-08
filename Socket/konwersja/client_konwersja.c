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
    adres_servera.sin_addr.s_addr = inet_addr("127.16.0.100");
    
    if(connect(gniazdo, (struct sockaddr*)&adres_servera, sizeof(adres_servera))<0){
        printf("nie ma polaczenia\n");
        exit(1);
    }
    
    for(;;){
    //wysylanie
    //bzero(wiadomosc,200);
    printf("jaka liczbe wyslac serwerowi?\n");
    int liczba,*liczba2;
    scanf("%d",&liczba);
    liczba2 = &liczba;
    //liczba2 = htonl(liczba);
    //fgets(wiadomosc,200,stdin);
    send(gniazdo, liczba2, sizeof(liczba2),0);
    
    //odbieranie
    bzero(wiadomosc,200);
    recv(gniazdo, wiadomosc,200,0);
    printf("wyslales: %s\n",wiadomosc);
    }
    
return 0;    
}
