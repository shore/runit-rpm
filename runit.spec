#
# spec file for package runit (Version 2.1.2)
#
# Copyright (c) 2010 Ian Meyer <ianmmeyer@gmail.com>

## This package understands the following switches:
## --with dietlibc ...  statically links against dietlibc

Name:           runit
Version:        2.1.2
Release:        3%{?_with_dietlibc:diet}%{?dist}.pharos

Group:          System/Base
License:        BSD

# Override _sbindir being /usr/sbin
%define _sbindir /sbin

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Url:            http://smarden.org/runit/
Source0:        http://smarden.org/runit/runit-%{version}.tar.gz
Source1:        runsvdir-start.service
Source2:        1
Source3:        2
Source4:        3
Source5:        runit.init
Patch0:         runit-2.1.2-pid1exit.patch

Obsoletes: runit <= %{version}-%{release}
Provides: runit = %{version}-%{release}

BuildRequires: make gcc
%if 0%{?rhel} >= 6
BuildRequires:  glibc-static
%endif

%{?_with_dietlibc:BuildRequires:        dietlibc}

Summary:        A UNIX init scheme with service supervision

%description
runit is a cross-platform Unix init scheme with service supervision; a
replacement for sysvinit and other init schemes. It runs on GNU/Linux, *BSD,
Mac OS X, and Solaris, and can easily be adapted to other Unix operating
systems. runit implements a simple three-stage concept. Stage 1 performs the
system's one-time initialization tasks. Stage 2 starts the system's uptime
services (via the runsvdir program). Stage 3 handles the tasks necessary to
shutdown and halt or reboot.

Authors:
---------
    Gerrit Pape <pape@smarden.org>

%prep
%setup -q -n admin/%{name}-%{version}
pushd src
echo "%{?_with_dietlibc:diet -Os }%__cc $RPM_OPT_FLAGS" >conf-cc
echo "%{?_with_dietlibc:diet -Os }%__cc -Os -pipe"      >conf-ld
popd
%patch0 -p 2

%build
sh package/compile

%install
%{__rm} -rf %{buildroot}

EXTRA_FILES=$RPM_BUILD_ROOT/extra_files
touch %{EXTRA_FILES}

for i in $(< package/commands) ; do
    %{__install} -D -m 0755 command/$i %{buildroot}%{_sbindir}/$i
done
for i in man/*8 ; do
    %{__install} -D -m 0755 $i %{buildroot}%{_mandir}/man8/${i##man/}
done

%{__install} -d -m 0755 %{buildroot}/service
%{__install} -d -m 0755 %{buildroot}/etc/service
%{__install} -d -m 0755 %{buildroot}/etc/runit
%{__install} -d -m 0755 %{buildroot}/etc/runit/1.d
%{__install} -d -m 0755 %{buildroot}/etc/runit/3.d
%{__install}    -m 0755 $RPM_SOURCE_DIR/1 %{buildroot}/etc/runit/1
%{__install}    -m 0755 $RPM_SOURCE_DIR/2 %{buildroot}/etc/runit/2
%{__install}    -m 0755 $RPM_SOURCE_DIR/3 %{buildroot}/etc/runit/3
%{__install} -D -m 0755 $RPM_SOURCE_DIR/runit.init %{buildroot}%{_initddir}/%{name}


# For systemd only
%if 0%{?rhel} >= 7
%{__install} -D -p -m 0644 $RPM_SOURCE_DIR/runsvdir-start.service \
                       $RPM_BUILD_ROOT%{_unitdir}/runsvdir-start.service
echo %{_unitdir}/runsvdir-start.service > %{EXTRA_FILES}
%endif

%clean
%{__rm} -rf %{buildroot}

%post
if [ $1 = 1 ] ; then
  /bin/ln -vsf /etc/runit/2 /sbin/runsvdir-start

  %if 0%{?rhel} > 6
    rpm --queryformat='%%{name}' -qf /sbin/init | grep -q upstart
    if [ $? -eq 0 ]; then
      cat >/etc/init/runsvdir.conf <<\EOT
# for runit - manage /usr/sbin/runsvdir-start
start on runlevel [2345]
stop on runlevel [^2345]
normal exit 0 111
respawn
exec /sbin/runsvdir-start
EOT
    fi
  %endif

  %if 0%{?rhel} <= 6
    /sbin/chkconfig --add runit
  %endif
fi

%preun
if [ $1 = 0 ]; then
  if [ -f /etc/init/runsvdir.conf ]; then
    stop runsvdir
  elif [ -f /etc/init.d/runit ]; then
    /sbin/chkconfig --del runit
  fi
fi

%postun
if [ $1 = 0 ]; then
  /bin/rm -vf /sbin/runsvdir-start

  if [ -f /etc/init/runsvdir.conf ]; then
    rm -f /etc/init/runsvdir.conf
  fi
fi

%files -f %{EXTRA_FILES}
%defattr(-,root,root,-)
%{_sbindir}/chpst
%{_sbindir}/runit
%{_sbindir}/runit-init
%{_sbindir}/runsv
%{_sbindir}/runsvchdir
%{_sbindir}/runsvdir
%{_sbindir}/sv
%{_sbindir}/svlogd
%{_sbindir}/utmpset
%{_mandir}/man8/*.8*
%doc doc/*
%doc package/CHANGES package/COPYING package/README package/THANKS package/TODO
%dir /service
%dir /etc/service
%dir /etc/runit
%dir /etc/runit/1.d
%dir /etc/runit/3.d
/etc/runit/1
/etc/runit/2
/etc/runit/3
%{_initddir}/runit

%changelog
* Thu Aug 21 2014 Chris Gaffney <gaffneyc@gmail.com> 2.1.2-1
- Initial release of 2.1.2

* Fri Jan 20 2012 Joe Miller <joeym@joeym.net> 2.1.1-6
- modified spec to build on centos-5 (by only requiring glibc-static on centos-6)

* Wed Oct 26 2011 Karsten Sperling <mail@ksperling.net> 2.1.1-5
- Optionally shut down cleanly even on TERM
- Don't call rpm in preun, it can cause problems
- Upstart / inittab tweaks

* Wed Jul 20 2011 Robin Bowes <robin.bowes@yo61.com> 2.1.1-4
-  2.1.1-3 Add BuildRequires
-  2.1.1-4 Support systems using upstart

* Sun Jan 23 2011 ianmmeyer@gmail.com
- Make compatible with Redhat based systems
