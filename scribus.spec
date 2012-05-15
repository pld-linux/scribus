#
# TODO: files (docs and some translations)
#
# Conditional build:
%bcond_without	cairo	# build with cairo support
%bcond_without	cups	# build without CUPS support
#
Summary:	Scribus - Open Source Desktop Publishing
Summary(pl.UTF-8):	Scribus - DTP dla Wolnego Oprogramowania
Name:		scribus
Version:	1.4.1
Release:	1
License:	GPL v2+
Group:		X11/Applications/Publishing
Source0:	http://downloads.sourceforge.net/scribus/%{name}-%{version}.tar.bz2
# Source0-md5:	aa6b74528c295153ab3bda88c86ba0d6
Source1:	%{name}.desktop
Patch1:		%{name}-standard-font-paths.patch
Patch2:		%{name}-docs.patch
Patch3:		%{name}-sparc.patch
URL:		http://www.scribus.net/
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtXml-devel
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
BuildRequires:	pkgconfig
BuildRequires:	podofo-devel
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
BuildRequires:	qt4-qmake
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Requires:	desktop-file-utils
Requires:	python-PIL
Requires:	python-tkinter
Requires:	shared-mime-info
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
%setup -q -n Scribus
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export QTDIR=%{_prefix}
export KDEDIR=%{_prefix}

%cmake . \
	-DASPELL_EXECUTABLE=%{_bindir}/aspell \
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

mv $RPM_BUILD_ROOT%{_datadir}/mimelnk/* $RPM_BUILD_ROOT%{_datadir}/mime/

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.lt_LT.qm $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.lt.qm

%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc/{AUTHORS,BUILDING,COPYING,ChangeLog,ChangeLogSVN,NEWS,PACKAGING,README,README.MacOSX,TODO}

# currently not used, -devel subpackage?
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/%{name}

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
%{_datadir}/%{name}/unicodenameslist.txt
# don't mark dictionaries with lang() --misiek
%{_datadir}/%{name}/dicts
%{_datadir}/%{name}/editorconfig
%{_datadir}/%{name}/keysets
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so*
%dir %{_libdir}/%{name}/plugins/gettext
%attr(755,root,root) %{_libdir}/%{name}/plugins/gettext/*.so*
%dir %{_datadir}/%{name}/profiles
%dir %{_datadir}/%{name}/translations
%{_datadir}/%%{name}/translations/scribus*.qm
%dir %{_datadir}/%{name}/swatches
%{_datadir}/%{name}/swatches/*
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
%{_datadir}/%{name}/scripts/*
%{_desktopdir}/%{name}.desktop
%{_mandir}/man1/%{name}.1*
%lang(pl) %{_mandir}/pl/man1/%{name}.1*
%lang(de) %{_mandir}/de/man1/%{name}.1*
%{_pixmapsdir}/%{name}.png
%{_datadir}/mime/application/vnd.scribus.desktop

#%files devel
#%defattr(644,root,root,755)
#%{_includedir}/scribus

%files docs
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}/doc
%{_datadir}/%{name}/doc/*
##%dir %{_datadir}/%{name}/doc/en
##%{_datadir}/%{name}/doc/en/*
##%dir %{_datadir}/%{name}/doc/it
##%{_datadir}/%{name}/doc/it/*
#%%lang(cs) %dir %{_datadir}/%{name}/doc/cs
#%%lang(cs) %dir %{_datadir}/%{name}/doc/cs/tutorials
#%%lang(cs) %dir %{_datadir}/%{name}/doc/cs/tutorials/scribus-short-words
#%%lang(cs) %{_datadir}/%{name}/doc/cs/tutorials/scribus-short-words/*
#%%lang(de) %dir %{_datadir}/%{name}/doc/de
#%%lang(de) %{_datadir}/%{name}/doc/de/*
#%%lang(fr) %dir %{_datadir}/%{name}/doc/fr
#%%lang(fr) %{_datadir}/%{name}/doc/fr/*.*ml
#%%lang(fr) %dir %{_datadir}/%{name}/doc/fr/tutorials
#%%lang(fr) %dir %{_datadir}/%{name}/doc/fr/tutorials/scribus-short-words
#%%lang(fr) %{_datadir}/%{name}/doc/fr/tutorials/scribus-short-words/*
#%%lang(pl) %dir %{_datadir}/%{name}/doc/pl
#%%lang(pl) %dir %{_datadir}/%{name}/doc/pl/tutorials
#%%lang(pl) %dir %{_datadir}/%{name}/doc/pl/tutorials/scribus-short-words
#%%lang(pl) %{_datadir}/%{name}/doc/pl/tutorials/scribus-short-words/*


%files icc
%defattr(644,root,root,755)
%{_datadir}/scribus/profiles/*

%files templates-base
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}/templates
%{_datadir}/%{name}/templates/*.xml
%dir %{_datadir}/%{name}/templates/br1
%{_datadir}/%{name}/templates/br1/*
%dir %{_datadir}/%{name}/templates/nl1
%{_datadir}/%{name}/templates/nl1/*
#%%dir %{_datadir}/%{name}/templates/sc_presentation
#%%{_datadir}/%{name}/templates/sc_presentation/*
%dir %{_datadir}/%{name}/templates/textbased
%{_datadir}/%{name}/templates/textbased/*
%dir %{_datadir}/%{name}/templates/buscard*
%{_datadir}/%{name}/templates/buscard*/*
%dir %{_datadir}/%{name}/templates/cover*
%{_datadir}/%{name}/templates/cover*/*
%dir %{_datadir}/%{name}/templates/grid_*
%{_datadir}/%{name}/templates/grid_*/*
%dir %{_datadir}/%{name}/templates/cc
%{_datadir}/%{name}/templates/cc/*
%dir %{_datadir}/%{name}/templates/mc
%{_datadir}/%{name}/templates/mc/*
%dir %{_datadir}/%{name}/templates/pres_backgr*
%{_datadir}/%{name}/templates/pres_backgr*/*

%if 0
  /usr/lib/scribus/import_la.prolog
   /usr/share/scribus/scripts/ChangeLog
   /usr/share/scribus/scripts/NEWS
   /usr/share/scribus/scripts/ReadMe
   /usr/share/scribus/scripts/TODO
   /usr/share/scribus/unicodenameslist.txt
%endif
