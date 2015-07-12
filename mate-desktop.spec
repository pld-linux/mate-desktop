#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_with	gtk3		# use GTK+ 3.x instead of GTK+ 2.x

Summary:	Shared code for mate-panel, mate-session, mate-file-manager, etc.
Summary(pl.UTF-8):	Kod współdzielony przez pakiety mate-panel, mate-session, mate-file-manager itd.
Name:		mate-desktop
Version:	1.10.1
Release:	1
License:	LGPL v2+ with MIT parts (library), GPL v2+ (mate-about)
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.10/%{name}-%{version}.tar.xz
# Source0-md5:	9e4cae2c9da09f00804141c7f77996e8
URL:		http://wiki.mate-desktop.org/mate-desktop
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.9
BuildRequires:	dconf-devel >= 0.13.4
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gdk-pixbuf2-devel >= 2.4.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gobject-introspection-devel >= 0.9.7
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.24.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	gtk-doc >= 1.4
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
%{!?with_gtk3:BuildRequires:	libunique-devel >= 1.0}
%{?with_gtk3:BuildRequires:	libunique3-devel >= 3.0}
BuildRequires:	mate-common
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	startup-notification-devel >= 0.5
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXrandr-devel >= 1.2
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	%{name}-libs = %{version}-%{release}
# for identifying monitors from pnp.ids (libmate-desktop/display-name.c)
Requires:	hwdata >= 0.243-6
Requires:	xdg-user-dirs-gtk >= 0.10-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The mate-desktop package contains an internal library (libmatedesktop)
used to implement some portions of the MATE desktop, and also some
data files and other shared components of the MATE user environment.

%description -l pl.UTF-8
Pakiet mate-desktop zawiera bibliotekę wewnętrzną (libmatedesktop)
służącą do implementacji niektórych elementów środowiska MATE, trochę
plików z danymi oraz inne współdzielone komponenty środowiska
użytkownika MATE.

%package libs
Summary:	Shared libmate-desktop library
Summary(pl.UTF-8):	Biblioteka współdzielona libmate-desktop
License:	LGPL v2+
Group:		Libraries
Requires:	gdk-pixbuf2 >= 2.4.0
Requires:	glib2 >= 1:2.36.0
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.24.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Requires:	startup-notification >= 0.5
Requires:	xorg-lib-libXrandr >= 1.2

%description libs
Shared libmate-desktop library.

%description libs -l pl.UTF-8
Biblioteka współdzielona libmate-desktop.

%package devel
Summary:	Header files for libmate-desktop
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmate-desktop
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gdk-pixbuf2-devel >= 2.4.0
Requires:	glib2-devel >= 1:2.36.0
%{!?with_gtk3:Requires:	gtk+2-devel >= 2:2.24.0}
%{?with_gtk3:Requires:	gtk+3-devel >= 3.0.0}
Requires:	startup-notification-devel >= 0.5

%description devel
Header files for the MATE-internal private library libmate-desktop.

%description devel -l pl.UTF-8
Pliki nagłówkowe prywatnej biblioteki wewnętrznej MATE
libmate-desktop.

%package apidocs
Summary:	mate-desktop API documentation
Summary(pl.UTF-8):	Dokumentacja API mate-desktop
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
mate-desktop API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API mate-desktop.

%prep
%setup -q

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-gtk-doc --with-html-dir=%{_gtkdocdir}} \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-static \
	--enable-unique \
	--enable-mpaste \
	%{?with_gtk3:--with-gtk=3.0} \
	--with-pnp-ids-path=/lib/hwdata/pnp.ids

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmate-desktop-2.la
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/cmn

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-desktop.convert

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/mate-about.desktop

%find_lang %{name} --with-mate --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%attr(755,root,root) %{_bindir}/mate-about
%attr(755,root,root) %{_bindir}/mate-color-select
%attr(755,root,root) %{_bindir}/mpaste
%{_mandir}/man1/mate-about.1*
%{_mandir}/man1/mate-color-select.1*
%{_mandir}/man1/mpaste.1*
%{_desktopdir}/mate-about.desktop
%{_desktopdir}/mate-color-select.desktop
%{_desktopdir}/mate-user-guide.desktop
%{_datadir}/mate-about
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-desktop-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmate-desktop-2.so.17
%{_libdir}/girepository-1.0/MateDesktop-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-desktop-2.so
%{_includedir}/mate-desktop-2.0
%{_datadir}/gir-1.0/MateDesktop-2.0.gir
%{_pkgconfigdir}/mate-desktop-2.0.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-desktop
%endif
