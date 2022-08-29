# Ransomware

# Description
This repo is one of the 2 that build a ransomware. It's the client(the ransomware itself, the dangerous one)
It encrypts all files in directory RANSOM, and to decrpt them the server(RANSOMWARE SERVER REPO) have to
decrypt one of your keys(fernet key) with it's private key.  
  
Again... IT'S A SOURCE CODE OF MALWARE - RANSOMWARE. DO NOT USE IT IF YOU DON'T KNOW WHAT YOU ARE DOING.
DO NOT PUT SENSITIVE FILES IN 'RANSOM' DIRECTORY. DO NOT CHANGE CODE CONSTANTS(SUCH AS ENCRYPTION DIRECTORYFOR YOUR OWN SAFETY)
THANKS IN ADVANCE  
  
anyway for more info view attached png files. Basically there are two points of focus in the project - the encryption/decryption algorithms,
the cryptography. And the bitcoin transaction validation logic.  
  
Currently It has no features of other malwares like evasion techniques, persistency etc. but pure ransomware logic.  
  
Made by Timur Pichkhadze, Ben Itshak Abadayev. Final cyber project Netanya Academic College 2022. Client part.  

# End Description  
  
Create virtual env (as long you didn't deleted it, run it on time):  
  
```  
python3 -m venv ./venv/ && ./venv/Scripts/activate.bat  
```  
  
Install dependencies:  
  
```  
pip3 install -r requirements.txt  
```  
  
To destroy virtual env:  
  
```  
deactivate && rm venv  
```  