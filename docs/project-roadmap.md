# Project Roadmap & Development Timeline

## Version History & Status

### v0.1.0 (Current - April 2026)
**Status**: Released  
**Release Date**: 2026-04-01

#### Features Completed
- [x] 21 MCP tools across 6 categories (Quote, Company, Financials, Listings, Trading, Global Markets, Funds)
- [x] 22 CLI commands with all tool functionality
- [x] 3 MCP transports (stdio, SSE, Streamable HTTP)
- [x] Configuration via environment variables
- [x] Data transformation from pandas to JSON
- [x] Graceful error handling (returns error dicts instead of crashing)
- [x] Table and JSON output formats for CLI
- [x] API key management with stdout suppression
- [x] Comprehensive README documentation

#### Known Issues & Limitations
- [ ] vnstock MSN source timezone bug affects forex/crypto/world_index (upstream issue)
- [ ] stock_price_depth unsupported by VCI/KBS sources (upstream limitation)
- [ ] No caching layer (all requests hit vnstock API)
- [ ] No async support in core functions (all blocking I/O)
- [ ] Limited to 30-day default date lookback
- [ ] No portfolio or comparison tools
- [ ] No technical analysis indicators

#### Test Coverage
- Stock tools: 17/21 passing
- Domestic stocks: PASS
- Company data: PASS
- Financials: PASS
- Listings: PASS
- Global markets (MSN source): Upstream bugs
- price_depth: Unsupported by current sources

---

## v0.2.0 (Planned - Q2 2026)

**Estimated Timeline**: June 2026  
**Focus**: Enhanced functionality, caching, better error handling

### New Features

#### Caching Layer
- In-memory cache for frequently accessed data (symbols, industries, etc.)
- TTL-based expiration (1 hour for live data, 1 day for reference data)
- Cache statistics and management tools
- CLI command: `vnstock-agent cache stats`, `cache clear`

**Impact**: Reduce API calls by 30-50% for typical workflows

#### Advanced Filtering & Aggregation
- Filter symbols by market cap, industry, sector
- Technical analysis helpers (moving averages, support/resistance)
- Portfolio aggregation across multiple symbols
- Sector performance comparison

**Tools Added**:
- `filter_symbols_by_criteria(market_cap_min, market_cap_max, industry, exchange)`
- `calculate_sector_performance(exchange, date_range)`
- `compare_portfolios(symbols_list1, symbols_list2, metric)`

#### Async Core Functions
- Convert core.py functions to async for concurrent vnstock API calls
- Enable parallel data fetching for multiple symbols
- Maintain backward compatibility with sync wrapper

**Performance Gain**: 5-10x faster for batch operations (10+ symbols)

#### Improved Error Handling & Logging
- Structured logging with JSON output
- Detailed error messages with troubleshooting suggestions
- Retry logic for transient API failures (exponential backoff)
- Circuit breaker pattern for persistent failures

#### Custom Time Zones
- Support time zone conversions for international users
- Handle daylight saving time correctly
- CLI option: `--timezone UTC|+07:00|Asia/Ho_Chi_Minh`

#### Integration Tests with Real API
- Test suite using real vnstock API (with mocking options)
- Fixture-based test data
- CI/CD pipeline with GitHub Actions

### Tasks
- [ ] Implement caching layer with tests
- [ ] Add 3 new MCP tools for filtering
- [ ] Convert core functions to async
- [ ] Add structured logging
- [ ] Implement retry logic
- [ ] Add timezone support
- [ ] Create integration tests
- [ ] Update documentation

### Breaking Changes
None planned for v0.2.0 (backward compatible)

---

## v0.3.0 (Planned - Q3 2026)

**Estimated Timeline**: September 2026  
**Focus**: Advanced analytics, persistence, web integration

### New Features

#### Portfolio Tracking & Analysis
- Store and track watchlists/portfolios
- Calculate portfolio performance metrics
- Historical performance comparison
- Dividend tracking and yield analysis

**Tools Added**:
- `portfolio_create(name, symbols, weights)`
- `portfolio_performance(portfolio_id, date_range)`
- `portfolio_dividend_yield(portfolio_id)`
- `portfolio_rebalance_suggestions(portfolio_id)`

