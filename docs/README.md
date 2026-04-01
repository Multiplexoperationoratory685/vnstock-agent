# VNStock Agent - Documentation Index

Welcome to the VNStock Agent documentation. This folder contains comprehensive guides for understanding, using, deploying, and contributing to the project.

## Quick Navigation

### For First-Time Users
Start here to understand what VNStock Agent is and how to use it:

1. **[Project Overview & PDR](./project-overview-pdr.md)** — What is VNStock Agent?
   - Project vision and goals
   - Target users and use cases
   - Feature overview (21 tools, 22 commands)
   - Technology stack
   - Requirements and success metrics

2. **[Deployment Guide](./deployment-guide.md)** — How do I set it up?
   - Installation instructions
   - Configuration (API keys, environment variables)
   - CLI quick start
   - MCP server setup (Claude Desktop, Cursor, HTTP)

### For Developers
Understand the codebase and contribute effectively:

1. **[Codebase Summary](./codebase-summary.md)** — How is the code organized?
   - File-by-file breakdown (5 source files, 1031 LOC)
   - Module responsibilities
   - Data flow and transformation pipeline
   - Dependency graph
   - Design patterns
   - Known limitations

2. **[Code Standards](./code-standards.md)** — What coding rules apply?
   - Python 3.10+ requirement
   - Naming conventions
   - Type hints and docstrings
   - Error handling patterns
   - Testing strategies
   - Commit message format
   - Code review checklist

3. **[System Architecture](./system-architecture.md)** — How do components fit together?
   - High-level architecture diagrams
   - Component interactions
   - Data transformation pipeline
   - Transport layer (stdio, SSE, HTTP)
   - Configuration management
   - Error handling architecture
   - Security considerations
   - Scalability and monitoring

### For Project Planning
Understand where the project is heading:

1. **[Project Roadmap](./project-roadmap.md)** — What's planned for future versions?
   - v0.1.0 status and test results
   - v0.2.0 planned features (caching, async, logging)
   - v0.3.0 planned features (portfolio, analytics, alerts)
   - v0.4.0+ vision (trading, AI, ecosystem)
   - Quarterly planning for 2026
   - Long-term vision (2027+)
   - Risk assessment
   - Contributing to the roadmap

---

## Documentation at a Glance

| Document | Purpose | Audience | Length |
|----------|---------|----------|--------|
| project-overview-pdr.md | Feature list, requirements, roadmap | Everyone | 197 LOC |
| codebase-summary.md | Code organization, design patterns | Developers | 411 LOC |
| code-standards.md | Coding conventions, standards | Contributors | 452 LOC |
| system-architecture.md | Architecture, data flows, deployment | Architects, DevOps | 628 LOC |
| project-roadmap.md | Timeline, planned features, vision | Project managers, community | 377 LOC |
| deployment-guide.md | Installation, configuration, troubleshooting | Users, DevOps, Admins | 805 LOC |

---

## Key Features

### 21 MCP Tools (for AI Assistants)
Access Vietnamese stock market data through Claude Desktop, Cursor, and other MCP clients.

| Category | Tools | Count |
|----------|-------|-------|
| **Stock Quotes** | history, intraday, price_depth | 3 |
| **Company Info** | overview, shareholders, officers, news, events | 5 |
| **Financials** | balance_sheet, income_statement, cash_flow, ratio | 4 |
| **Listings** | all_symbols, symbols_by_group, symbols_by_exchange, industries | 4 |
| **Trading** | price_board | 1 |
| **Global Markets** | fx_history, crypto_history, world_index_history | 3 |
| **Funds** | fund_listing | 1 |
| **Total** | | **21** |

### 22 CLI Commands (for Terminal Users)
Use Vietnamese stock market data from your terminal or scripts.

```bash
vnstock-agent history VNM              # Get stock prices
vnstock-agent overview FPT             # Company info
vnstock-agent symbols                  # List all stocks
vnstock-agent --format json history VNM  # JSON output
```

### 3 MCP Transports
Connect via stdio (Claude Desktop), SSE (HTTP streaming), or Streamable HTTP (REST).

---

## Common Tasks

### I want to use VNStock Agent

**Steps**:
1. Read [Project Overview & PDR](./project-overview-pdr.md) — understand features
2. Follow [Deployment Guide](./deployment-guide.md) — install and configure
3. Start using CLI commands or MCP tools

### I want to contribute code

**Steps**:
1. Read [Codebase Summary](./codebase-summary.md) — understand structure
2. Review [Code Standards](./code-standards.md) — learn conventions
3. Make changes following the standards
4. Run tests and linting: `pytest` and `ruff check src/`
5. Submit pull request

### I want to deploy to production

**Steps**:
1. Review [System Architecture](./system-architecture.md) — understand design
2. Follow [Deployment Guide](./deployment-guide.md) — cloud/Docker setup
3. Configure environment variables and API keys
4. Monitor logs and performance

### I want to understand the roadmap

**Steps**:
1. Read [Project Roadmap](./project-roadmap.md) — see v0.1 through v0.4+ plans
2. Check quarterly planning section — next milestones
3. Review known issues — what's being worked on
4. See contributing section — how to propose features

