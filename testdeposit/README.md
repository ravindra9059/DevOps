# DepositSolutionsTest
Committed files for Deposit Solutions

4 ubuntu vms (each of 2 GB RAM & 2 CPU) are spun up to run two app servers, two database (1 master & 1 slave) for redundancy, 1 load balancer (nginx also reverse proxy) & 1 monitoring server (having ganglia agent). All the machines were created by Oracle VM box hypervisor & vagrant.

Below are the host names, configurations & software installed.
1) lb01 : Acts as load balancer, reverse proxy, ansible control server & nginx log parser. 
   a) nginx configuration files are in /etc/nginx/ directory. (nginx.conf & conf.d/defaults.conf files)
   b) cached responses are stored in /home/vagrant/nginxcache
   c) nginx log files are sored in /var/log/nginx/ directory. (both access.log & error.log)
   d) ansible configurations are stored in /home/vagrant/ansible directory (ansible.cfg, inventory & playbooks)
   e) Finally lb01 has goaccess software to parse nginx logs and pretty present the logs as mentioned in section 4
      command to run is : "sudo goaccess -f /var/log/nginx/access.log"
   
2) app01 : Acts as an application server & slave mysql database
   a) app codebase in app/springboot-demo-app directory and "java -jar target/entries-1.0.0.jar" will run the java process
   b) env variables containing are permanently stored and could be viewed by printenv command
      export APP_DATABASE_USER=slave_user
      export APP_DATABASE_PASSWORD=ItsComplexPas1word!
      export APP_DATABASE_URL='jdbc:mysql://192.168.135.121:3306/deposit_solutions?autoReconnect=true'
      export APP_DATABASE_SCHEMA=none
      export APP_FLYWAY_ENABLED=false
      export MAVEN_OPTS="-Xms512m -Xmx1024m" 
   c) It acts as the slave mysql database as well. Run "show slave status\G;" command to check the replication status. Slave configuration present in /etc/mysql/my.cnf file
 
 3) db01 : Acts as a mysql database server & application server
    a) Acts as MySQL master database. "Run show master status\G;" to check the master status. Master configuration present in /etc/mysql/my.cnf file.
    b) Application configuration is same as app01 including env variables
    c) Database replicated is deposit_solutions and it has entries table which is created by flyway schema migration.
    
 4) m01 : Acts as a montoring server. Ganglia is the opensource montioring tool.
    a) Ganglia configurations are in /etc/ganglia directory. gmetad.conf & gmond.conf are the configuration files
    b) gmetad.conf file has server related metadata & gmond.conf has client related configuration to monitor ganglia server
    c) All ganglia clients db01, app01 & lb01 nodes have gmond process which ingest data to m01 and they are part of "Deposit Solution Cluster" available at http://94.130.52.98:8090/ganglia webpage.  The webpage has both cluster & server wise metric details.
   
 For Load Testing :
 
      I've used locust in my local machine to generate the load. Locust is a python application which could generate load to test http APIs. 

      locust.py is attached to this repo. Command to trigger the load is "locust --host=http://<host:port>". Upon issuing the above command, open http://localhost:8089/ on the browser and issue the load parameters suiting your needs. API urls, http methods are configured in locust.py file.

  Publicly accessible URLs :
       http://94.130.52.98:9090/api/v1/entries
       http://94.130.52.98:8090/ganglia
       
    The port forwarding is done via Vagrantfile configuration and it is attached to this repository.
    
  MYSQL master-slave replication :
      
      Database : deposit_solutions
      dbuser : slave_user
      dbpassword : ItsComplexPas1word!
      dburl : jdbc:mysql://192.168.135.121:3306/deposit_solutions?autoReconnect=true
      master node : 192.168.135.121:3306
      slave node : 192.168.135.111:3306
      root-user : root
      root-password : Password1
      Both the servers have same credentials
   
   Vagrant configuration :
       
       With attached Vagrantfile in the directory, a simple "vagrant up" will spin up 4 machines. lb01 ssh key is shared with other vagrant hosts as ansible works with SSH. In case if you would like to logon to the box with user credentials, use "vagrant" user. password is also "vagrant". Example: "ssh vagrant@app01". vagrant user has root priveleges when used with "sudo".


