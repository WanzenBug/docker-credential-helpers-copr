# Generated by go2rpm 1.14.0
%bcond check 1
%bcond bootstrap 0

%global debug_package %{nil}
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^golang\\(.*\\)$

# https://github.com/moby/buildkit
%global goipath         github.com/docker/docker-credential-helpers
%global tag             v0.8.2
Version:                0.8.2

%gometa -L -f

%global common_description %{expand:
Programs to keep Docker login credentials safe by storing in platform keystores.}

%global golicenses      LICENSE
%global godocs          README.md

Name:           docker-credential-helpers
Release:        %autorelease
Summary:        Concurrent, cache-efficient, and Dockerfile-agnostic builder toolkit

License:        BSD-3-Clause AND MIT
URL:            %{gourl}
Source0:        %{gosource}
Source1:        go-vendor-tools.toml

BuildRequires:  go-vendor-tools
BuildRequires:  libsecret-devel

%description %{common_description}

%gopkg

%prep
%goprep -A -k
%autopatch -p1

%generate_buildrequires
%go_vendor_license_buildrequires -c %{S:1}

%build
GO_LDFLAGS="-X %{goipath}/credentials.Version=%{version} -X %{goipath}/credentials.Package=%{goipath}"
for cmd in secretservice pass ; do
  %gobuild -o %{gobuilddir}/bin/docker-credential-$cmd %{goipath}/$cmd/cmd
done

%install
%go_vendor_license_install -c %{S:1}
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/* %{buildroot}%{_bindir}/

%if %{with check}
%check
%go_vendor_license_check -c %{S:1}
%endif

%files -f %{go_vendor_license_filelist}
%doc README.md
%{_bindir}/docker-credential-pass
%{_bindir}/docker-credential-secretservice

%changelog
%autochangelog
