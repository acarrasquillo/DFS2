README
====
# Index

* [Tech Stack](#tech-stack)
* [Development setup](#development-setup)
* [Environment variables](#environment-variables)
* [Contributing](#contributing)
* [TODO](#todo)
* [Team](#team)
* [Help](#help)

# Tech stack
* Python Libraries
  * MySQLdb
  * sys
  * socket
  * json
  * datetime
* mds_db (Provided by the Professor José Ortiz-Ubarri)

# Development setup
0. Install [mysql-python](http://mysql-python.sourceforge.net/MySQLdb.html)
1. Connect to the mysql database with `mysql -u root`.
2. Create a user to connect to the databse with `CREATE USER 'user'@'localhost' IDENTIFIED BY 'pass';`.
3. Grant proviledges to the 'user' created above with `GRANT ALL PRIVILEGES ON * . * TO 'user'@'localhost;`;
4. Create the database with `CREATE DATABASE ccom4017_dfs_ram;`
5. Exit from mysql with the Crtl+D command
6. Go to the file `mds_db.py` and make shure that the `DB_USER` and the `DB_PASS` are the same as the one you setted up in step 2.
7. Verify that in `db.sql` the first line have the following `use ccom4017_dfs_ram ;` wich is the database created in step 4.
7. Create the tables with `mysql -u ram -p < db.sql`.
8. Run `python test.py` to make shure everything in running normal.

# Files Invcluded
0. Data Nodes (data_node.py): 
  0.1
Este file representa los “data nodes”. Primero se crea un directorio en el que se guardarán los “chunks” y después los “data nodes” se reportan al metadata server a través de un socket. Luego los “data nodes” se quedan esperando hasta que reciban instrucciones. Una vez se recibe una instrucción(read o write) el data node hace lo siguiente:

-Si es read:
el datanode simplemente copia el contenido del file en una variable y envia esa variable a la misma dirección donde se recibió la instrucción.
-Si es write:
el datanode guarda el string que recibió a traves del socket en un file en el directorio del nodo.

Metadata Server (meta_data.py):

Este file representa el Metadata Server. El metadata primero se conecta a la base de datos y luego se queda esperando a recibir instrucciones a través de sockets. Una vez se recibe una instrucción(reporte de nodos, list, read,write) el metadata server hace lo siguiente:

-Si es reporte de nodos:
El metadata añade el nodo a la base de datos y luego verifica y reporta al usuario si el nodo fue insertado exitosamente

-Si es list:
El metadata le pide a la base de datos que le brinde toda su información(nombre de los files y su tamaño respectivamente) y luego se los desplega al usuario.

-Si es read:
El metadata verifica si el file se encuentra en la base de datos.
Si el file se encuentra en la base de datos, el meta data le pide a la base de datos que le brinde toda la información de ese file(el nombre del file, tamaño,los id de los nodos, etc.) y se las desplega al usuario.
Si el file no existe, el metadata simplemente le deja saber al usuario que el file no se encuentra en la base de datos.

-Si es write:
El metadata se encarga de dividir el file entre los nodos disponibles para luego enviar cada chunk a un nodo diferente(esto se hace a traves del “cliente” kopy.py)
