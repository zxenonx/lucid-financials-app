from fastapi import Request, HTTPException, status

def payload_size_limiter(max_bytes: int = 1024 * 1024):
    """
    Returns a dependency that limits the size of the request payload.

    Args:
        max_bytes: The maximum size of the request payload in bytes. Defaults
            to 1MB.

    Returns:
        A dependency that raises a 413 error if the payload size
        exceeds the specified limit.
    """
    async def dependency(request: Request):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Payload too large. Maximum size is {max_bytes // (1024 * 1024)}MB"
            )
    return dependency
