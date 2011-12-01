%define name nant
%define version 0.91
%define fname %name-%version-src

Summary: Build tool for Mono and .NET
Name: %{name}
Version: %{version}
Release: %mkrel 1
Epoch: 1
Source0: http://prdownloads.sourceforge.net/nant/%{fname}.tar.gz
Patch0: nant-0.91-no_ndoc.patch
Patch1: nant-0.90-no_sharpcvslib.patch
Patch2: nant-0.91-system_log4net.patch
Patch3: nant-0.90-system_nunit.patch
Patch4: nant-0.91-system_sharpziplib.patch
License: GPL
Group: Development/Other
Url: http://nant.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#gw required for mono.pc
Requires: mono-devel
BuildRequires: mono-devel
BuildRequires: log4net-devel
BuildArch: noarch

%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.

%prep
%setup -q -n %name-%version
%apply_patches
find . -type d|xargs chmod 755
find . -type f|xargs chmod 644
# remove DOS line endings
find doc src -type f |xargs perl -pi -e "s/\r\n/\n/"

rm src/NAnt.DotNet/Tasks/NDocTask.cs
find lib -name 'NDoc*.dll' | xargs rm
find lib -iname 'nunit*' | xargs rm
find lib -name "*SharpCvsLib*.dll" | xargs rm
find lib -name "scvs.exe" | xargs rm
find lib -name "*SharpZipLib*.dll" | xargs rm
rm -rf lib/*
mkdir -p lib/common/neutral
cp /usr/lib/mono/log4net/log4net.dll lib/common/neutral

%build
make prefix=%_prefix

%install
rm -rf %{buildroot}
%makeinstall
perl -pi -e "s°%buildroot°°" %buildroot%_bindir/%name
find examples -name \*.dll -o -name \*.exe|xargs rm -f
rm -rf %buildroot%_datadir/NAnt/doc

# gw fix paths in the nant script
perl -pi -e "s^%buildroot^^" %buildroot%_bindir/nant

mv %buildroot%_prefix/lib*/pkgconfig %buildroot%_datadir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.txt examples
%doc %_datadir/doc/NAnt
%_bindir/%name
%_datadir/NAnt/
%_datadir/pkgconfig/nant.pc

