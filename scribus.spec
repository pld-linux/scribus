Summary:	Scribus - Desktop Publishing for Linux
Summary(pl):	Scribus - DTP dla Linuksa
Name:		scribus
Version:	0.7.3
Release:	0.1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://web2.altmuehlnet.de/fschmid/%{name}-%{version}.tar.gz
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	qt-devel >= 3.0.2
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

#%patch

%build
%configure2_13 \
	--prefix=%{_prefix} \
	--with-qt-includes=%{_prefix}/include/qt \
	--with-qt-libraries=%{_prefix}/lib
%{__make} RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} DESTDIR=$RPM_BUILD_ROOT install
	  
%clean
rm -rf $RPM_BUILD_ROOT

%post
%postun

%files
%defattr(644,root,root,755)
#%doc
#%attr(,,)
