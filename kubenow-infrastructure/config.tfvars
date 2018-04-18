# Cluster configuration
provider = "openstack"
cluster_prefix = "virt-workshop"

floating_ip_pool = "Public External IPv4 network"
external_network_uuid = "af006ff3-d68a-4722-a056-0f631c5a0039" # The uuid of the external network in the OpenStack tenancy

boot_image = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"
bootstrap_script = "bootstrap/plain.sh"
skip_image_import = "true"

# Master configuration
master_flavor = "ssc.small"
master_count = 2

# Node configuration
node_count = "2"
node_flavor = "ssc.small"

provision = {

}

provisioner_image = "kubenow/provisioners:development-phenomenal-dalcotidine"
