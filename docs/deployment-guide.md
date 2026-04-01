# Deployment Guide

## Quick Start

### Installation

#### Via pip (Recommended)
```bash
pip install vnstock-agent
```

#### From Source
```bash
git clone https://github.com/mrgoonie/vnstock-agent.git
cd vnstock-agent
pip install -e .
```

#### With Development Tools
```bash
pip install -e ".[dev]"  # Includes pytest, ruff
```

### Verify Installation
```bash
vnstock-agent --version
# Output: vnstock-agent, version 0.1.0

vnstock-agent --help
# Shows all available commands
```

---

## Configuration

### Environment Variables

All configuration via environment variables. Set before running server or CLI:

```bash
# Required (for some operations)
export VNSTOCK_API_KEY="your_api_key_here"

# Optional - Data source (default: VCI)
export VNSTOCK_SOURCE="VCI"  # Options: VCI, KBS, MSN

# Optional - MCP Server Settings (default: stdio)
export VNSTOCK_MCP_TRANSPORT="stdio"  # Options: stdio, sse, http
export VNSTOCK_MCP_HOST="0.0.0.0"     # Server bind address
export VNSTOCK_MCP_PORT="8000"        # Server port

# Optional - Python logging (development)
export PYTHONUNBUFFERED=1  # Unbuffered stdout for real-time logs
```

### Get API Key

1. Visit [vnstocks.com](https://vnstocks.com) (Vietnamese stock data provider)
2. Sign up and log in
3. Go to Settings → API Keys
4. Copy your free API key
5. Set in environment: `export VNSTOCK_API_KEY="..."`

**Free vs Paid**:
- Free tier: Sufficient for most use cases (1K+ calls/month)
- Paid tier: Higher rate limits, priority support

---

## CLI Usage

### Basic Commands

#### Stock Price History
```bash
# Last 30 days (default)
vnstock-agent history VNM

# Custom date range
vnstock-agent history VNM --start 2025-01-01 --end 2025-03-31

# Different interval
vnstock-agent history VNM --interval 1H  # 1-hour candles

# Different source
vnstock-agent history VNM --source KBS
```

**Output Options**:
```bash
# Table format (default)
vnstock-agent history VNM

# JSON format
vnstock-agent --format json history VNM
```

#### Company Information
```bash
vnstock-agent overview FPT        # Company overview
vnstock-agent shareholders FPT    # Major shareholders
vnstock-agent officers FPT        # Management team
vnstock-agent news FPT            # Latest news
vnstock-agent events FPT          # Dividends, AGM, etc.
```

#### Financial Statements
```bash
vnstock-agent balance-sheet VCB --period quarter   # Quarterly
vnstock-agent balance-sheet VCB --period annual    # Annual
vnstock-agent income VCB
vnstock-agent cashflow VCB
vnstock-agent ratio VCB
```

#### Market Listings
```bash
vnstock-agent symbols              # All listed symbols
vnstock-agent group --group VN30    # VN30 index symbols
vnstock-agent group --group HNX30   # HNX30 index symbols
vnstock-agent exchange              # Symbols by exchange
vnstock-agent industries            # ICB industries
```

#### Trading Data
```bash
vnstock-agent intraday VNM              # Today's trading data
vnstock-agent intraday VNM --page-size 200
vnstock-agent depth VNM                 # Order book (bid/ask)
vnstock-agent board "VNM,FPT,ACB,VCB"  # Real-time price board
```

#### Global Markets
```bash
vnstock-agent fx EURUSD --start 2025-01-01      # Forex
vnstock-agent crypto BTC --start 2025-01-01     # Cryptocurrency
vnstock-agent index DJI --start 2025-01-01      # World indices
vnstock-agent funds                              # Mutual funds
```

### Output Formats

#### Table Format (Default)
```bash
$ vnstock-agent history VNM

symbol    date          open    high     low     close   volume
------  ----------  -------  -------  -------  -------  ---------
VNM     2025-03-31   76500    76900   76200    76800   2500000
VNM     2025-03-28   76200    76600   76000    76500   2300000
VNM     2025-03-27   76000    76400   75800    76200   2100000
```

#### JSON Format
```bash
$ vnstock-agent --format json history VNM

[
  {
    "symbol": "VNM",
    "date": "2025-03-31",
    "open": 76500,
    "high": 76900,
    "low": 76200,
    "close": 76800,
    "volume": 2500000
  },
  ...
]
```

### Tips & Tricks

```bash
# Pipe to other tools
vnstock-agent --format json history VNM | jq '.[] | select(.close > 76000)'

# Save to file
vnstock-agent --format json history VNM > vnm_history.json

# Multiple symbols in price board
vnstock-agent board "VNM,FPT,ACB,VCB,BAC"

# Use in shell scripts
PRICE=$(vnstock-agent --format json history VNM | jq -r '.[0].close')
echo "VNM closing price: $PRICE"
```

---

## MCP Server Setup

### Transport 1: stdio (Claude Desktop & Cursor)

**Best For**: Local development, Claude Desktop, Cursor Editor

#### Step 1: Verify Installation
```bash
which vnstock-mcp
# Output: /usr/local/bin/vnstock-mcp (or similar)
```

#### Step 2: Configure Claude Desktop

Edit Claude Desktop config file:

**macOS/Linux**:
```bash
~/.claude/claude_desktop_config.json
```

**Windows**:
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Config Content**:
```json
{
  "mcpServers": {
    "vnstock": {
      "command": "vnstock-mcp",
      "env": {
        "VNSTOCK_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

#### Step 3: Restart Claude Desktop
Close and reopen Claude Desktop. The vnstock tool should now be available.

#### Step 4: Test in Claude
Ask Claude: "What is the current price of VNM stock?"

Claude can now use the `stock_intraday` tool to fetch real-time data.

#### Configure Cursor Editor

Similar to Claude Desktop, Cursor also supports MCP servers.

Edit Cursor config (or use UI settings):
- Settings → Features → Model Context Protocol
- Add MCP Server
- Command: `vnstock-mcp`
- Environment: `VNSTOCK_API_KEY`

### Transport 2: SSE (HTTP Streaming)

**Best For**: Remote access, multi-client scenarios, cloud deployments

#### Step 1: Start Server
```bash
export VNSTOCK_API_KEY="your_api_key_here"
export VNSTOCK_MCP_TRANSPORT="sse"
export VNSTOCK_MCP_PORT="8000"

vnstock-mcp
# Output: INFO: Uvicorn running on http://0.0.0.0:8000
```

#### Step 2: Test with curl
```bash
# List available tools
curl http://localhost:8000/mcp/tools

# Call a tool
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "stock_history",
      "arguments": {"symbol": "VNM"}
    }
  }'
