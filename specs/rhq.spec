Summary:        RHQ server
Name:           rhq
Version:        3.0.0
Release:        1
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        http://downloads.sourceforge.net/project/%{name}/%{name}/%{name}-%{version}/rhq-server-%{version}.zip
Source3:        rhq.init
Source4:        preconfigure-rhq.sh
Source5:        rhq-server.properties
Requires:       shadow-utils
Requires:       java-1.6.0-openjdk
Requires:       unzip
Requires:       urw-fonts
Requires(pre):  postgresql-server
Requires(post): /sbin/chkconfig
Requires(post): /bin/sed
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv:    0
AutoReq:        0

%define runuser %{name}
%define __jar_repack %{nil}

%description
The RHQ project is an abstraction and plug-in based systems management suite that provides extensible and integrated systems management for multiple products and platforms across a set of core features. The project is designed with layered modules that provide a flexible architecture for deployment. It delivers a core user interface that delivers audited and historical management across an entire enterprise. A Server/Agent architecture provides remote management and plugins implement all specific support for managed products. RHQ is an open source project licensed under the GPL, with some pieces individually licensed under a dual GPL/LGPL license to facilitate the integration with extended packages such as Jopr and Embedded Jopr.

%prep
echo RPM_BUILD_DIR
rm -rf $RPM_BUILD_DIR
unzip -q %{SOURCE0} -d $RPM_BUILD_DIR

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}-%{version}
cd %{name}-server-%{version} 
cp -R . $RPM_BUILD_ROOT/opt/%{name}-%{version}

install -d -m 755 $RPM_BUILD_ROOT/usr/share/%{name}
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT/usr/share/%{name}/preconfigure-rhq.sh
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/usr/share/%{name}/rhq-server.properties

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "RHQ_VERSION=%{version}"            > $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "RHQ_HOME=/opt/%{name}-%{version}" >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}/%{name}

%clean
rm -Rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r %{name} 2>/dev/null || :
/usr/sbin/useradd -c "%{name}" -r -s /bin/bash -d /opt/%{name}-%{version} -g %{name} %{name} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig %{name} on

%files
%defattr(-,rhq,rhq)
/

%changelog
* Thu Jul 08 2010 Marek Goldmann 3.0.0
- Upgrade to upstream 3.0.0 release

* Tue Jun 29 2010 Marek Goldmann 3.0.0.B06
- Upgrade to upstream 3.0.0.B06 release

* Fri May 05 2010 Marek Goldmann 3.0.0.B05
- Upgrade to upstream 3.0.0.B05 release

* Mon Feb 22 2010 Marek Goldmann 3.0.0.B03
- Upgrade to upstream 3.0.0.B03 release

* Mon Feb 01 2010 Marek Goldmann 3.0.0.B01
- Upgrade to upstream 3.0.0.B01 release

* Tue Dec 24 2009 Marek Goldmann 1.4.0.B01
- Initial packaging
