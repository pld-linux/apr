Summary:	Apache Portable Runtime
Name:		apr
Version:	0.9.3
Release:	1
Epoch:		1
License:	GPL
Group:		Libraries
Source0:	http://www.apache.org/dist/apr/%{name}-%{version}.tar.gz
# Source0-md5:	03b243de20ffcf4f30565bc4771489a6
URL:		http://apr.apache.org/
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

%package devel
Summary:	Header files and develpment documentation for apr
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}
Requires:	libtool

%description devel
Header files and develpment documentation for apr.

%package static
Summary:	Static apr library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}

%description static
Static apr library.

%prep
%setup  -q

%build
%configure \
	--enable-threads
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf %{_bindir}/libtool $RPM_BUILD_ROOT%{_datadir}/libtool

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES STATUS docs/*.html
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/apr.exp
%{_includedir}
%dir %{_datadir}
%dir %{_datadir}/build
%{_datadir}/build/*.mk
%attr(755,root,root) %{_datadir}/build/libtool

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
