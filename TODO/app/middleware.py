import time
import uuid
from collections.abc import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 1. Reuse existing trace ID from caller/gateway, or generate a fresh UUID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start_time = time.perf_counter()

        # 2. Attach request_id to state for downstream route access
        request.state.request_id = request_id

        # 3. Process the incoming request
        response = await call_next(request)

        # 4. Calculate total response duration in milliseconds
        process_time = (time.perf_counter() - start_time) * 1000

        # 5. Inject observability headers into the response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

        return response