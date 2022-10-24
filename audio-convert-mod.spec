Name:              audio-convert-mod
Version:           4.0.0
Release:           4%{?dist}
BuildArch:         noarch
Summary:           A simple audio file converter supporting many formats
Group:             Applications/Multimedia
License:           GPLv2+
URL:               https://github.com/nkudriavtsev/audio-convert-mod/edit/master/audio-convert-mod
Source0:           https://github.com/nkudriavtsev/audio-convert-mod/archive/refs/tags/master.zip
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     desktop-file-utils
BuildRequires:     intltool
BuildRequires:     python3-devel >= 3.6
# For tag support in testbench
BuildRequires:     python3-mutagen

Requires:          python3 >= 3.6
Requires:          python3-notify2
# FOSS encoders, decoders, taggers
Requires:          flac
Requires:          id3lib
Requires:          vorbis-tools
Requires:          wavpack
Requires:          python3-mutagen

%description
audio-convert-mod is a simple audio file converter supporting various formats
via external binaries. It facilitates the batch conversion of audio files
from one format to another at a right-click. Drag-and-drop is also supported.
File tags/metadata are preserved when possible.


%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor fedora\
    --dir ${RPM_BUILD_ROOT}%{_datadir}/applications\
    --delete-original \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/%{name}/
%{_datadir}/applications/fedora-*.desktop

%doc AUTHORS ChangeLog COPYING NEWS INSTALL README TODO


%changelog
* Thu Dec 03 2020 Nicholas Kudriavtsev <nkudriavtsev at gmail.com> 4.0.0-4
- DATADIRNAME correction

* Sat Jul 06 2019 Nicholas Kudriavtsev <nkudriavtsev at gmail.com> 4.0.0-3
- Status is changed from beta to release 
- Fixed progress indicator for codecs without the one

* Sun Jun 30 2019 Nicholas Kudriavtsev <nkudriavtsev at gmail.com> 4.0.0b-2
- Removed libmp4v2 requirement

* Sun Jun 30 2019 Nicholas Kudriavtsev <nkudriavtsev at gmail.com> 4.0.0b
- Update to 4.0.0b (see ChangeLog for details on version changes)

* Mon Dec 7 2009 Stewart Adam <s.adam at diffingo.com> 3.46.0b
- Update to 3.46.0b (see ChangeLog for details on version changes)

* Fri Aug 14 2009 Stewart Adam <s.adam at diffingo.com> 3.46.0a
- Update to 3.46.0a (see ChangeLog for details on version changes)

* Tue Aug 4 2009 Stewart Adam <s.adam at diffingo.com> 3.46.0-1
- Update to 3.46.0 (see ChangeLog for details on version changes)
- Update Source0: and URL: URLs
- Add python-mutagen (build) requirements

* Mon Jan 12 2009 Stewart Adam <s.adam at diffingo.com> 3.45.5-1
- Update to 3.45.5 (see ChangeLog for details on version changes)
- Add BR on autoconf
- Require libmp4v2 for AAC tagging, id3lib for MP3 tagging and notify-python
- Add %%check section

* Sun May 11 2008 Stewart Adam <s.adam at diffingo.com> 3.45.4-1
- Update to 3.45.4 bugfix release

* Fri Apr 25 2008 Stewart Adam <s.adam at diffingo.com> 3.45.3-1
- Update to 3.45.3 (see CHANGELOG file for details on version changes)
- Fixes RH#442502

* Sat Jan 19 2008 Stewart Adam <s.adam at diffingo.com> 3.45.2-3
- Rebuild

* Sat Sep 8 2007 Stewart Adam <s.adam at diffingo.com> 3.45.2-2
- Fix traceback upon calling --help

* Wed Sep 5 2007 Stewart Adam <s.adam at diffingo.com> 3.45.2-1
- Update to 3.45.2 (see CHANGELOG file for details on version changes)
- Fixes RH#277871

* Fri Aug 24 2007 Stewart Adam <s.adam at diffingo.com> 3.45.1-1
- Update to 3.45.1 (see CHANGELOG file for details on version changes)
- Remove uninstall script from package
- Update License tag per guideline changes
- Use sitelib, not sitearch

* Fri Aug 3 2007 Stewart Adam <s.adam at diffingo.com> 3.45.0-1
- Update to 3.45.0 (see CHANGELOG file for details on version changes)

* Tue Jul 31 2007 Stewart Adam <s.adam at diffingo.com> 3.45.0-0.1
- Initial RPM release, 3.45.0 beta
