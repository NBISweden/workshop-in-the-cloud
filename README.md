# How to setup a virtual workshop in the cloud


## Prerequisites


### Docker

Download and install the docker community edition from the [docker
website][dockerwebsite].


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

Go to the [cloud portal][cloud-portal] and in the left hand menu there's a
link to `Set your API password`. Go there and do that.


### Get credentials file from the openstack instance

Go to the webinterface of the openstack project, go to `Compute -> Access &
Security` in the sidebar and click the `API Access` tab and then `Download
OpenStack RC File v3`. Save that file as `credentials.sh` or something
similar.

Then you have to source this file and enter the API password:

    source credentials.sh


## Setup

To create the configuration for the system run `create_course.py`. This will
create the configuration files for the cloud and also generate a file,
`passwords.txt` with usernames and passowords for the students.

For example it can be run something like this:

    ./create_course.py --users 1 --student-disk-size 30 --shared-dir /data --local-data data --local-data ref

This will create a course instance with 10 users and a work area for each
student that is 30Gb.

These are all the configuration settings (can also be viewed with the `--help` switch):


	usage: create_course.py [-h] --users USERS [--cluster-prefix <virt-workshop>]
							[--master-flavor <ssc.small>] [--master-disk-size <0>]
							[--student-flavor <ssc.small>]
							[--student-disk-size <10>] [--shared-dir <shared-dir>]

	optional arguments:
	  -h, --help            show this help message and exit
	  --users USERS         Either The number of users to generate credentials for
							or a file with usernames, one per line.
	  --cluster-prefix <virt-workshop>
							Cluster prefix for hostnames in openstack, default is
							virt-workshop
	  --master-flavor <ssc.small>
							The openstack flavor for the master node, default is
							ssc.small
	  --master-disk-size <0>
							The disk size for the extra disk of the master node,
							in Gb, default is 0
	  --student-flavor <ssc.small>
							The openstack flavor for the student nodes, default is
							ssc.small
	  --student-disk-size <10>
							The disk size for the extra disk of the student nodes,
							in Gb, default is 10
	  --shared-dir <shared-dir>
							Directory that should be shared from the master node
							to the compute nodes, can be repeated. For example: "
							--shared-dir /data --shared_dir /references"

## Launch the system

    ./kn apply

## Data upload

To make your data available in the system run `upload_data.py`. This will upload your local data to a NFS server.

For instance, you can do:

    ./upload_data.py --local-dir $(pwd)/data --remote-dir /data

These are all the configuration settings (can also be viewed with the `--help` switch):

    	usage: upload_data.py [-h] --local-dir DIRS --remote-dir DIR

    	optional arguments:
    	  -h, --help            show this help message and exit
        --local-dir <local-dir>
    							Local directory to upload to NFS. For example: "--local-dir $(pwd)/dir --local-dir $(pwd)/references
    	  --remote-dir <remote-dir>
    							Remote directory. For example: "--remote_dir /data"


[dockerwebsite]: https://www.docker.com/community-edition "The docker website"
[cloud-portal]: https://cloud.snic.se/ "SNIC Cloud Portal"
