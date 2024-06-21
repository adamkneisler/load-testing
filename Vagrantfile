# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "locust"

  config.vm.provider "virtualbox" do |v| 
    v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    v.memory = 1024
    v.cpus = 2
    #v.gui = true
  end

  config.vm.synced_folder "./", "/vagrant",
      owner: "vagrant", group: "vagrant"

  # Forward a port from the guest to the host, which allows for outside
  # computers to access the VM, whereas host only networking does not.
  config.vm.network :forwarded_port, guest: 8089, host: 8089

  # Provision using the development ansible role
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "./deployment/locust.yml"
  end

  config.vm.provision "shell", privileged: false, inline: <<-EOF
    echo "Load testing environment provisioned!"
    echo "vagrant ssh  <----- log into VM."
    echo "sh run-test.sh <--- start load test."
    EOF
end
