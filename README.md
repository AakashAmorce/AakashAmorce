### Aakash Desai

Product manager and engineer in Oakland, CA. Software and hardware.

Since 2024 I've run **Breakstep Group**, a software and product studio that builds data and tracking tools for clients and for my own products. Before that I spent almost four years at Ginkgo Bioworks working on biosecurity field hardware.

I build with Claude Code. I write the requirements and review the output until it holds up.

Most of my code is in private repos, because it is client work or my own products. This page describes those projects. The activity graph below includes private contributions.

---

#### What I'm building

| Project | What it is | Status | Stack |
|---|---|---|---|
| [**Limnal Research**](https://limnalresearch.com) · [overview](https://github.com/AakashAmorce/limnal-research-overview) | Daily macro-regime monitoring for active investors. Six independent models feed one allocation function that gives a single measure of current market risk. | Live, subscription | Python, FastAPI, Postgres, Supabase, Next.js, GitHub Actions |
| **TPO Watch** · [overview](https://github.com/AakashAmorce/tpo-watch-overview) | Keeps Just Cause eviction and rent-control tables current across 110 Bay Area jurisdictions for a legal services organization. Claude drafts each changed cell with a citation, and an analyst approves or rejects it. | In use by client | Python, Postgres (Supabase), Next.js, Claude API, GitHub Actions |
| [**Rent Facts**](https://rentfacts.io) · [overview](https://github.com/AakashAmorce/rent-facts-overview) | Tenant reviews from identity-verified renters, starting with 3,379 Oakland properties. It includes moderation and row-level security. | Live | TypeScript, Next.js, Supabase, Leaflet |
| [**Lineup**](https://lineup-pied.vercel.app) | A nonprofit-to-creator marketplace. It keeps raw, AI-derived, and human-confirmed records in separate tiers, with an append-only budget ledger. The demo runs on demo data. | Demo | TypeScript, Next.js, tRPC, Drizzle, Postgres, Claude API |
| **Sisturn** | A multi-tenant case-management prototype for workforce nonprofits. I remapped Lineup's data model into it in two days. | Prototype | TypeScript |

#### How I work

- **AI drafts and people review.** In TPO Watch, each proposal is pending until an analyst approves or rejects it, and approval writes a versioned value. I set the review rules with the people doing the reviewing.
- **Scheduled jobs that catch up.** Limnal's model runs were going missing with no error. I traced it to the scheduler dying when the server scaled to zero. I moved scheduling to GitHub Actions cron and added an idempotent catch-up job that backfills gaps without duplicates.
- **Cost controls.** In TPO Watch, weekly spend caps keep model costs inside the client's budget.

#### Hardware work at Ginkgo Bioworks

I was Product Manager III / R&D Lead, Physical Products, from 2020 to 2024. I took five biosecurity products through concept, prototype, field trials, and production. They included aircraft wastewater collection devices deployed at SFO, Boston Logan, and JFK.

I ran failure analysis on field failures, built test rigs, and added verification checks to assembly and refurbishment. The field failure rate fell from about 2% to 0.1% in six months.

#### Activity across all repos

<!-- STATS:START -->
_A GitHub Action updates this section each week._
<!-- STATS:END -->

---

[aakashdesai.com](https://aakashdesai.com) · [LinkedIn](https://www.linkedin.com/in/aakashdesai)
