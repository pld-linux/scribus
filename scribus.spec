Summary:	Scribus - Desktop Publishing for Linux
Summary(pl):	Scribus - DTP dla Linuksa
Name:		scribus
Version:	0.7.7
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://web2.altmuehlnet.de/fschmid/%{name}-%{version}.tar.gz
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	qt-devel >= 3.0.5
BuildRequires:	zlib-devel
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
Scribus is a Layout program for Linux(R), similar to Adobe(R)
PageMaker(TM), QuarkXPress(TM) or Adobe(R) InDesign(TM), except that
it is published under the GNU GPL.
			
%description -l pl
Scribus to program dla systemu Linux(R) do tworzenia publikacji,
podobny do programów Adobe(R) PageMaker(TM), QuarkXPress(TM) czy
Adobe(R) InDesign(TM), ale opublikowany na licencji GNU GPL.

%prep
%setup -q

%build
%configure2_13 \
	--prefix=%{_prefix} \
	--with-qt-includes=%{_prefix}/include/qt \
	--with-qt-libraries=%{_prefix}/lib
%{__make} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install

#rm -rf $RPM_BUILD_ROOT%{_datadir}/scribus/doc/
	  
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scribus
%{_datadir}/scribus/scribus.*.qm
%{_datadir}/scribus/*.enc
%{_datadir}/scribus/plugins/*
%{_datadir}/scribus/libs/*
%{_datadir}/scribus/icons/*.png
%{_datadir}/scribus/icons/*.xpm
%{_datadir}/scribus/icons/*.jpg
%{_datadir}/scribus/doc/

%{_includedir}/scribus/*.h
%{_includedir}/scribus/libpostscript/*.h
