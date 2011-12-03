Summary:	GCC output colorizer
Name:		colorgcc
Version:	1.3.2
Release:	14
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
%apply_patches

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
