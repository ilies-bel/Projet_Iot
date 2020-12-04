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

### Installing Grafana

To install Grafana on Windows, go to the [Grafana Installation Documentation](https://grafana.com/docs/grafana/latest/installation/windows/)

Otherwise if you are installing Grafana on GNU/Linux execute the following lines :

```bash
apt update && apt install grafana && sudo systemctl start grafana-server.service
```

If you are using WSL use this command instead : 

```bash
apt update && apt install grafana && sudo service grafana-server.service start
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

## Viewing results on Grafana

Once Grafana installed, go to `http://localhost:3000/` on your web browser to have access to your different dashboards and visualize your data on Grafana.

Then, you have to go on `http://localhost:3000/datasources` to add a new datasource corresponding to the InfluxDB database of the project. The HTTP URL of the new datasource should be `http://localhost:8086` as 8086 is the default port of InfluxDB. If you have change it, write the new port.

**BELDJILALI Ilies, CHAPUIS Flavian, FOLLÉAS Brice, GAUTHIER Gwendal, GONNET Anthony**
