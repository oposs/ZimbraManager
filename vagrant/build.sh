#!/bin/sh
if [ -d build ]; then
    cd build
    cp -v ~/checkouts/hin-perl-rpm/RPMS/x86_64/perl-opt-5.22.0-1.el6.x86_64.rpm .
    vagrant up
    vagrant ssh -c /vagrant/make.sh
    vagrant rsync-back
    vagrant destroy
    cd ..
fi
if [ -d build/RPMS ]; then
    if [ -d RPMS ]; then
        rm -r RPMS
    fi
    mv build/RPMS .
fi