```

#### Step 3: Remote Access
If server on remote machine (e.g., VPS), expose with Ngrok or reverse proxy:

```bash
# Use Ngrok (free tier available)
ngrok http 8000
# Get public URL: https://xxxx-xx-xx.ngrok.io

# Update MCP client to point to public URL
```

#### Step 4: Configure MCP Client
Some MCP clients support HTTP transport. Configure endpoint:
```
http://localhost:8000/mcp
```

### Transport 3: Streamable HTTP

**Best For**: Traditional REST API integration, legacy systems

#### Step 1: Start Server
```bash
export VNSTOCK_API_KEY="your_api_key_here"
export VNSTOCK_MCP_TRANSPORT="http"
export VNSTOCK_MCP_PORT="8000"

vnstock-mcp
```

#### Step 2: Test with curl
```bash
# Call tool with POST request
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "stock_history",
      "arguments": {
        "symbol": "VNM",
        "start": "2025-01-01",
        "end": "2025-03-31"
      }
    }
  }' | jq .
```

#### Step 3: Integration Example (Python)
```python
import requests
import json

MCP_URL = "http://localhost:8000/mcp"
API_KEY = "your_api_key_here"

def call_mcp_tool(tool_name, arguments):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    response = requests.post(MCP_URL, json=payload)
    return response.json()

# Get stock history
result = call_mcp_tool("stock_history", {
    "symbol": "VNM",
    "start": "2025-01-01",
    "end": "2025-03-31"
})
print(json.dumps(result, indent=2))
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install vnstock-agent
RUN pip install --no-cache-dir vnstock-agent

# Create non-root user
RUN useradd -m vnstock

USER vnstock

# Expose port for SSE/HTTP transports
EXPOSE 8000

# Default to stdio, can override with env vars
CMD ["vnstock-mcp"]
```

### Build & Run

```bash
# Build
docker build -t vnstock-agent:0.1.0 .

# Run with stdio (interactive)
docker run -it vnstock-agent:0.1.0

