Summary:	Build tool for Mono and .NET
Name:		nant
Epoch:		1
Version:	0.91
Release:	5
License:	GPLv2
Group:		Development/Other
Url:		http://nant.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/nant/%{name}-%{version}-src.tar.gz
Patch0:		nant-0.91-no_ndoc.patch
Patch1:		nant-0.90-no_sharpcvslib.patch
Patch2:		nant-0.91-system_log4net.patch
Patch3:		nant-0.90-system_nunit.patch
Patch4:		nant-0.91-system_sharpziplib.patch
BuildArch:	noarch
BuildRequires:	pkgconfig(log4net)
BuildRequires:	pkgconfig(mono)

%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.

%package devel
Summary:	The pkgconfig for %{name}
Group:		Development/Other
Requires:	%{name} = %{EVRD}

%description devel
The pkgconfig for %{name}.

%prep
%setup -q
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
make prefix=%{_prefix}

%install
%makeinstall
perl -pi -e "s^%{buildroot}^^" %{buildroot}%{_bindir}/%{name}
find examples -name \*.dll -o -name \*.exe|xargs rm -f
rm -rf %{buildroot}%{_datadir}/NAnt/doc

# gw fix paths in the nant script
perl -pi -e "s^%{buildroot}^^" %{buildroot}%{_bindir}/nant

mv %{buildroot}%{_prefix}/lib*/pkgconfig %{buildroot}%{_datadir}

%files
%doc README.txt examples
%doc %{_datadir}/doc/NAnt
%{_bindir}/%{name}
%{_datadir}/NAnt/

%files devel
%{_datadir}/pkgconfig/nant.pc

