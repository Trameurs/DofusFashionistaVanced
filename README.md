# Prerequisites

Python 3.9.16 or  but < 3.12 (lxml not available)

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
python3 get_equipments3.py
python3 get_equipments4.py  
cd ..
python3 resize_images.py
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
✅ Sets 2.70 done  
✅ Updated all special effects to 2.70     
✅ Special items effects updated including Prytek         
✅ Update UI to reflect new Dofus and Prytek       
✅ Add Forgelance          
✅ Update all spells to 2.70          
✅ Update weights of special items including Dofus and Prysmaradite         
✅ Release a beta version          
✅ Add support for new languages         
    ✅ Deutsche          
    ✅ Italian          
🚧 Translate new content           
    ✅ 100% English           
    🚧 95% French (some spells left)            
    🚧 80% Spanish (some spells and text left)           
    🚧 80% Portuguese (some spells and text left)          
    🚧 30% Deutsche (only items done)           
    ❌ 0% Italian (Ankama removed Italian language)           
✅ All equipments and mounts updated to Dofus 3 Unity 3.0.38.27      
✅ Bug fixes and improvement for 3.0 release   
❌ Add ability to forbid prysmaradite       
❌ Make it mobile friendly             
        
❌ New features after 3.0 TBD         
       
✅ Dofus 3 Unity             
❌ Dofus Touch            
❌ Dofus Retro             
              

# Reference

This is a fork of https://github.com/PiwiSlayer/DofusFashionista      
All items data comes from https://github.com/dofusdude/doduapi