---

## Key Architecture

```
┌─────────────────────────────────────────┐
│    MCP Clients / Terminal / Web         │
│  (Claude Desktop, Cursor, CLI, etc.)    │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴─────────┐
       │                 │
   ┌───▼───────┐  ┌──────▼───────┐
   │ MCP Server│  │ CLI Interface │
   │(server.py)│  │  (cli.py)     │
   └───┬───────┘  └──────┬────────┘
       │                 │
       └────────┬────────┘
                │
         ┌──────▼──────────┐
         │  Shared Core    │
         │   (core.py)     │
         │  21 functions   │
         └────────┬────────┘
                  │
         ┌────────▼─────────┐
         │  vnstock Library  │
         │ Vietnamese Stocks │
         │ Forex / Crypto    │
         └───────────────────┘
```

---

## File Organization

```
vnstock-agent/
├── docs/                          ← You are here
│   ├── README.md                  ← Navigation guide
│   ├── project-overview-pdr.md    ← What is this?
│   ├── codebase-summary.md        ← How is it built?
│   ├── code-standards.md          ← How to contribute code
│   ├── system-architecture.md     ← How does it work?
│   ├── project-roadmap.md         ← What's next?
│   └── deployment-guide.md        ← How to deploy?
│
├── src/vnstock_agent/             ← Source code
│   ├── __init__.py
│   ├── config.py                  ← Settings & env vars
│   ├── core.py                    ← Business logic (21 functions)
│   ├── server.py                  ← MCP tools
│   └── cli.py                     ← CLI commands
│
├── tests/                         ← Test suite
│   ├── test_core.py
│   └── test_cli.py
│
├── pyproject.toml                 ← Package config
├── README.md                      ← User README
└── LICENSE                        ← MIT License
```

---

## Current Status (v0.1.0)

| Item | Status | Details |
|------|--------|---------|
| **Release** | ✓ Released | 2026-04-01 |
| **Features** | ✓ Complete | 21 tools, 22 commands, 3 transports |
| **Tests** | ✓ 17/21 Passing | 80%+ coverage on core functions |
| **Docs** | ✓ Complete | 6 documents, 2,870 LOC |
| **Code Standards** | ✓ Enforced | Ruff linting, type hints, docstrings |
| **Known Issues** | 2 | MSN timezone bug (upstream), price_depth unsupported |

---

## Support & Resources

- **GitHub Repository**: https://github.com/mrgoonie/vnstock-agent
- **Issues & Bug Reports**: GitHub Issues
- **Discussions & Questions**: GitHub Discussions
- **vnstock Library**: https://github.com/thinh-vu/vnstock
- **MCP Specification**: https://modelcontextprotocol.io
- **API Key**: https://vnstocks.com

---

## Quick Links

### Getting Started
- [Installation](./deployment-guide.md#installation)
- [Configuration](./deployment-guide.md#configuration)
- [CLI Examples](./deployment-guide.md#basic-commands)

### Setup MCP Server
- [Claude Desktop](./deployment-guide.md#transport-1-stdio-claude-desktop--cursor)
- [Cursor Editor](./deployment-guide.md#transport-1-stdio-claude-desktop--cursor)
- [Remote HTTP](./deployment-guide.md#transport-3-streamable-http)
- [Docker](./deployment-guide.md#docker-deployment)

### Development
- [Code Organization](./codebase-summary.md#file-manifest)
- [Architecture](./system-architecture.md)
- [Coding Standards](./code-standards.md)
- [Design Patterns](./codebase-summary.md#key-design-patterns)

### Operations
- [Troubleshooting](./deployment-guide.md#troubleshooting)
- [Performance Tuning](./deployment-guide.md#performance-tuning)
- [Security](./deployment-guide.md#security-considerations)
- [Monitoring](./deployment-guide.md#monitoring--logging)

---

## Version History

- **v0.1.0** (April 2026) — Initial release, 21 tools, 22 commands
- **v0.2.0** (Planned Q2 2026) — Caching, async, improved error handling
- **v0.3.0** (Planned Q3 2026) — Portfolio tracking, technical analysis
- **v0.4.0+** (2027+) — Trading, AI, ecosystem expansion

See [Project Roadmap](./project-roadmap.md) for details.

---

## Contributing

Want to contribute? Follow these steps:

1. **Read** [Code Standards](./code-standards.md) — learn the conventions
2. **Understand** [Codebase Summary](./codebase-summary.md) — see how it works
3. **Follow** the code review checklist — pass all checks
4. **Reference** [System Architecture](./system-architecture.md) — maintain design
5. **Test** thoroughly — run `pytest` and `ruff check src/`
6. **Submit PR** with clear description

---

## Last Updated

- **Documentation Generated**: 2026-04-01
- **VNStock Agent Version**: 0.1.0
- **Last Verification**: 2026-04-01

For updates, check GitHub releases and CHANGELOG.md.

---

**Start with [Project Overview & PDR](./project-overview-pdr.md) if you're new to the project.**
