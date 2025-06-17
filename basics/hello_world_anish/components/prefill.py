import logging
import uuid
from typing import AsyncGenerator

from dynamo.sdk import DYNAMO_IMAGE, service, endpoint

from .utils import PrefillRequest, PrefillResponse

logger = logging.getLogger(__name__)

@service(
    dynamo={"namespace": "dynamo-demo"},
    image=DYNAMO_IMAGE,
)
class PrefillService:
    """Service that handles the prefill stage of text generation."""
    
    @endpoint()
    async def process(self, request: PrefillRequest) -> AsyncGenerator[PrefillResponse, None]:
        """Process the prefill request."""
        logger.info(f"Prefill received request: {request}")
        
        # Simulate tokenization and KV cache creation
        # In a real implementation, this would use a proper tokenizer and model
        fake_tokens = [i for i in range(len(request.text.split()))]
        kv_cache_id = str(uuid.uuid4())
        
        response = PrefillResponse(
            prefill_tokens=fake_tokens,
            kv_cache_id=kv_cache_id
        )
        
        logger.info(f"Prefill generated response: {response}")
        yield response