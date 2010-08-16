#
# TODO:
#	- mimelnk integration? IMHO an unneeded dep, although
#	  Patrys will disagree propably (WRT to his latest posts ;)
#
# Conditional build:
%bcond_with	cairo	# build with cairo support
%bcond_without	cups	# build without CUPS support
#
Summary:	Scribus - Open Source Desktop Publishing
Summary(pl.UTF-8):	Scribus - DTP dla Wolnego Oprogramowania
Name:		scribus
Version:	1.3.3.13
Release:	7
License:	GPL v2
Group:		X11/Applications/Publishing
Source0:	http://dl.sourceforge.net/scribus/%{name}-%{version}.tar.bz2
# Source0-md5:	e698b0d118c7f037e57163cba302d96e
Source1:	%{name}.desktop
Patch1:		%{name}-standard-font-paths.patch
Patch2:		%{name}-docs.patch
Patch3:		%{name}-sparc.patch
URL:		http://www.scribus.net/
%{?with_cairo:BuildRequires:	cairo-devel >= 1.2.0}
BuildRequires:	cmake >= 2.4.5
%if %{with cups}
BuildRequires:	cups-devel
%else
BuildConflicts:	cups-devel
%endif
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	lcms-devel >= 1.09
%{!?with_cairo:BuildRequires:	libart_lgpl-devel >= 2.3.14}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	qt-devel >= 6:3.0.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.293
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Requires:	desktop-file-utils
Requires:	python-PIL
Requires:	python-tkinter
Obsoletes:	scribus-scripting
Obsoletes:	scribus-short-words
Obsoletes:	scribus-svg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer

%description
Scribus is an open source desktop page layout program with the aim of
producing commerical grade output in PDF and Postscript, primarily,
though not exclusively for Linux(R).

%description -l pl.UTF-8
Scribus jest to program do tworzenia publikacji z założenia generujący
dokumenty PDF oraz Postscript nadające się do użytku komercyjnego,
przeznaczony głównie, lecz nie tylko, dla systemu Linux(R).

%package devel
Summary:	Header files for Scribus plugins development
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia wtyczek Scribusa
Group:		Development/Libraries
# currently it doesn't require base
Requires:	qt-devel

%description devel
Header files for Scribus plugins development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek Scribusa.

%package docs
Summary:	Documentation for Scribus
Summary(pl.UTF-8):	Dokumentacja dla Scribusa
License:	custom OPL (see License),FDL
Group:		X11/Applications/Publishing

%description docs
User documentation for Scribus.

%description docs -l pl.UTF-8
Dokumentacja użytkownika dla Scribusa.

%package icc
Summary:	ICC profiles for Scribus
Summary(pl.UTF-8):	Profile ICC dla Scribusa
License:	freely distributable
Group:		X11/Applications/Publishing
Requires:	%{name} = %{version}-%{release}

%description icc
Some standard ICM CMYK and RGB profiles for use with Scribus. You
should take care to use custom ones!

%description icc -l pl.UTF-8
Standardowe profile ICM w formacie CMYK i RGB do użycia w Scribusie.
Zalecane jest używanie własnych profili zamiast nich!

%package templates-base
Summary:	Default document templates
Summary(pl.UTF-8):	Domyślne szablony dokumentów
License:	GPL v2
Group:		X11/Applications/Publishing
Requires:	%{name} = %{version}-%{release}
Obsoletes:	scribus-templates < 1.2.1

%description templates-base
Default document templates shipped with Scribus.

%description templates-base -l pl.UTF-8
Domyślne szablony dokumentów dostarczane wraz ze Scribusem.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export QTDIR=%{_prefix}
export KDEDIR=%{_prefix}

%cmake . \
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
%if %{with cairo}
	-DWANT_CAIRO=1
%else
	-DWANT_LIBART=1
