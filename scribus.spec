Summary:	Scribus - Desktop Publishing for Linux
Summary(pl):	Scribus -
Name:		scribus
Version:	0.7.3
Release:	0.1
Copyright:	GPL
Group:		Application/DTP
Group(pl):	Aplikacje/DTP
Source0:	http://web2.altmuehlnet.de/fschmid/%{name}-%{version}.tar.gz
BuildRequires:	qt-devel >= 3.0.2
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:	zlib-devel
#Requires:	
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_prefix	/usr/X11R6

%description

%description -l pl

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
%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} install

%post
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc
%attr(,,)
