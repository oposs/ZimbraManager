%define zimbramanagerver 1.5.1
%define zimbramanagername ZimbraManager-%{zimbramanagerver}
%define zimbramanagerpath /opt/oss/ZimbraManager-%{zimbramanagerver}
%define zimbra-user hea_diu2

Name:           ZimbraManager 
Version:        1.5.1
Release:        2.el6_6.6
Summary:        Zimbra commandline administration with Perl and SOAP 
Group:          misc
License:        GPLv1+
URL:            https://github.com/oposs/ZimbraManager 
Source0:        https://github.com/oposs/ZimbraManager/archive/v1.5.1.tar.gz 
Packager:       OETIKER+PARTNER AG Manuel Oetiker <http://www.oetiker.ch>
BuildRoot:      %{_tmppath}/%{zimbramanagername}-%{release}-root-%(%{__id_u} -n)
AutoReq:        no
AutoProv:       no
requires:       perl-opt 


# this is necessary to prevent the scanning for rpaths in built libs
%undefine __arch_install_post



%description
Zimbra commandline administration with Perl and SOAP.
This tool runs much faster than calling 'zmprov' from the command line.

%prep
%setup -q -n %{zimbramanagername}


%build
setup/build-perl-modules.sh

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt/oss/%{zimbramanagername}
cp -r {AUTHORS,CHANGES,COPYRIGHT,LICENSE,README.md,bin,lib,test,thirdparty} %{buildroot}/opt/oss/%{zimbramanagername}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/ZimbraManager/wsdl
install -p -m644 setup/rhel/sysconfig/ZimbraManager %{buildroot}%{_sysconfdir}/sysconfig/ZimbraManager
install -p -m755 setup/rhel/rc.d/init.d/ZimbraManager %{buildroot}%{_initrddir}/ZimbraManager
install -p -m755 setup/rhel/logrotate.d/ZimbraManager %{buildroot}%{_sysconfdir}/logrotate.d/ZimbraManager
chmod -R u+w %{buildroot}/*

%clean
rm -rf %{buildroot}

%files
%{zimbramanagerpath}/AUTHORS
%{zimbramanagerpath}/CHANGES
%{zimbramanagerpath}/COPYRIGHT
%{zimbramanagerpath}/LICENSE
%{zimbramanagerpath}/README.md
%{zimbramanagerpath}/bin
%{zimbramanagerpath}/lib
%{zimbramanagerpath}/test
%{zimbramanagerpath}/thirdparty
%config(noreplace) %{_sysconfdir}/sysconfig/ZimbraManager
%config(noreplace) %{_sysconfdir}/ZimbraManager
%{_sysconfdir}/logrotate.d/ZimbraManager
%{_initrddir}/ZimbraManager

%defattr(-,root,root,-)

%post
if [ -h /opt/oss/ZimbraManager ]; then
        unlink /opt/oss/ZimbraManager
fi
ln -s /opt/oss/%{zimbramanagername} /opt/oss/ZimbraManager
chkconfig --add ZimbraManager
if [ -h /opt/oss/%{zimbramanagername}/etc ]; then
        unlink /opt/oss/%{zimbramanagername}/etc 
fi
ln -s  /etc/ZimbraManager /opt/oss/%{zimbramanagername}/etc
echo "###########################################################"
echo "cd /etc/ZimbraManager/wsdl"
echo "/opt/oss/ZimbraManager/bin/get-wsdl.sh zimbra.hostname"
echo "###########################################################"

%preun
if [ "$1" -eq 0 ]; then
   /sbin/chkconfig --del ZimbraManager 
fi
:

%changelog
* Tue Aug 25 2015 Manuel Oetiker <manuel@oetiker.ch> 1.5
- Initial RPM release
* Tue Aug 25 2015 Manuel Oetiker <manuel@oetiker.ch> 1.5 -> 1.5.1
- Add module versions 
