# Vagrantfile to spin up 4 virtual machines
# 1) lb01/ansible control server
# 2) app01 server
# 3) db01 server
# 4) m01 server for monitoring
# This should put you at the lb01/control host
#  with access, by name, to other vms
Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true

  config.vm.box = "ubuntu/trusty64"

  config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2
  end
  
  config.vm.define "lb01", primary: true do |h|
    h.vm.network "private_network", ip: "192.168.135.10"
    h.vm.network :forwarded_port, guest: 80, host: 9090
    h.vm.provision :shell, :inline => <<'EOF'
if [ ! -f "/home/vagrant/.ssh/id_rsa" ]; then
  ssh-keygen -t rsa -N "" -f /home/vagrant/.ssh/id_rsa
fi
cp /home/vagrant/.ssh/id_rsa.pub /vagrant/control.pub

cat << 'SSHEOF' > /home/vagrant/.ssh/config
Host *
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
SSHEOF

chown -R vagrant:vagrant /home/vagrant/.ssh/
EOF
  end

  config.vm.define "m01" do |h|
    h.vm.network "private_network", ip: "192.168.135.101"
    h.vm.network :forwarded_port, guest: 80, host: 8090
    h.vm.provision :shell, inline: 'cat /vagrant/control.pub >> /home/vagrant/.ssh/authorized_keys'
  end

  config.vm.define "app01" do |h|
    h.vm.network "private_network", ip: "192.168.135.111"
    h.vm.provision :shell, inline: 'cat /vagrant/control.pub >> /home/vagrant/.ssh/authorized_keys'
  end

  config.vm.define "db01" do |h|
    h.vm.network "private_network", ip: "192.168.135.121"
    h.vm.provision :shell, inline: 'cat /vagrant/control.pub >> /home/vagrant/.ssh/authorized_keys'
  end
end
