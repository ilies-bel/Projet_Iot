#### BELDJILALI Ilies, CHAPUIS Flavian, FOLLÉAS Brice, GAUTHIER Gwendal, GONNET Anthony

# Projet - Mise en place d’une mini-architecture IoT

## Exercice 1 : Mise en place du réseau

Dans l'objectif de définir un protocole de communication sécurisé nous souhaitons mettre en place une identification via CHAP et chiffrer notre canal de communication en utilisant l'algorithme de chiffrement AES-128.

### AES-128

L'algorithme prend en entrée un bloc de 16 octets (128 bits) et sa clé peut faire 128 bits. Avec la nouvelle version de micro:bit, le processeur est nRF52833 et dispose déjà d’un moteur de cryptage AES 128 bits et de fonctionnalités de mises à jour du firmware.

Bous utiliserons python pour la programmation d'une micro:bit donc voyons comment mettre en place AES-128.

#### Comment mettre en place AES-128 en python?

Pour implémenter AES dans nos micro:bit on commencera par utiliser la bibliothèque pycrypto via :
`pip install pycrypto`

Si vous rencontrez une erreur, vérifiez que vous avez bien Python d'installer avec `python --version` ou `python3 --version` et pip d'installer avec `pip --version`.
Si vous n'avez pas python rendez-vous sur [le site de téléchargement de Python](https://www.python.org/downloads/).
Si vous n'avez pas **pip** installez-le avec `apt install python-pip` (ou `apt install python3-pip` si vous utilisez Python 3).

> PIP est un gestionnaire de paquets python PIP. 

Création d'un nouveau fichier .py :
```
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
```

Création de la classe python pour mettre en place AES-128.

```
class AESCipher(object):
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()
```

En survolant les lignes de ce constructeur, il reçoit une clé qui peut être de n'importe quelle longueur. 
Ensuite, nous procédons à la génération d'un hachage de 256 bits à partir de cette clé. Vous pouvez ainsi transmettre au constructeur , et il générera une clé unique de 256 bits pour votre code. Nous avons également défini block_size à 128, qui est la taille de bloc de l'AES.

Avant de définir les méthodes `encrypt` et `decrypt` pour notre classe AESCipher, commençons par créer les méthodes `__pad` et `__unpad`.
**pad :**
```
   def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text
```

La méthode `__pad` reçoit le texte simple à crypter et ajoute un nombre d'octets pour que le texte soit un multiple de 128 bits (modulo self.block_size (=128)) puisque nous encryptons par block de 128 bits. Ce nombre est stocké dans la varaible number_of_bytes_to_pad. Ensuite, dans la variable ascii_string, nous générons notre caractère de remplissage, et padding_str contiendra ce caractère multiplié par number_of_bytes_to_pad.
Nous n'avons donc qu'à ajouter padding_str à la fin de notre texte en clair, de sorte qu'il s'agit maintenant d'un multiple de 128 bits.

**unpad :**
```
	@staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        bytes_to_remove = ord(last_character)
        return plain_text[:-bytes_to_remove]
```

De manière similaire, la méthode `__unpad` recevra le texte décrypté, également connu sous le nom de plain_text, et supprimera tous les caractères supplémentaires ajoutés dans la méthode `__pad`. Pour cela, nous devons d'abord identifier le dernier caractère et stocker dans bytes_to_remove le nombre d'octets dont nous avons besoin pour couper la fin du texte en clair afin de le décoder.

**encrypt :**
```
    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")
```
La méthode de cryptage reçoit le texte en clair à crypter (plain_text). Nous commençons par ajouter le padding à ce texte en clair afin de pouvoir le chiffrer (block de 128 bits). Ensuite, nous générons un nouvel `iv` (initialization vector) aléatoire de la taille d'un bloc AES, 128 bits. un iv est un bloc de bits combiné avec le premier bloc de données lors d'une opération de chiffrement. contrairement à certains chiffrement par blocs (tel EBC), l'utilisation d'un vecteur d'initialisation permet d'éviter de répéter le même encodage pour le même bloc de texte en clair.
Nous créons maintenant notre chiffrement AES avec AES.new et notre clé, en mode CBC et avec notre iv qui vient d'être généré. Nous invoquons maintenant la fonction de cryptage de notre chiffrement, en lui transmettant notre texte en clair converti en bits. La sortie chiffrée est ensuite placée après notre iv et reconvertie de bits en caractères lisibles.

