#
# Conditional build:
# _without_cups	- without CUPS support
#
Summary:	Scribus - Desktop Publishing for Linux
Summary(pl):	Scribus - DTP dla Linuksa
Name:		scribus
Version:	1.1.4
Release:	1
License:	GPL v2
Group:		X11/Applications/Publishing
Source0:	http://ahnews.music.salford.ac.uk:82/%{name}-%{version}.tar.gz
# Source0-md5:	7e9577ce56b0a5955ed9b37bb2a8c7a1
Source1:	http://ahnews.music.salford.ac.uk:82/%{name}-i18n-en.tar.gz
# Source1-md5:	cccfe4ddd9c646813cd9c5b12cf79138
Source2:	ftp://ftp.ntua.gr/pub/gnu/scribus/%{name}-samples-0.1.tar.gz
# Source2-md5:	799976e2191582faf0443a671374a67f
Source5:	%{name}.desktop
Source6:	%{name}icon.png
Patch0:		%{name}-standard-font-paths.patch
Patch1:		%{name}-module-fixes.patch
Patch2:		%{name}-nolibs.patch
Patch3:		%{name}-gcc2.patch
URL:		http://www.scribus.org.uk/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_cups:BuildRequires:	cups-devel}
%{?_without_cups:BuildConflicts:	cups-devel}
BuildRequires:	freetype-devel
BuildRequires:	lcms-devel >= 1.09
BuildRequires:	libart_lgpl-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	python-devel
BuildRequires:	qt-devel >= 3.0.5
BuildRequires:	zlib-devel
Obsoletes:	scribus-svg
Obsoletes:	scribus-scripting
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	"-fomit-frame-pointer"

%description
Scribus is a Layout program for Linux(R), similar to Adobe(R)
PageMaker(TM), QuarkXPress(TM) or Adobe(R) InDesign(TM), except that
it is published under the GNU GPL.

%description -l pl
Scribus to program dla systemu Linux(R) do tworzenia publikacji,
podobny do programów Adobe(R) PageMaker(TM), QuarkXPress(TM) czy
Adobe(R) InDesign(TM), ale opublikowany na licencji GNU GPL.

%package devel
Summary:	Header files for Scribus plugins development
Summary(pl):	Pliki nag³ówkowe do tworzenia wtyczek Scribusa
Group:		Development/Libraries
# currently it doesn't require base
Requires:	qt-devel

%description devel
Header files for Scribus plugins development.

%description devel -l pl
Pliki nag³ówkowe do tworzenia wtyczek Scribusa.

%prep
%setup -q -a1 -a2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
QTDIR=%{_prefix}
KDEDIR=%{_prefix}
export QTDIR KDEDIR

%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%{__perl} admin/am_edit
%configure
%{__make}
cd scribus-i18n-en
%configure
%{__make}
cd ../scribus-samples-*
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/doc
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

ln -sf $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_datadir}

for dir in . scribus-*; do
	[ ! -d "$dir" ] && continue
	olddir=$(pwd)
	cd $dir
	%{__make} install \
		DESTDIR=$RPM_BUILD_ROOT
	cd $olddir
done

#Install .desktop and .icon (temporary)
install %{SOURCE5} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE6} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scribus
%dir %{_libdir}/%{name}
# don't mark dictionaries with lang() --misiek
%{_libdir}/%{name}/dicts
%dir %{_libdir}/%{name}/doc
%{_libdir}/%{name}/doc/en
%{_libdir}/%{name}/icons
%dir %{_libdir}/%{name}/libs
%attr(755,root,root) %{_libdir}/%{name}/libs/*.so*
%{_libdir}/%{name}/libs/*.la
%dir %{_libdir}/%{name}/plugins
#%%lang(da) %{_libdir}/%{name}/plugins/*.da.qm
%lang(no) %{_libdir}/%{name}/plugins/*.no.qm
%lang(sk) %{_libdir}/%{name}/plugins/*.sk.qm
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so*
%{_libdir}/%{name}/plugins/*.la
%{_libdir}/scribus/profiles
%{_libdir}/scribus/samples
%lang(bg) %{_libdir}/scribus/scribus.bg.qm
%lang(br) %{_libdir}/scribus/scribus.br.qm
#%lang(ca) %{_libdir}/scribus/scribus.ca.qm
%lang(cs) %{_libdir}/scribus/scribus.cs.qm
%lang(cy) %{_libdir}/scribus/scribus.cy.qm
%lang(da) %{_libdir}/scribus/scribus.da.qm
%lang(de) %{_libdir}/scribus/scribus.de.qm
%lang(en_GB) %{_libdir}/scribus/scribus.en_GB.qm
%lang(es) %{_libdir}/scribus/scribus.es.qm
%lang(fr) %{_libdir}/scribus/scribus.fr.qm
%lang(gl) %{_libdir}/scribus/scribus.gl.qm
%lang(hu) %{_libdir}/scribus/scribus.hu.qm
%lang(id) %{_libdir}/scribus/scribus.id.qm
%lang(it) %{_libdir}/scribus/scribus.it.qm
#%lang(lt) %{_libdir}/scribus/scribus.lt.qm
%lang(nl) %{_libdir}/scribus/scribus.nl.qm
%lang(no) %{_libdir}/scribus/scribus.no.qm
%lang(pl) %{_libdir}/scribus/scribus.pl.qm
%lang(ru) %{_libdir}/scribus/scribus.ru.qm
%lang(sk) %{_libdir}/scribus/scribus.sk.qm
%lang(tr) %{_libdir}/scribus/scribus.tr.qm
%lang(uk) %{_libdir}/scribus/scribus.uk.qm
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}icon.png

%files devel
%defattr(644,root,root,755)
%{_includedir}/scribus
