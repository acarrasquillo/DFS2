README
====
# Index

* [Tech Stack](#tech-stack)
* [Development setup](#development-setup)
* [Files Included](#files-included)
* [Team](#team)

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
7. If the server will run in an external IP Address, make shure that the server point to the database, go to the `mdsConfig.py` and change the variables `mds_PORT` and `mds_HOST` to the ones desired.
7. Verify that in `db.sql` the first line have the following `use ccom4017_dfs_ram ;` wich is the database created in step 4.
7. Create the tables with `mysql -u ram -p < db.sql`.
8. Run `python test.py` to make shure everything in running normal.


# Files Included
0. Metadata Server (meta_data.py):

* This file represents the Server. If first connect to the database and then wait for instructions. If the server recieve:

  * List       : Rerurn all the files and their size showed in the database.
  * Node Report: If a node report, it's inserted in the database and then returns a message of succesfull or fail.
  * Read       : The server looks for the file in the database. If exists the database returns all the information about that file. If not it's notified to the user.
  * Write      : Once recieve a write, the server divides it between the nodes and then send each chunk to a different node.
 
* How to run it?

  *  The server is run with the following command: `sudo python meta_data.py` (Sudo because of the sockets permissions)
  *  The list command: `python list.py <meta-data-server-ip-address>`
  *  The node report : `python data_node.py <port> <name-of-chunk-directory>`
  *  Write and read are used by the `kopy.py` command:
     - Copy from computer to DFS: `python copy <path of the file> <metadata-server-ip-address:path on the DFS>`
     - Copy from DFS to computer: `python copy <metadata-server-ip-address:path on the DFS> <path of the file>`
 
1. Data Nodes (data_node.py): 

* This file represents the data nodes. Once created, a Folder is created to store the 'chunks', the the data node is reported to the server, notifying that it's available. Then the data node it's constantly receiving server orders.

  * Read : The data-node copies the content of a file and save it in the corresponded file indicated in the call.
  * Write: The data-node stores the data recieved from the server in the node's directory.

* How to run it?
   - Run in a terminal `python data_node.py <port> <name-of-chunk-directory>`
   - Note: The server must be running to recieve the node. 

