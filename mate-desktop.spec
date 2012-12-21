# TODO
# - split or move libs to skip circular deps:
# error: LOOP:
#error: removing mate-desktop-1.5.5-0.3.i686 "Requires: mate-desktop-libs = 1.5.5-0.3" from tsort relations.
#error:     mate-desktop-1.5.5-0.3.i686              Requires: mate-desktop-libs = 1.5.5-0.3
#error: removing mate-desktop-libs-1.5.5-0.3.i686 "Requires: mate-desktop = 1.5.5-0.3" from tsort relations.
#error:     mate-desktop-libs-1.5.5-0.3.i686         Requires: mate-desktop = 1.5.5-0.3
# - fix gtk-doc building (probably missing some dtd's)
# - devel: /usr/share/gtk-doc/html is needed by mate-desktop-devel-1.5.5-0.4.i686

# Conditional build:
%bcond_with	doc	# gtk doc. broken

Summary:	Shared code for mate-panel, mate-session, mate-file-manager, etc
Name:		mate-desktop
Version:	1.5.5
Release:	0.4
URL:		http://mate-desktop.org
Source0:	http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
# Source0-md5:	683a8c3efcb5270cd215d9c856b0ced6
Source1:	user-dirs-update-mate.desktop
License:	GPLv2+ and LGPLv2+ and MIT
Group:		X11/Applications
BuildRequires:	desktop-file-utils
BuildRequires:	mate-common
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
%{?with_apidoc:BuildRequires:	pkgconfig(mate-doc-utils)}
BuildRequires:	pkgconfig(unique-1.0)
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
Requires:	%{name} = %{version}-%{release}

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

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
	--enable-gnucat \
	--disable-scrollkeeper \
	--disable-static \
	--disable-schemas-compile \
	--with-pnp-ids-path="%{_datadir}/hwdata/pnp.ids" \
	--enable-unique \
	%{?with_doc:--enable-gtk-doc} \
	--with-omf-dir=%{_datadir}/omf/mate-desktop

%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

desktop-file-install \
	--remove-category="MATE" \
	--add-category="X-Mate" \
	--delete-original \
	--dir=$RPM_BUILD_ROOT%{_desktopdir} \
$RPM_BUILD_ROOT%{_desktopdir}/mate-about.desktop

install -Dp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/user-dirs-update-mate.desktop

%find_lang %{name}

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
%{_sysconfdir}/xdg/autostart/user-dirs-update-mate.desktop
%{_desktopdir}/mate-about.desktop
# XXX %lang
%{_datadir}/mate/help/*/*/*.xml
%{_datadir}/omf/mate-desktop/
%{_datadir}/mate-about/
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_mandir}/man1/mate-about.1*
%{_pixmapsdir}/gnu-cat*

# XXX package these help dirs where?
%dir %{_datadir}/mate/help/fdl
%dir %{_datadir}/mate/help/gpl
%dir %{_datadir}/mate/help/lgpl
%dir %{_datadir}/mate/help/fdl/C
# XXX %lang
%dir %{_datadir}/mate/help/fdl/ar
%dir %{_datadir}/mate/help/fdl/ca
%dir %{_datadir}/mate/help/fdl/de
%dir %{_datadir}/mate/help/fdl/el
%dir %{_datadir}/mate/help/fdl/es
%dir %{_datadir}/mate/help/fdl/eu
%dir %{_datadir}/mate/help/fdl/fr
%dir %{_datadir}/mate/help/fdl/hu
%dir %{_datadir}/mate/help/fdl/ko
%dir %{_datadir}/mate/help/fdl/oc
%dir %{_datadir}/mate/help/fdl/pl
%dir %{_datadir}/mate/help/fdl/sv
%dir %{_datadir}/mate/help/fdl/uk
%dir %{_datadir}/mate/help/fdl/vi
%dir %{_datadir}/mate/help/gpl/C
%dir %{_datadir}/mate/help/gpl/ar
%dir %{_datadir}/mate/help/gpl/ca
%dir %{_datadir}/mate/help/gpl/cs
%dir %{_datadir}/mate/help/gpl/de
%dir %{_datadir}/mate/help/gpl/el
%dir %{_datadir}/mate/help/gpl/es
%dir %{_datadir}/mate/help/gpl/eu
%dir %{_datadir}/mate/help/gpl/fi
%dir %{_datadir}/mate/help/gpl/fr
%dir %{_datadir}/mate/help/gpl/hu
%dir %{_datadir}/mate/help/gpl/ko
%dir %{_datadir}/mate/help/gpl/nds
%dir %{_datadir}/mate/help/gpl/oc
%dir %{_datadir}/mate/help/gpl/pa
%dir %{_datadir}/mate/help/gpl/sv
%dir %{_datadir}/mate/help/gpl/uk
%dir %{_datadir}/mate/help/gpl/vi
%dir %{_datadir}/mate/help/gpl/zh_CN
%dir %{_datadir}/mate/help/lgpl/C
%dir %{_datadir}/mate/help/lgpl/ar
%dir %{_datadir}/mate/help/lgpl/de
%dir %{_datadir}/mate/help/lgpl/el
%dir %{_datadir}/mate/help/lgpl/es
%dir %{_datadir}/mate/help/lgpl/eu
%dir %{_datadir}/mate/help/lgpl/fi
%dir %{_datadir}/mate/help/lgpl/fr
%dir %{_datadir}/mate/help/lgpl/hu
%dir %{_datadir}/mate/help/lgpl/ko
%dir %{_datadir}/mate/help/lgpl/oc
%dir %{_datadir}/mate/help/lgpl/pa
%dir %{_datadir}/mate/help/lgpl/sv
%dir %{_datadir}/mate/help/lgpl/uk
%dir %{_datadir}/mate/help/lgpl/vi
%dir %{_datadir}/mate/help/lgpl/zh_CN

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-desktop-2.so.*.*.*
%ghost %{_libdir}/libmate-desktop-2.so.17

%files devel
%defattr(644,root,root,755)
#%doc %{_datadir}/gtk-doc/html/mate-desktop
%{_libdir}/libmate-desktop-2.so
%{_pkgconfigdir}/mate-desktop-2.0.pc
%{_includedir}/mate-desktop-2.0
