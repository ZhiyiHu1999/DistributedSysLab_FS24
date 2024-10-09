HEAD is now at ee1b680438 [Doc] Fix rendering of the unicode characters (#134695)
CMake Warning at cmake/public/cuda.cmake:219 (message):
  Cannot find cuDNN library.  Turning the option off
Call Stack (most recent call first):
  cmake/Dependencies.cmake:43 (include)
  CMakeLists.txt:853 (include)


CMake Warning at cmake/public/cuda.cmake:244 (message):
  Cannot find cuSPARSELt library.  Turning the option off
Call Stack (most recent call first):
  cmake/Dependencies.cmake:43 (include)
  CMakeLists.txt:853 (include)


CMake Warning at cmake/Dependencies.cmake:201 (message):
  MKL could not be found.  Defaulting to Eigen
Call Stack (most recent call first):
  CMakeLists.txt:853 (include)


CMake Warning at cmake/Dependencies.cmake:243 (message):
  Preferred BLAS (MKL) cannot be found, now searching for a general BLAS
  library
Call Stack (most recent call first):
  CMakeLists.txt:853 (include)


CMake Warning (dev) at /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cmake-3.21.3-zt24jfeuemvwweacziyho6ccdsdn2w4s/share/cmake-3.21/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (OpenMP_C)
  does not match the name of the calling package (OpenMP).  This can lead to
  problems in calling code that expects `find_package` result variables
  (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  cmake/Modules/FindOpenMP.cmake:590 (find_package_handle_standard_args)
  third_party/fbgemm/CMakeLists.txt:136 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cmake-3.21.3-zt24jfeuemvwweacziyho6ccdsdn2w4s/share/cmake-3.21/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (OpenMP_CXX)
  does not match the name of the calling package (OpenMP).  This can lead to
  problems in calling code that expects `find_package` result variables
  (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  cmake/Modules/FindOpenMP.cmake:590 (find_package_handle_standard_args)
  third_party/fbgemm/CMakeLists.txt:136 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning at third_party/fbgemm/CMakeLists.txt:138 (message):
  OpenMP found! OpenMP_C_INCLUDE_DIRS =


CMake Warning at third_party/fbgemm/CMakeLists.txt:232 (message):
  ==========


CMake Warning at third_party/fbgemm/CMakeLists.txt:233 (message):
  CMAKE_BUILD_TYPE = Release


CMake Warning at third_party/fbgemm/CMakeLists.txt:234 (message):
  CMAKE_CXX_FLAGS_DEBUG is -g


CMake Warning at third_party/fbgemm/CMakeLists.txt:235 (message):
  CMAKE_CXX_FLAGS_RELEASE is -O3 -DNDEBUG


CMake Warning at third_party/fbgemm/CMakeLists.txt:236 (message):
  ==========


** AsmJit Summary **
   ASMJIT_DIR=/users/zhu/pytorch/third_party/fbgemm/third_party/asmjit
   ASMJIT_TEST=FALSE
   ASMJIT_TARGET_TYPE=STATIC
   ASMJIT_DEPS=pthread;rt
   ASMJIT_LIBS=asmjit;pthread;rt
   ASMJIT_CFLAGS=-DASMJIT_STATIC
   ASMJIT_PRIVATE_CFLAGS=-Wall;-Wextra;-Wconversion;-fno-math-errno;-fno-threadsafe-statics;-fno-semantic-interposition;-DASMJIT_STATIC
   ASMJIT_PRIVATE_CFLAGS_DBG=
   ASMJIT_PRIVATE_CFLAGS_REL=-O2;-fmerge-all-constants;-fno-enforce-eh-specs
CMake Warning at cmake/Dependencies.cmake:944 (message):
  Not compiling with MPI.  Suppress this warning with -DUSE_MPI=OFF
Call Stack (most recent call first):
  CMakeLists.txt:853 (include)


CMake Warning (dev) at third_party/tensorpipe/tensorpipe/CMakeLists.txt:237 (find_package):
  Policy CMP0074 is not set: find_package uses <PackageName>_ROOT variables.
  Run "cmake --help-policy CMP0074" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.

  Environment variable CUDA_ROOT is set to:

    /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cuda-11.8.0-fjdnxm6yggxxp75sb62xrxxmeg4s24ml

  For compatibility, CMake is ignoring the variable.
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at third_party/gloo/CMakeLists.txt:21 (option):
  Policy CMP0077 is not set: option() honors normal variables.  Run "cmake
  --help-policy CMP0077" for policy details.  Use the cmake_policy command to
  set the policy and suppress this warning.

  For compatibility with older versions of CMake, option is clearing the
  normal variable 'BUILD_BENCHMARK'.
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at third_party/gloo/cmake/Cuda.cmake:109 (find_package):
  Policy CMP0074 is not set: find_package uses <PackageName>_ROOT variables.
  Run "cmake --help-policy CMP0074" for policy details.  Use the cmake_policy
  command to set the policy and suppress this warning.

  CMake variable CUDAToolkit_ROOT is set to:

    /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cuda-11.8.0-fjdnxm6yggxxp75sb62xrxxmeg4s24ml

  For compatibility, CMake is ignoring the variable.
Call Stack (most recent call first):
  third_party/gloo/cmake/Dependencies.cmake:115 (include)
  third_party/gloo/CMakeLists.txt:111 (include)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cmake-3.21.3-zt24jfeuemvwweacziyho6ccdsdn2w4s/share/cmake-3.21/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (NCCL) does
  not match the name of the calling package (nccl).  This can lead to
  problems in calling code that expects `find_package` result variables
  (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  third_party/gloo/cmake/Modules/Findnccl.cmake:45 (find_package_handle_standard_args)
  third_party/gloo/cmake/Dependencies.cmake:128 (find_package)
  third_party/gloo/CMakeLists.txt:111 (include)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning at third_party/gloo/cmake/Dependencies.cmake:133 (message):
  Not compiling with NCCL support.  Suppress this warning with
  -DUSE_NCCL=OFF.
Call Stack (most recent call first):
  third_party/gloo/CMakeLists.txt:111 (include)


Generated: /users/zhu/pytorch/build/third_party/onnx/onnx/onnx_onnx_torch-ml.proto
Generated: /users/zhu/pytorch/build/third_party/onnx/onnx/onnx-operators_onnx_torch-ml.proto
Generated: /users/zhu/pytorch/build/third_party/onnx/onnx/onnx-data_onnx_torch.proto
disabling ROCM because NOT USE_ROCM is set
-- Will build oneDNN Graph
CMake Warning (dev) at /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cmake-3.21.3-zt24jfeuemvwweacziyho6ccdsdn2w4s/share/cmake-3.21/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (OpenMP_C)
  does not match the name of the calling package (OpenMP).  This can lead to
  problems in calling code that expects `find_package` result variables
  (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  cmake/Modules/FindOpenMP.cmake:590 (find_package_handle_standard_args)
  third_party/ideep/mkl-dnn/cmake/OpenMP.cmake:55 (find_package)
  third_party/ideep/mkl-dnn/CMakeLists.txt:119 (include)
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cmake-3.21.3-zt24jfeuemvwweacziyho6ccdsdn2w4s/share/cmake-3.21/Modules/FindPackageHandleStandardArgs.cmake:438 (message):
  The package name passed to `find_package_handle_standard_args` (OpenMP_CXX)
  does not match the name of the calling package (OpenMP).  This can lead to
  problems in calling code that expects `find_package` result variables
  (e.g., `_FOUND`) to follow a certain pattern.
Call Stack (most recent call first):
  cmake/Modules/FindOpenMP.cmake:590 (find_package_handle_standard_args)
  third_party/ideep/mkl-dnn/cmake/OpenMP.cmake:55 (find_package)
  third_party/ideep/mkl-dnn/CMakeLists.txt:119 (include)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- <FindZVECTOR>
-- ZVECTOR flags were NOT set.
-- </FindZVECTOR>
INFO ROCM_SOURCE_DIR = 
INFO CUPTI_INCLUDE_DIR = /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cuda-11.8.0-fjdnxm6yggxxp75sb62xrxxmeg4s24ml/extras/CUPTI/include
INFO ROCTRACER_INCLUDE_DIR = /include/roctracer
INFO DYNOLOG_INCLUDE_DIR = /users/zhu/pytorch/third_party/kineto/libkineto/third_party/dynolog/
INFO IPCFABRIC_INCLUDE_DIR = /users/zhu/pytorch/third_party/kineto/libkineto/third_party/dynolog//dynolog/src/ipcfabric/
   Target system: Linux-4.18.0-348.12.2.el8_5.x86_64
   Target processor: x86_64
   Host system: Linux-4.18.0-348.12.2.el8_5.x86_64
   Host processor: x86_64
   Detected C compiler: GNU @ /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/gcc-10.2.0-fqf4ze2mfclmx6e7ehrjckznpoqnevmi/bin/gcc
   CMake: 3.21.3
   Make program: /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/ninja-1.10.2-wdynop4omsowbsqvfv6gvco6dxqkdvgh/bin/ninja-build
AT_INSTALL_INCLUDE_DIR include/ATen/core
core header install: /users/zhu/pytorch/build/aten/src/ATen/core/TensorBody.h
core header install: /users/zhu/pytorch/build/aten/src/ATen/core/aten_interned_strings.h
core header install: /users/zhu/pytorch/build/aten/src/ATen/core/enum_tag.h
CMake Warning at CMakeLists.txt:1282 (message):
  Generated cmake files are only fully tested if one builds with system glog,
  gflags, and protobuf.  Other settings may generate files that are not well
  tested.


error: can't create or remove files in install directory

The following error occurred while trying to add or remove files in the
installation directory:

    [Errno 13] Permission denied: '/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/python-3.8.12-dhpibk3qutj5jasu4ygzx5lqfctlhcdv/lib/python3.8/site-packages/test-easy-install-963842.write-test'

The installation directory you specified (via --install-dir, --prefix, or
the distutils default setting) was:

    /apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/python-3.8.12-dhpibk3qutj5jasu4ygzx5lqfctlhcdv/lib/python3.8/site-packages/

Perhaps your account does not have write access to this directory?  If the
installation directory is a system-owned directory, you may need to sign in
as the administrator or "root" account.  If you do not have administrative
access to this machine, you may wish to choose a different installation
directory, preferably one that is listed in your PYTHONPATH environment
variable.

For information on other options, you may wish to consult the
documentation at:

  https://setuptools.readthedocs.io/en/latest/easy_install.html

Please make the appropriate changes for your system and try again.

