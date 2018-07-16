# pan-get-device-state
A script to gather device-state from every PaloAlto Network firewall managed by your Panorama. 

## Explanation & Motivation
Device-state are bundle ( tgz ) used to fully restore or mirror a PaloAlto Network firewall. Usually, configuration blocks can be located in the running configuration but also in the Templates & Device Groups so restore in case  of RMA can be tricky. For instance by saving only the running config you might end-up having only a small portion of your full setup. A device state include all those configuration statement so the restore is neat.

## How does it work
The script will connect to Panorama, lists every firewall connected to them and execute an API call to download their device-state in a local directory. It requires:
- The Panorama FQDN or IP
- A Panorama admin account & password
- A super-user account & password on each firewall ( same login & password on each device so please make it secure )
- A host ( windows / linux ) & local directory path where the device-states will be saved

## How to Run it
```
pan-dev-state.py -pi <panorama_ip> -pl <panorama_api_login> -pp <panorama_api_password> -fl <fw_api_login> -fp <fw_api_password> -d <backup_directory>
```

## Example
```
# ~/pan-device-state$ ./pan-device-state.py -pi 10.10.10.234 -pl apiuser -pp apipass -fl apiuser -fp apipass -d /var/tmp/
IP:172.16.1.10 -- HOSTNAME:fw-remote-10
IP:172.16.1.11 -- HOSTNAME:fw-remote-11
IP:172.16.1.12 -- HOSTNAME:fw-remote-12
IP:172.16.1.13 -- HOSTNAME:fw-remote-13
IP:172.16.1.14 -- HOSTNAME:fw-remote-14
IP:172.16.1.15 -- HOSTNAME:fw-remote-15
IP:172.16.1.16 -- HOSTNAME:fw-remote-16
IP:172.16.1.17 -- HOSTNAME:fw-remote-17
IP:172.16.1.18 -- HOSTNAME:fw-remote-18
IP:172.16.1.19 -- HOSTNAME:fw-remote-19
IP:172.16.1.20 -- HOSTNAME:fw-remote-20
IP:172.16.1.21 -- HOSTNAME:fw-remote-21
IP:172.16.1.22 -- HOSTNAME:fw-remote-22
IP:172.16.1.23 -- HOSTNAME:fw-remote-23

# ~/pan-device-state$ ls /var/tmp/
2018-7-10  2018-7-12  2018-7-16

# ~/pan-device-state$ ls /var/tmp/2018-7-16/
fw-remote-10.tgz  
fw-remote-11.tgz  
fw-remote-12.tgz  
fw-remote-13.tgz  
fw-remote-14.tgz  
fw-remote-15.tgz  
....

```

## How to restore a device state on a firewall
```
Firewall WebUI > Device > Setup > Operations > Import Device state
```

