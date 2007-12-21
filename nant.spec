%define name nant
%define version 0.86
%define prerel beta1
%define fname %name-%version-%prerel-src
%define rel 0.%prerel.2

Summary: NAnt is a build tool for Mono and .NET
Name: %{name}
Version: %{version}
Release: %mkrel %rel
Epoch: 1
Source0: http://prdownloads.sourceforge.net/nant/%{fname}.tar.gz
#gw from cvs, fix upstream bug 1850383
Patch: nant-fix-useruntimeengine-override.patch
License: GPL
Group: Development/Other
Url: http://nant.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#gw required for mono.pc
Requires: mono-devel
BuildRequires: mono-devel
BuildArch: noarch

%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.

%prep
%setup -q -n %name-%version-%prerel
find . -type d|xargs chmod 755
find . -type f|xargs chmod 644
# remove DOS line endings
find doc src -type f |xargs perl -pi -e "s/\r\n/\n/"
cd src/NAnt.Core/Tasks/
%patch -p0 -b .useruntimeengine
cd ../../..

%build
#gw to find the log4net.dll
export MONO_PATH=`pwd`/lib
make prefix=/usr/

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
perl -pi -e "s°%buildroot°°" %buildroot%_bindir/%name
find examples -name \*.dll -o -name \*.exe|xargs rm -f
rm -rf %buildroot%_datadir/NAnt/doc

# gw fix paths in the nant script
perl -pi -e "s^%_libdir/pkgconfig/../../bin^%_bindir^" %buildroot%_bindir/nant

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README.txt doc/* examples
%_bindir/%name
%_datadir/NAnt/


