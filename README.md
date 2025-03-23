#  Semantic Chatbot API

A production-grade, event-driven, AI-powered chatbot system built with **FastAPI**, featuring:

- Real-time WebSocket-based messaging
- Semantic search using Qdrant
- Kafka background processing for GDPR deletions
- MongoDB for chat history storage
- OpenTelemetry + Prometheus for observability
- OpenAI embeddings for semantic understanding

---

## Architecture Overview

```
flowchart TD
    A[Client/WebSocket] -->|Send/Receive Message| B(FastAPI App)
    B --> C[MongoDB - Chat History]
    B --> D[Qdrant - Vector Store]
    B --> E[Kafka - GDPR Delete Events]
    E --> F[GDPR Worker - Async Processing]
    B --> G[Prometheus + OpenTelemetry Exporter]
    G --> H[OpenTelemetry Collector --> Jaeger]

Project Structure
├── app/
│   ├── api/                  # REST + WebSocket APIs
│   ├── services/             # Business logic
│   ├── embeddings/           # OpenAI embedding handler
│   ├── observability/        # Logging + Tracing
│   ├── queue/                # Kafka Queue abstraction
│   ├── utils/                # Config & helper modules
│   └── main.py               # App entrypoint
├── docker-compose.yml
├── .env
├── README.md

```
---
## How To Run
```
Create .env File

# MongoDB
MONGO_URI=mongodb://mongodb:27017
MONGO_DB_NAME=chatbot_db

# Qdrant
QDRANT_HOST=http://qdrant:6333
QDRANT_COLLECTION=chat_vectors
EMBEDDING_DIM=1536

# OpenAI
OPENAI_API_KEY=your-openai-key
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=gdpr_deletions
KAFKA_GROUP_ID=chatbot-consumer-group

# OpenTelemetry
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318/v1/traces

```
## Build and running this stack

docker compose up --build

## Available APIs

```
Endpoint	Method	Description
/	GET	Health check
/api/chat	POST	Send message to chatbot
/api/search	POST	Semantic search on chat history
/ws/chat	WS	WebSocket real-time chat support

```
## Observability
Traces: Exported via OpenTelemetry → Otel Collector → Jaeger (http://localhost:16686)

Metrics: Collected via prometheus-fastapi-instrumentator

Structured Logging: JSON logs via Python’s structlog

## Kafka for GDPR Deletion

```
Background worker runs every 10s

Dequeues GDPR events from Kafka

Performs secure deletions from MongoDB + Qdrant

```
## Acknowledgements
```
This project integrates ideas from various AI engineering resources and architecture patterns, including support from OpenAI’s GPT models, observability best practices, and contributions from AI/ML engineering communities.

```
## Author
Srikanth Satturi

https://www.linkedin.com/in/srikanth-satturi/