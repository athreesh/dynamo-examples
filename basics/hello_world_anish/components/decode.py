import logging
import asyncio
from typing import AsyncGenerator

from dynamo.sdk import DYNAMO_IMAGE, service, endpoint

from .utils import DecodeRequest, DecodeResponse

logger = logging.getLogger(__name__)

@service(
    dynamo={"namespace": "dynamo-demo"},
    image=DYNAMO_IMAGE,
)
class DecodeService:
    """Service that handles the decode stage of text generation."""
    
    @endpoint()
    async def process(self, request: DecodeRequest) -> AsyncGenerator[DecodeResponse, None]:
        """Process the decode request."""
        logger.info(f"Decode received request: {request}")
        
        # Simulate token generation using the KV cache
        # In a real implementation, this would use the actual model
        words = ["Hello", "from", "decode", "service", "using", "cache", request.kv_cache_id]
        
        for i in range(min(len(words), request.max_new_tokens)):
            response = DecodeResponse(
                generated_text=words[i],
                finished=(i == min(len(words), request.max_new_tokens) - 1)
            )
            logger.info(f"Decode generated token: {response}")
            yield response
            await asyncio.sleep(0.1)  # Simulate generation time