#
# TODO:
# - seperate scripts subpackage
# - seperate templates add proper obsoletes for it
#
# Conditional build:
%bcond_without	cups	# build without CUPS support
#
Summary:	Scribus - Desktop Publishing for Linux
Summary(pl):	Scribus - DTP dla Linuksa
Name:		scribus
Version:	1.2.1
Release:	3
License:	GPL v2
Group:		X11/Applications/Publishing
Source0:	http://www.scribus.org.uk/downloads/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	002cb629e817722f4123df7a41fc824b
Source1:	ftp://ftp.ntua.gr/pub/gnu/scribus/%{name}-samples-0.1.tar.gz
# Source1-md5:	799976e2191582faf0443a671374a67f
Source5:	%{name}.desktop
Source6:	%{name}icon.png
Patch0:		%{name}-python.patch
Patch1:		%{name}-standard-font-paths.patch
Patch2:		%{name}-module-fixes.patch
Patch3:		%{name}-nolibs.patch
Patch4:		%{name}-destdir.patch
URL:		http://www.scribus.net/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with cups}
BuildRequires:	cups-devel
%else
BuildConflicts:	cups-devel
%endif
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	lcms-devel >= 1.09
BuildRequires:	libart_lgpl-devel >= 2.3.14
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	python-devel
BuildRequires:	qt-devel >= 3.0.5
BuildRequires:	zlib-devel
Requires:	python-Imaging
Requires:	python-tkinter
Obsoletes:	scribus-svg
Obsoletes:	scribus-scripting
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer
%define		_ulibdir	%{_prefix}/lib

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

%package docs
Summary:	Documentation for Scribus
Summary(pl):	Dokumentacja dla Scribusa
License:	custom OPL (see License),FDL
Group:		X11/Applications/Publishing
Requires:	scribus

%description docs
On-line user documentation for Scribus.

%description docs -l pl
Dokumentacja u¿ytkownika dla Scribusa.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{__perl} -pi -e 's@(ac_python_dir/lib /usr/)lib@$1%{_lib}@' acinclude.m4

%build
QTDIR=%{_prefix}
KDEDIR=%{_prefix}
export QTDIR KDEDIR

%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%{__perl} admin/am_edit
%configure \
	--with-qt-libraries=%{_libdir} \
	--libdir=%{_ulibdir}
%{__make}
cd scribus-samples-*
cp ../admin/config.sub admin
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

for dir in . scribus-samples; do
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

rm -f $RPM_BUILD_ROOT%{_ulibdir}/scribus/*.no.qm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scribus
%dir %{_ulibdir}/%{name}
%{_ulibdir}/%{name}/import.prolog
# don't mark dictionaries with lang() --misiek
%{_ulibdir}/%{name}/dicts
%dir %{_ulibdir}/%{name}/libs
%attr(755,root,root) %{_ulibdir}/%{name}/libs/*.so*
%{_ulibdir}/%{name}/libs/*.la
%dir %{_ulibdir}/%{name}/plugins
#%lang(da) %{_ulibdir}/%{name}/plugins/*.da.qm
#%lang(nb) %{_ulibdir}/%{name}/plugins/*.no.qm
#%lang(sk) %{_ulibdir}/%{name}/plugins/*.sk.qm
%attr(755,root,root) %{_ulibdir}/%{name}/plugins/*.so*
%{_ulibdir}/%{name}/plugins/*.la
%dir %{_ulibdir}/%{name}/plugins/gettext
%attr(755,root,root) %{_ulibdir}/%{name}/plugins/gettext/*.so*
%{_ulibdir}/%{name}/plugins/gettext/*.la
%{_ulibdir}/scribus/profiles
%{_ulibdir}/scribus/rgb*
%lang(af) %{_ulibdir}/scribus/scribus.af.qm
%lang(bg) %{_ulibdir}/scribus/scribus.bg.qm
%lang(br) %{_ulibdir}/scribus/scribus.br.qm
%lang(ca) %{_ulibdir}/scribus/scribus.ca.qm
%lang(cs) %{_ulibdir}/scribus/scribus.cs.qm
%lang(cy) %{_ulibdir}/scribus/scribus.cy.qm
%lang(da) %{_ulibdir}/scribus/scribus.da.qm
%lang(de) %{_ulibdir}/scribus/scribus.de.qm
%lang(en_GB) %{_ulibdir}/scribus/scribus.en_GB.qm
%lang(eo) %{_ulibdir}/scribus/scribus.eo.qm
%lang(es) %{_ulibdir}/scribus/scribus.es.qm
%lang(eu) %{_ulibdir}/scribus/scribus.eu.qm
%lang(fi) %{_ulibdir}/scribus/scribus.fi.qm
%lang(fr) %{_ulibdir}/scribus/scribus.fr.qm
%lang(gl) %{_ulibdir}/scribus/scribus.gl.qm
%lang(hu) %{_ulibdir}/scribus/scribus.hu.qm
%lang(id) %{_ulibdir}/scribus/scribus.id.qm
%lang(it) %{_ulibdir}/scribus/scribus.it.qm
%lang(ko) %{_ulibdir}/scribus/scribus.ko.qm
%lang(lt) %{_ulibdir}/scribus/scribus.lt.qm
%lang(nl) %{_ulibdir}/scribus/scribus.nl.qm
%lang(nb) %{_ulibdir}/scribus/scribus.nb.qm
%lang(pl) %{_ulibdir}/scribus/scribus.pl.qm
%lang(ru) %{_ulibdir}/scribus/scribus.ru.qm
%lang(se) %{_ulibdir}/scribus/scribus.se.qm
%lang(sk) %{_ulibdir}/scribus/scribus.sk.qm
%lang(sl) %{_ulibdir}/scribus/scribus.sl.qm
%lang(sq) %{_ulibdir}/scribus/scribus.sq.qm
%lang(sr) %{_ulibdir}/scribus/scribus.sr.qm
%lang(tr) %{_ulibdir}/scribus/scribus.tr.qm
%lang(uk) %{_ulibdir}/scribus/scribus.uk.qm
%lang(zh_CN) %{_ulibdir}/scribus/scribus.zh.qm
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/doc
%{_datadir}/%{name}/icons
%dir %{_datadir}/%{name}/samples
%{_datadir}/%{name}/samples/*
%dir %{_datadir}/%{name}/scripts
%{_datadir}/%{name}/scripts/*
%dir %{_datadir}/%{name}/templates
%{_datadir}/%{name}/templates/*.xml
%dir %{_datadir}/%{name}/templates/br1
%{_datadir}/%{name}/templates/br1/*
%dir %{_datadir}/%{name}/templates/nl1
%{_datadir}/%{name}/templates/nl1/*
%dir %{_datadir}/%{name}/templates/nl2
%{_datadir}/%{name}/templates/nl2/*
%dir %{_datadir}/%{name}/templates/sc_presentation
%{_datadir}/%{name}/templates/sc_presentation/*
%dir %{_datadir}/%{name}/templates/textbased
%{_datadir}/%{name}/templates/textbased/*
%{_desktopdir}/%{name}.desktop
%{_mandir}/man1/%{name}.*
%lang(pl) %{_mandir}/pl/man1/%{name}.*
%{_pixmapsdir}/%{name}icon.png

%files devel
%defattr(644,root,root,755)
%{_includedir}/scribus

%files docs
%dir %{_datadir}/%{name}/doc/en
%{_datadir}/%{name}/doc/en/*
