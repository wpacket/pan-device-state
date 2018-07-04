# pan-get-device-state
A script to gather device-state from every PaloAlto Network firewall managed by your Panorama. 

## Explanation & Motivation
Device-state are bundle ( tgz ) used to fully restore or mirror a PaloAlto Network firewall. Usually, configuration blocks can be located in the running configuration but also in the Templates & Device Groups so restore in case  of RMA can be tricky. For instance by saving only the running config you might end-up having only a small portion of your full setup. A device state include all those configuration statement so the restore is neat.

## How does it work
The script will connect to Panorama, lists every firewall connected to them and execute an API call to download their device-state in a local directory. It requires:
- The Panorama FQDN or IP
- A Panorama admin account & password
- A super-user account & password on each firewall ( same login & password on each device )
- A host ( windows / linux ) & local directory path where the device-states will be saved

# How to Run it
```
pan-dev-state.py -pi <panorama_ip> -pl <panorama_api_login> -pp <panorama_api_password> -fl <fw_api_login> -fp <fw_api_password> -d <backup_directory>
```

# How to restore a device state on a firewall
```
Firewall WebUI > Device > Setup > Operations > Import Device state
```

