#
# Conditional build:
%bcond_with	cairo	# build with cairo support
%bcond_without	cups	# build without CUPS support
#
Summary:	Scribus - Open Source Desktop Publishing
Summary(pl.UTF-8):	Scribus - DTP dla Wolnego Oprogramowania
Name:		scribus
Version:	1.3.3.8
Release:	1
License:	GPL v2
Group:		X11/Applications/Publishing
Source0:	http://dl.sourceforge.net/scribus/%{name}-%{version}.tar.bz2
# Source0-md5:	fa79c8bba3e6e09b0bdeaf16579d6fa1
Source1:	%{name}.desktop
Patch1:		%{name}-standard-font-paths.patch
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
%define		_ulibdir	%{_prefix}/lib

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

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install $RPM_BUILD_ROOT%{_datadir}/%{name}/icons/scribusicon.png $RPM_BUILD_ROOT%{_pixmapsdir}

mv $RPM_BUILD_ROOT%{_ulibdir}/scribus/%{name}.lt_LT.qm $RPM_BUILD_ROOT%{_ulibdir}/scribus/%{name}.lt.qm

rm -f $RPM_BUILD_ROOT%{_ulibdir}/scribus/*.no.qm

rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/{AUTHORS,BUILDING,COPYING,ChangeLog,ChangeLogCVS,INSTALL,NEWS,PACKAGING,README,README.MacOSX,TODO}

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
%doc AUTHORS BUILDING ChangeLog ChangeLogCVS INSTALL NEWS README TODO
%attr(755,root,root) %{_bindir}/scribus
%dir %{_ulibdir}/%{name}
%{_ulibdir}/%{name}/import.prolog
# don't mark dictionaries with lang() --misiek
%{_ulibdir}/%{name}/dicts
%{_ulibdir}/%{name}/keysets
%dir %{_ulibdir}/%{name}/plugins
%attr(755,root,root) %{_ulibdir}/%{name}/plugins/*.so*
%dir %{_ulibdir}/%{name}/plugins/gettext
%attr(755,root,root) %{_ulibdir}/%{name}/plugins/gettext/*.so*
%dir %{_ulibdir}/scribus/profiles
%lang(af) %{_ulibdir}/scribus/scribus.af.qm
%lang(bg) %{_ulibdir}/scribus/scribus.bg.qm
%lang(br) %{_ulibdir}/scribus/scribus.br.qm
%lang(ca) %{_ulibdir}/scribus/scribus.ca.qm
%lang(cs) %{_ulibdir}/scribus/scribus.cs.qm
%lang(cy) %{_ulibdir}/scribus/scribus.cy.qm
%lang(da) %{_ulibdir}/scribus/scribus.da.qm
%lang(de) %{_ulibdir}/scribus/scribus.de.qm
%lang(de_CH) %{_ulibdir}/scribus/scribus.de_CH.qm
%lang(de) %{_ulibdir}/scribus/scribus.de_ol.qm
%lang(dz) %{_ulibdir}/scribus/scribus.dz.qm
%lang(el) %{_ulibdir}/scribus/scribus.el.qm
#%lang(en_AU) %{_ulibdir}/scribus/scribus.en_AU.qm
%lang(en_GB) %{_ulibdir}/scribus/scribus.en_GB.qm
#%lang(en_US) %{_ulibdir}/scribus/scribus.en_US.qm
%lang(eo) %{_ulibdir}/scribus/scribus.eo.qm
%lang(es) %{_ulibdir}/scribus/scribus.es.qm
%lang(es) %{_ulibdir}/scribus/scribus.es_LA.qm
%lang(et) %{_ulibdir}/scribus/scribus.et.qm
%lang(eu) %{_ulibdir}/scribus/scribus.eu.qm
%lang(fi) %{_ulibdir}/scribus/scribus.fi.qm
%lang(fr) %{_ulibdir}/scribus/scribus.fr.qm
%lang(gl) %{_ulibdir}/scribus/scribus.gl.qm
%lang(hu) %{_ulibdir}/scribus/scribus.hu.qm
%lang(id) %{_ulibdir}/scribus/scribus.id.qm
%lang(it) %{_ulibdir}/scribus/scribus.it.qm
%lang(ja) %{_ulibdir}/scribus/scribus.ja.qm
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
%lang(th) %{_ulibdir}/scribus/scribus.th_TH.qm
%lang(tr) %{_ulibdir}/scribus/scribus.tr.qm
%lang(uk) %{_ulibdir}/scribus/scribus.uk.qm
%lang(zh_CN) %{_ulibdir}/scribus/scribus.zh.qm
%dir %{_ulibdir}/%{name}/swatches
%{_ulibdir}/%{name}/swatches/*
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
%{_mandir}/man1/%{name}.*
%lang(pl) %{_mandir}/pl/man1/%{name}.*
%{_pixmapsdir}/%{name}icon.png

#%files devel
#%defattr(644,root,root,755)
#%{_includedir}/scribus

%files docs
%defattr(644,root,root,755)
%dir %{_docdir}/%{name}
%dir %{_docdir}/%{name}/en
%{_docdir}/%{name}/en/*
%lang(cs) %dir %{_docdir}/%{name}/cs
%lang(cs) %dir %{_docdir}/%{name}/cs/tutorials
%lang(cs) %dir %{_docdir}/%{name}/cs/tutorials/scribus-short-words
%lang(cs) %{_docdir}/%{name}/cs/tutorials/scribus-short-words/*
%lang(de) %dir %{_docdir}/%{name}/de
%lang(de) %{_docdir}/%{name}/de/*
%lang(fr) %dir %{_docdir}/%{name}/fr
%lang(fr) %{_docdir}/%{name}/fr/*.html
%lang(fr) %dir %{_docdir}/%{name}/fr/tutorials
%lang(fr) %dir %{_docdir}/%{name}/fr/tutorials/scribus-short-words
%lang(fr) %{_docdir}/%{name}/fr/tutorials/scribus-short-words/*
%lang(pl) %dir %{_docdir}/%{name}/pl
%lang(pl) %dir %{_docdir}/%{name}/pl/tutorials
%lang(pl) %dir %{_docdir}/%{name}/pl/tutorials/scribus-short-words
%lang(pl) %{_docdir}/%{name}/pl/tutorials/scribus-short-words/*

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
%dir %{_datadir}/%{name}/templates/sc_presentation
%{_datadir}/%{name}/templates/sc_presentation/*
%dir %{_datadir}/%{name}/templates/textbased
%{_datadir}/%{name}/templates/textbased/*
