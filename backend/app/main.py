from fastapi import FastAPI
from app.api.ussd import router as ussd_router
from app.api.webhook import router as webhook_router

app = FastAPI(
    title="MzaziRada Backend",
    description="High-Speed USSD & SMS Gateway for School Data Management",
    version="1.0.0"
)

# Register API endpoints
app.include_router(ussd_router, prefix="/api/v1")
app.include_router(webhook_router, prefix="/api/v1")

@app.get("/")
async def health_check():
    return {"status": "online", "service": "MzaziRada Backend"}
