from fastapi import Query, HTTPException
from starlette import status

from converter.core import get_rate, RemoteException
from converter.app import app


@app.get("/api/rates")
async def convert_ep(
    from_: str = Query(alias="from"), to: str = Query(...), value: float = 1.0
):
    try:
        rate = await get_rate(from_, to)
    except RemoteException as e:
        if e.status == 422:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unprocessable entity. Remote service has returned the following errors: {e.errors}",
            )
        if e.status != 200:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                headers={"Retry-After": "60"},
                detail=f"Service is temporarily unavailable. Remote service has returned the code {e.status}",
            )

    result = rate * value
    return {"result": result}
