from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/tcp-connect")
def tcp_connect() -> None:
    # logique privée — non incluse
    raise HTTPException(status_code=501, detail="not implemented")


@router.post("/tls-audit")
def tls_audit() -> None:
    # logique privée — non incluse
    raise HTTPException(status_code=501, detail="not implemented")


@router.get("/catalog")
def catalog() -> None:
    # logique privée — non incluse
    raise HTTPException(status_code=501, detail="not implemented")
