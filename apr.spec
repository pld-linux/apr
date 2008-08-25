Summary:	Apache Portable Runtime
Summary(pl.UTF-8):	Apache Portable Runtime - przenośna biblioteka uruchomieniowa
Name:		apr
Version:	1.3.3
Release:	2
Epoch:		1
License:	Apache v2.0
Group:		Libraries
Source0:	http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
# Source0-md5:	2090c21dee4f0eb1512604127dcd158f
Patch0:		%{name}-link.patch
Patch1:		%{name}-metuxmpm.patch
Patch2:		%{name}-libtool.patch
URL:		http://apr.apache.org/
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
%if "%{pld_release}" != "ac"
BuildRequires:	libtool >= 2:2.2
%else
BuildRequires:	libtool
%endif
BuildRequires:	libuuid-devel
BuildRequires:	python
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
%if "%{pld_release}" != "ac"
BuildRequires:	uname(release) >= 2.6
Requires:	uname(release) >= 2.6
%endif
Conflicts:	kernel24
Conflicts:	kernel24-smp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	/usr/include/apr
%define		_datadir	/usr/share/apr

%description
The mission of the Apache Portable Runtime (APR) project is to create
and maintain software libraries that provide a predictable and
consistent interface to underlying platform-specific implementations.
The primary goal is to provide an API to which software developers may
code and be assured of predictable if not identical behaviour
regardless of the platform on which their software is built, relieving
them of the need to code special-case conditions to work around or
take advantage of platform-specific deficiencies or features.

%description -l pl.UTF-8
Celem projektu APR (Apache Portable Runtime) jest stworzenie i
utrzymywanie bibliotek dostarczających przewidywalnego i spójnego
interfejsu do leżących u podstaw implementacji zależnych od platformy.
Głównym celem jest dostarczenie API, którego mogą używać programiści
mając pewność, że zachowuje się w sposób przewidywalny, jeśli nie
identyczny, niezależnie od platformy na jakiej oprogramowanie jest
budowane oraz bez potrzeby kodowania specjalnych warunków do
obchodzenia lub wykorzystywania specyficznych dla platform różnic lub
możliwości.

%package devel
Summary:	Header files and development documentation for apr
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty do apr
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	automake
%if "%{pld_release}" != "ac"
Requires:	libtool >= 2:2.2
%else
Requires:	libtool
%endif
Requires:	libuuid-devel
Requires:	python-modules

%description devel
Header files and development documentation for apr.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty do apr.

%package static
Summary:	Static apr library
Summary(pl.UTF-8):	Statyczna biblioteka apr
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static apr library.

%description static -l pl.UTF-8
Statyczna biblioteka apr.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

cat >> config.layout <<'EOF'
<Layout PLD>
sbindir:	%{_sbindir}
libexecdir:	%{_libdir}/apr
installbuilddir: ${datadir}/build-${APR_MAJOR_VERSION}
localstatedir:	/var/run
runtimedir:	/var/run
libsuffix:	-${APR_MAJOR_VERSION}
</Layout>
EOF

%build
install /usr/share/automake/config.* build
%{__autoconf}

%configure \
	--enable-layout=PLD \
%ifarch %{ix86} %{i8664}
%ifnarch i386
	--enable-nonportable-atomics \
%endif
%endif
	--enable-threads \
	--with-devrandom=/dev/urandom
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/build-1 $RPM_BUILD_ROOT%{_datadir}/build
install build/{*apr*.m4,*.awk,*.sh,gen-build.py} $RPM_BUILD_ROOT%{_datadir}/build
ln -snf /usr/share/automake/config.{guess,sub} $RPM_BUILD_ROOT%{_datadir}/build
if [ -f /usr/share/libtool/config/ltmain.sh ]; then
	ln -snf /usr/share/libtool/config/ltmain.sh $RPM_BUILD_ROOT%{_datadir}/build
else
	ln -snf /usr/share/libtool/ltmain.sh $RPM_BUILD_ROOT%{_datadir}/build
fi
ln -snf /usr/bin/libtool $RPM_BUILD_ROOT%{_datadir}/build
ln -sf build $RPM_BUILD_ROOT%{_datadir}/build-1

sed -i -e 's@^\(APR_SOURCE_DIR=\).*@\1"%{_datadir}"@' \
	$RPM_BUILD_ROOT%{_bindir}/apr-1-config
sed -i -e 's@^\(apr_builddir\|apr_builders\)=.*@\1=%{_datadir}/build-1@' \
	$RPM_BUILD_ROOT%{_datadir}/build/apr_rules.mk
sed -i -e '1s@#!.*python@#!%{__python}@' $RPM_BUILD_ROOT%{_datadir}/build/gen-build.py

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES docs/*.html
%attr(755,root,root) %{_libdir}/libapr-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libapr-1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/apr-1-config
%attr(755,root,root) %{_libdir}/libapr-1.so
%{_libdir}/libapr-1.la
%{_libdir}/apr.exp
%{_includedir}
%dir %{_datadir}
%dir %{_datadir}/build
%{_datadir}/build/*.mk
%{_datadir}/build/*.m4
%{_datadir}/build/*.awk
%attr(755,root,root) %{_datadir}/build/config.*
%attr(755,root,root) %{_datadir}/build/*.sh
%attr(755,root,root) %{_datadir}/build/libtool
%attr(755,root,root) %{_datadir}/build/gen-build.py
%{_datadir}/build-1
%{_pkgconfigdir}/apr-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libapr-1.a