%endif

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install $RPM_BUILD_ROOT%{_datadir}/%{name}/icons/scribus.png $RPM_BUILD_ROOT%{_pixmapsdir}

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.lt_LT.qm $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.lt.qm

rm -f $RPM_BUILD_ROOT%{_libdir}/scribus/*.no.qm

rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/doc/{AUTHORS,BUILDING,COPYING,ChangeLog,ChangeLogCVS,ChangeLogSVN,INSTALL,NEWS,PACKAGING,README,README.MacOSX,README.OS2,TODO}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database

%postun
%update_desktop_database_postun
%update_mime_database

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog ChangeLogSVN NEWS README
%attr(755,root,root) %{_bindir}/scribus
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/import.prolog
# don't mark dictionaries with lang() --misiek
%{_datadir}/%{name}/dicts
%{_libdir}/%{name}/keysets
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so*
%dir %{_libdir}/%{name}/plugins/gettext
%attr(755,root,root) %{_libdir}/%{name}/plugins/gettext/*.so*
%dir %{_libdir}/scribus/profiles
%dir %{_datadir}/%{name}/translations
%lang(af) %{_datadir}/%{name}/translations/scribus.af.qm
%lang(ar) %{_datadir}/%{name}/translations/scribus.ar.qm
%lang(bg) %{_datadir}/%{name}/translations/scribus.bg.qm
%lang(br) %{_datadir}/%{name}/translations/scribus.br.qm
%lang(ca) %{_datadir}/%{name}/translations/scribus.ca.qm
%lang(cs) %{_datadir}/%{name}/translations/scribus.cs.qm
%lang(cy) %{_datadir}/%{name}/translations/scribus.cy.qm
%lang(da) %{_datadir}/%{name}/translations/scribus.da.qm
%lang(de) %{_datadir}/%{name}/translations/scribus.de.qm
%lang(de_CH) %{_datadir}/%{name}/translations/scribus.de_CH.qm
%lang(de) %{_datadir}/%{name}/translations/scribus.de_ol.qm
%lang(dz) %{_datadir}/%{name}/translations/scribus.dz.qm
%lang(el) %{_datadir}/%{name}/translations/scribus.el.qm
%lang(en_GB) %{_datadir}/%{name}/translations/scribus.en_GB.qm
%lang(eo) %{_datadir}/%{name}/translations/scribus.eo.qm
%lang(es) %{_datadir}/%{name}/translations/scribus.es.qm
%lang(es) %{_datadir}/%{name}/translations/scribus.es_LA.qm
%lang(et) %{_datadir}/%{name}/translations/scribus.et.qm
%lang(eu) %{_datadir}/%{name}/translations/scribus.eu.qm
%lang(fi) %{_datadir}/%{name}/translations/scribus.fi.qm
%lang(fr) %{_datadir}/%{name}/translations/scribus.fr.qm
%lang(gl) %{_datadir}/%{name}/translations/scribus.gl.qm
%lang(hu) %{_datadir}/%{name}/translations/scribus.hu.qm
%lang(id) %{_datadir}/%{name}/translations/scribus.id.qm
%lang(it) %{_datadir}/%{name}/translations/scribus.it.qm
%lang(ja) %{_datadir}/%{name}/translations/scribus.ja.qm
%lang(ko) %{_datadir}/%{name}/translations/scribus.ko.qm
%lang(lt) %{_datadir}/%{name}/translations/scribus.lt.qm
%lang(nl) %{_datadir}/%{name}/translations/scribus.nl.qm
%lang(nb) %{_datadir}/%{name}/translations/scribus.nb.qm
%lang(pl) %{_datadir}/%{name}/translations/scribus.pl.qm
%lang(pt_BR) %{_datadir}/%{name}/translations/scribus.pt_BR.qm
%lang(ru) %{_datadir}/%{name}/translations/scribus.ru.qm
%lang(sk) %{_datadir}/%{name}/translations/scribus.sk.qm
%lang(sl) %{_datadir}/%{name}/translations/scribus.sl.qm
%lang(sq) %{_datadir}/%{name}/translations/scribus.sq.qm
%lang(sr) %{_datadir}/%{name}/translations/scribus.sr.qm
%lang(sv) %{_datadir}/%{name}/translations/scribus.sv.qm
%lang(th) %{_datadir}/%{name}/translations/scribus.th_TH.qm
%lang(tr) %{_datadir}/%{name}/translations/scribus.tr.qm
%lang(uk) %{_datadir}/%{name}/translations/scribus.uk.qm
%lang(zh_CN) %{_datadir}/%{name}/translations/scribus.zh.qm
%lang(zh_TW) %{_datadir}/%{name}/translations/scribus.zh_TW.qm
%dir %{_libdir}/%{name}/swatches
%{_libdir}/%{name}/swatches/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/dtd
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/loremipsum
%{_datadir}/mime/packages/scribus.xml
%dir %{_datadir}/%{name}/plugins
%{_datadir}/%{name}/plugins/*
%dir %{_datadir}/%{name}/samples
%{_datadir}/%{name}/samples/*.py
%dir %{_datadir}/%{name}/scripts
%{_datadir}/%{name}/scripts/*.py
%{_desktopdir}/%{name}.desktop
%{_mandir}/man1/%{name}.1*
%lang(pl) %{_mandir}/pl/man1/%{name}.1*
%{_pixmapsdir}/%{name}.png

#%files devel
#%defattr(644,root,root,755)
#%{_includedir}/scribus

%files docs
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}/doc
%dir %{_datadir}/%{name}/doc/en
%{_datadir}/%{name}/doc/en/*
%lang(cs) %dir %{_datadir}/%{name}/doc/cs
%lang(cs) %dir %{_datadir}/%{name}/doc/cs/tutorials
%lang(cs) %dir %{_datadir}/%{name}/doc/cs/tutorials/scribus-short-words
%lang(cs) %{_datadir}/%{name}/doc/cs/tutorials/scribus-short-words/*
%lang(de) %dir %{_datadir}/%{name}/doc/de
%lang(de) %{_datadir}/%{name}/doc/de/*
%lang(fr) %dir %{_datadir}/%{name}/doc/fr
%lang(fr) %{_datadir}/%{name}/doc/fr/*.*ml
%lang(fr) %dir %{_datadir}/%{name}/doc/fr/tutorials
%lang(fr) %dir %{_datadir}/%{name}/doc/fr/tutorials/scribus-short-words
%lang(fr) %{_datadir}/%{name}/doc/fr/tutorials/scribus-short-words/*
%lang(pl) %dir %{_datadir}/%{name}/doc/pl
%lang(pl) %dir %{_datadir}/%{name}/doc/pl/tutorials
%lang(pl) %dir %{_datadir}/%{name}/doc/pl/tutorials/scribus-short-words
%lang(pl) %{_datadir}/%{name}/doc/pl/tutorials/scribus-short-words/*


%files icc
%defattr(644,root,root,755)
%{_libdir}/scribus/profiles/*

%files templates-base
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}/templates
%{_datadir}/%{name}/templates/*.xml
%dir %{_datadir}/%{name}/templates/br1
%{_datadir}/%{name}/templates/br1/*
%dir %{_datadir}/%{name}/templates/nl1
%{_datadir}/%{name}/templates/nl1/*
%dir %{_datadir}/%{name}/templates/sc_presentation
%{_datadir}/%{name}/templates/sc_presentation/*
%dir %{_datadir}/%{name}/templates/textbased
%{_datadir}/%{name}/templates/textbased/*

%if 0
  /usr/lib/scribus/import_la.prolog
   /usr/share/scribus/scripts/ChangeLog
   /usr/share/scribus/scripts/NEWS
   /usr/share/scribus/scripts/ReadMe
   /usr/share/scribus/scripts/TODO
   /usr/share/scribus/unicodenameslist.txt
%endif
