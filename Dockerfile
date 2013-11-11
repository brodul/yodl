FROM base

env   DEBIAN_FRONTEND noninteractive

# REPOS
run    apt-get install -y software-properties-common
run    add-apt-repository -y "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"
run    apt-get --yes update
run    apt-get --yes upgrade --force-yes

#SHIMS
run    dpkg-divert --local --rename --add /sbin/initctl
run    ln -s /bin/true /sbin/initctl

# TOOLS
run    apt-get install -y -q curl git wget 

env   DEBIAN_FRONTEND dialog

## App required
run    apt-get --yes install rabbitmq-server --force-yes
run    apt-get --yes install supervisor python-pip python-dev build-essential  --force-yes

## Setup App
run    cd /opt; git clone https://github.com/dz0ny/yodl.git app --depth 1
run    cd /opt/app ; python setup.py install

add    ./supervisor/supervisord.conf /etc/supervisor/supervisord.conf
add    ./supervisor/conf.d/yodl.conf /etc/supervisor/conf.d/yodl.conf

expose :80

ENTRYPOINT ["/usr/bin/supervisord"]