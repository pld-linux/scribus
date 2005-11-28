#
# Conditional build:
%bcond_with	cairo	# build with cairo support
%bcond_without	cups	# build without CUPS support
#

Summary:	Scribus - Open Source Desktop Publishing
Summary(pl):	Scribus - DTP dla Wolnego Oprogramowania
Name:		scribus
Version:	1.3.1
Release:	1
License:	GPL v2
Group:		X11/Applications/Publishing
Source0:	http://www.scribus.org.uk/downloads/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	ad36f7de1bba1229d143b93d2b6cd8e9
Source1:	%{name}.desktop
Source2:	%{name}icon.png
Patch0:		%{name}-python.patch
Patch1:		%{name}-standard-font-paths.patch
Patch2:		%{name}-module-fixes.patch
Patch3:		%{name}-nolibs.patch
Patch4:		%{name}-DESTDIR.patch
URL:		http://www.scribus.net/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_cairo:BuildRequires:	cairo-devel}
%if %{with cups}
BuildRequires:	cups-devel
%else
BuildConflicts:	cups-devel
%endif
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	lcms-devel >= 1.09
%{?without_cairo:BuildRequires:	libart_lgpl-devel >= 2.3.14}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	qt-devel >= 3.0.5
BuildRequires:	zlib-devel
Requires:	python-Imaging
Requires:	python-tkinter
Obsoletes:	scribus-svg
Obsoletes:	scribus-scripting
Obsoletes:	scribus-short-words
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer
%define		_ulibdir	%{_prefix}/lib

%description
Scribus is an open source desktop page layout program with the aim of
producing commerical grade output in PDF and Postscript, primarily,
though not exclusively for Linux(R).

%description -l pl
Scribus jest to program do tworzenia publikacji z za³o¿enia generuj±cy
dokumenty PDF oraz Postscript nadaj±ce siê do u¿ytku komercyjnego,
przeznaczony g³ównie, lecz nie tylko, dla systemu Linux(R).

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

%package icc
Summary:	ICC profiles for Scribus
Summary(pl):	Profile ICC dla Scribusa
License:	freely distributable
Group:		X11/Applications/Publishing
Requires:	scribus >= 1.2.3

%description icc
Some standard ICM CMYK and RGB profiles for use with Scribus.
You should take care to use custom ones!

%description icc -l pl
Standardowe profile ICM w formacie CMYK i RGB do u¿ycia
w Scribusie.
Zalecane jest u¿ywanie w³asnych profili zamiast nich!

%package templates-base
Summary:	Default document templates
Summary(pl):	Domy¶lne szablony dokumentów
License:	GPL v2
Group:		X11/Applications/Publishing
Requires:	scribus
Obsoletes:	scribus-templates < 1.2.1

%description templates-base
Default document templates shipped with Scribus.

%description templates-base -l pl
Domy¶lne szablony dokumentów dostarczane wraz ze Scribusem.

%prep
%setup -q
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
	%{?with_cairo:--enable-cairo} \
	--with-qt-libraries=%{_libdir} \
	--libdir=%{_ulibdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_datadir}/mime/packages/}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#Install .desktop, .icon and .xml
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
install scribus.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/scribus.xml

rm -f $RPM_BUILD_ROOT%{_ulibdir}/scribus/*.no.qm

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:
[ ! -x /usr/bin/update-mime-database ] || /usr/bin/update-mime-database %{_datadir}/mime >/dev/null 2>&1 ||:

%postun
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:
[ ! -x /usr/bin/update-mime-database ] || /usr/bin/update-mime-database %{_datadir}/mime >/dev/null 2>&1 ||:

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scribus
%dir %{_ulibdir}/%{name}
%{_ulibdir}/%{name}/import.prolog
# don't mark dictionaries with lang() --misiek
%{_ulibdir}/%{name}/dicts
%{_ulibdir}/%{name}/keysets
%dir %{_ulibdir}/%{name}/plugins
#%lang(da) %{_ulibdir}/%{name}/plugins/*.da.qm
#%lang(nb) %{_ulibdir}/%{name}/plugins/*.no.qm
#%lang(sk) %{_ulibdir}/%{name}/plugins/*.sk.qm
%attr(755,root,root) %{_ulibdir}/%{name}/plugins/*.so*
%{_ulibdir}/%{name}/plugins/*.la
%dir %{_ulibdir}/%{name}/plugins/gettext
%attr(755,root,root) %{_ulibdir}/%{name}/plugins/gettext/*.so*
%{_ulibdir}/%{name}/plugins/gettext/*.la
%dir %{_ulibdir}/scribus/profiles
%{_ulibdir}/scribus/rgb*
%lang(af) %{_ulibdir}/scribus/scribus.af.qm
%lang(bg) %{_ulibdir}/scribus/scribus.bg.qm
%lang(ca) %{_ulibdir}/scribus/scribus.ca.qm
%lang(cs) %{_ulibdir}/scribus/scribus.cs.qm
%lang(cy) %{_ulibdir}/scribus/scribus.cy.qm
%lang(da) %{_ulibdir}/scribus/scribus.da.qm
%lang(de) %{_ulibdir}/scribus/scribus.de.qm
%lang(en_GB) %{_ulibdir}/scribus/scribus.en_GB.qm
%lang(eo) %{_ulibdir}/scribus/scribus.eo.qm
%lang(es) %{_ulibdir}/scribus/scribus.es.qm
%lang(es_LA) %{_ulibdir}/scribus/scribus.es_LA.qm
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
%lang(pt_BR) %{_ulibdir}/scribus/scribus.pt_BR.qm
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
%{_datadir}/%{name}/dtd
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/loremipsum
%{_datadir}/mime/packages/scribus.xml
%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/plugins/*.rc
%dir %{_datadir}/%{name}/samples
%{_datadir}/%{name}/samples/*
%dir %{_datadir}/%{name}/scripts
%{_datadir}/%{name}/scripts/*
%{_desktopdir}/%{name}.desktop
%{_mandir}/man1/%{name}.*
%lang(pl) %{_mandir}/pl/man1/%{name}.*
%{_pixmapsdir}/%{name}icon.png

%files devel
%defattr(644,root,root,755)
%{_includedir}/scribus

%files docs
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}/doc/en
%{_datadir}/%{name}/doc/en/*
%lang(cs) %dir %{_datadir}/%{name}/doc/cs
%lang(cs) %dir %{_datadir}/%{name}/doc/cs/tutorials
%lang(cs) %dir %{_datadir}/%{name}/doc/cs/tutorials/scribus-short-words
%lang(cs) %{_datadir}/%{name}/doc/cs/tutorials/scribus-short-words/*
%lang(fr) %dir %{_datadir}/%{name}/doc/fr
%lang(fr) %dir %{_datadir}/%{name}/doc/fr/tutorials
%lang(fr) %dir %{_datadir}/%{name}/doc/fr/tutorials/scribus-short-words
%lang(fr) %{_datadir}/%{name}/doc/fr/tutorials/scribus-short-words/*
%lang(pl) %dir %{_datadir}/%{name}/doc/pl
%lang(pl) %dir %{_datadir}/%{name}/doc/pl/tutorials
%lang(pl) %dir %{_datadir}/%{name}/doc/pl/tutorials/scribus-short-words
%lang(pl) %{_datadir}/%{name}/doc/pl/tutorials/scribus-short-words/*

%files icc
%defattr(644,root,root,755)
%{_ulibdir}/scribus/profiles/*

%files templates-base
%defattr(644,root,root,755)
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
