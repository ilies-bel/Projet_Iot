#### BELDJILALI Ilies, CHAPUIS Flavian, FOLLÉAS Brice, GAUTIER Gwendal, GONNET Anthony

# Application android
## Résumé de l'application
Cette application android a pour but l'affichage d'une valeur de température ou d'une valeur de luminosité suivant ce que l'utilisateur a décidé.
### Fonctionnement de l'application
Lorsque l'utilisateur va entrer dans l'application, il va commencer par choisir une adresse IP et un port. Ces valeurs correspondent aux caractéristiques avec lesquelles notre application pourra communiquer en UDP.
Dans cette première communication, nous allons définir quelle valeur entre la luminosité et la température sera envoyée.
Par la suite le serveur va nous répondre en nous communicant la valeur souhaitée. Cette valeur sera récupérée par écoute UDP pour ensuite être affiché pour lecture.

## Interface Graphique
L'interface peut se décomposer en 4 parties (de haut en bas) :
 - Première partie : elle contient les champs permettant de renseigner l'IP et le port. Ce sont les deux champs qui permettront de communiquer avec le serveur par protocole UDP
 - Deuxième partie : elle se compose d'un simple switch qui selon son état permettra la demande de données de luminosité ou de température.
 - Troisième partie : Elle contient un champ texte dans lequel se trouvera la valeur reçu par le serveur.
 - Quatrième partie : Elle se compose d'un bouton, c'est sur ce bouton que l'utilisateur devra appuyer lorsqu'il aura configuré la partie 1 et 2 afin de commencer la communication.

## Envoie UDP
L'envoie d'une donnée par UDP se fait dans la class SendData. Cette classe commence par initialiser le datagramme et l'adresse du serveur. On charge par la suite le packet UDP par la ligne 104 : 
```
DatagramPacket packet = new DatagramPacket(buf, buf.length, serverAddr, sPORT);
```
Le paquet est ensuite clairement envoyé à la ligne 112 :
```
socket.send(packet);
```
Bien sûr le programme est ponctué de différentes ligne de log qui permettent un débogage plus clair de l'application.

## Écoute UDP
L'écoute UDP s'effectue sur la même classe que l'envoie UDP. C'est à dire "SendData". En pratique cette classe après avoir effectué son envoie va se mettre à écouter. Elle continura son écoute jusqu'à qu'un packet est été trouvé :
```
socket.receive(packet);
Log.d("UDP", "Receive :" + new String(packet.getData()));
```

## Affichege de la donnée
Lorsqu'une donné esr reçue par UDP, elle est de type bytes. La donnée que nous voulont est de type int, il s'agira dès lors de traduire ce byte en int. Cela s'effectue grâce à la classe "byte_to_ascii"