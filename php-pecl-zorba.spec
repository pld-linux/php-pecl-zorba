%define		php_name	php%{?php_suffix}
%define		modname	zorba
%define		status		alpha
Summary:	%{modname} - PHP support for XQuery
Summary(pl.UTF-8):	%{modname} - wsparcie PHP dla XQuery
Name:		%{php_name}-pecl-%{modname}
Version:	0.9.9
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	68435be7b5be3c7006d524d14f3f7801
URL:		http://pecl.php.net/package/xquery/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
BuildRequires:	zorba-devel
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension is a wrapper of Zorba library to allow PHP developers
to use XQuery.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to wrapper biblioteki Zorba pozwalającej programistom PHP
na korzystanie z XQuery.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
