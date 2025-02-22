%define		debug_package %{nil}

Name:		grub-btrfs
Version:	4.13
Release:	1
Source0:	https://github.com/Antynea/grub-btrfs/archive/%{version}/%{name}-%{version}.tar.gz
Summary:	Include btrfs snapshots at boot menu for GRUB
URL:		https://github.com/Antynea/grub-btrfs
License:	GPL-3.0
Group:		System

BuildArch:      noarch
BuildRequires:	bash
BuildRequires:  bzip2

Requires:		btrfs-progs
Requires:		grub2
Requires:		util-linux
Requires:		grep

%description
grub-btrfs is a simple script that automatically includes btrfs snapshots in the GRUB boot menu,
allowing you to select snapshots for booting in case of system failures.

%prep
%autosetup -p1

%build
mkdir   TEMP_DIR
cp manpages/grub-btrfs.8.man TEMP_DIR/grub-btrfs.8
bzip2 TEMP_DIR/grub-btrfs.8 
cp manpages/grub-btrfsd.8.man TEMP_DIR/grub-btrfsd.8
bzip2 TEMP_DIR/grub-btrfsd.8 

%install
install -Dm755 -t "%{buildroot}%{_sysconfdir}/grub.d/" 41_snapshots-btrfs
install -Dm644 -t "%{buildroot}%{_sysconfdir}/default/grub-btrfs/" config
install -Dm755 -t "%{buildroot}%{_bindir}/" grub-btrfsd
install -Dm644 -t "%{buildroot}%{_prefix}/lib/systemd/system/" grub-btrfsd.service
install -Dm644 -t "%{buildroot}%{_mandir}/man8" "TEMP_DIR/grub-btrfs.8.bz2"
install -Dm644 -t "%{buildroot}%{_mandir}/man8" "TEMP_DIR/grub-btrfsd.8.bz2"


%post
if [ "$(stat -c %d:%i /)" = "$(stat -c %d:%i /proc/1/root/.)" ]; then
	%{_sbindir}/update-grub2
fi

%files
%license LICENSE
%doc README.md initramfs/readme.md
%{_sysconfdir}/grub.d/41_snapshots-btrfs
%{_sysconfdir}/default/grub-btrfs/config
%{_bindir}/grub-btrfsd
%{_mandir}/man8/grub-btrf*.8.zst
%{_prefix}/lib/systemd/system/grub-btrfsd.service

