Summary:	Scribus - Desktop Publishing for Linux
Summary(pl):	Scribus - DTP dla Linuksa
Name:		scribus
Version:	0.9.3
Release:	1
License:	GPL
Group:		X11/Applications/Publishing
Source0:	http://web2.altmuehlnet.de/fschmid/%{name}-%{version}.tar.gz
Patch0:		%{name}-standard-font-paths.patch
Patch1:		%{name}-module-fixes.patch
BuildRequires:	lcms-devel >= 1.08-2
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	qt-devel >= 3.0.5
BuildRequires:	zlib-devel
# fonts are required locally!
Requires:	XFree86-fonts
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
%patch0 -p1
%patch1 -p1

%build
%configure2_13 \
	--prefix=%{_prefix} \
	--with-qt-includes=/usr/X11R6/include/qt \
	--with-qt-libraries=/usr/X11R6/lib

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/scribus
%dir %{_datadir}/scribus
%{_datadir}/scribus/*.enc
%{_datadir}/scribus/*enc.txt
%{_datadir}/scribus/icons
%dir %{_datadir}/scribus/profiles
%dir %{_libdir}/scribus
%attr(755,root,root) %{_libdir}/scribus/lib*.so*
%dir %{_libdir}/scribus/plugins
%attr(755,root,root) %{_libdir}/scribus/plugins/lib*.so*
%dir %{_datadir}/scribus/plugins
%lang(de) %{_datadir}/scribus/plugins/*.de.qm
%lang(sk) %{_datadir}/scribus/plugins/*.sk.qm
%lang(bg) %{_datadir}/scribus/scribus.bg.qm
%lang(ca) %{_datadir}/scribus/scribus.ca.qm
%lang(de) %{_datadir}/scribus/scribus.de.qm
%lang(es) %{_datadir}/scribus/scribus.es.qm
%lang(fr) %{_datadir}/scribus/scribus.fr.qm
%lang(gl) %{_datadir}/scribus/scribus.gl.qm
%lang(hu) %{_datadir}/scribus/scribus.hu.qm
%lang(it) %{_datadir}/scribus/scribus.it.qm
%lang(lt) %{_datadir}/scribus/scribus.lt.qm
%lang(sk) %{_datadir}/scribus/scribus.sk.qm
%lang(tr) %{_datadir}/scribus/scribus.tr.qm
%lang(uk) %{_datadir}/scribus/scribus.uk.qm
# ONLINE documentation
%docdir %{_datadir}/scribus/doc
%dir %{_datadir}/scribus/doc
#%lang(de) %{_datadir}/scribus/doc/de
%{_datadir}/scribus/doc/en
#%lang(fr) %{_datadir}/scribus/doc/fr

# -devel package?
#%{_includedir}/scribus
