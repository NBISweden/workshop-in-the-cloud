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
    (Valentin) this is something important to decide on, because it adds a lot of complexity

Other notes to start off with
  + We can test on SSC, on which there is a project
  + Use Terraform / Ansible for provider-agnosticity and setup automation
  + one instance per user would be great but on SSC we are limited in IP adresses and disk space, and we cannot attach volumes to multiple instances
  + According to henrik SLURM is not used normally during courses, instead nodes are booked to login to

Infrastructure notes
  + Since we are starting on SSC we'll have limited public IPs, so we probably want to run a public frontend login node and worker nodes with private IPs
  + A nice way to automate this would be to have the frontend act as a simple load balancer which forwards the user to their worker node upon login
  + This is currently what is happening on UPPMAX bianca system, where the shell is a script that forwards a user
  
UX
  + run script `./start_cluster --target SNIC --users users.txt  # users.txt is eg tab separated and contains usernames/pubkeys`
  + This launches some instances from an image containing tools, instance amount will depend on nr of users, predefined ratios?
  + Attaches a volume or muliple volumes with data
  + Will return a text file or similar result with IP number(s) for students to login to
