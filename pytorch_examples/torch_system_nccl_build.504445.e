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


CMake Error: Cannot open file for write: /users/zhu/pytorch/build/confu-deps/XNNPACK/cmake_install.cmake.tmp2f61b
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/confu-deps/XNNPACK/CTestTestfile.cmake.tmp612bd
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/googletest/cmake_install.cmake.tmpdd69a
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/googletest/CTestTestfile.cmake.tmp00e61
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/googletest/googlemock/cmake_install.cmake.tmp0a0e6
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/googletest/googlemock/CTestTestfile.cmake.tmpcef94
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/googletest/googletest/cmake_install.cmake.tmpb517c
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/googletest/googletest/CTestTestfile.cmake.tmpedb2f
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/benchmark/cmake_install.cmake.tmpf658c
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/benchmark/CTestTestfile.cmake.tmpc2c20
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/benchmark/src/cmake_install.cmake.tmp3000c
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/benchmark/src/CTestTestfile.cmake.tmpbb911
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/fbgemm/cmake_install.cmake.tmp77c8b
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: cannot write to file "/users/zhu/pytorch/build/third_party/fbgemm/CMakeFiles/Export/share/cmake/fbgemm/fbgemmLibraryConfig.cmake": No space left on device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/fbgemm/CTestTestfile.cmake.tmpb4632
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/fbgemm/asmjit/cmake_install.cmake.tmp1b4c0
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: cannot write to file "/users/zhu/pytorch/build/third_party/fbgemm/asmjit/CMakeFiles/Export/lib64/cmake/asmjit/asmjit-config.cmake": No space left on device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/fbgemm/asmjit/CTestTestfile.cmake.tmp077e0
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ittapi/cmake_install.cmake.tmp7ab3e
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ittapi/CTestTestfile.cmake.tmp5ecf2
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/tensorpipe/cmake_install.cmake.tmpfa0d1
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: cannot write to file "/users/zhu/pytorch/build/third_party/tensorpipe/CMakeFiles/Export/share/cmake/Tensorpipe/TensorpipeTargets.cmake": No space left on device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/tensorpipe/CTestTestfile.cmake.tmp8074e
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/tensorpipe/tensorpipe/cmake_install.cmake.tmp274c7
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/tensorpipe/tensorpipe/CTestTestfile.cmake.tmp0fef1
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/tensorpipe/third_party/libuv/cmake_install.cmake.tmpb896d
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/tensorpipe/third_party/libuv/CTestTestfile.cmake.tmpf915b
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/cmake_install.cmake.tmpfcc7d
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/CTestTestfile.cmake.tmpe08f4
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/cmake_install.cmake.tmp67196
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/CTestTestfile.cmake.tmpdbc2a
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/common/cmake_install.cmake.tmp1a76f
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/common/CTestTestfile.cmake.tmp26e33
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/mpi/cmake_install.cmake.tmp1fe33
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/mpi/CTestTestfile.cmake.tmp99b74
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/rendezvous/cmake_install.cmake.tmpf7c5b
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/rendezvous/CTestTestfile.cmake.tmpd1e7f
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/transport/cmake_install.cmake.tmp84e37
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/transport/CTestTestfile.cmake.tmp0642c
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/transport/tcp/cmake_install.cmake.tmp070e9
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/gloo/gloo/transport/tcp/CTestTestfile.cmake.tmp14e0f
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/onnx/cmake_install.cmake.tmp2c7ca
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: cannot write to file "/users/zhu/pytorch/build/third_party/onnx/CMakeFiles/Export/lib64/cmake/ONNX/ONNXTargets.cmake": No space left on device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/onnx/CTestTestfile.cmake.tmp853f5
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/foxi/cmake_install.cmake.tmp504c8
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/foxi/CTestTestfile.cmake.tmp73cf2
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/cmake_install.cmake.tmp872fe
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/CTestTestfile.cmake.tmp45434
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/cmake_install.cmake.tmp03795
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: cannot write to file "/users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/CMakeFiles/Export/lib64/cmake/dnnl/dnnl-targets.cmake": No space left on device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/CTestTestfile.cmake.tmpc081c
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/common/cmake_install.cmake.tmp845ed
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/common/CTestTestfile.cmake.tmp51fa4
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/cpu/cmake_install.cmake.tmpcdd93
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/cpu/CTestTestfile.cmake.tmp1ce43
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/cpu/x64/cmake_install.cmake.tmp9e884
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/cpu/x64/CTestTestfile.cmake.tmpaf7fe
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/cmake_install.cmake.tmp3ddd3
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/CTestTestfile.cmake.tmpeda48
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/interface/cmake_install.cmake.tmpcfdca
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/interface/CTestTestfile.cmake.tmpbe8c3
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/backend/cmake_install.cmake.tmpaa8b7
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/backend/CTestTestfile.cmake.tmp0900e
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/backend/fake/cmake_install.cmake.tmpf79bc
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/backend/fake/CTestTestfile.cmake.tmp58345
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/backend/dnnl/cmake_install.cmake.tmp0cb93
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/backend/dnnl/CTestTestfile.cmake.tmpa244b
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/backend/graph_compiler/cmake_install.cmake.tmpfc027
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/backend/graph_compiler/CTestTestfile.cmake.tmpa1d84
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/utils/cmake_install.cmake.tmp1561c
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/src/graph/utils/CTestTestfile.cmake.tmpdfda2
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/examples/cmake_install.cmake.tmp7787c
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/examples/CTestTestfile.cmake.tmp7d3a7
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/tests/cmake_install.cmake.tmp1bc49
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/ideep/mkl-dnn/tests/CTestTestfile.cmake.tmpbf015
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/fmt/cmake_install.cmake.tmp07f26
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: cannot write to file "/users/zhu/pytorch/build/third_party/fmt/CMakeFiles/Export/lib64/cmake/fmt/fmt-targets.cmake": No space left on device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/fmt/CTestTestfile.cmake.tmp69d12
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/kineto/libkineto/cmake_install.cmake.tmp0f1b4
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: cannot write to file "/users/zhu/pytorch/build/third_party/kineto/libkineto/CMakeFiles/Export/share/cmake/kineto/kinetoLibraryConfig.cmake": No space left on device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/kineto/libkineto/CTestTestfile.cmake.tmpb1b35
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/kineto/libkineto/third_party/dynolog/dynolog/src/ipcfabric/cmake_install.cmake.tmp88346
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/third_party/kineto/libkineto/third_party/dynolog/dynolog/src/ipcfabric/CTestTestfile.cmake.tmp2e12a
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/cmake_install.cmake.tmp94461
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/CTestTestfile.cmake.tmpbc0e4
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/test/cmake_install.cmake.tmp004bf
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/test/CTestTestfile.cmake.tmp028e7
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/benchmark/cmake_install.cmake.tmp127bd
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/benchmark/CTestTestfile.cmake.tmp2e4bd
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/cuda/cmake_install.cmake.tmp86d2b
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/cuda/CTestTestfile.cmake.tmpe7a13
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/cuda/test/cmake_install.cmake.tmp6d969
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/c10/cuda/test/CTestTestfile.cmake.tmp6b6e8
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/cmake_install.cmake.tmpaf5cf
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/CTestTestfile.cmake.tmp0356c
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/cmake_install.cmake.tmp7ad00
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/CTestTestfile.cmake.tmp8a042
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/THC/cmake_install.cmake.tmpd5b3f
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/THC/CTestTestfile.cmake.tmpebb50
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/ATen/cmake_install.cmake.tmp301dc
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/ATen/CTestTestfile.cmake.tmp52f92
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/ATen/quantized/cmake_install.cmake.tmp0caa3
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/ATen/quantized/CTestTestfile.cmake.tmp9e669
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/ATen/nnapi/cmake_install.cmake.tmp1d757
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/ATen/nnapi/CTestTestfile.cmake.tmp0232d
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/sleef/cmake_install.cmake.tmpef097
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: cannot write to file "/users/zhu/pytorch/build/sleef/CMakeFiles/Export/lib64/cmake/sleef/sleefTargets.cmake": No space left on device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/sleef/CTestTestfile.cmake.tmp41720
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/sleef/src/cmake_install.cmake.tmp5c160
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/sleef/src/CTestTestfile.cmake.tmp1fa35
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/sleef/src/libm/cmake_install.cmake.tmp91b76
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/sleef/src/libm/CTestTestfile.cmake.tmp07140
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/sleef/src/common/cmake_install.cmake.tmp42c65
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/sleef/src/common/CTestTestfile.cmake.tmp945b1
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/ATen/test/cmake_install.cmake.tmp35125
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/aten/src/ATen/test/CTestTestfile.cmake.tmp05a77
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/core/cmake_install.cmake.tmpfa667
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/core/CTestTestfile.cmake.tmp25007
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/serialize/cmake_install.cmake.tmp256ee
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/serialize/CTestTestfile.cmake.tmp4fe91
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/utils/cmake_install.cmake.tmpf6811
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/utils/CTestTestfile.cmake.tmpe1fcb
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_edge_op_registration/cmake_install.cmake.tmpf898e
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_edge_op_registration/CTestTestfile.cmake.tmp420eb
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_jit/cmake_install.cmake.tmp4e162
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_jit/CTestTestfile.cmake.tmpbf27d
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_tensorexpr/cmake_install.cmake.tmp27043
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_tensorexpr/CTestTestfile.cmake.tmp4e6a3
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_cpp_c10d/cmake_install.cmake.tmpc067a
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_cpp_c10d/CTestTestfile.cmake.tmp26590
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/dist_autograd/cmake_install.cmake.tmp00425
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/dist_autograd/CTestTestfile.cmake.tmp34477
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_cpp_rpc/cmake_install.cmake.tmpead78
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_cpp_rpc/CTestTestfile.cmake.tmp5213a
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_api/cmake_install.cmake.tmp5c825
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_api/CTestTestfile.cmake.tmpab302
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_lazy/cmake_install.cmake.tmp5c781
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/test_lazy/CTestTestfile.cmake.tmp3968d
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/torch/cmake_install.cmake.tmp545ec
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/torch/CTestTestfile.cmake.tmp98fdd
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/torch/lib/libshm/cmake_install.cmake.tmpe58b6
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/caffe2/torch/lib/libshm/CTestTestfile.cmake.tmp97748
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/functorch/cmake_install.cmake.tmp566f0
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: Cannot open file for write: /users/zhu/pytorch/build/functorch/CTestTestfile.cmake.tmpb35ac
CMake Error: : System Error: Inappropriate ioctl for device
CMake Error: cannot write to file "/users/zhu/pytorch/build/third_party/benchmark/benchmarkTargets.cmake": No space left on device
CMake Generate step failed.  Build files cannot be regenerated correctly.
