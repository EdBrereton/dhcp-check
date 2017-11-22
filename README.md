# DHCP-Check

DHCP-Check is a small python project designed to check on who is currently connected to a wifi network. It does this by connecting to the router DHCP log page and pulling out the returned MAC addresses. It is possible to register a MAC address to a name, so that the name is returned.

## Dependancies

DHCP-Check is written using only python3, and has no additional dependancies.

It also assumes that you have a Netgear router. Currently it is known to work on a DGND3700, and has the username and password hard coded. It should be able to work on any router if you are able to find the url, user and password required for the DHCP status page.

## Usage

Available functions

* Initialise database
* Add/register MAC address to db
* Clear database
* Scan

### Initialise Database
To initialise the databse, do the following

```bash:~>./getmacs.py init```

### Add/register MAC address
To add a MAC address to the DB, do the following

```bash:~>./getmacs.py <mac_address> <name>```

### Clear Database
To clear out an existing database (and not remove the database file), do the following

```bash:~>./getmacs.py clear```

### Scan
To perform a scan and display the devices on the network, do the following

```bash:~>./getmacs.py ```

