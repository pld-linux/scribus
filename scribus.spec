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
Version:	1.5.5
Release:	1
License:	GPL v2+
Group:		X11/Applications/Publishing
Source0:	http://downloads.sourceforge.net/scribus/%{name}-%{version}.tar.xz
# Source0-md5:	6a9ddc8c45356d3c6c741e4c7bb0565a
Patch1:		%{name}-standard-font-paths.patch
Patch2:		%{name}-docs.patch
Patch3:		%{name}-sparc.patch
Patch4:		qt-5.15.patch
Patch5:		poppler-0.84.0.patch
Patch6:		poppler-0.86.0.patch
Patch7:		gcc10.patch
URL:		http://www.scribus.net/
BuildRequires:	GraphicsMagick-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5OpenGL-devel
BuildRequires:	Qt5PrintSupport-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	Qt5Xml-devel
%{?with_cairo:BuildRequires:	cairo-devel >= 1.2.0}
BuildRequires:	cmake >= 2.4.5
%if %{with cups}
BuildRequires:	cups-devel
%else
BuildConflicts:	cups-devel
%endif
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	harfbuzz-devel
BuildRequires:	harfbuzz-icu-devel
BuildRequires:	hunspell-devel
BuildRequires:	lcms-devel >= 1.09
%{!?with_cairo:BuildRequires:	libart_lgpl-devel >= 2.3.14}
BuildRequires:	libcdr-devel
BuildRequires:	libfreehand-devel
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmspub-devel
BuildRequires:	libpagemaker-devel
BuildRequires:	libpng-devel
BuildRequires:	libqxp-devel
BuildRequires:	librevenge-devel
BuildRequires:	libtiff-devel
BuildRequires:	libvisio-devel
BuildRequires:	libxml2-devel
BuildRequires:	libzmf-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	podofo-devel
BuildRequires:	poppler-cpp-devel
BuildRequires:	poppler-devel
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	qt5-build
BuildRequires:	qt5-linguist
BuildRequires:	qt5-qmake
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
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
mkdir -p build
cd build

%cmake .. \
	-DASPELL_EXECUTABLE=%{_bindir}/aspell \
	-DWANT_GRAPHICSMAGICK:BOOL=ON \
%if %{with cairo}
	-DWANT_CAIRO=1
%else
	-DWANT_LIBART=1
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.lt_LT.qm $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.lt.qm

%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc/{AUTHORS,COPYING,ChangeLog,README,LINKS,TRANSLATION}

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/scribus
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/scribus.css
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so*
%dir %{_libdir}/%{name}/plugins/gettext
%attr(755,root,root) %{_libdir}/%{name}/plugins/gettext/*.so*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/dicts
%{_datadir}/%{name}/editorconfig
%{_datadir}/%{name}/keysets
%dir %{_datadir}/%{name}/profiles
%dir %{_datadir}/%{name}/translations
%{_datadir}/%%{name}/translations/scribus*.qm
%dir %{_datadir}/%{name}/swatches
%{_datadir}/%{name}/swatches/*
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
%{_datadir}/%{name}/unicodenameslist.txt
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*x*/apps/scribus.png
%{_datadir}/metainfo/scribus.appdata.xml
%{_mandir}/man1/%{name}.1*
%lang(de) %{_mandir}/de/man1/%{name}.1*
%lang(pl) %{_mandir}/pl/man1/%{name}.1*

%files docs
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}/doc
%{_datadir}/%{name}/doc/en
%lang(de) %{_datadir}/%{name}/doc/de
%lang(it) %{_datadir}/%{name}/doc/it

%files icc
%defattr(644,root,root,755)
%{_datadir}/scribus/profiles/*

%files templates-base
%defattr(644,root,root,755)
%{_datadir}/%{name}/templates
