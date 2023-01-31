Name:           navidrome
Version:        0.49.0
Release:        2%{?dist}
Summary:        Modern Music Server and Streamer compatible with Subsonic/Airsonic 

License:        GPLv3
URL:            https://www.navidrome.org/
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz
Source1:        navidrome.service
Source2:        navidrome.sysusers
Source3:        navidrome.toml

# https://github.com/navidrome/navidrome/pull/1767
#Patch0:         0002-Fix-Build-on-F36.patch
Patch0:         0003-Verbose-Build-Info.patch

BuildRequires:  git
BuildRequires:  golang >= 1.18
BuildRequires:  nodejs >= 16.0
BuildRequires:  npm
BuildRequires:  taglib-devel, zlib-devel, zlib
BuildRequires:  make, gcc, gcc-c++
BuildRequires:  systemd-units
BuildRequires:  systemd-rpm-macros

Requires: systemd-units
Requires: zlib
Requires: ffmpeg

%description

Navidrome is an open source web-based music collection server and streamer. 
It gives you freedom to listen to your music collection from any browser 
or mobile device.

%global debug_package %{nil}

%prep
%setup -q
%patch0 -p1

%build
export NODE_OPTIONS="--max-old-space-size=8192"
make setup
make buildall

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sharedstatedir}/%{name}
install -d %{buildroot}%{_sharedstatedir}/%{name}/data
install -d %{buildroot}%{_sharedstatedir}/%{name}/music

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
install -p -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/%{name}.toml

%pre
%sysusers_create_compat %{SOURCE2}
chown navidrome:navidrome %{_sharedstatedir}/%{name}
chown navidrome:navidrome %{_sharedstatedir}/%{name}/data
chown navidrome:navidrome %{_sharedstatedir}/%{name}/music

%files
%license LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.toml

%changelog
