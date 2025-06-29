#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests (many failures)

Summary:	Service that accepts unix domain socket connections and present the stacktraces
Summary(pl.UTF-8):	Usługa przyjmująca połączenia na gnieździe uniksowym i pokazująca ślady stosu
Name:		python-manhole
# keep 1.8.0 here for python2 support
Version:	1.8.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/manhole/
Source0:	https://files.pythonhosted.org/packages/source/m/manhole/manhole-%{version}.tar.gz
# Source0-md5:	ab4bd604da75a013bab39ce7815727e5
URL:		https://pypi.org/project/manhole/
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-eventlet >= 0.30.2
BuildRequires:	python-gevent >= 21.1.2
BuildRequires:	python-process_tests
BuildRequires:	python-pytest
BuildRequires:	python-requests
#BuildRequires:	python-uwsgi >= 2.0.19.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_py3doc_enhanced_theme
BuildRequires:	sphinx-pdg-2 >= 1.3
%endif
Requires:	python-modules >= 1:2.7
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
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif

%if %{with doc}
sphinx-build-2 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/manhole-cli{,-2}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/manhole-cli-2
%{py_sitescriptdir}/manhole
%{py_sitescriptdir}/manhole.pth
%{py_sitescriptdir}/manhole-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,reference,*.html,*.js}
%endif
