# Multi-Node Dynamo Pipeline Example

This example demonstrates a simple multi-node Dynamo inference pipeline with two services:
1. PrefillService: Handles the initial tokenization and KV cache setup
2. DecodeService: Handles token generation using the KV cache

## Architecture

The pipeline is designed to run on two 8xA100 80GB nodes (16 GPUs total) with InfiniBand enabled, distributing the workload across both nodes:

- PrefillService: 8 replicas (1 GPU each, distributed 4 per node)
- DecodeService: 8 replicas (1 GPU each, distributed 4 per node)

The configuration uses pod anti-affinity to ensure even distribution of services across nodes and InfiniBand for high-speed inter-node communication.

## Prerequisites

1. Kubernetes cluster with:
   - NVIDIA A100 80GB GPUs
   - InfiniBand enabled
   - Dynamo platform components installed in `dynamo-cloud` namespace

2. Required Python packages:
   ```bash
   pip install "ai-dynamo[all]"
   ```

## Deployment Steps

1. Build and push the Dynamo base image:
   ```bash
   ./container/build.sh
   docker tag dynamo:latest-vllm <your-registry>/dynamo-base:latest-vllm
   docker push <your-registry>/dynamo-base:latest-vllm
   ```

2. Deploy the pipeline to Kubernetes:
   ```bash
   export DYNAMO_IMAGE=<your-registry>/dynamo-base:latest-vllm
   kl
   ```

3. Verify the deployment:
   ```bash
   kubectl
   \

## Testing the Pipeline

1. Port-forward the Dynamo API:
   ```bash
   kubectl port-forward svc/dynamo-api -n dynamo-cloud 8080:80
   ```

2. Send a test request:
   ```python
   import asyncio
   from dynamo.sdk import Client

   async def test_pipeline():
       client = Client("http://localhost:8080")
       ns = await client.namespace("dynamo-demo")
       
       # Get prefill service
       prefill = await ns.component("PrefillService").endpoint("process").client()
       
       # Send prefill request
       prefill_resp = await prefill.generate({
           "text": "Hello world",
           "max_length": 100
       })
       
       # Get decode service
       decode = await ns.component("DecodeService").endpoint("process").client()
       
       # Send decode request using KV cache from prefill
       async for token in decode.generate({
           "kv_cache_id": prefill_resp["kv_cache_id"],
           "max_new_tokens": 20
       }):
           print(f"Generated token: {token}")

   asyncio.run(test_pipeline())
   ```

## Monitoring

Monitor the pipeline using:
```bash
kubectl logs -f -l app=prefill-service -n dynamo-playground
kubectl logs -f -l app=decode-service -n dynamo-playground
```