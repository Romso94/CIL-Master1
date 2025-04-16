

Options :

-sn : Scan Network → Scan ARP

-v | -vv : Verbose

-A : Agressive Mode

-oN : Output in text file

-p : Spécifier le port

-o : Output file

Scan du réseau pour trouver notre machine victime :

- nmap -sn -v 192.168.56.0/24 (-oN ScanNetwork)

[ScanNetwork](https://prod-files-secure.s3.us-west-2.amazonaws.com/dee6f2e0-9b35-41c3-b6ab-11d6d0bb40f1/f3d67781-9179-44d3-aac5-58e8ee32a53e/ScanNetwork.txt)

Scan des Vulnérabilités de la machine victime :

- nmap -sV -v -A 192.168.56.101

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/dee6f2e0-9b35-41c3-b6ab-11d6d0bb40f1/a4ac2ae3-5154-4109-84bd-2be1dec0f4bb/image.png)

Exemple Utilisation de Scripts pour ssh :

- nmap 192.168.56.101 --script ssh-hostkey --script-args ssh_hostkey=full

=all : Permets de recuperer plus d’informations sur les clés

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/dee6f2e0-9b35-41c3-b6ab-11d6d0bb40f1/b5ecd10e-1339-4b55-8445-96f6a9b73fd9/image.png)

Ici on récupère la clé SSH

Scanner un port Spécifique ici le port 53 par exemple:

- nmap --script dns-nsid 192.168.56.101 -p 53

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/dee6f2e0-9b35-41c3-b6ab-11d6d0bb40f1/8d68412e-a82e-4ee1-80f5-36f335d91eff/image.png)

Pour archiver dans un fichier HTML :

- nmap -sV 192.168.56.101 -o nom.html

Utilisation d’un NSE :

- nmap —script banner 192.168.56.101

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/dee6f2e0-9b35-41c3-b6ab-11d6d0bb40f1/bfb2bd4c-ffe5-4fc8-be95-a0c0223ce781/image.png)

Utilisation de Vulscan pour trouver des CVE:

- nmap –script vulscan/vulscan.nse -sV -p22 192.168.56.101

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/dee6f2e0-9b35-41c3-b6ab-11d6d0bb40f1/3331b6d5-4de3-4c59-8586-bb12bbe21a8f/image.png)

Enumerer les services d’authentification :

- nmap --script ssh-auth-methods --script-args="ssh.user=romso" -p 22 192.168.56.101

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/dee6f2e0-9b35-41c3-b6ab-11d6d0bb40f1/001771fd-f000-494f-9c0d-ebd39676dabc/image.png)

Brute force du ssh :

- nmap --script ssh-brute -p 22 192.168.56.101

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/dee6f2e0-9b35-41c3-b6ab-11d6d0bb40f1/218bb598-15b2-4ff1-9dc6-42907d2e8b34/image.png)