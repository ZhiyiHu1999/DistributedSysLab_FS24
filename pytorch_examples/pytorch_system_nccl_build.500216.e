CMake Warning at cmake/public/cuda.cmake:140 (message):
  Failed to compute shorthash for libnvrtc.so
Call Stack (most recent call first):
  cmake/Dependencies.cmake:44 (include)
  CMakeLists.txt:863 (include)


CMake Warning at cmake/public/cuda.cmake:214 (message):
  Cannot find cuDNN library.  Turning the option off
Call Stack (most recent call first):
  cmake/Dependencies.cmake:44 (include)
  CMakeLists.txt:863 (include)


CMake Warning at cmake/public/cuda.cmake:239 (message):
  Cannot find cuSPARSELt library.  Turning the option off
Call Stack (most recent call first):
  cmake/Dependencies.cmake:44 (include)
  CMakeLists.txt:863 (include)


CMake Warning at cmake/public/cuda.cmake:255 (message):
  Cannot find CUDSS library.  Turning the option off
Call Stack (most recent call first):
  cmake/Dependencies.cmake:44 (include)
  CMakeLists.txt:863 (include)


CMake Warning at cmake/Dependencies.cmake:95 (message):
  Not compiling with XPU.  Could NOT find SYCL.Suppress this warning with
  -DUSE_XPU=OFF.
Call Stack (most recent call first):
  CMakeLists.txt:863 (include)


CMake Warning at cmake/Dependencies.cmake:208 (message):
  MKL could not be found.  Defaulting to Eigen
Call Stack (most recent call first):
  CMakeLists.txt:863 (include)


CMake Warning at cmake/Dependencies.cmake:250 (message):
  Preferred BLAS (MKL) cannot be found, now searching for a general BLAS
  library
Call Stack (most recent call first):
  CMakeLists.txt:863 (include)


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
CMake Warning at cmake/Dependencies.cmake:956 (message):
  Not compiling with MPI.  Suppress this warning with -DUSE_MPI=OFF
Call Stack (most recent call first):
  CMakeLists.txt:863 (include)


CMake Error at cmake/public/utils.cmake:302 (message):
   Could not detect ROCm arch for GPUs on machine. Result: 'No such file or directory'
Call Stack (most recent call first):
  cmake/public/LoadHIP.cmake:26 (torch_hip_get_arch_list)
  cmake/Dependencies.cmake:1042 (include)
  CMakeLists.txt:863 (include)


