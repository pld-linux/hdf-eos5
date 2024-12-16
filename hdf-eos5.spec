#
# Conditional build:
%bcond_without	szip		# SZIP support (must match hdf build bcond)
%bcond_without	tests		# unit tests
#
Summary:	HDF-EOS 5 library
Summary(pl.UTF-8):	Biblioteka HDF-EOS 5
Name:		hdf-eos5
Version:	5.2.0
Release:	1
License:	MIT-like
Group:		Libraries
Source0:	https://git.earthdata.nasa.gov/projects/DAS/repos/hdfeos5/raw/hdf-eos5-2.0-src.tar.gz?at=refs/heads/HDFEOS5_2.0#/hdf-eos5-2.0-src.tar.gz
# Source0-md5:	151c04a8e7660f868da9fef0fa6c631a
Patch1:		%{name}-link.patch
Patch2:		%{name}-fortran.patch
Patch3:		%{name}-types.patch
Patch4:		%{name}-bufsize.patch
URL:		http://hdfeos.org/software/library.php#HDF-EOS5
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	hdf5-devel >= 1.8.19
BuildRequires:	libtool
%{?with_szip:BuildRequires:	libaec-szip-devel >= 1.0}
BuildRequires:	zlib-devel
Requires:	hdf5 >= 1.8.19
%{?with_szip:Requires:	libaec-szip >= 1.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HDF-EOS is a software library designed to support EOS-specific data
structures, namely Grid, Point, and Swath. The new data structures are
constructed from standard HDF data objects, using EOS conventions,
through the use of a software library. A key feature of HDF-EOS files
is that instrument-independent services, such as subsetting by
geolocation, can be applied to the files across a wide variety of data
products. The library is extensible and new data structures can be
added.

%description -l pl.UTF-8
HDF-EOS to biblioteka programowa zaprojektowana w celu obsługi
struktur danych związanych z EOS, takich jak Grid, Point i Swath. Nowe
struktury danych są tworzone z obiektów danych HDF, przy użyciu
konwencji EOS, poprzez bibliotekę programową. Kluczową cechą plików
HDF-EOS jest to, że usługi niezależne od przyrządu, takie jak na
przykład podział według geolokalizacji, można wykonywać na plikach
zawierających różnorodne zbiory danych. Biblioteka jest rozszerzalna i
pozwala na dodawanie nowych struktur danych.

%package devel
Summary:	Header files for HDF-EOS 5 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HDF-EOS 5
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	hdf5-devel >= 1.8.19
%{?with_szip:Requires:	libaec-szip-devel >= 1.0}
Requires:	zlib-devel

%description devel
Header files for HDF-EOS 5 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HDF-EOS 5.

%package static
Summary:	Static HDF-EOS 5 library
Summary(pl.UTF-8):	Statyczna biblioteka HDF-EOS 5
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static HDF-EOS 5 library.

%description static -l pl.UTF-8
Statyczna biblioteka HDF-EOS 5.

%prep
%setup -q -n hdf-eos5-2.0
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
FFLAGS="%{rpmcflags} -fallow-argument-mismatch"
# hdf5 installs in plain /usr/include, but we want to isolate headers
# from system include dir (hdf-eos2 uses the same filenames)
%configure \
	--includedir=%{_includedir}/he5 \
	--enable-fortran \
	--enable-shared \
	%{?with_szip:--with-szlib}

%{__make}

# note: random failures occur when tests are executed in parallel, so use -j1
%{?with_tests:%{__make} -j1 check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/README
%attr(755,root,root) %{_libdir}/libhe5_Gctp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhe5_Gctp.so.0
%attr(755,root,root) %{_libdir}/libhe5_hdfeos.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhe5_hdfeos.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhe5_Gctp.so
%attr(755,root,root) %{_libdir}/libhe5_hdfeos.so
%{_libdir}/libhe5_Gctp.la
%{_libdir}/libhe5_hdfeos.la
%dir %{_includedir}/he5
%{_includedir}/he5/HE5_GctpFunc.h
%{_includedir}/he5/HE5_HdfEosDef.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libhe5_Gctp.a
%{_libdir}/libhe5_hdfeos.a
