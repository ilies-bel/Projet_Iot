#### BELDJILALI Ilies, CHAPUIS Flavian, FOLLÉAS Brice, GAUTHIER Gwendal, GONNET Anthony

# Server controller 

## Installation

### Installer InfluxDB
Commencez par installer InfluxDB sur votre machine :

Si vous êtes sur un OS GNU/Linux, installez InfluDb via les commandes suivantes :
```bash 
sudo apt-get update && sudo apt-get install influxdb && sudo systemctl unmask influxdb.service && sudo systemctl start influxdb
 ```

Si vous utilisez WSL executez la commande suivante pour lancer le service :
```bash 
sudo apt-get update && sudo apt-get install influxdb && sudo systemctl unmask influxdb.service && sudo service influxdb start
 ```

Si vous rencontrez un problème de connexion refusée, executez la commande suivante :

```bash
sudo influxd
```
### Utilisation de InfluxDB

Une fois que votre service est lancé côté serveur, vous pouvez gérer les données en utilisant la commande `influx` et ainsi voir les différentes données sur vos *databases*.

En utilisant `show databases` on peut voir les différentes *databases* d'InfluxDb. La base qui nous intéresse est data qui récupère nos différentes mesures (température et luminosité).

> Ne pas oublier d'utiliser `USE data` pour spécifier quelle database est utilisée.

Par exemple, En utilisant `show measurements on data` on a accès à la liste des différentes valeurs du champ *measurements*. On va donc remplacer *measurements* par les champs qui nous intéresse.

Les requêtes que nous faisons pour afficher les données de notre base sont donc les requêtes suivantes :
- `SELECT "value" FROM "temperature"` 
- `SELECT "value" FROM "luminosite"`

### Installer Grafana

Pour installer Grafana sur Windows, allez sur la [documentation d'installation](https://grafana.com/docs/grafana/latest/installation/windows/)

Si vous êtes sur GNU/Linux, executez la commande suivante :

```bash
apt update && apt install grafana && sudo systemctl start grafana-server.service
```

Si vous utilisez WSL, executez la commande suivante: 

```bash
apt update && apt install grafana && sudo service grafana-server.service start
```

## Lancer le serveur

Passez au fichier **/Server_controller** de votre projet et lancer le serveur avec :
```bash
./start-server.sh
``` 

Si vous rencontrez l'erreur `-bash: ./start-server.sh: /bin/sh^M: bad interpreter: No such file or directory` executez les commandes suivantes :

Cette erreur est due au fait que votre shell n'est pas au bon format UNIX.
Pour convertir le fichier shell, installez le paquet *dos2unix* :
```bash
sudo apt-get install dos2unix && dos2unix ./start-server.sh
```

Une fois que votre fichier est sous le bon format, executez le à nouveau.

## Voir les données sur Grafana

Une fois que Grafana est installé, allez sur `http://localhost:3000/` sur votre navigateur web pour avoir accès à vos différents *dashboards* et visualiser vos données sur Grafana.

Ensuite, vous devez ajouter une source de donnée via la page sur `http://localhost:3000/datasources` et ajouter une nouvelle *datasource* qui correspond à votre base de donnée InfluxDB de votre projet. Votre URL HTTP de votre nouvelle datasource devrait être `http://localhost:8086` dans le cas où vous n'auriez pas un changer le port par défaut d'InfluxDB qui est 8086.

**BELDJILALI Ilies, CHAPUIS Flavian, FOLLÉAS Brice, GAUTHIER Gwendal, GONNET Anthony**
