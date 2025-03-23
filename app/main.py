from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import chat, search, websocket
from app.workers.gdpr_worker import process_gdpr_queue
from app.observability.logger import setup_logging
from app.observability.tracing import setup_tracer
import asyncio
from opentelemetry import trace

# Set up structured logger
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Chatbot API",
    description="Event-driven, AI-powered chat system with GDPR compliance and real-time support.",
    version="1.0.0"
)

# ✅ Prometheus metrics middleware — MUST be added before startup
Instrumentator().instrument(app).expose(app)
logger.info("Prometheus instrumentation enabled")

# ✅ Tracing setup — should happen before startup too
setup_tracer(app)
logger.info("OpenTelemetry tracing initialized")

# Middleware for logging HTTP requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("request_received", method=request.method, path=request.url.path)
    response = await call_next(request)
    logger.info("request_handled", method=request.method, path=request.url.path, status_code=response.status_code)
    return response

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(search.router, prefix="/api", tags=["Search"])
app.include_router(websocket.router, tags=["WebSocket"])

# Health check endpoint

@app.get("/")
async def health_check():
    tracer = trace.get_tracer("chatbot-api")
    with tracer.start_as_current_span("health-check-span"):
        return {"status": "ok", "message": "Chatbot API is running"}
# GDPR background worker
@app.on_event("startup")
async def startup_worker():
    logger.info("Starting GDPR background worker")
    asyncio.create_task(gdpr_background_loop())

# Background loop for GDPR queue
async def gdpr_background_loop():
    while True:
        await process_gdpr_queue()
        await asyncio.sleep(10)

@app.get("/test-trace")
async def test_trace():
    from opentelemetry import trace
    tracer = trace.get_tracer("chatbot-api")
    with tracer.start_as_current_span("manual-test-span"):
        return {"message": "Tracing test completed!"}
