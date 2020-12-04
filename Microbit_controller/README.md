#### BELDJILALI Ilies, CHAPUIS Flavian, FOLLÉAS Brice, GAUTIER Gwendal, GONNET Anthony

# Microbit_controller

Cette partie du projet va s'intéresser à l'initialisation et au pilotage de la passerelle microbit, ainsi que du contrôleur de capteur de température et de luminosité.

## Controle de la passerelle - gateway_control.py

La passerelle est une carte micro:bit dont l'utilité est de servir de passerelle entre le contrôleur de capteur en bout de chaîne, et le serveur. 

La passerelle communique avec son homologue micro:bit par radio, et avec le serveur en Uart.

## Contrôle du contrôleur de capteurs - main.py 

Le contrôleur de capteurs est un élément de bout de chaîne qui possède 3 fonctions :

1. Répondre aux requêtes de données du serveur,
2. Récupérer les valeurs relevées par les capteurs de température et de luminosité,
3. Afficher ces valeurs sur l'écran OLED associé. 

## Communication entre les deux micro:bit

Le contrôleur de capteur initie la communication entre les deux éléments en envoyant son code PIN pour être reconnue par la passerelle, dans un message de type "ask". 
La passerelle répond à ce message en renvoyant au contrôleur un id qui correspondra à son numéro.

Le capteur peut ensuite envoyer ses données dans des messages de type data sous la forme :
```
    idDestination/data/T:vaT&L:valL
```
où valT et valL sont les valeurs récupérées par les capteurs. 

## Pilotage par la passerelle 

La passerelle est susceptible de transmettre des ordres de pilotage au contrôleur de capteur pour modifier son affichage OLED. Dans ce cas, le message prendra la forme : 
```
  idDestination/cmd/commande
```
Où commande correspond à TL ou Lt, déterminant l'ordre dans lequel sont affichées les valeurs. 
