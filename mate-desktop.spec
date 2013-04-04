#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

Summary:	Shared code for mate-panel, mate-session, mate-file-manager, etc
Name:		mate-desktop
Version:	1.6.0
Release:	2
License:	GPL v2+ and LGPL v2+ and MIT
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	425e5bf587372cc05dcb4538b8c3825d
URL:		http://wiki.mate-desktop.org/mate-desktop
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libunique-devel
BuildRequires:	mate-common
%{?with_apidocs:BuildRequires:	mate-doc-utils >= 1.1.0}
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	startup-notification-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
# for identifying monitors from pnp.ids (libmate-desktop/display-name.c)
Requires:	hwdata >= 0.243-6
Requires:	xdg-user-dirs-gtk >= 0.10-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The mate-desktop package contains an internal library (libmatedesktop)
used to implement some portions of the MATE desktop, and also some
data files and other shared components of the MATE user environment.

%package libs
Summary:	Shared libraries for libmate-desktop
License:	LGPL v2+
Group:		Libraries

%description libs
Shared libraries for libmate-desktop

%package devel
Summary:	Libraries and headers for libmate-desktop
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Libraries and header files for the MATE-internal private library
libmatedesktop.

%package apidocs
Summary:	mate-desktop API documentation
Summary(pl.UTF-8):	Dokumentacja API mate-desktop
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
mate-desktop API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API mate-desktop.

%prep
%setup -q

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-silent-rules \
	--disable-scrollkeeper \
	--disable-static \
	--disable-schemas-compile \
	--with-pnp-ids-path=/lib/hwdata/pnp.ids \
	--enable-unique \
	%{?with_apidocs:--enable-gtk-doc --with-html-dir=%{_gtkdocdir}} \
	--with-omf-dir=%{_datadir}/omf/%{name}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmate-desktop-2.la

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-desktop.convert

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/mate-about.desktop

%find_lang %{name} --with-mate --with-omf --all-name

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING.LIB NEWS README
%attr(755,root,root) %{_bindir}/mate-about
%{_mandir}/man1/mate-about.1*
%{_desktopdir}/mate-about.desktop
%dir %{_datadir}/omf/%{name}/fdl
%dir %{_datadir}/omf/%{name}/gpl
%dir %{_datadir}/omf/%{name}/lgpl
%{_datadir}/mate-about
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-desktop-2.so.*.*.*
%ghost %{_libdir}/libmate-desktop-2.so.17

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmate-desktop-2.so
%{_pkgconfigdir}/mate-desktop-2.0.pc
%{_includedir}/mate-desktop-2.0

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-desktop
%endif
