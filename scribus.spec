Summary:	Scribus - Desktop Publishing for Linux
Summary(pl):	Scribus - DTP dla Linuksa
Name:		scribus
Version:	0.9.9
Release:	1
License:	GPL
Group:		X11/Applications/Publishing
Source0:        http://web2.altmuehlnet.de/fschmid/%{name}-%{version}.tar.gz
Source1:        http://web2.altmuehlnet.de/fschmid/%{name}-i18n-en.tar.gz
Source2:        http://web2.altmuehlnet.de/fschmid/%{name}-i18n-de.tar.gz
Source3:        http://web2.altmuehlnet.de/fschmid/%{name}-i18n-fr.tar.gz
Source4:        http://web2.altmuehlnet.de/fschmid/%{name}-samples-0.1.tar.gz
Patch0:		%{name}-standard-font-paths.patch
Patch1:		%{name}-module-fixes.patch
Patch2:		%{name}-nolibs.patch
URL:		http://web2.altmuehlnet.de/fschmid/
BuildRequires:	lcms-devel >= 1.08-2
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	qt-devel >= 3.0.5
BuildRequires:	zlib-devel
# fonts are required locally!
Requires:	XFree86-fonts
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Group:          Development/Libraries
# for now it doesn't require base
#Requires:       %{name} = %{version}
Requires:	qt-devel

%description devel
Header files for Scribus plugins development.

%description devel -l pl
Pliki nag³ówkowe do tworzenia wtyczek Scribusa.

%prep
%setup -q -a1 -a2 -a3 -a4
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
QTDIR=%{_prefix}
KDEDIR=%{_prefix}
export QTDIR KDEDIR

%{__aclocal}
%{__autoconf}
# don't regenerate Makefile.ins, they are broken by kdevelop
touch Makefile.in */Makefile.in */*/Makefile.in */*/*/Makefile.in
%configure
%{__make}
cd scribus-i18n-en
%configure
%{__make}
cd ../scribus-i18n-de
%configure2_13
%{__make}
cd ../scribus-i18n-fr
%configure2_13
%{__make}
cd ../scribus-samples-0.1
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/doc
ln -s $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_datadir}

for dir in . scribus-*; do
	olddir=$(pwd)
	cd $dir
	%{__make} install \
		DESTDIR=$RPM_BUILD_ROOT
	cd $olddir
done

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
%lang(de) %{_libdir}/%{name}/doc/de
%lang(fr) %{_libdir}/%{name}/doc/fr
%{_libdir}/%{name}/icons
%dir %{_libdir}/%{name}/libs
%attr(755,root,root) %{_libdir}/%{name}/libs/*.so*
%attr(755,root,root) %{_libdir}/%{name}/libs/*.la
%dir %{_libdir}/%{name}/plugins
%lang(da) %{_libdir}/%{name}/plugins/*.da.qm
%lang(de) %{_libdir}/%{name}/plugins/*.de.qm
%lang(sk) %{_libdir}/%{name}/plugins/*.sk.qm
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so*
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.la
%{_libdir}/scribus/profiles
%{_libdir}/scribus/samples
%{_libdir}/scribus/*.enc
%{_libdir}/scribus/*enc.txt
%lang(bg) %{_libdir}/scribus/scribus.bg.qm
#%lang(ca) %{_libdir}/scribus/scribus.ca.qm
%lang(da) %{_libdir}/scribus/scribus.da.qm
%lang(de) %{_libdir}/scribus/scribus.de.qm
%lang(en_GB) %{_libdir}/scribus/scribus.en_GB.qm
%lang(es) %{_libdir}/scribus/scribus.es.qm
%lang(fr) %{_libdir}/scribus/scribus.fr.qm
%lang(gl) %{_libdir}/scribus/scribus.gl.qm
#%lang(hu) %{_libdir}/scribus/scribus.hu.qm
%lang(it) %{_libdir}/scribus/scribus.it.qm
#%lang(lt) %{_libdir}/scribus/scribus.lt.qm
%lang(pl) %{_libdir}/scribus/scribus.pl.qm
%lang(sk) %{_libdir}/scribus/scribus.sk.qm
%lang(tr) %{_libdir}/scribus/scribus.tr.qm
%lang(uk) %{_libdir}/scribus/scribus.uk.qm

%files devel
%defattr(644,root,root,755)
%{_includedir}/scribus
