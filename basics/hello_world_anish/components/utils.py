from pydantic import BaseModel

class PrefillRequest(BaseModel):
    """Request model for prefill stage."""
    text: str
    max_length: int = 100

class PrefillResponse(BaseModel):
    """Response model for prefill stage."""
    prefill_tokens: list[int]
    kv_cache_id: str

class DecodeRequest(BaseModel):
    """Request model for decode stage."""
    kv_cache_id: str
    max_new_tokens: int = 20

class DecodeResponse(BaseModel):
    """Response model for decode stage."""
    generated_text: str
    finished: bool = False

async def check_required_workers(client, min_workers: int, tag: str = "worker", timeout: float = 60):
    """Wait for required number of workers to be ready."""
    import asyncio
    import logging
    logger = logging.getLogger(__name__)
    
    start_time = asyncio.get_event_loop().time()
    while True:
        workers = client.endpoint_ids()
        if len(workers) >= min_workers:
            logger.info(f"{tag}: Required {min_workers} workers are ready")
            break
        
        if asyncio.get_event_loop().time() - start_time > timeout:
            raise TimeoutError(f"{tag}: Timeout waiting for {min_workers} workers")
            
        logger.info(f"{tag}: Waiting for {min_workers} workers, currently have {len(workers)}")
        await asyncio.sleep(1)