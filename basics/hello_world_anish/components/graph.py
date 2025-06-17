from .prefill import PrefillService
from .decode import DecodeService

# Link the services in the pipeline
PrefillService.link(DecodeService)