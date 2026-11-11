# ⚗️ CATALYST LAB

Personal biotech catalyst tracking and analysis terminal. It tracks active FDA and trial catalyst positions, surfaces new researched catalyst ideas, models probability and expected value with bull/base/bear scenarios, and logs results so your decisions improve over time.

---

## What This Is

A single `index.html` file that runs in any browser: no server, no npm, no build tools. Double-click it to open locally, or deploy it to Cloudflare Pages to reach it anywhere.

**v2.0 (research refreshed Nov 8, 2026).** The page is split into six tabs (keys `1`–`6`):

| Tab | What it's for |
|-----|---------------|
| **Overview** | A **To do** list of everything that needs a decision (catalysts that resolved, decisions within 30 days, stops hit, new ideas coming up), key stats, a timeline of positions and ideas, and the next 8 events |
| **My Positions** | Cards for trades you own. Each card has a summary strip (price, return, days to decision, odds, EV) and a plain-English verdict. Resolved catalysts show what happened and a suggested next step |
| **New Ideas** | 10 researched catalyst candidates, each with a bull thesis, why-now, a bull/base/bear **scenario planner** with price targets and an "if I invest $X" calculator, a trade plan (entry, size, exits, stop), risks, key dates and sources |
| **Calendar** | Every dated event, grouped by month, with a warning when decisions cluster |
| **Performance** | Closed trades (now saved, with undo), win rate, odds calibration and risk exposure |
| **How it works** | Daily routine, selection rules and a glossary (PDUFA, CRL, Class 2, AdCom, EV…) |

Other features: live prices from Yahoo Finance (with CORS-proxy fallbacks, refreshed every 5 min), an editable probability and upside/downside slider on every card, the Decision Framework, a pre-catalyst checklist, a trade journal, and export/import of all your data.

### Current positions (as of Nov 8, 2026)
- **CAPR**: live. The deramiocel PDUFA moved to **Nov 22, 2026** after a 9-3 negative AdCom and a major amendment (upper-limb indication).
- **CING**: CRL on Jun 2 (CMC only). Waiting for the resubmission.
- **NMRA**, **VTGN**: catalysts failed. Log your exits.
- **MNKD**: pediatric Afrezza approved May 29. Take profit or move to the long-term portfolio.
- **NVAX**: no binary catalyst left. Reclassify or exit.

### New ideas
SMMT (Nov 14, marked PASS) · COGT (Nov 30 / Dec 30) · VNDA (Dec 12) · CORT (Dec 17) · MLYS (Dec 22) · PRAX (Dec 27 / Jan 29) · IBRX (Jan 6) · DYN (Jan 21) · BLTE (Feb 12) · CGEM (Feb 27) · **APMD (Feb 28)** · AQST (Mar 16)

**Deep dive tab** (APMD, AQST): what the market is pricing in, an EV stress test, valuation, competition, a watch list and sizing.

**On deck** (huge markets, no PDUFA date yet): CMPS (TRD), ARWR (sHTG), OCUL (wet AMD), ALMS (psoriasis). They get promoted to idea cards once the FDA sets a date. Add more in the `watchlist` array.

Press **+ Track (I bought this)** on an idea and enter your shares and cost. It then appears under My Positions with live P&L. Tracked trades are saved in your browser.

---

## How to Add or Update a Position

Open `index.html` in a text editor and find the `CONFIG` block at the top of the `<script>` tag. Add an entry to `positions` (things you own) or `ideas` (candidates):

```javascript
{
  ticker: "ACME", company: "ACME Therapeutics",
  drug: "Drug Name (compound)", indication: "Disease — patient population",
  status: "active",                // active | won | failed | delayed | reclassify
  outcome: "",                     // what happened (for resolved statuses)
  nextStep: "",                    // suggested action (for resolved statuses)
  catalystType: "PDUFA",           // PDUFA | PhaseData | AdCom | Earnings | Other
  catalystDate: "2027-03-15",      // YYYY-MM-DD, or null if TBD
  pathway: "NDA",
  myProbability: 0.60, upside: 120, downside: 50,
  shares: 10, avgCost: 5.00, stopPct: 0.30,
  reviewStatus: "NDA under review. No AdCom planned.",
  thesis: "Your bull case.",       // string or array of bullet strings
  risks: "Key risks.",             // string or array
  keyDates: [{ date: "2027-03-15", label: "PDUFA decision" }],
  scenarios: {                     // optional: bull/base/bear planner
    bull: { p: 0.50, pct: 120, what: "Clean approval" },
    base: { p: 0.10, pct: 10,  what: "Approval, narrow label" },
    bear: { p: 0.40, pct: -50, what: "CRL" },
  },
  marketCap: "~$200M", cashRunway: "Q2 2027",
  sources: [["Press release", "https://..."]],
},
```

