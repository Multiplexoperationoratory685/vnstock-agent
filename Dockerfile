FROM python:3.12-alpine

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN apk add --no-cache gcc musl-dev python3-dev && pip install --no-cache-dir . && apk del gcc musl-dev python3-dev

ENV VNSTOCK_API_KEY=""
ENV VNSTOCK_MCP_TRANSPORT="sse"
ENV VNSTOCK_MCP_HOST="0.0.0.0"
ENV VNSTOCK_MCP_PORT="8000"

EXPOSE 8000

CMD ["vnstock-mcp"]