#### Technical Analysis Indicators
- Moving averages (SMA, EMA, WMA)
- Bollinger Bands
- MACD
- RSI
- Support & resistance levels
- Candlestick pattern recognition

**Tools Added**:
- `calculate_sma(symbol, period)`
- `calculate_bollinger_bands(symbol, period, std_dev)`
- `calculate_macd(symbol, fast, slow, signal)`
- `identify_support_resistance(symbol, lookback_period)`

#### Alert System
- Price alerts (when stock crosses threshold)
- Technical indicator alerts (RSI overbought/oversold)
- News alerts (company news, dividend announcements)
- Customizable alert channels (email, webhook, etc.)

#### Web Dashboard (Optional)
- Real-time stock price updates
- Portfolio visualization
- Technical charts
- Alert management
- User authentication

**Tech Stack**: React + FastAPI + WebSocket

#### Data Persistence
- SQLite/PostgreSQL backend for portfolios and watchlists
- Historical data caching in database
- User accounts and preferences

### Tasks
- [ ] Design portfolio data model
- [ ] Implement portfolio CRUD operations
- [ ] Add 8 technical analysis tools
- [ ] Implement alert system
- [ ] Create web dashboard (optional)
- [ ] Add data persistence layer
- [ ] Write integration tests
- [ ] Performance testing

### Breaking Changes
May require database migration for v0.3.0+ (v0.2.0 users)

---

## v0.4.0+ (Roadmap - 2027+)

**Focus**: Trading integration, AI enhancement, ecosystem expansion

### Potential Features

#### Trading Integration
- Real-time trade execution (via brokerage APIs)
- Order management and history
- Portfolio margin and leverage
- Backtest trading strategies
- Paper trading simulator

#### AI-Enhanced Features
- AI-generated investment theses
- Sentiment analysis from news
- Predictive price modeling
- Automated trading recommendations
- Multi-agent analysis (different perspectives)

#### Ecosystem Expansion
- Mobile app (iOS/Android)
- Browser extension
- Telegram bot
- Discord bot
- Slack integration
- Email digest subscriptions

#### Internationalization
- Multi-language support (Vietnamese, English, Chinese, Japanese)
- Support for international exchanges (NASDAQ, LSE, HK, Singapore)
- Multi-currency conversion
- Global economic indicators

#### Enterprise Features
- Team collaboration and permissions
- Institutional-grade data (real-time quotes, Level 2 data)
- API rate limits and usage tracking
- Enterprise support SLA
- White-label options

---

## Dependency Updates Timeline

### Critical Updates
When upstream dependency releases major version:
- **vnstock 4.0+**: Review breaking changes, update core.py
- **FastMCP 4.0+**: Review transport changes, update server.py

### Dependency Status (as of v0.1.0)

| Dependency | Version | Status | Next Check |
|-----------|---------|--------|-----------|
| vnstock | 3.5.0 | Current | Q3 2026 |
| fastmcp | ≥2.0.0 | Current | Q3 2026 |
| click | ≥8.0 | Current | Q4 2026 |
| pandas | ≥1.5.0 | Current | Q4 2026 |
| pydantic-settings | ≥2.0 | Current | Q1 2027 |
| Python | 3.10+ | Current | Q1 2027 |

---

## Development Velocity & Milestone Summary

### Metrics (Estimated)
- **v0.1.0**: 3 weeks (research + build + test)
- **v0.2.0**: 4 weeks (caching + async + testing)
- **v0.3.0**: 6 weeks (portfolio + analytics + UI)
- **v0.4.0**: 8+ weeks (trading + AI + ecosystem)

### Community Engagement Milestones
- **v0.1.0**: Initial release, GitHub repo, README
- **v0.2.0**: First bug reports, community PRs
- **v0.3.0**: Featured in Vietnamese fintech blogs/forums
- **v0.4.0**: Trading community adoption, enterprise interest

---

## Known Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| vnstock API downtime | Tools unavailable | Implement fallback sources, caching |
| Breaking vnstock API changes | Core functions fail | Maintain 2 versions of vnstock lib |
| MCP protocol changes | Server incompatible | Monitor MCP spec, upgrade FastMCP promptly |
| Data accuracy issues | User decisions based on bad data | Add data validation, disclaimer |
| Security vulnerabilities in deps | Potential exploit | Security scanning (Dependabot), prompt patching |
| Feature scope creep | Delayed releases | Time-box features, defer to v0.4.0+ |