# Run with SSE transport
docker run -d \
  -e VNSTOCK_MCP_TRANSPORT=sse \
  -e VNSTOCK_API_KEY="your_api_key" \
  -p 8000:8000 \
  vnstock-agent:0.1.0

# Check logs
docker logs -f <container_id>
```

### Docker Compose

```yaml
version: '3'

services:
  vnstock-agent:
    image: vnstock-agent:0.1.0
    environment:
      VNSTOCK_API_KEY: ${VNSTOCK_API_KEY}
      VNSTOCK_MCP_TRANSPORT: sse
      VNSTOCK_MCP_PORT: "8000"
    ports:
      - "8000:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Optional: Reverse proxy (nginx)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - vnstock-agent
```

---

## Cloud Deployment

### AWS EC2

```bash
# 1. Launch EC2 instance (t3.micro, Ubuntu 22.04)
# 2. SSH into instance
ssh -i key.pem ubuntu@instance_ip

# 3. Install dependencies
sudo apt update
sudo apt install -y python3.11 python3-pip

# 4. Install vnstock-agent
pip install vnstock-agent

# 5. Set environment variables
echo 'export VNSTOCK_API_KEY="..."' >> ~/.bashrc
echo 'export VNSTOCK_MCP_TRANSPORT="sse"' >> ~/.bashrc
source ~/.bashrc

# 6. Run with systemd (persistent)
sudo tee /etc/systemd/system/vnstock-mcp.service <<EOF
[Unit]
Description=VNStock Agent MCP Server
After=network.target

[Service]
Type=simple
User=ubuntu
Environment="VNSTOCK_API_KEY=your_api_key"
Environment="VNSTOCK_MCP_TRANSPORT=sse"
Environment="VNSTOCK_MCP_PORT=8000"
ExecStart=/usr/local/bin/vnstock-mcp
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable vnstock-mcp
sudo systemctl start vnstock-mcp
sudo systemctl status vnstock-mcp
```

### AWS Lambda (Serverless)

```python
# lambda_function.py
from vnstock_agent import core
import json

