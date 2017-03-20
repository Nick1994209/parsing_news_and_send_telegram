# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

    config.vm.box = "centos/7"
    config.vm.network "forwarded_port", guest: 80, host: 7171
    config.vm.network :private_network, ip: '10.11.12.20'
    config.vm.synced_folder ".", "/home/vagrant/python_projects", type: "rsync"

    # Configure the window for gatling to coalesce writes.
    if Vagrant.has_plugin?("vagrant-gatling-rsync")
        config.gatling.latency = 1.5
        config.gatling.time_format = "%H:%M:%S"
        # Automatically sync when machines with rsync folders come up.
        config.gatling.rsync_on_startup = true
    end

    config.vm.provider "virtualbox" do |vb|
        # vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/vagrant","1"]
        vb.memory = "2048"
    end

    config.trigger.after :up, :provision => "value" do
        run "vagrant gatling-rsync-auto"
    end

    config.vm.provision :ansible do |ansible|
        tags = 'system'

        if ENV['ANSIBLE_TAGS'].to_s.length != 0
            tags = ENV['ANSIBLE_TAGS'].split(',').collect{|x| x.strip || x }
        end

        ansible.playbook = 'provisioning/playbook.yml'
        ansible.host_key_checking = false
        ansible.tags = tags
    end

end