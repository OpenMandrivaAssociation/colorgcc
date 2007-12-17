%define name colorgcc
%define version 1.3.2
%define release %mkrel 6

Summary: GCC output colorizer
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Patch0: colorgcc-1.3.2-mdkconf.patch
Patch1: colorgcc-1.3.2-handle-translated-output.patch
License: GPL
Group: Development/C
Url: http://www.schlueters.de/colorgcc.html
Requires: gcc
Obsoletes: gcc2.96-colorgcc
Obsoletes: gcc-colorgcc <= 4.2.1
Provides: gcc-colorgcc <= 4.2.1
BuildArch: noarch

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
%patch0 -p1 -b .mdkconf
%patch1 -p1 -b .i18n

cat <<'EOF' > colorgcc.sh
PATH=%{_datadir}/%{name}:$PATH
export PATH
EOF

cat <<'EOF' > colorgcc.csh
if ( $?PATH ) then
   setenv PATH %{_datadir}/%{name}:$PATH
else
   setenv PATH %{_datadir}/%{name}
endif
EOF

%build

%install
rm -rf %{buildroot}

install -D -m 755 colorgcc     %{buildroot}%{_bindir}/colorgcc
install -D -m 644 colorgccrc   %{buildroot}%{_sysconfdir}/colorgccrc
install -D -m 644 colorgcc.sh  %{buildroot}%{_sysconfdir}/profile.d/20colorgcc.sh
install -D -m 644 colorgcc.csh %{buildroot}%{_sysconfdir}/profile.d/20colorgcc.csh
# nb: prefixing colorgcc.sh by "20" so that it is sourced before 80icecream.sh

install -d %{buildroot}%{_datadir}/%{name}
ln -s ../../bin/colorgcc %{buildroot}%{_datadir}/%{name}/colorgcc
for i in gcc cc g++ c++ gfortran gcj; do
    ln -s colorgcc %{buildroot}%{_datadir}/%{name}/$i
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING CREDITS ChangeLog
%config(noreplace) %{_sysconfdir}/colorgccrc
%{_sysconfdir}/profile.d/*
%{_bindir}/colorgcc
%{_datadir}/colorgcc

%changelog
* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.2-6mdv2008.0
- Rebuild