Ideas use the same fields minus `shares/avgCost/status`, plus `oneLiner`, `whyNow`, `refPrice`/`refDate` (fallback price), `plan` (entry/size/win/loss/stop) and `criteria` (runway/clean/liquid).

---

## How to Mark a Position Closed

Click **✅ Log exit** in the card footer. Enter the exit price, date and outcome (Win / Loss / Mixed) plus notes. The trade moves to the **Performance** tab and is saved in your browser. Use ↩ there to undo it.

---

## How to Export / Import Journal Data

**Export:** Open Settings (⚙ gear icon, top right) → click **Export Data (JSON)**. Saves a `.json` file with all journal entries, probability overrides, and decisions.

**Import:** Settings → **Import Data (JSON)** → select your backup file. Restores everything.

Do this before clearing browser data or switching machines.

---

## Cloudflare Pages Deployment

1. Create a GitHub repo (e.g. `catalyst-lab`)
2. Add `index.html`, `README.md`, `.nojekyll`
3. Push to GitHub
4. Go to [Cloudflare Pages](https://pages.cloudflare.com) → Create a project → Connect GitHub
5. Select the repo. Build settings:
   - **Build command:** (leave blank)
   - **Output directory:** `/` (or leave blank)
6. Deploy. Your site is live at `https://catalyst-lab-xxx.pages.dev`
7. Optional: add a custom domain in the Pages settings

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `1`–`6` | Switch tab (Overview, My Positions, New Ideas, Calendar, Performance, How it works) |
| `R` | Refresh all prices |
| `?` | Show shortcuts overlay |
| `Esc` | Close any modal/overlay |

---

## Linking Back to Your Dashboard

Add this to your main dashboard's nav or footer:

```html
<a href="https://your-catalyst-lab-url.pages.dev" target="_blank">⚗️ Catalyst Lab</a>
```

---

## ◎ Long-Term Portfolio (`portfolio.html`)

A second dashboard for the long-term holdings (16 holdings as of Nov 11: BRK.B, OKLO, CBRS, RKLB, RDW, ACIW, GPOR, ATEN, SPXC, TER, CGNX, GLPI, RIO, PFE, AQST, APMD. FSS, AYI, ADUS and an NVDA day trade are under Closed positions; SYM, FLNC and NRGV are planned buys on the Holdings tab). Open `portfolio.html`, or use the **◎ Portfolio** button in Catalyst Lab's top bar.

- **Three NYSE-style tapes:** equities and indices, ETFs, and FX, Treasury yields and bond ETFs. They stay pinned to the top of the screen as you scroll. Hover to pause.
- **Command Wheel:** the outer ring has one slice per holding, sized by weight, with a tick for today's move. Click a slice to load it in the center. The four inner quadrants (Position · Risk & Mitigants · Thesis & Catalysts · Valuation) each open their page. The center opens the full stock overview.
- **Tabs:** Dashboard · Holdings (sortable) · Risk Register (heat map plus auto-calculated portfolio risks) · Allocation (theme/style/sector, equal-weight drift, 1Y vs SPY) · Calendar (earnings with beat/miss, dividends, custom events) · Journal.
- **Editable:** risks and mitigants, thesis, catalysts, conviction, price levels, a buy/sell log that recalculates average cost, and adding or removing holdings. Edits are saved in localStorage. Back them up with ⚙ → Export JSON.
- **Data:** live prices come from Yahoo Finance (with CORS-proxy fallbacks, refreshed every 5 min). Until they load, the page uses a Nov 5, 2026 snapshot. Fundamentals, earnings dates and 1Y weekly history are embedded from that same snapshot.
- To change the base holdings, edit the `HOLDINGS` array at the top of the script.

---

## Zach's Portfolio (`zach.html`)

A blank copy of the long-term dashboard for Zach Cheney: same wheel, tapes, risk register, allocation, calendar and journal, with no holdings loaded. It opens to a welcome screen with **+ Add your first holding**. It keeps its own browser storage, so it never mixes with `portfolio.html` on the same site. To make holdings load on every device, list them in the `HOLDINGS` array at the top of the script (there's an example in the comment).
