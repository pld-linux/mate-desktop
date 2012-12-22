#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

Summary:	Shared code for mate-panel, mate-session, mate-file-manager, etc
Name:		mate-desktop
Version:	1.5.5
Release:	0.11
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	683a8c3efcb5270cd215d9c856b0ced6
Source1:	user-dirs-update-mate.desktop
License:	GPLv2+ and LGPLv2+ and MIT
Group:		X11/Applications
URL:		http://mate-desktop.org/
BuildRequires:	desktop-file-utils
BuildRequires:	mate-common
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
%{?with_apidoc:BuildRequires:	pkgconfig(mate-doc-utils)}
BuildRequires:	pkgconfig(unique-1.0)
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.26.0
Requires:	python-pygtk-gtk
#Requires:	redhat-menus
Requires:	xdg-user-dirs-gtk
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
	--enable-gnucat \
	--disable-scrollkeeper \
	--disable-static \
	--disable-schemas-compile \
	--with-pnp-ids-path="%{_datadir}/hwdata/pnp.ids" \
	--enable-unique \
	%{?with_apidocs:--enable-gtk-doc --with-html-dir=%{_gtkdocdir}} \
	--with-omf-dir=%{_datadir}/omf/%{name}

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmate-desktop-2.la

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/mate-about.desktop

install -Dp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/user-dirs-update-mate.desktop

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
%{_sysconfdir}/xdg/autostart/user-dirs-update-mate.desktop
%attr(755,root,root) %{_bindir}/mate-about
%{_mandir}/man1/mate-about.1*
%{_pixmapsdir}/gnu-cat*
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
