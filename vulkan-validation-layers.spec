%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define tarname Vulkan-ValidationLayers
Name:           vulkan-validation-layers
Version:        1.2.151
Release:        1
Summary:        Vulkan validation layers

License:        ASL 2.0
URL:            https://github.com/KhronosGroup/Vulkan-ValidationLayers
Source0:        https://github.com/KhronosGroup/Vulkan-ValidationLayers/archive/v%{version}/%{tarname}-%{version}.tar.gz
#Patch0:         fix_shared.patch

BuildRequires:  cmake
BuildRequires:  glslang-devel
BuildRequires:  ninja
BuildRequires:  python-devel
BuildRequires:  libspirv-tools-devel
BuildRequires:  spirv-headers
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xcb)

%description
Vulkan validation layers

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       vulkan-headers

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{tarname}-%{version}


%build
export CC=gcc
export CXX=g++

# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')


%cmake -DCMAKE_BUILD_TYPE=Release \
        -DGLSLANG_INSTALL_DIR=%{_prefix} \
        -DBUILD_LAYER_SUPPORT_FILES:BOOL=ON \
        -DSPIRV_HEADERS_INSTALL_DIR=%{_includedir}/spirv \
        -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir}/vulkan/
%make_build


%install
%make_install -C build


%ldconfig_scriptlets


%files
%license LICENSE.txt
%doc README.md CONTRIBUTING.md
%{_datadir}/vulkan/explicit_layer.d/*.json
%{_libdir}/libVkLayer_*.so

%files devel
%{_includedir}/vulkan/
