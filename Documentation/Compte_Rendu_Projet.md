#### BELDJILALI Ilies, CHAPUIS Flavian, FOLLÉAS Brice, GAUTHIER Gwendal, GONNET Anthony

# Projet - Mise en place d’une mini-architecture IoT

## Exercice 1 : Mise en place du réseau TODO

Dans l'objectif de définir un protocole de communication sécurisé nous souhaitons mettre en place une identification via CHAP et chiffrer notre canal de communication en utilisant l'algorithme de chiffrement AES-128.


## Exercice 2 : configuration des capteurs TODO

Une étape importante de la mise en place de l’infrastructure côté objet consiste à configurer l’objet à déployer dans les bureaux, afin que ce dernier puisse collecter les informations souhaitées :
température et luminosité.
Les informations doivent être envoyées au serveur (passerelle) et enfin afficher les informations dans l’ordre demandé par le serveur.
Pour ce faire, vous disposez d’un micro-contrôleur micro :bit qui compte plusieurs capteurs intégrés. De plus, l’objet dispose d’un afficheur OLED sur lequel les données pourront être affichées.

2 Affichage sur l’écran OLED
Une partie de la configuration de l’objet est l’affichage des données sur l’écran OLED qui accompagne le module micro :bit. Avant d’afficher directement les informations dans l’ordre défini par le serveur, assurez vous de comprendre comment afficher des informations sur cet écran. Ainsi,
pour commencer, vous pouvez programmer votre module micro :bit afin que ce dernier affiche les données récupérées des capteurs.


Si vous programmez le micro :bit en micro-python, vous disposez du code contrôleur d’un
écran OLED Adafruit sur le git : https://github.com/CPELyon/microbit_ssd1306. Un exemple
d’utilisation de la bibliothèque est dans le sous-dossier /samples/hello-world/.
Dans le code donné, on utilise l’interface I2C pour pouvoir envoyer les informations à afficher,
on positionne les données en indiquant la ligne et colonnes à utiliser, la distribution des pins dans
la carte est présenté dans la figure 2.


Communications avec la passerelle
Cette étape englobe deux rôles. En effet, il faut que votre objet soit capable d’envoyer les
informations récoltées à la passerelle, mais qu’il soit également capable d’écouter les messages
envoyés par la même afin de pouvoir afficher le contenu des messages sur l’écran OLED.
Le format des messages à envoyer à la passerelle est libre, ainsi les données peuvent être envoyées
brutes (sans traitement côté objet), ou bien suivant un format précis (type ficher de configuration
format JSON par exemple). Dans un premier temps, n’utilisez aucun format et envoyez les données
brutes au serveur, le choix d’un format est optionnel.
Le micro :bit attaché au PC fera le rôle de récepteur RF 2.4GHz de la passerelle et recevra
les données de la part des capteurs déployés, mais sera aussi en mesure d’envoyer la configuration
d’affichage à chaque objet. Les données de configuration seront reçus à travers son interface USB
(UART), indiquant l’ordre d’affichage des données par 2 lettres majuscules, ainsi :
— TL : Indique que la Température sera affiché en premier, puis la Luminosité
3
— LT : Indique que la Luminosité sera affiché en premier, puis la Température

## Exercice 3 : configuration de la passerelle et TODO

Le PC, dans un premier temps, doit être configuré pour stocker les données reçues au format
brut dans un fichier texte, de cette façon il fera aussi le rôle de serveur.
Puis ce dernier va écouter les requêtes du client Android par UDP :
— Message ”getValues()” : le serveur répond à ce message en envoyant les données reçu dans
sa passerelle au client Android sous le même format envoyé depuis l’objet (texte, JSON,...).

Exemple de code serveur

Le code d’un serveur effectuant les tâches demandées au point précédent est disponible sur :
https://github.com/CPELyon/4irc-aiot-mini-projet/blob/master/controller.py
Dans ce code python à exécuter dans un PC linux et à adapter pour d’autres systèmes d’exploitation, un serveur est démarré sur le port 10000 pour écouter les requêtes UDP selon le protocole
décrit précédemment.

L’écriture et lecture dans la sortie UART est aussi géré dans ce code, faites attention au port
qui est associé au micro :bit pour le faire correspondre à celui défini dans le code.

#### Comment lancer le serveur ?

1. Cloner le dépôt [git hub](https://github.com/ilies-bel/Projet_Iot.git).

```bash
git clone https://github.com/ilies-bel/Projet_Iot.git
```

2. Installer le paquet **pyserial** avec la commande suivante :

`pip3 install pyserial`

Alternativement :
`curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py`

3. Lancer le serveur :
`./start-server.sh`

En cas de questions ou de problèmes rencontrés, se renseigner sur Server_Controller\README.md

### Évolutions du serveur

Dans le cadre de l'évolution du serveur nous aovns mis en place plusieurs fonctionnélitées :

— L'utilisation de InfluxDb pour stocker les données plutôt que d'utiliser le fichier texte initial.
Pour cela nous ajoutons une *database* : **data** : qui a pour champs : 
- "measurement"
- "tags": {"sensor"}
- "time"
- "fields": {"value"} 

- Pour la communication entre microcontroleurs on utilise un format json défini dans db_control.py.

- On utilise l'interface web Grafana afin de pouvoir visualiser les données. Sa configuration est spécifiée dans le Server_Controller\README.md 

Dans les évolutions qui resteraient à implémenter seraient :
— Donner la possibilité de gérer plusieurs objets. Dans l’état actuel le serveur reçoit des données brutes sans faire un filtrage et de ce fait, il n’est pas possible de gérer plus d’un objet, vous pouvez donc implémenter un protocole pour pouvoir gérer plusieurs objets au même temps et les gérer depuis l’interface web et/ou l’application Android.

# Création de l’application Android

La dernière partie de la mise en place de l’architecture IoT consiste à développer une application Android qui permet de contrôler l’ordre d’affichage des données collectées sur un des objets en
particulier. 

Pour se faire nous avons d'abord commencer par définir une [maquette](TODO) de notre applicaiton Android qui reste simple et intuitive au niveau de l'nterface. 

## Exercice 1 : choix d’affichage

On utilise donc un bouton, plus précisément un switch, pour définir l'ordre d'affichage, le choix de l'interface étant défini par la maquette pré-définie. Ainsi on passe de l'affichage de la température/luminosité de luminosité/température.

## Exercice 2 : définir le serveur de destination

On utilise donc deux EditText l'un pour l'adresse IP du serveur et un pour le port.

On communique avec la passerelle via l'adresse IP et le port et on appuye sur le bouton afin de pouvoir envoyer les paquets au serveur.
Le listener sur ce bouton permet de créer un nouveau thread qui fait l'envoie au serveur.

## Exercice 3 : Communication bidirectionnelle avec le Smartphone

Afin d'afficher également sur l'application les informations de Température et Luminosité on réceptionnera les paquets UDP via la classe ResultListener de mainActivity.java. On écoute ainsi les différents paquets venus de l'adresse IP et du port rentré en paramètre sur l'application. Si l'on reçoit un paquet sur notre socket alors la 

L'affichage se fait sur deux TextView.

# Annexe

## Liens utiles 

[GitHub](https://github.com/ilies-bel/Projet_Iot)
[GitHub Professeur](https://github.com/CPELyon/4irc-aiot-mini-projet)
[Sujet Projet](https://prod.e-campus.cpe.fr/pluginfile.php/52754/mod_resource/content/1/projet.pdf)
[Driver Micro:bit](https://github.com/CPELyon/microbit_ssd1306)
