# Prerequisites

Python 3   
MySql

# dofusfashionista
The Dofus Fashionista, an equipment advisor for Dofus    
This is a fork and an attempt at putting back up the website and update it to the latest version of Dofus

## Install and Run Fashionista:

Unix :     
$ git clone https://github.com/Trameurs/DofusFashionista.git fashionista  
Add "export PYTHONPATH=/home/<\<user\>>/fashionista/fashionistapulp" at the end of ~/.bashrc  
$ chmod 777 fashionista  
$ chmod 777 fashionista/fashionistapulp/fashionistapulp  
$ cd fashionista  
$ sudo ./configure_fashionista_root.py -i -s -d  
$ ./configure_fashionista.py  
$ sudo ./run_fashionista.sh  

Windows :     
$ git clone https://github.com/Trameurs/DofusFashionista.git fashionista   
Add "C:\Users\YourUsername\fashionista\fashionistapulp" to your "Environment Variables" section "User variables" with the variable name "PYTHONPATH"    
Run the "CMD" as administrator    
$ cd fashionista    
$ python configure_fashionista_root.py -i -s -d    
$ python configure_fashionista.py    
$ run_fashionista.bat    

# Reference

This is a fork of https://github.com/PiwiSlayer/DofusFashionista.git
