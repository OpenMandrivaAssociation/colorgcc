Summary:	GCC output colorizer
Name:		colorgcc
Version:	1.3.2
Release:	17
Source0:	%{name}-%{version}.tar.bz2
Patch0:		005_old_changes.patch
Patch1:		01_split_non_quoted.patch
Patch2:		02_stderr.patch
Patch3:		03_color_warnings.patch
Patch4:		04_g++_color.patch
Patch5:		05_console-colors.patch
Patch6:		06_use_distcc.patch
Patch7:		07_invalid_attr.patch
Patch8:		08_force_color_opt.patch 
Patch9:		09_color_warnings.patch
Patch10:	10_utf8_output.patch
Patch11:	colorgcc-1.3.2-handle-translated-output.patch
Patch12:	colorgcc-1.3.2-dont-use-unitialized-env-value.patch
# fix so that colorgcc wrapper will work with other wrappers such as ie.
# icecream, distcc & ccache
Patch13:	colorgcc-1.3.2-get-gcc-path-properly.patch
# magenta color is easier on the eyes than dark blue, especially when using a
# dark background
Patch14:	colorgcc-1.3.2-make-linenumber-magenta-colored.patch

License:	GPL
Group:		Development/C
Url:		http://www.schlueters.de/colorgcc.html
Requires:	gcc
Obsoletes:	gcc2.96-colorgcc
%rename		gcc-colorgcc
BuildArch:	noarch

%description
ColorGCC is a Perl wrapper to colorize the output of compilers with
warning and error messages matching the GCC output format.

This package is configured to run with the associated system compiler. If you
want to use it for another compiler (e.g. gcc 2.96), you may have to define
gccVersion: 2.96 and uncomment the respective compiler paths in
%{_sysconfdir}/colorgccrc for a system-wide effect, or in ~/.colorgccrc for
your user only.

%prep
%setup -q
%autopatch -p1

cat <<'EOF' > colorgcc.sh
case ":${PATH}:" in
    :: )
	PATH=%{_datadir}/%{name}
	export PATH
    ;;
    *:%{_datadir}/%{name}:* )
	: Already set
    ;;
    * )
	PATH=%{_datadir}/%{name}:$PATH
	export PATH
    ;;
esac
EOF

cat <<'EOF' > colorgcc.csh
if ( $?PATH ) then
    switch (:${PATH}:)
	case *":%{_datadir}/%{name}:"* :
		breaksw
	default :
		setenv PATH %{_datadir}/%{name}:$PATH
		breaksw
	endsw
else
   setenv PATH %{_datadir}/%{name}
endif
EOF

%build

%install
install -D -m 755 colorgcc     %{buildroot}%{_bindir}/colorgcc
install -D -m 644 colorgccrc   %{buildroot}%{_sysconfdir}/colorgccrc
install -D -m 644 colorgcc.sh  %{buildroot}%{_sysconfdir}/profile.d/90colorgcc.sh
install -D -m 644 colorgcc.csh %{buildroot}%{_sysconfdir}/profile.d/90colorgcc.csh

install -d %{buildroot}%{_datadir}/%{name}
ln -s ../../bin/colorgcc %{buildroot}%{_datadir}/%{name}/colorgcc
for i in gcc cc g++ c++ gfortran gcj; do
    ln -s colorgcc %{buildroot}%{_datadir}/%{name}/$i
done

%files
%doc COPYING CREDITS ChangeLog
%config(noreplace) %{_sysconfdir}/colorgccrc
%{_sysconfdir}/profile.d/*
%{_bindir}/colorgcc
%{_datadir}/colorgcc


%changelog
* Thu May 24 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.3.2-16
+ Revision: 800353
- make line number magenta colored to make it easier on the eyes to read (P14)

* Wed Mar 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.3.2-15
+ Revision: 782794
- fix current working directory being added to $PATH in colorgcc
- load colorgccrc from the correct path

* Sat Dec 03 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.3.2-14
+ Revision: 737399
- fix so that colorgcc wrapper should be working in combination with other gcc
  wrappers as well (P13)

* Thu Jul 14 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.3.2-13
+ Revision: 689959
- merge debian patches

* Tue Apr 26 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.3.2-12
+ Revision: 659385
- fix warnings when $HOME for some reason isn't defined
- cleanups

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.2-11mdv2011.0
+ Revision: 610152
- rebuild

* Tue Nov 03 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 1.3.2-10mdv2010.1
+ Revision: 460412
- do not duplicate PATH entry on recursive shell invocation

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 1.3.2-9mdv2010.0
+ Revision: 424937
- rebuild

* Wed Jul 23 2008 Thierry Vignaud <tv@mandriva.org> 1.3.2-8mdv2009.0
+ Revision: 243606
- rebuild

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 1.3.2-6mdv2008.1
+ Revision: 136330
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.2-6mdv2008.0
+ Revision: 89587
- rebuild

* Mon Aug 06 2007 Pixel <pixel@mandriva.com> 1.3.2-5mdv2008.0
+ Revision: 59559
- rebuild for build system test

* Mon Aug 06 2007 Pixel <pixel@mandriva.com> 1.3.2-4mdv2008.0
+ Revision: 59553
- rebuild for build system test

* Mon Aug 06 2007 Pixel <pixel@mandriva.com> 1.3.2-3mdv2008.0
+ Revision: 59543
- rebuild for build system test

* Mon Aug 06 2007 Pixel <pixel@mandriva.com> 1.3.2-2mdv2008.0
+ Revision: 59484
- fix parsing warnings as warnings when messages are translated (#32282)

* Wed Jul 11 2007 Pixel <pixel@mandriva.com> 1.3.2-1mdv2008.0
+ Revision: 51263
- standalone package which replaces gcc-colorgcc
- uses its own path to be independant of installed gcc
- Create colorgcc

