# Public Equity Financials Lens

Use this lens for listed companies, liquid secondary-market targets, tickers/security codes, or any request asking whether a stock is worth buying. Integrate it into the report; do not append it as a generic finance checklist. The purpose is professional financial statement analysis, not only debt or balance-sheet screening.

## Core Question

Decide whether the current share price misprices future cash flow, asset value, risk, or catalysts.

The report must answer:

1. What is the stock, exchange, currency, latest price, trading date/time, market cap, and enterprise value if available?
2. What financial statements are the source of truth, and what period do they cover?
3. Are revenue, earnings, and cash flow improving for durable reasons or temporary reasons?
4. What do the income statement, balance sheet, cash flow statement, and notes reveal when read together?
5. Is the balance sheet healthy enough to survive the bear case?
6. Is valuation attractive relative to growth, quality, cyclicality, leverage, and peers?
7. What catalyst or evidence would make the market re-rate the stock?
8. What position size is justified by downside risk and evidence confidence?

## Source Priority

Use primary or near-primary sources first:

- US: SEC EDGAR 10-K, 10-Q, 8-K, DEF 14A, company IR releases.
- Mainland China A-share: 巨潮资讯/CNINFO, SSE/SZSE/BSE company announcements, annual/interim/quarterly reports.
- Hong Kong: HKEXnews, company annual/interim reports, announcements.
- Other markets: local exchange filings, regulator filings, company IR documents.
- Market data: exchange pages, reliable finance tools, broker/market-data terminals, or clearly cited finance aggregators. Record timestamp, currency, and exchange.

Do not rely only on media summaries or finance aggregator snippets for financial statements. Aggregators are acceptable for a first pass or market data, but material financial claims should trace back to filings or company IR.

## Required Workpapers

For public equities, `_work/evidence_matrix.md` must include dedicated rows for:

- Ticker / exchange / currency / latest price / market cap.
- Income statement: revenue, segment/product/geographic mix, gross margin, operating margin, net income, EPS, taxes, minority interests, and recurring vs. non-recurring items.
- Cash flow statement: operating cash flow, capex, free cash flow, FCF conversion, working-capital drivers, financing cash flow, dividends/buybacks/issuance.
- Balance sheet: cash, debt, net debt/cash, asset quality, leverage, liquidity, maturity profile, receivables, inventory, goodwill/intangibles, leases, provisions, contingent liabilities, and restricted/pledged assets where available.
- Notes and accounting quality: revenue recognition, capitalization policy, impairments, fair-value gains/losses, subsidies, related-party transactions, auditor opinion, restatements, and key estimates.
- Valuation: P/E, EV/EBITDA, EV/Sales, P/B, FCF yield, dividend/buyback yield when relevant.
- Peer comparison and historical trading range.
- Consensus, guidance, profit warning, order/backlog, or other expectation anchor where available.
- Catalysts, risks, and downside scenario.

If data is unavailable, write `未披露/未找到` and explain how that limits the conclusion.

## Professional Financial Statement Analysis

Analyze trends over at least 3 years when available, plus the latest interim/quarterly period.

Read the three statements and notes together. The analysis should explain economic reality, not only reproduce line items. Use common-size analysis, year-over-year and multi-year CAGR/trend analysis, peer comparison, and ratio analysis where data supports it.

Income statement:

- Separate volume, price, mix, FX, acquisition/disposal, one-off, and accounting effects where possible.
- Check gross margin and operating margin drivers rather than only reporting changes.
- Flag stock-based compensation, capitalization of expenses, fair-value gains, subsidies, asset sales, impairment reversals, and other non-operating items.
- Compare reported net income, adjusted/non-GAAP profit, operating profit, EBITDA, EPS, and tax rate; explain which profit measure is most decision-relevant and why.
- For segment disclosures, identify which segment creates value, which consumes capital, and whether mix shift improves or weakens quality.

Cash flow:

- Compare net income to operating cash flow and free cash flow.
- Identify working-capital pulls: receivables, inventory, payables, contract assets/liabilities, prepayments.
- For capex-heavy companies, distinguish maintenance capex from growth capex when possible.
- Treat earnings growth with weak cash conversion as lower quality unless there is a clear temporary reason.
- Reconcile CFO, capex, acquisitions/disposals, financing cash flows, dividends, buybacks, issuance, and debt repayment to the change in cash.
- Check whether free cash flow is structurally positive, cyclical, temporarily depressed, or dependent on working-capital release.

