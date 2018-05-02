# How to setup a virtual workshop in the cloud


## Prerequisites


### Docker

Download and install the docker community edition from the [docker website][dockerwebsite].


### Python prerequisites

You need python3 installed.

I recommend that you use `virtualenv` for installation of python dependencies
(this is optional though):

    virtualenv venv
    source venv/bin/activate


To install the python libraries simply run


    pip install -r requirements.txt


### KubeNow cloud provisioner

We are using the KubeNow cloud provisioning client to set up the cloud, you
need to download this. Here is a simple commandline to do that and store it in
the root of this project.

    curl -f "https://raw.githubusercontent.com/kubenow/KubeNow/development/phenomenal-dalcotidine/bin/kn" -o "kn"
    chmod +x ./kn


### Set the SNIC Science CLoud API Password

Go to the [cloud portal][cloud-portal] and in the left hand menu there's a link
to `Set your API password`. Go there and do that.


### Get credentials file from the openstack instance

Go to the webinterface of the openstack project, go to `Compute -> Access &
Security` in the sidebar and click the `API Access` tab and then `Download
OpenStack RC File v3`. Save that file as `credentials.sh` or something similar.

Then you have to source this file and enter the API password:

    source credentials.sh


## Setup

    ./create-users.py <num users>


## Launch the system

_This doesn't work without editing a bunch of files._

    ./kn apply


[dockerwebsite]: https://www.docker.com/community-edition "The docker website"
[cloud-portal]: https://cloud.snic.se/ "SNIC Cloud Portal"
