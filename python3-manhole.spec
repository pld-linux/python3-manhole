#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests (many failures)

Summary:	Service that accepts unix domain socket connections and present the stacktraces
Summary(pl.UTF-8):	Usługa przyjmująca połączenia na gnieździe uniksowym i pokazująca ślady stosu
Name:		python3-manhole
Version:	1.8.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/manhole/
Source0:	https://files.pythonhosted.org/packages/source/m/manhole/manhole-%{version}.tar.gz
# Source0-md5:	f464d2b4f7772a513ce2db2176d90cb6
URL:		https://pypi.org/project/manhole/
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools >= 1:64
%if %{with tests}
BuildRequires:	python3-eventlet >= 0.36.1
BuildRequires:	python3-gevent >= 24.2.1
BuildRequires:	python3-process_tests
BuildRequires:	python3-pytest
BuildRequires:	python3-requests
#BuildRequires:	python3-uwsgi >= 2.0.26
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Manhole is in-process service that will accept unix domain socket
connections and present the stacktraces for all threads and an
interactive prompt.

%description -l pl.UTF-8
Manhole to usługa wewnątrz procesu przyjmująca połączenia po gnieździe
uniksowym i przedstawiająca ślady stosu dla wszystkich wątków oraz
interaktywną zachętę.

%package apidocs
Summary:	API documentation for Python manhole module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona manhole
Group:		Documentation

%description apidocs
API documentation for Python manhole module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona manhole.

%prep
%setup -q -n manhole-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/manhole-cli{,-3}
ln -sf manhole-cli-3 $RPM_BUILD_ROOT%{_bindir}/manhole-cli

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/manhole-cli
%attr(755,root,root) %{_bindir}/manhole-cli-3
%{py3_sitescriptdir}/manhole
%{py3_sitescriptdir}/manhole.pth
%{py3_sitescriptdir}/manhole-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,reference,*.html,*.js}
%endif
