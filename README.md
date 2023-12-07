# Prerequisites

Python 3.9.16 or higher  

## Python Packages

All Python packages required for this project are listed in the requirements.txt file. 
Install them with pip:  
```shell   
pip install -r requirements.txt
```

# Dofus Fashionista
The Dofus Fashionista, an equipment advisor for Dofus    
This is a fork and an attempt at putting back up the website and update it to the latest version of Dofus

# Install Fashionista:

## Unix / AWS EC2

SSH into your EC2 instance if needed

```shell 
git clone https://github.com/Trameurs/DofusFashionista.git fashionista  
echo "export PYTHONPATH=/home/<\<user\>>/fashionista/fashionistapulp" >> ~/.bashrc  
chmod 777 fashionista  
chmod 777 fashionista/fashionistapulp/fashionistapulp  
cd fashionista  
sudo python3 ./configure_fashionista_root.py -i -s -d  
```

Configure files in /etc/fashionista

```shell
python3 ./configure_fashionista.py
```

## Windows

I started working on Windows compatibily but abandonned, it should work until run_fashionista.bat, still a lot to fix if you want to try.

```shell
git clone https://github.com/Trameurs/DofusFashionista.git fashionista
setx PYTHONPATH "C:\Users\YourUsername\fashionista\fashionistapulp"
cd fashionista
python configure_fashionista_root.py -i -s -d
```

Configure files in /APPDATA/fashionista

```shell
python configure_fashionista.py
```

# Items scraper

The old scraper is still in the folder itemscraper, it uses the Dofus website Encyclopedia. It is veryyyy slow and the Encyclopedia is missing a lot of items, it's not viable to use it anymore. I made a new scraper that just convert the data from https://docs.dofusdu.de/ to something that store_venom.py can use.

```shell
cd itemscraper  
python3 get_equipments.py  
python3 get_equipments2.py  
cd ..
python3 store_venom.py
```

# Run Dofus Fashionista

Running Dofus Fashionista will create/populate the database the first time you run it or recreate it if you used the Scraper.

## Unix / AWS EC2

```shell
./run_fashionista.sh
```

## Windows

```shell
run_fashionista.bat
```

# Progress and Roadmap

✅ Website is fully operational     
✅ All equipments and mounts updated to Dofus 2.70     
✅ Larger filter for Temporis items done   
✅ Sets done     
✅ Special items effects added    
❌ Details before release

# Reference

This is a fork of https://github.com/PiwiSlayer/DofusFashionista      
The scraper now uses https://github.com/dofusdude/doduapi