# Cluster configuration
provider = "openstack" # cloud provider for this config(don't change it)
cluster_prefix = "your-cluster-prefix" # Your cluster prefix
floating_ip_pool = "your-pool-name"
external_network_uuid = "external-net-uuid" # The uuid of the external network in the OpenStack tenancy
boot_image = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"
bootstrap_script = "bootstrap/plain.sh"
skip_image_import = "true"

# Master configuration
master_flavor = "your-master-flavor"

# Node configuration
node_count = "3"
node_flavor = "your-node-flavor"

provision = {

}

provisioner_image = "kubenow/provisioners:development-phenomenal-dalcotidine"
