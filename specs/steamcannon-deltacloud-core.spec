%define jruby_version 1.8
%define deltacloud_version 0.0.7.1
%define gemname steamcannon-deltacloud-core
%define gemdir /opt/jruby/lib/ruby/gems/%{jruby_version}
%define geminstdir %{gemdir}/gems/%{gemname}-%{deltacloud_version}
%define gemcommand /opt/jruby/bin/jruby -S gem

Summary: Deltacloud REST API
Name: %{gemname}-deployment
Version: %{deltacloud_version}
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://www.deltacloud.org
Source0: http://rubygems.org/gems/%{gemname}-%{deltacloud_version}.gem
BuildRoot: %{_tmppath}/%{name}-%{deltacloud_version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{deltacloud_version}
Requires: torquebox-cloud-profile-deployers

%description
The Deltacloud API is built as a service-based REST API.
You do not directly link a Deltacloud library into your program to use it.
Instead, a client speaks the Deltacloud API over HTTP to a server
which implements the REST interface.


%prep

%build

%install
rm -Rf $RPM_BUILD_ROOT

cd %{_topdir}/BUILD
install -d -m 755 %{buildroot}%{gemdir}/gems

# install required gems 
%{gemcommand} install --install-dir=%{buildroot}%{gemdir} --ignore-dependencies --force --no-ri --no-rdoc %{gemname} -v %{deltacloud_version}

# Write deltacloud-rack.yml file 
printf "application:\n\tRACK_ROOT: %{geminstdir}-java\n\tRACK_ENV: production\nweb:\\n\tcontext: /deltacloud\nenvironment:\n\tAPI_DRIVER: ec2" > /opt/jboss-as/server/cluster-ec2/deploy/deltacloud-rack.yml

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gemdir}/bin/deltacloudd
%{gemdir}/gems/%{gemname}-%{deltacloud_version}-java/
%{gemdir}/cache/%{gemname}-%{deltacloud_version}-java.gem
%{gemdir}/specifications/%{gemname}-%{deltacloud_version}-java.gemspec


%changelog
* Mon Oct 11 2010  <builder@localhost.localdomain> - 0.0.7.1-1
- Initial package