**decrypt :**
```
    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)
```

Pour décrypter, il faut revenir sur toutes les étapes de la méthode de cryptage. Tout d'abord, nous convertissons notre texte crypté en bits et nous extrayons le iv, qui sera les 128 premiers bits de notre texte crypté. Comme auparavant, nous créons maintenant un nouveau code AES avec notre clé, en mode CBC et avec le iv extrait. Nous invoquons maintenant la méthode de décryptage de notre chiffre et le convertissons en texte à partir de bits. Nous enlevons le padding avec `__unpad` et c'est tout !

Visualisation de notre classe AESCipher :
Cette classe sera donc instancier dans le fichier aescipher.py

```
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

class AESCipher(object):
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]
```

## Exemple d'envoie de message encodé depuis une micro:bit :

Il s'agit ici du code python à implémenter sur la carte microbit.

```
import radio
from microbit import *
from aescipher.py import AESCipher # Il ne faut pas oublier d'importer notre classe pour pouvoir encoder nos messages.

if __name__ == "__main__" :

	# Activation de radio.
	radio.on()

	# On définit une clé de crypatge quelconque que l'autre micro:bit devra également avoir.
	key = ';|)xnb6t6xJA\;'

	# Instanciation de l'objet AESCipher
	aes = AESCipher(key)

	# On définit ici un message quelconque.
	message = 'Hello World !'

	# Boucle événementielle.
	while True:
	    # Le bouton A envoie un message.
	    if button_a.was_pressed():
	        radio.send(aes.encrypt(message))

	    # On lit tous les messages entrant en le décryptant
	    message_received = aes.decrypt(radio.receive())
	    
	    # Vérification que le message n'est pas null
	    if (message_received != None):

	        # Si il y a un message entrant
	        sleep(500)

	        # On affiche alors le message
	        display.scroll(message_received)
```

Source : https://github.com/burned301/AES

## Exercice 2 : configuration des capteurs


Une étape importante de la mise en place de l’infrastructure côté objet consiste à configurer
l’objet à déployer dans les bureaux, afin que ce dernier puisse collecter les informations souhaitées :
température et luminosité.
Les informations doivent être envoyées au serveur (passerelle) et enfin afficher les informations
dans l’ordre demandé par le serveur.
Pour ce faire, vous disposez d’un micro-contrôleur micro :bit qui compte plusieurs capteurs
intégrés. De plus, l’objet dispose d’un afficheur OLED sur lequel les données pourront être affichées.
2
Affichage sur l’écran OLED
Une partie de la configuration de l’objet est l’affichage des données sur l’écran OLED qui
accompagne le module micro :bit. Avant d’afficher directement les informations dans l’ordre défini
par le serveur, assurez vous de comprendre comment afficher des informations sur cet écran. Ainsi,
pour commencer, vous pouvez programmer votre module micro :bit afin que ce dernier affiche les
données récupérées des capteurs.
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

## Exercice 3 : configuration de la passerelle et 

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
** Clonez le projet suivant :**
https://github.com/ilies-bel/Projet_Iot.git
2. Installer le paquet **pyserial** avec la commande suivante
`pip3 install pyserial`

Alternativement :
curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py

3. Lancer le serveur avec la commande suivante :
`./start-server.sh`

### Évolutions du serveur
L’objectif de cet exercice est de faire évoluer le serveur, plusieurs tâches sont possibles :
— Remplacer le fichier texte par une vrai structure de base de données telle que MongoDB,
InfluxDB ou SQLite, afin d’avoir une meilleure gestion des données côté serveur, pour une
gestion plus facile, n’hésitez pas à regarder des solutions en conteneurs.
— Définir un format spécifique pour l’échange des données avec le client Android et le microcontrôleur, comme par exemple un fichier de configuration au format JSON. Cependant, le
choix du format reste libre
— Définir une interface web pour la visualisation des données reçus, par exemple Grafana
— Donner la possibilité de gérer plusieurs objets. Dans l’état actuel le serveur reçoit des données
brutes sans faire un filtrage et de ce fait, il n’est pas possible de gérer plus d’un objet, vous
pouvez donc implémenter un protocole pour pouvoir gérer plusieurs objets au même temps
et les gérer depuis l’interface web et/ou l’application Android.
— ...