---

## Exit Criteria By Version

### v0.1.0 (Current) ✓
- [x] All 21 MCP tools implemented
- [x] All 22 CLI commands working
- [x] 3 transport modes supported
- [x] Error handling in place
- [x] README documentation complete
- [x] 17/21 tools passing tests
- [x] Ruff linting passes

### v0.2.0 Entry Criteria
- [x] v0.1.0 released and stable
- [x] Community feedback gathered (2+ weeks)
- [x] High-impact bugs fixed

### v0.2.0 Exit Criteria
- [ ] Caching layer implemented with tests
- [ ] Async core functions + backward compat wrapper
- [ ] Test coverage >80%
- [ ] Integration tests passing
- [ ] Zero security vulnerabilities
- [ ] Performance benchmarks documented
- [ ] Backward compatible with v0.1.0 data

### v0.3.0 Entry Criteria
- [ ] v0.2.0 released and stable (4+ weeks)
- [ ] Portfolio API designed and validated
- [ ] Technical indicator requirements finalized

### v0.3.0 Exit Criteria
- [ ] Portfolio CRUD operations complete
- [ ] 8 technical analysis tools passing tests
- [ ] Alert system functional
- [ ] Database schema stable
- [ ] Migration path from v0.2.0 documented
- [ ] Dashboard (if included) responsive and accessible

---

## Quarterly Planning (2026)

### Q1 2026 (Jan-Mar)
- Research & architecture planning
- v0.1.0 development and testing
- Initial GitHub repo setup
- **Expected Release**: v0.1.0 (EOQ1)

### Q2 2026 (Apr-Jun)
- Gather v0.1.0 user feedback
- Implement caching and async
- Community support and documentation
- **Expected Release**: v0.2.0 (EOQ2)

### Q3 2026 (Jul-Sep)
- Develop portfolio system
- Add technical analysis tools
- Design alert system
- **Expected Release**: v0.3.0 (EOQ3)

### Q4 2026 (Oct-Dec)
- Stabilize v0.3.0
- Gather requirements for trading integration
- Plan v0.4.0 architecture
- Year-end community engagement

---

## Long-Term Vision (2027+)

### Strategic Goals
1. **Become default MCP tool** for Vietnamese stock market data
2. **Enable AI assistants** to make informed financial decisions
3. **Empower retail traders** with institutional-grade analytics
4. **Build trading ecosystem** around Vietnamese markets
5. **International expansion** to other Asian markets

### 5-Year Targets
- **Users**: 10K+ active users (v0.2), 100K+ (v0.4)
- **Tools**: 21 (v0.1) → 35 (v0.2) → 60 (v0.3) → 100+ (v0.4)
- **Platforms**: CLI (v0.1) → Web (v0.3) → Mobile (v0.4)
- **Markets**: Vietnamese stocks → Global equities, crypto, commodities
- **AI Integration**: AI tool access → AI-powered recommendations → AI-driven trading

### Success Metrics
- GitHub stars: 100+ by EOY 2026, 1K+ by EOY 2027
- Community contributions: 5+ community PRs by v0.3.0
- User testimonials: 10+ public case studies by v0.4.0
- Enterprise adoption: 2+ enterprise customers by v0.4.0
- Market impact: Referenced in Vietnamese fintech news

---

## How to Track Progress

**GitHub Issues**: Track bugs and feature requests
**GitHub Projects**: Kanban board for v0.X planning
**GitHub Milestones**: Version releases and target dates
**Changelog**: Detailed changes per version (CHANGELOG.md)
**Releases**: GitHub releases with release notes and artifacts

---

## Contributing to Roadmap

To suggest features or changes:
1. Open a GitHub Issue with `[RFC]` prefix
2. Describe the feature, use case, and expected impact
3. Include implementation difficulty estimate
4. Reference related features or versions
5. Community discussion and feedback
6. Acceptance/rejection decision with rationale

**Roadmap freeze**: 2 weeks before version release (no new features added to current sprint)
