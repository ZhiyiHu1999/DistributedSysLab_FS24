#include <stdio.h>
#include "cuda_runtime.h"
#include "nccl.h"
#include "mpi.h"
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>

#define MPICHECK(cmd) do {                          \
  int e = cmd;                                      \
  if( e != MPI_SUCCESS ) {                          \
    printf("Failed: MPI error %s:%d '%d'\n",        \
        __FILE__,__LINE__, e);   \
    exit(EXIT_FAILURE);                             \
  }                                                 \
} while(0)


#define CUDACHECK(cmd) do {                         \
  cudaError_t e = cmd;                              \
  if( e != cudaSuccess ) {                          \
    printf("Failed: Cuda error %s:%d '%s'\n",             \
        __FILE__,__LINE__,cudaGetErrorString(e));   \
    exit(EXIT_FAILURE);                             \
  }                                                 \
} while(0)


#define NCCLCHECK(cmd) do {                         \
  ncclResult_t r = cmd;                             \
  if (r!= ncclSuccess) {                            \
    printf("Failed, NCCL error %s:%d '%s'\n",             \
        __FILE__,__LINE__,ncclGetErrorString(r));   \
    exit(EXIT_FAILURE);                             \
  }                                                 \
} while(0)


static uint64_t getHostHash(const char* string) {
  // Based on DJB2a, result = result * 33 ^ char
  uint64_t result = 5381;
  for (int c = 0; string[c] != '\0'; c++){
    result = ((result << 5) + result) ^ string[c];
  }
  return result;
}


static void getHostName(char* hostname, int maxlen) {
  gethostname(hostname, maxlen);
  for (int i=0; i< maxlen; i++) {
    if (hostname[i] == '.') {
        hostname[i] = '\0';
        return;
    }
  }
}


int main(int argc, char* argv[])
{
  int size = 2*1024*1024;
  // int size = 32*1024*1024;


  int myRank, nRanks, localRank = 0;


  //initializing MPI
  MPICHECK(MPI_Init(&argc, &argv));
  MPICHECK(MPI_Comm_rank(MPI_COMM_WORLD, &myRank));
  MPICHECK(MPI_Comm_size(MPI_COMM_WORLD, &nRanks));


  //calculating localRank based on hostname which is used in selecting a GPU
  uint64_t hostHashs[nRanks];
  char hostname[1024];
  getHostName(hostname, 1024);
  hostHashs[myRank] = getHostHash(hostname);
  MPICHECK(MPI_Allgather(MPI_IN_PLACE, 0, MPI_DATATYPE_NULL, hostHashs, sizeof(uint64_t), MPI_BYTE, MPI_COMM_WORLD));
  for (int p=0; p<nRanks; p++) {
     if (p == myRank) break;
     if (hostHashs[p] == hostHashs[myRank]) localRank++;
  }

  printf("The local rank is: %d\n", localRank);


  ncclUniqueId id_0;
  ncclUniqueId id_1;
  ncclComm_t comm_0;
  ncclComm_t comm_1;
  float *sendbuff_0, *recvbuff_0;
  float *sendbuff_1, *recvbuff_1;
  cudaStream_t s_0;
  cudaStream_t s_1;


  //get NCCL unique ID at rank 0 and broadcast it to all others
  if (myRank == 0) ncclGetUniqueId(&id_0);
  if (myRank == 0) ncclGetUniqueId(&id_1);
  MPICHECK(MPI_Bcast((void *)&id_0, sizeof(id_0), MPI_BYTE, 0, MPI_COMM_WORLD));
  MPICHECK(MPI_Bcast((void *)&id_1, sizeof(id_1), MPI_BYTE, 0, MPI_COMM_WORLD));


  //picking a GPU based on localRank, allocate device buffers
  CUDACHECK(cudaSetDevice(localRank));
  CUDACHECK(cudaMalloc(&sendbuff_0, size * sizeof(float)));
  CUDACHECK(cudaMalloc(&recvbuff_0, size * sizeof(float)));
  CUDACHECK(cudaMalloc(&sendbuff_1, size * sizeof(float)));
  CUDACHECK(cudaMalloc(&recvbuff_1, size * sizeof(float)));
  
  CUDACHECK(cudaMemset(sendbuff_0, 0, size * sizeof(float)));
  CUDACHECK(cudaMemset(recvbuff_0, 0, size * sizeof(float)));
  CUDACHECK(cudaMemset(sendbuff_1, 0, size * sizeof(float)));
  CUDACHECK(cudaMemset(recvbuff_1, 0, size * sizeof(float)));
 
  CUDACHECK(cudaStreamCreate(&s_0));
  CUDACHECK(cudaStreamCreate(&s_1));


  //initializing NCCL
  NCCLCHECK(ncclCommInitRank(&comm_0, nRanks, id_0, myRank));
  NCCLCHECK(ncclCommInitRank(&comm_1, nRanks, id_1, myRank));


  //communicating using NCCL
  NCCLCHECK(ncclAllReduce((const void*)sendbuff_0, (void*)recvbuff_0, size, ncclFloat, ncclSum, comm_0, s_0));
  // sleep(2);
  CUDACHECK(cudaStreamSynchronize(s_0));

  printf("[MPI Rank %d] Success \n", myRank);

  NCCLCHECK(ncclAllReduce((const void*)sendbuff_1, (void*)recvbuff_1, size, ncclFloat, ncclSum, comm_1, s_1));

  // //completing NCCL operation by synchronizing on the CUDA stream
  // CUDACHECK(cudaStreamSynchronize(s_0));
  CUDACHECK(cudaStreamSynchronize(s_1));
  printf("[Rank MPI %d] Success \n", myRank);


  //free device buffers
  CUDACHECK(cudaFree(sendbuff_0));
  CUDACHECK(cudaFree(recvbuff_0));
  CUDACHECK(cudaFree(sendbuff_1));
  CUDACHECK(cudaFree(recvbuff_1));

  //finalizing NCCL
  ncclCommDestroy(comm_0);
  ncclCommDestroy(comm_1);


  //finalizing MPI
  MPICHECK(MPI_Finalize());


  // printf("[MPI Rank %d] Success \n", myRank);
  
  return 0;
}
