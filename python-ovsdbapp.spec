%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library ovsdbapp
%global module ovsdbapp
%global with_doc 0

%global common_desc \
A library for writing Open vSwitch OVSDB-based applications.

%global common_desc_tests \
Python OVSDB Application Library tests. \
This package contains Python OVSDB Application Library test files.

%bcond_with tests

Name:       python-%{library}
Version:    1.6.0
Release:    1.CROC1%{?dist}
Summary:    Python OVSDB Application Library
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

Patch0:     0001-nb-fix-port-KeyError-in-lr_route_add.patch

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git

%package -n python3-%{library}
Summary:    Python OVSDB Application Library
%{?python_provide:%python_provide python3-%{library}}
Requires:   python3-openvswitch
Requires:   python3-pbr
Requires:   python3-netaddr >= 0.7.18

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-mock
BuildRequires:  python3-openvswitch
BuildRequires:  python3-netaddr >= 0.7.18

%description -n python3-%{library}
%{common_desc}


%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    Python OVSDB Application Library documentation

BuildRequires: python3-sphinx

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.
%endif

%description
%{common_desc}


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{library}-%{upstream_version} -S git -p 1


%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%files -n python3-%{library}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Mon Nov 09 2020 RDO <dev@lists.rdoproject.org> 1.6.0-1
- Update to 1.6.0

* Wed Oct 21 2020 Joel Capitao <jcapitao@redhat.com> 1.5.0-2
- Enable sources tarball validation using GPG signature.

* Fri Sep 18 2020 RDO <dev@lists.rdoproject.org> 1.5.0-1
- Update to 1.5.0

