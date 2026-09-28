#!/bin/bash

export gRPC_DIR=${HOME}/vPSIJ_util/grpc
mkdir -p $gRPC_DIR
cp src/executor_pb2.py $gRPC_DIR/
cp src/executor_pb2_grpc.py $gRPC_DIR/
cp src/job_rpc_client.py $gRPC_DIR/