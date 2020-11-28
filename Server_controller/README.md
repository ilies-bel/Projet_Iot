#### BELDJILALI Ilies, CHAPUIS Flavian, FOLLÉAS Brice, GAUTHIER Gwendal, GONNET Anthony

# Server controller 

## Installation

### Installing InfluxDB
You should first install InfluxDB on your working environment :

If your booted on a Linux OS execute this command line as follow to install InfluxDB and run the service :
```bash 
sudo apt-get update && sudo apt-get install influxdb && sudo systemctl unmask influxdb.service && sudo systemctl start influxdb
 ```

If your using WSL execute the following line to install InfluxDB and run the service :
```bash 
sudo apt-get update && sudo apt-get install influxdb && sudo systemctl unmask influxdb.service && sudo service influxdb start
 ```

## Launching the server

Move to **/Server_controller** of your project and then start the server with this command line : 

```bash 
 ./start-server.sh
```

If you encounter a `-bash: ./start-server.sh: /bin/sh^M: bad interpreter: No such file or directory` do the instructions as followed :

This error is due to the fact that your file is not on a UNIX format.
To convert this to the right format install *dos2unix* :
```bash
sudo apt-get install dos2unix && dos2unix ./start-server.sh
```

Once your file is in the right format execute it once again.