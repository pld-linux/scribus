# TODO:
# - OpenSceneGraph support (WANT_NOOSG to disable)
# - system hyphen
# - more system libs, see scribus/third_party (e.g. libwpg)
#
# Conditional build:
%bcond_without	cups	# CUPS support
#
%define	qt_ver	5.7.0
Summary:	Scribus - Open Source Desktop Publishing
Summary(pl.UTF-8):	Scribus - DTP dla Wolnego Oprogramowania
Name:		scribus
Version:	1.5.5
Release:	3
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
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Network-devel >= %{qt_ver}
BuildRequires:	Qt5OpenGL-devel >= %{qt_ver}
BuildRequires:	Qt5PrintSupport-devel >= %{qt_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	Qt5Xml-devel >= %{qt_ver}
BuildRequires:	boost-devel
BuildRequires:	cairo-devel >= 1.2.0
BuildRequires:	cmake >= 3.2.0
%if %{with cups}
BuildRequires:	cups-devel
%else
BuildConflicts:	cups-devel
%endif
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.1.0
BuildRequires:	harfbuzz-devel >= 0.9.42
BuildRequires:	harfbuzz-icu-devel
BuildRequires:	hunspell-devel
# missing find_package(HYPHEN); bundled version is used
#BuildRequires:	hyphen-devel
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libcdr-devel >= 0.1
BuildRequires:	libfreehand-devel >= 0.1
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmspub-devel >= 0.1
BuildRequires:	libpagemaker-devel
# disabled in 1.5.5
#BuildRequires:	libpng-devel
BuildRequires:	libqxp-devel
BuildRequires:	librevenge-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtiff-devel
BuildRequires:	libvisio-devel >= 0.1
BuildRequires:	libxml2-devel >= 2
BuildRequires:	libzmf-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	podofo-devel
BuildRequires:	poppler-cpp-devel >= 0.58.0
BuildRequires:	poppler-devel >= 0.58.0
BuildRequires:	python-devel >= 2
BuildRequires:	python-modules >= 2
BuildRequires:	qt5-build >= %{qt_ver}
BuildRequires:	qt5-linguist >= %{qt_ver}
BuildRequires:	qt5-qmake >= %{qt_ver}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.577
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	Qt5Core >= %{qt_ver}
Requires:	Qt5Gui >= %{qt_ver}
Requires:	Qt5Network >= %{qt_ver}
Requires:	Qt5OpenGL >= %{qt_ver}
Requires:	Qt5PrintSupport >= %{qt_ver}
Requires:	Qt5Widgets >= %{qt_ver}
Requires:	Qt5Xml >= %{qt_ver}
Requires:	harfbuzz >= 0.9.42
Requires:	hicolor-icon-theme
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
License:	custom OPL (see License), FDL
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
	-DWANT_GRAPHICSMAGICK:BOOL=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{cs_CZ,cs}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{da_DK,da}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{es_ES,es}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{fa_IR,fa}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{he_IL,he}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{hi_IN,hi}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{hr_HR,hr}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{kn_IN,kn}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{lt_LT,lt}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{mn_MN,mn}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{nb_NO,nb}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{pl_PL,pl}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{pt_PT,pt}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{sk_SK,sk}.qm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.{th_TH,th}.qm

echo '%%defattr(644,root,root,755)' >%{name}.lang
for f in $RPM_BUILD_ROOT%{_datadir}/%{name}/translations/%{name}.*.qm ; do
	bn="$(basename $f .qm)"
	lang="${bn#%{name}.}"
	echo "%%lang(${lang}) ${f#${RPM_BUILD_ROOT}}" >>%{name}.lang
done

%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc/{AUTHORS,COPYING,ChangeLog,README,LINKS,TRANSLATION}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_mime_database
%update_icon_cache hicolor

%postun
%update_desktop_database_postun
%update_mime_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
# COPYING contains many additional notes
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/scribus
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/scribus.css
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so*
%dir %{_libdir}/%{name}/plugins/gettext
%attr(755,root,root) %{_libdir}/%{name}/plugins/gettext/*.so*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/dtd
%{_datadir}/%{name}/dicts
%{_datadir}/%{name}/editorconfig
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/keysets
%{_datadir}/%{name}/loremipsum
%{_datadir}/%{name}/plugins
%dir %{_datadir}/%{name}/profiles
%dir %{_datadir}/%{name}/samples
%{_datadir}/%{name}/samples/*.py
%{_datadir}/%{name}/scripts
%{_datadir}/%{name}/swatches
%dir %{_datadir}/%{name}/translations
%{_datadir}/%{name}/unicodenameslist.txt
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*x*/apps/scribus.png
%{_datadir}/mime/packages/scribus.xml
%{_datadir}/metainfo/scribus.appdata.xml
%{_mandir}/man1/scribus.1*
%lang(de) %{_mandir}/de/man1/scribus.1*
%lang(pl) %{_mandir}/pl/man1/scribus.1*

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
