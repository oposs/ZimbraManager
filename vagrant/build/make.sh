#!/bin/bash
#
# This is a simple script to allow someone on an RPM-based
# system to build the custom perl package defined by
# the RPM specfile in this same directory.
#
# @author: Stephen R. Scaffidi <sscaffidi@tripadvisor.com>
# @date: Oct. 2012
#

# abort on any error
set -e

SCRIPTDIR=$(dirname $0)
SPECNAME="zimbramanager.spec"
export PATH=/opt/oss/perl/bin:${PATH}

if [[ "$(whoami)" == "root" ]]; then
  echo "Please don't build RPMs as root!"
  echo "Run this script as a normal user."
  exit 1
fi

# make sure we have the tools we need to build RPMs
if ! which rpmdev-setuptree &> /dev/null; then
  echo "You need to install the rpmdevtools package."
  echo "To do so automatically, please enter your password for sudo."
  sudo yum -y install rpmdevtools
fi

sudo yum -y install libxml2-devel.x86_64

# install perl
if ! [ -d /opt/oss/perl ];then
  sudo rpm -i /vagrant/perl-opt-5.22.0-2.el6_6.6.x86_64.rpm
fi

# create an RPM build tree
rpmdev-setuptree

# download the perl source into the proper place in the build-tree
spectool --get-files -R "$SCRIPTDIR/zimbramanager.spec"

# ask the RPM system where certain build-dirs will be
RPMDIR=$(rpm --eval "%{_rpmdir}")
SPECDIR=$(rpm --eval "%{_specdir}")

# copy the specfile into the build tree
cp "$SCRIPTDIR/$SPECNAME" "$SPECDIR"

# finally, build the rpm!
echo "Building the RPM, please wait..."
#rpmbuild --quiet -ba "$SPECDIR/$SPECNAME"
rpmbuild -ba "$SPECDIR/$SPECNAME"

rsync -av $RPMDIR /vagrant
