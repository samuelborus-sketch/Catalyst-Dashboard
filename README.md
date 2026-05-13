# ⚗️ CATALYST LAB

Personal biotech catalyst tracking and analysis terminal. Tracks active FDA/trial catalyst positions, models probability and expected value, and logs pre/post analysis to improve decision-making over time.

---

## What This Is

A single `index.html` file that runs in any browser — no server, no npm, no build tools. Double-click to open locally or deploy to Cloudflare Pages for access anywhere.

**Key features:**
- Live prices from Yahoo Finance (auto-refreshes every 5 min)
- Probability gauge + EV calculator per position
- Catalyst countdown rings with urgency color system
- Scenario planner (Bull / Base / Bear) per card
- Inline probability editor with real-time sliders
- Decision Framework modal (6-step pre-catalyst checklist)
- Trade journal with timestamps (persists in localStorage)
- Pre-catalyst checklist per position
- Performance log with EV calibration chart
- Risk exposure summary by catalyst type and time bucket
- Full export/import of all journal + decision data

---

## How to Add a New Position

Open `index.html` in any text editor. Find the `CONFIG` block at the top of the `<script>` tag. Add a new entry to the `positions` array:

```javascript
{
  ticker: "ACME",
  company: "ACME Therapeutics",
  drug: "Drug Name (compound)",
  indication: "Disease — patient population",
  catalystType: "PDUFA",           // PDUFA | PhaseData | AdCom | Earnings | Other
  catalystDate: "2026-09-15",      // YYYY-MM-DD
  pathway: "NDA",                  // FDA pathway or trial phase
  myProbability: 0.60,             // 0–1, your estimate
  upside: 120,                     // % gain on success
  downside: 50,                    // % loss on failure
  shares: 10,
  avgCost: 5.00,
  stopPct: 0.30,                   // stop loss % below avg cost
  reviewStatus: "NDA under review. No InfoRequest issued.",
  thesis: "Your bull case here.",
  risks: "Key risks here.",
  keyDates: [
    { date: "2026-09-15", label: "PDUFA Decision" },
  ],
  analystTarget: 18.00,            // null if none
  marketCap: "~$200M",
  cashRunway: "Q2 2027",
},
```

---

## How to Mark a Position Closed

Click the **✅ Close** button in the card footer. Enter your exit price, outcome (Win / Loss / Mixed), and final notes. The position moves to the Performance Log automatically and your EV calibration chart updates.

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
| `R` | Refresh all prices |
| `?` | Show shortcuts overlay |
| `1`–`6` | Jump to position card by index |
| `D` | Open Decision Framework |
| `Esc` | Close any modal/overlay |

---

## Linking Back to Your Dashboard

Add this to your main dashboard's nav or footer:

```html
<a href="https://your-catalyst-lab-url.pages.dev" target="_blank">⚗️ Catalyst Lab</a>
```