# Création de l’application Android

La dernière partie de la mise en place de l’architecture IoT consiste à développer une application
Android qui permet de contrôler l’ordre d’affichage des données collectées sur un des objets en
particulier. Ainsi, l’application a deux fonctionnalités, le choix de l’affichage des données d’un des
objets et le choix du serveur sur lequel cela s’applique.
Pour simplifier, on assume qu’il y a seulement un objet associé à chaque serveur et donc on doit
choisir seulement l’adresse du serveur de destination et pas un des objets qui lui sont associés.
4
Pour faciliter le développement de votre application, les données seront envoyées via le protocole
UDP, et votre Smartphone sera connecté au serveur via WiFi si vous êtes en physique ou via le
réseau interne de votre PC si vous êtes en simulateur.

## Exercice 1 : choix d’affichage
Dans un premier temps votre application devra être en mesure de définir un ordre d’affichage
pour les 2 différentes données collectées. Vous pouvez, pour ceci, afficher les trois données à l’écran
et par simple pression du doigt définir l’ordre d’affichage des données. Ceci n’est qu’un exemple, et
le choix d’interface visuel de votre application reste libre.

## Exercice 2 : définir le serveur de destination
En plus de choisir l’ordre d’affichage des données, votre application doit être en mesure de choisir
le serveur de destination. En effet, le but est de pouvoir contrôler l’affichage des données pour
chaque objet via le serveur avec lequel il communique. Ainsi, le choix du serveur dans l’application
est indispensable. La configuration du serveur dans l’application Android se fait via l’adresse IP
du serveur et son port d’écoute (par défaut : 10000). Donc dans votre application Android, vous
devez disposer de deux champs dans lequel il sera possible de saisir une adresse IP et un port, qui
permettront la communication avec le serveur souhaité.
De plus, la communication sera effectuée via le protocole UDP, et aucun ACK n’est demandé.
Ainsi, votre application doit seulement faire de l’émission en direction du serveur, sans se préoccuper
de devoir réceptionner des paquets. Les données envoyées par votre application seront les 2 lettres
majuscules indiquant l’ordre d’affichage dans l’écran OLED.


## Exercice 3 : Communication bidirectionnelle avec le Smartphone
Dans l’objectif d’être capable d’afficher les données également sur votre Smartphone, votre
application doit être en mesure de recevoir des messages venant du serveur. Tout comme le serveur
envoie des données à l’objet, ce dernier devra pouvoir envoyer les mêmes données avec le même
format à votre Smartphone. Ce dernier devra être capable de réceptionner les données et de les
afficher dans l’application créée précédemment.
De plus, le Smartphone ne doit réceptionner que les données émises depuis le serveur avec lequel
il est connecté (défini dans l’exercice précédent).
Rendu final et démo
L’évaluation du mini-projet sera faite par une présentation de vos choix technologiques et une
démonstration de votre implémentation d’une durée de 10 minutes maximum le 7 décembre aprèsmidi.
De même, un rendu sur la plateforme e-campus devra être fait au plus tard le 4 décembre à
18h. Le rendu doit contenir :
1. Un rapport très synthétique listant les membres de l’équipe et décrivant les activités réalisées
(au moins 2 pages)
5
2. L’application Android documenté créée pour le contrôle et accès à votre architecture de
l’internet des objets
3. Votre projet ou code documenté créé pour gérer la capture et affichage des données dans
l’objet
4. Votre projet ou code documenté créé pour le micro-contrôleur faisant le rôle de passerelle
5. L’application coté serveur documenté

# Annexe

## Liens utiles 

[git hub](https://github.com/ilies-bel/Projet_Iot)
[git hub prof](https://github.com/CPELyon/4irc-aiot-mini-projet)
[sujet projet](https://prod.e-campus.cpe.fr/pluginfile.php/52754/mod_resource/content/1/projet.pdf)
[driver micro:bit](https://github.com/CPELyon/microbit_ssd1306)