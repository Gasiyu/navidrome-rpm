Name:           navidrome
Version:        0.55.1
Release:        1%{?dist}
Summary:        Modern Music Server and Streamer compatible with Subsonic/Airsonic 

License:        GPLv3
URL:            https://www.navidrome.org/
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz
Source1:        navidrome.service
Source2:        navidrome.sysusers
Source3:        navidrome.toml

Patch0:         0004-Modification-for-Packaging.patch
Patch1:         0006-Specify-Taglib2-Dependency.patch

BuildRequires:  git
BuildRequires:  golang >= 1.21
BuildRequires:  nodejs20
BuildRequires:  nodejs-npm
BuildRequires:  taglib2-devel, zlib-devel, zlib
BuildRequires:  make, gcc, gcc-c++
BuildRequires:  systemd-units
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}

Requires: systemd-units
Requires: zlib
Requires: ffmpeg
Requires: taglib2

%description

Navidrome is an open source web-based music collection server and streamer. 
It gives you freedom to listen to your music collection from any browser 
or mobile device.

%global debug_package %{nil}

%pretrans
echo "Notice from navidrom package maintainer:"
echo
echo "Navidrome have been migrated to `taglib` version 2.0. Since Fedora's `taglib` "
echo "pacakge remains on version 1.31.1 for now and have not decided when and how "
echo "to migrate(Bugzilla 2335641), a package with name `taglib2` is provided
echo "within the copr repository. It adds `-2` suffix to library and is provided
echo "as `libtag-2.so`, which will NOT conflict with current version 1.13's "
echo "`libtag.so`, as well as other packages build with taglib version 1.13 "
echo "from Fedora's main repository. "

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1

%build
export NODE_OPTIONS="--max-old-space-size=8192"
export GOTOOLCHAIN="auto"
export GOSUMDB="sum.golang.org"
make setup GIT_TAG="%{version}-%{release}"
make build GIT_TAG="%{version}-%{release}"

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/%{name}

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/data
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/music
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

install -p -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/%{name}.toml

%pre
%sysusers_create_compat %{SOURCE2}

%files
%license LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.toml
%dir %{_sharedstatedir}/%{name}

%changelog
