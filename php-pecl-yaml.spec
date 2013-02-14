%global pecl_name yaml

%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

Name:           php-pecl-yaml
Version:        1.1.0
Release:        3%{?dist}
Summary:        Support for YAML 1.1 serialization using the LibYAML library
Group:          Development/Languages

License:        MIT
URL:            http://code.google.com/p/php-yaml/
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRequires:      php-devel >= 5.2.0
BuildRequires:      php-pear libyaml-devel
Requires:           php(zend-abi) = %{php_zend_api}
Requires:           php(api) = %{php_core_api}
Requires(post):     %{__pecl}
Requires(postun):   %{__pecl}

Provides:       php-pecl(%{pecl_name}) = %{version}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$


%description
The YAML PHP Extension provides a wrapper to the LibYAML library. It gives the
user the ability to parse YAML document streams into PHP constructs and emit PHP
constructs as valid YAML 1.1 documents.

%prep
%setup -q -c
mv package.xml %{pecl_name}-%{version}/package.xml


%build
cd %{pecl_name}-%{version}
phpize
%configure
make %{?_smp_mflags}


%check
cd %{pecl_name}-%{version}
make test NO_INTERACTION=1 | tee ../rpmtests.log
if grep -q "FAILED TEST" ../rpmtests.log; then
  exit 1
fi


%install
rm -rf %{buildroot}
cd %{pecl_name}-%{version}
make install INSTALL_ROOT=%{buildroot}

# Basic configuration
mkdir -p %{buildroot}%{_sysconfdir}/php.d
cat > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; %{pecl_name} extension configuration
; see http://www.php.net/manual/en/yaml.configuration.php

; Decode entities which have the explicit tag "tag:yaml.org,2002:binary"
yaml.decode_binary = 0
; Controls the decoding of "tag:yaml.org,2002:timestamp"
; 0 will not apply any decoding.
; 1 will use strtotime().
; 2 will use date_create().
yaml.decode_timestamp = 0
; Cause canonical form output.
yaml.output_canonical = 0
; Number of spaces to indent sections. Value should be between 1 and 10.
yaml.output_indent = 2
; Set the preferred line width. -1 means unlimited.
yaml.output_width = 80
EOF

# Package info
mkdir -p %{buildroot}%{pecl_xmldir}
install -p -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]  ; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/CREDITS %{pecl_name}-%{version}/LICENSE
%doc %{pecl_name}-%{version}/README
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Theodore Lee <theo148@gmail.com> - 1.1.0-1
- Update to upstream 1.1.0 release
- Drop upstreamed cflags patch

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-6
- build against php 5.4
- fix filters

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 13 2011 Theodore Lee <theo148@gmail.com> - 1.0.1-4
- Fix commenting in module configuration

* Thu May 12 2011 Theodore Lee <theo148@gmail.com> - 1.0.1-3
- Remove unused php_apiver macro
- Specify version in php-devel requires
- Note upstream report for CFLAGS patch
- Add check section
- Document options in default config file

* Wed May 04 2011 Theodore Lee <theo148@gmail.com> - 1.0.1-2
- Update patch to preserve original compiler flags

* Tue May 03 2011 Theodore Lee <theo148@gmail.com> - 1.0.1-1
- Initial package
