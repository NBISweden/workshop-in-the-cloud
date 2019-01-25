# How to setup a virtual workshop in the cloud


## Prerequisites


### Docker

Download and install the docker community edition from the [docker
website][dockerwebsite].


### Python prerequisites

You need `python3` installed.

I recommend that you use `virtualenv` for installation of python dependencies
(this is optional though):

    virtualenv venv
    source venv/bin/activate


To install the python libraries simply run


    pip install -r requirements.txt

### Set the SNIC Science Cloud API Password

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

    ./create_course.py --users 3 --course-name biostatistics --cluster-prefix workshop --student-flavor ssc.small --student-disk-size 30 --master-disk-size 100 --shared-dir /data

This will create a course instance and spin up three `student virtual machines` with 30Gb disks attached to them. Also, a `NFS server` with capacity of 100Gb is setup in the master node and mounted onto the student machines under `/data`. You can find information about virtual machine flavors in the [SNIC website][snic].

These are all the configuration settings (can also be viewed with the `--help` switch):


	usage: create_course.py [-h] --users USERS --course-name NAME [--cluster-prefix <virt-workshop>]
							[--master-flavor <ssc.small>] [--master-disk-size <0>]
							[--student-flavor <ssc.small>]
							[--student-disk-size <10>] [--shared-dir <shared-dir>]        

	optional arguments:
	  -h, --help            show this help message and exit
	  --cluster-prefix <virt-workshop>
							Cluster prefix for hostnames in openstack, default is
							virt-workshop
	  --master-flavor <ssc.small>
							The openstack flavor for the master node, default is
							ssc.small.
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

## Installing scientific software with Conda

Under `<course-name>/playbooks` there is a file called `environment.yml` where it is possible to define what Conda packages to install in the Conda environment. See an example below:

```YAML
channels:
  - bioconda
  - conda-forge
  - defaults
dependencies:
  - star=2.5.4a
  - bwa=0.7.15
```

You can find the available bioconda packages in the Bioconda [archive][bio]. For more information on how to manage Conda environments consult the [documentation][conda]

## Launch the system

The course configuration will be located under a new folder with its corresponding name. Navigate to it and launch the virtual infrastructure.

> **NOTE:** Before launching the system, you might need to add your private key to the key chain.

    cd <course-name>
    chmod 400 ssh_key && ssh-add ssh_key
    ./kn apply

> **TIP:** In order to wipe out the virtual infrastructure, you can use:

    ./kn destroy


## Data upload

To make your data available in the system use the `upload_data.py` script. This will upload your local data to a NFS server.

> **NOTE:** You might need to grant execution privileges to the upload script.

    chmod +x upload_data.py
    ./upload_data.py --local-dir ./dir1 --local-dir /opt/dir2 --remote-dir /data

These are all the configuration settings (can also be viewed with the `--help` switch):

	usage: upload_data.py [-h] --local-dir DIRS --remote-dir DIR

	 arguments:
	  -h, --help            show this help message and exit
	  --local-dir <local-dir>
						Local directory to upload to NFS. Can be repeated. For example: "--local-dir ./dir1 --local-dir /opt/dir2"
	  --remote-dir <remote-dir>
						Remote directory. For example: "--remote_dir /data"

## Student login

The credentials for accessing the virtual machines can be found in the `passwords.txt` file. Students should be able to access their instance via `ssh` by using their username and password. The `master node` IP address can be found in the `inventory` of the course folder.

    ssh <student-name>@<master-node-ip>
    
## Administrator login
Teachers should be able to access the master node via `ssh` with private key authentication.

    ssh ubuntu@<master-node-ip>

[dockerwebsite]: https://www.docker.com/community-edition "The docker website"
[cloud-portal]: https://cloud.snic.se/ "SNIC Cloud Portal"
[conda]: https://conda.io/docs/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually "Conda environments docs"
[bio]: https://bioconda.github.io/recipes.html# "Bioconda archive"
[snic]: https://cloud.snic.se/index.php/instances/ "SNIC machine flavors"
