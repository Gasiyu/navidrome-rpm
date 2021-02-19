Name:           navidrome
Version:        0.40.0
Release:        1%{?dist}
Summary:        Modern Music Server and Streamer compatible with Subsonic/Airsonic 

License:        GPLv3
URL:            https://www.navidrome.org/
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz
Source1:        navidrome.service
Source2:        navidrome.sysusers

BuildRequires:  git
BuildRequires:  golang >= 1.15
BuildRequires:  nodejs >= 14.0
BuildRequires:  npm
BuildRequires:  taglib-devel
BuildRequires:  make
BuildRequires:  systemd-units
BuildRequires:  systemd-rpm-macros

Requires: systemd-units
Requires: ffmpeg

%description

Navidrome is an open source web-based music collection server and streamer. 
It gives you freedom to listen to your music collection from any browser 
or mobile device.

%global debug_package %{nil}

%prep
%setup

%build
export NODE_OPTIONS="--max-old-space-size=8192"
make setup
make buildall

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sharedstatedir}/%{name}
install -d %{buildroot}%{_unitdir}

install -p -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

%pre
%sysusers_create_compat %{SOURCE2}

%files
%license LICENSE
%dir %{buildroot}%{_sharedstatedir}/%{name}
%config(noreplace) %{buildroot}%{_sharedstatedir}/%{name}/navidrome.toml
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf

%changelog