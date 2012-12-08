Summary:	Build tool for Mono and .NET
Name:		nant
Version:	0.91
Release:	2
Epoch:		1
License:	GPL
Group:		Development/Other
Url:		http://nant.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/nant/%{name}-%{version}-src.tar.gz
Patch0:		nant-0.91-no_ndoc.patch
Patch1:		nant-0.90-no_sharpcvslib.patch
Patch2:		nant-0.91-system_log4net.patch
Patch3:		nant-0.90-system_nunit.patch
Patch4:		nant-0.91-system_sharpziplib.patch
#gw required for mono.pc
Requires:	mono-devel
BuildRequires:	mono-devel
BuildRequires:	log4net-devel
BuildArch:	noarch

%description
NAnt is a free .NET build tool. In theory it is kind of like make
without make's wrinkles. In practice it's a lot like Ant.

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
%{_datadir}/pkgconfig/nant.pc

%changelog
* Mon Oct 24 2011 GÃ¶tz Waschk <waschk@mandriva.org> 1:0.91-1mdv2012.0
+ Revision: 705821
- new version
- rediff patches 0,2,4
- fix build
- update file list

* Sun May 01 2011 Funda Wang <fwang@mandriva.org> 1:0.90-3
+ Revision: 661155
- bump rel
- add fedora patch to use system mono libs

* Mon Oct 11 2010 Funda Wang <fwang@mandriva.org> 1:0.90-2mdv2011.0
+ Revision: 584902
- rebuild

* Sat Jul 10 2010 GÃ¶tz Waschk <waschk@mandriva.org> 1:0.90-1mdv2011.0
+ Revision: 550280
- new version
- drop patch
- fix installation
- update file list

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.86-0.beta1.4mdv2010.1
+ Revision: 523405
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:0.86-0.beta1.3mdv2010.0
+ Revision: 426203
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.86-0.beta1.2mdv2009.0
+ Revision: 170442
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Tue Dec 18 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:0.86-0.beta1.2mdv2008.1
+ Revision: 132901
- patch to make it build boo again

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Dec 13 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:0.86-0.beta1.1mdv2008.1
+ Revision: 119367
- new version
- drop patch

* Tue Oct 16 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1:0.85-3mdv2008.1
+ Revision: 98913
- fix build with new mono


* Mon Oct 16 2006 GÃ¶tz Waschk <waschk@mandriva.org> 0.85-2mdv2006.0
+ Revision: 65449
+ Status: not released
- fix startup script

* Mon Oct 16 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1:0.85-1mdv2007.1
+ Revision: 65387
- Import nant

* Mon Oct 16 2006 Götz Waschk <waschk@mandriva.org> 0.85-1mdv2007.1
- unpack patch
- new version

* Sat Jun 03 2006 Götz Waschk <waschk@mandriva.org> 0.85-0.rc4.1mdv2007.0
- new version

* Mon Dec 12 2005 Götz Waschk <waschk@mandriva.org> 0.85-0.rc3.20051203.1mdk
- drop merged patch 0
- fix build
- new version

* Wed Nov 09 2005 Götz Waschk <waschk@mandriva.org> 0.85-0.rc3.4mdk
- fix build
- rebuild for new mono

* Tue May 24 2005 Götz Waschk <waschk@mandriva.org> 1:0.85-0.rc3.3mdk
- fix deps

* Tue May 24 2005 Götz Waschk <waschk@mandriva.org> 0.85-0.rc3.2mdk
- patch to fix build with mono 1.1.7
- requires mono

* Thu Apr 21 2005 Götz Waschk <waschk@mandriva.org> 0.85-0.rc3.1mdk
- fix build
- new version

* Tue Apr 19 2005 Götz Waschk <waschk@mandriva.org> 0.85-0.rc2.2mdk
- Rebuild

* Sat Apr 02 2005 Götz Waschk <waschk@linux-mandrake.com> 1:0.85-0.rc2.1mdk
- new version

* Sat Oct 23 2004 Götz Waschk <waschk@linux-mandrake.com> 0.85-0.20041021.1mdk
- new snapshot
- fix buildrequires

* Fri Oct 22 2004 Götz Waschk <waschk@linux-mandrake.com> 0.85-0.20041020.1mdk
- initial package

