# Prerequisites

Python 3.9.16 or higher but < 3.12 (lxml not available for Python 3.12+)

## Python Packages

All Python packages required for this project are listed in the requirements.txt file. 
Install them with pip:  
```shell   
pip install -r requirements.txt
```

For Windows, use:
```shell
pip install -r requirements_win.txt
```

# Dofus Fashionista
The Dofus Fashionista, an equipment advisor for Dofus    
This is a fork and an attempt at putting back up the website and update it to the latest version of Dofus

# Install Fashionista:

## Windows 11

Le support pour Windows 11 est maintenant pleinement fonctionnel avec une méthode d'installation simplifiée ! Suivez ces étapes pour installer le projet :

### Option la plus simple : Exécuter DofusFashionista_Windows11.bat

```shell
# Clonage du dépôt (ou téléchargez l'archive ZIP)
git clone https://github.com/Trameurs/DofusFashionista.git fashionista
cd fashionista

# Exécution du fichier batch pour Windows 11
DofusFashionista_Windows11.bat
```

Ce fichier batch va automatiquement configurer et démarrer l'application en une seule étape.

### Options alternatives d'installation

#### Option 1 : Installation avec PowerShell

```shell
# Exécution du script PowerShell amélioré pour Windows 11
powershell -ExecutionPolicy Bypass -File run_windows11.ps1
```

Ce script PowerShell robuste va :
1. Vérifier et installer tous les prérequis nécessaires
2. Configurer automatiquement l'environnement Windows
3. Optimiser les paramètres pour la compatibilité Windows 11
4. Configurer la base de données et exécuter les migrations
5. Démarrer le serveur avec gestion automatique des erreurs

#### Option 2 : Installation traditionnelle

```shell
# Exécution du script d'installation automatisé
install_windows.bat
```

Le script d'installation automatisé va:
1. Configurer l'environnement Windows correctement
2. Installer les dépendances nécessaires
3. Configurer les fichiers de configuration
4. Créer et configurer la base de données

Une fois l'installation terminée, lancez l'application avec:
```shell
run_fashionista.bat
```

Puis accédez à `http://localhost:8000` dans votre navigateur.

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

# Dépannage Windows 11

Si vous rencontrez des problèmes lors de l'installation sur Windows 11, voici quelques solutions courantes:

1. **Erreurs MySQL**:
   - Vérifiez que MySQL est installé et que le service est démarré
   - Vérifiez que le nom d'utilisateur et le mot de passe MySQL sont corrects

2. **Erreurs de dépendances**:
   - Vérifiez que Visual C++ Redistributable est installé
   - Vérifiez que ImageMagick est installé

3. **Erreurs de ports**:
   - Si le port 8000 est déjà utilisé, modifiez la dernière ligne de run_fashionista.bat

4. **Problèmes de chemin**:
   - Vérifiez que PYTHONPATH est correctement défini
   - Redémarrez votre terminal après avoir défini PYTHONPATH

# Progress and Roadmap

✅ Website is fully operational     
✅ All equipments and mounts updated to Dofus 3.1.5.4      
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
✅ Bug fixes and improvement for 3.0 release 
✅ Windows 11 compatibility         
🚧 Translate new content           
    ✅ 100% English           
    🚧 95% French (some spells left)            
    🚧 80% Spanish (some spells and text left)           
    🚧 80% Portuguese (some spells and text left)          
    🚧 30% Deutsche (only items done)           
    ❌ 0% Italian (Ankama removed Italian language)           
❌ Add ability to forbid prysmaradite       
❌ Make it mobile friendly             
        
❌ New features after 3.0 TBD         
       
✅ Dofus 3 Unity             
❌ Dofus Touch            
❌ Dofus Retro             

# Reference

This is a fork of https://github.com/PiwiSlayer/DofusFashionista      
All items data comes from https://github.com/dofusdude/doduapi
