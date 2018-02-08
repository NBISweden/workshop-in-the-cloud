# The NBIS virtual fallback cluster
The virtual fallback cluster is a simulated bioinformatics cluster environment which is used for training purposes in cases where the regular cluster system is not available.
__This is very much work in progress__

Demands for this system are
  + Contain data and tools necessary for courses
  + Support maximally 30 simultaneous users
  + Easy to set up for course responsible (automatic)

Nice to have
  + Run on a cloud system (probably a demand turn on/off functionality is a good fit)
  + Cloud-provider agnostic
  + Emulate UPPMAX with SLURM and modules (although this can be seen as a learning overhead)

Other notes to start off with
  + We can test on SSC, on which there is a project
  + Use Terraform / Ansible for provider-agnosticity and setup automation
