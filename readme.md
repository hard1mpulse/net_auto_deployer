Python 3.12 required!
Tested on Netbox v4.0.5

To install all requirements:
```
python -m pip install -r requirements.txt
```
Add x attribute to main.py
```
chmod +x main.py
```

You need to add custom fiels "transport_cred" and "transport_method" in your netbox to associate your credential configuration and transport method.
After that you need to set this custiom fiels to all your network device which you want to backup.

