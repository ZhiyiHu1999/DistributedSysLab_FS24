Connection to Agent lost. This is most likely a bug. Internal reason: 'End of file'.
Please refer to the troubleshooting section of the docs:
https://docs.nvidia.com/nsight-systems/UserGuide/index.html#troubleshooting
/dvs/p4/build/sw/devtools/Agora/Rel/QuadD_Main/QuadD/Common/ProtobufComm/Client/ClientProxy.cpp(389): Throw in function QuadDProtobufComm::Endpoint QuadDProtobufComm::Client::ClientProxy::GetLocalEndpoint() const
Dynamic exception type: boost::wrapexcept<QuadDCommon::RuntimeException>
std::exception::what: RuntimeException
[QuadDCommon::tag_message*] = Local Endpoint is not available.

srun: error: ault43: task 3: Exited with exit code 1
srun: error: ault42: task 0: Exited with exit code 1
srun: got SIGCONT
slurmstepd: error: *** STEP 508475.1 ON ault42 CANCELLED AT 2024-09-18T22:08:20 ***
srun: Job step aborted: Waiting up to 32 seconds for job step to finish.
slurmstepd: error: *** JOB 508475 ON ault42 CANCELLED AT 2024-09-18T22:08:20 ***
srun: forcing job termination