Balance sheet:

- Assess net cash/debt, debt maturity, interest coverage, refinancing risk, pledged assets, guarantees, off-balance-sheet commitments, lease liabilities, and contingent liabilities where disclosed.
- Assess asset quality: goodwill/intangibles, capitalized R&D, inventory age, receivable concentration/aging, related-party balances, investment property/fair value assets, restricted cash.
- Compare leverage and liquidity with peer norms and cyclicality.
- State whether assets and liabilities are healthy, stretched, or fragile under the bear case.
- Analyze equity quality: retained earnings, accumulated losses, minority interests, treasury shares, accumulated other comprehensive income, and dilution from options/convertibles.
- For banks/insurers/financials, replace industrial leverage metrics with capital adequacy, asset quality, NPL/credit cost, reserve coverage, duration/ALM, solvency, and regulatory capital metrics.

Notes and disclosures:

- Read accounting policies and key estimates before judging quality.
- Check revenue recognition, lease accounting, impairment testing, fair-value hierarchy, provisions, tax contingencies, related-party transactions, guarantees, pledges, restricted cash, commitments, and post-balance-sheet events.
- Flag auditor qualifications, emphasis of matter, material weakness, internal-control issues, delayed filings, restatements, regulator inquiries, or enforcement actions.

Return and efficiency:

- Calculate or discuss ROE, ROA, ROIC, asset turnover, working-capital turnover, inventory days, receivable days, payable days, cash conversion cycle, and incremental margins when relevant.
- Compare returns with cost of capital and peer ranges. A company that grows below its cost of capital may destroy value even if revenue grows.

Capital allocation:

- Review dividends, buybacks, issuance, M&A, related-party transactions, insider ownership, management incentives, and historical ROIC.
- Ask whether management compounds capital or dilutes/allocates poorly.

Forecast bridge:

- Build a compact bridge from historical results to bull/base/bear scenarios: revenue growth, margin, tax, capex, working capital, FCF, share count, and terminal/multiple assumption.
- Tie every forecast driver to evidence: backlog/order book, pricing, utilization, capacity, regulation, end-market demand, management guidance, consensus, or peer base rates.

## Market Data and Valuation

Always timestamp market data:

```text
Price as of [date/time timezone], exchange [exchange], currency [currency].
```

Use valuation methods appropriate to the company:

- Stable profitable company: P/E, EV/EBIT, FCF yield, DCF/sensitivity.
- Cyclical/industrial: mid-cycle earnings, EV/EBITDA, P/B, replacement value, downside book/asset value.
- Financials: P/B, ROE/COE, asset quality, capital adequacy, NIM, credit cost.
- Growth/software/platform: EV/Sales, gross profit multiple, FCF path, Rule of 40, retention if disclosed.
- Biotech/pre-revenue: cash runway, pipeline probability, milestone/risk-adjusted value.
- Distressed: liquidation/recovery value, liability stack, covenant/maturity wall.

Valuation must connect to fundamentals. Do not call a stock cheap only because the multiple is low; explain whether low multiple reflects cyclicality, leverage, governance, decline risk, accounting quality, or market neglect.

## Recommendation and Position Sizing

Use a clear public-equity action:

- Buy / Add / Hold / Watchlist / Reduce / Sell / Avoid.

Include:

- Current price context and valuation band.
- Bull/base/bear target or return range when data supports it.
- Downside drawdown or permanent-loss risk.
- Time horizon.
- Catalyst calendar.
- Evidence confidence.
- Position sizing guidance: full, starter, watchlist only, or zero position, with reasoning.

When evidence is incomplete, prefer `Watchlist` or `Hold off` over a false-precision Buy/Sell.

## Red Flags

Escalate these issues into risk and recommendation:

- Rising revenue with deteriorating cash conversion.
- Receivables/inventory growing much faster than revenue.
- High leverage with near-term maturity wall.
- Large goodwill/intangibles relative to equity.
- Repeated equity issuance or convertible dilution.
- Related-party transactions, guarantees, pledged shares, or restricted cash.
- Aggressive capitalization, subsidy dependence, fair-value gains, or non-recurring profit support.
- Auditor change, delayed filings, qualified opinions, restatements, enforcement actions.
- Management guidance misses or disclosure inconsistency.
