#!/bin/bash
# Simple script to confgiure upstart 
#

set -e

if [ $USER != 'root' ];then
    echo "You need to run this script as root"
    exit 1
fi

echo "Configuring cito-plugin-server.."
ln -sf /lib/init/upstart-job /etc/init.d/cito-plugin-server
cp /opt/cito/bin/upstart/cito-plugin-server.conf /etc/init/
/usr/sbin/update-rc.d cito-plugin-server defaults