def lambda_handler(event, context):
    """Handle MCP tool calls from Lambda."""
    tool_name = event.get('tool')
    arguments = event.get('arguments', {})
    
    # Call appropriate core function
    if tool_name == 'stock_history':
        result = core.stock_history(
            arguments['symbol'],
            arguments.get('start'),
            arguments.get('end'),
            arguments.get('interval', '1D'),
            arguments.get('source', 'VCI')
        )
    else:
        return {'error': f'Unknown tool: {tool_name}'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

### Google Cloud Run

```bash
# 1. Create Cloud Run service
gcloud run deploy vnstock-agent \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --memory 256Mi \
  --set-env-vars VNSTOCK_API_KEY="your_api_key",VNSTOCK_MCP_TRANSPORT="http"

# 2. Get service URL
gcloud run describe vnstock-agent --region asia-southeast1

# 3. Call via HTTPS
curl https://vnstock-agent-xxx.run.app/mcp -X POST ...
```

---

## Systemd Service (Linux)

For running as a background service on Linux:

```bash
# Create service file
sudo tee /etc/systemd/system/vnstock-mcp.service <<EOF
[Unit]
Description=VNStock Agent MCP Server
After=network.target

[Service]
Type=simple
User=vnstock
Group=vnstock
Environment="VNSTOCK_API_KEY=your_api_key"
Environment="VNSTOCK_MCP_TRANSPORT=sse"
Environment="VNSTOCK_MCP_PORT=8000"
ExecStart=/usr/local/bin/vnstock-mcp
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable vnstock-mcp
sudo systemctl start vnstock-mcp

# Check status
sudo systemctl status vnstock-mcp

# View logs
sudo journalctl -u vnstock-mcp -f
```

---

## Troubleshooting

### Issue: "API key not set"
```
Error: API key not set. Set VNSTOCK_API_KEY environment variable.
```

**Solution**:
```bash
export VNSTOCK_API_KEY="your_api_key"
vnstock-agent history VNM
```

### Issue: "Connection refused" (Remote MCP)
```
Error: Failed to connect to MCP server at localhost:8000
```

**Solutions**:
- Verify server is running: `curl http://localhost:8000/health`
- Check firewall: `sudo ufw allow 8000`
- Verify port not in use: `lsof -i :8000`
- Check server logs: `docker logs <container>`

### Issue: "Invalid symbol"
```
Error: {'error': 'Invalid symbol'}
```

**Solutions**:
- Use uppercase symbols: `VNM` not `vnm`
- Verify symbol exists: `vnstock-agent symbols | grep SYMBOL`

### Issue: "No data returned"
```
Result: []
```

**Solutions**:
- Verify date range is valid and has trading data
- Weekend/holiday may have no data
- Check with different date: `--start 2025-01-01 --end 2025-03-31`

### Issue: Timezone mismatches (forex/crypto)
```
Dates appear shifted by 1-2 hours
```

**Workaround**: Known vnstock issue with MSN source. Use VCI source where possible or wait for vnstock fix.

### Issue: Docker permission denied
```
Error: permission denied: /app/vnstock-mcp
```

**Solution**:
```dockerfile
RUN chmod +x /app/vnstock-mcp
```

---

## Performance Tuning

### Caching

For frequently accessed data, implement client-side caching:

```python
import time
from functools import lru_cache

# Simple TTL cache
cache = {}
CACHE_TTL = 300  # 5 minutes

def get_symbols_cached():
    if 'symbols' in cache:
        timestamp, data = cache['symbols']
        if time.time() - timestamp < CACHE_TTL:
            return data
    
    # Fetch fresh data
    data = core.listing_all_symbols()
    cache['symbols'] = (time.time(), data)
    return data
```

### Connection Pooling

For high-concurrency HTTP transport, configure uvicorn workers:

```bash
VNSTOCK_MCP_WORKERS=4 vnstock-mcp
```

### Load Balancing

For production, use nginx to balance load:

```nginx
upstream vnstock_backend {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    listen 80;
    location / {
        proxy_pass http://vnstock_backend;
    }
}
```

---

## Security Considerations

### API Key Management
- Never commit `VNSTOCK_API_KEY` to version control
- Use `.env` file (add to `.gitignore`)
- Use secrets manager in production (AWS Secrets Manager, HashiCorp Vault)
- Rotate API keys regularly

### Network Security
- Use HTTPS for remote access (nginx with Let's Encrypt)
- Restrict server IP access (firewall rules)
- Use VPN for sensitive deployments
- Disable stdio transport in production (use HTTP/SSE only)

### Rate Limiting
```nginx
limit_req_zone $binary_remote_addr zone=vnstock:10m rate=10r/s;

server {
    location / {
        limit_req zone=vnstock burst=20;
        proxy_pass http://vnstock_backend;
    }
}
```

---

## Monitoring & Logging

### Basic Health Check
```bash
# For stdio: Requires interaction
echo '{"method": "tools/list"}' | vnstock-mcp

# For HTTP/SSE: Use curl
curl http://localhost:8000/health
```

### Prometheus Metrics (Future)

When implemented in v0.2.0:
```
vnstock_request_count_total
vnstock_request_duration_seconds
vnstock_error_count_total
vnstock_cache_hit_ratio
```

### Log Levels
```bash
export PYTHONUNBUFFERED=1
export LOGLEVEL=DEBUG
vnstock-mcp
```

---

## Upgrade Guide

### From v0.1.0 to v0.2.0

```bash
# Backup configuration
cp ~/.env ~/.env.backup

# Upgrade package
pip install --upgrade vnstock-agent

# No database migrations needed for v0.2.0
# Restart services
systemctl restart vnstock-mcp

# Verify
vnstock-agent --version  # Should show 0.2.0
```

### Breaking Changes
- None planned for v0.2.0 (backward compatible)
- Check CHANGELOG.md for each version

---

## Uninstallation

```bash
# Uninstall package
pip uninstall vnstock-agent

# Remove systemd service (if installed)
sudo systemctl stop vnstock-mcp
sudo systemctl disable vnstock-mcp
sudo rm /etc/systemd/system/vnstock-mcp.service
sudo systemctl daemon-reload

# Remove environment variables
unset VNSTOCK_API_KEY
unset VNSTOCK_MCP_TRANSPORT
```

---

## Support & Resources

- **GitHub Issues**: Report bugs at github.com/mrgoonie/vnstock-agent/issues
- **Discussions**: Ask questions in GitHub Discussions
- **Documentation**: Read docs/ folder in repository
- **vnstock Documentation**: https://vnstock.site
- **MCP Specification**: https://modelcontextprotocol.io
