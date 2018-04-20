# How to setup a virtual workshop cloud

## Install the kn client

    curl -f "https://raw.githubusercontent.com/kubenow/KubeNow/development/phenomenal-dalcotidine/bin/kn" -o "kn"
    chmod +x /usr/local/bin/kn

## Get credentials from the openstack instance

Go to the webinterface of the openstack project, go to `Compute -> Access &
Security` in the sidebar and click the `API Access` tab and then `Download
OpenStack RC File v3`. Save that file as `credentials.sh`.

## Customize the setup

    ./create-users.py <num users>


## Launch the system

    ./kn apply
