# Mike dashboard

**Status:** plan, written before the code. This is the dashboard's own spec: what the client is, what each tab shows, and the approved mockup for each. The API it speaks is [`mike-dashboard-api.md`, the dashboard API contract](mike-dashboard-api.md). The domain it shows is [`mike.md`, the Mike spec](mike.md). Each tab gets its mockup here, inline, before it is built; a tab with no mockup is not ready to build.

## 1. What the dashboard is

The dashboard is how humans see and control Mike: the fleet, the board, the priorities list, review state, gauges, settings, logs, and every verb a human may run. It is a client of the **Mike dashboard API**, and it is the only client Mike ships; an attached session or a second client speaks the same API.

**The API is Mike's own contract**, written in [`mike-dashboard-api.md`, the dashboard API](mike-dashboard-api.md). Factory's dashboard API was the starting point for that file, nothing more: parts of it were never hardened, its spec text lagged its code, and it was shaped by one client. Nothing in Mike refers to factory's contract as law. What the Mike contract must hold:

- **One version, one gate.** The API carries a semantic version. An added field is a minor bump; a removed or renamed field, a changed meaning or a changed event name is a major bump. A client reads the version first and stops, saying it must be updated, on a major it was not built for. It never draws a half-compatible page. A test fails on any schema edit that has no version bump.
- **Live by push, complete by read.** One server-sent stream carries a frame per part (version, health, seats, board, priorities, review, gauges, settings, attached sessions, logs, jobs) when that part changes, with a keep-alive so a dead stream is noticed. Every part is also a plain JSON read, so a client that cannot hold a stream still works. No message broker.
- **A command is a job.** Every command returns a job id at once and reports its outcome (applied, refused, cancelled, with the why) by stream and by read, so a slow answer still lands where a human can see it. A command the caller may not run is refused with the caller matrix's reason, not hidden.
- **Reads cost nothing.** A health or sessions read makes no vendor call, no GitHub call, and no subprocess; it serves what the loop last wrote. A part the loop has not written is absent, and the client says so. It never draws ok for a missing part, and never 0 for unmeasured.
- **Verbs come from the server.** Each seat row lists the verbs that fit it now. The client enables a verb only when every selected row lists it, and derives nothing from liveness or any other field.
- **Identity is a verified bearer.** A human, an attached session, a seat, and a seat host each carry their own token; the route says which it needs; no header names a caller.
- **Times on the wire are ISO 8601 with offset.** The client never parses human prose.

## 2. The client

**The client is a full rewrite.** Factory's dashboard is not evolved, imported, or copied from. The user stories in [the user stories, section 1, dashboard and UI](mike-user-stories.md#1-dashboard-and-ui-stories) and [section 3, what the spec requires](mike-user-stories.md#3-stories-mikemd-requires-that-neither-source-had) are its requirements. What it must be that factory's page is not:

- **Responsive and phone-first.** Every tab lays out at 375 px with no horizontal page scroll; every single-seat verb has a touch path; a human on a phone can read the board, steer a seat, and request a merge.
- **A review surface**: ready pull requests by urgency and age, which reviewer holds each, each verdict, and send-backs with their owner seat.
- **The board** Arthur reads, shown to humans as Arthur sees it, with target versus actual share per lane and each row's note.
- **Gauges per runtime** with the mint threshold drawn against them, and unmeasured shown as unmeasured.
- **Attached sessions** on their own list with last call and token age, and a Revoke verb.
- **Edits survive a frame.** What a human is typing is never overwritten by a live update; the page diffs, it does not repaint.
- **Every command's outcome is visible** on the row it changed, however long it took.

## 3. The Seats tab and the seat card

The tab factory calls Sessions is the **Seats** tab in Mike. It shows every seat as one **seat card**, a single shared component, rendered the same way wherever a seat appears. Tig approved the mockup below on 2026-10-06. Its source is [`mockups/seat-card.html`, the seat card at desktop and phone widths](mockups/seat-card.html); open it to click the expander, the hamburger and the switch.

- **Card groups.** Cards sit in groups by role: orchestrators, lane-PEs, workers, reviewers. A group lays its cards out responsively: side by side at desktop widths, stacked at phone widths. The card's own inside is responsive too, by its container width, not the viewport's.
- **Info on top.** Name and role; liveness as a rectangular LED (green responding, red not-responding, gray unmeasured with the reason on hover, hollow not-minted) always beside its word, never color alone; the driver as runtime, vendor, access method and model; last mint; the assignment with the time it was assigned; the last steer, clipped, with the time it was delivered or that it is queued; context pressure as a bar gauge whose fill turns warning and then critical as the window fills; tokens since mint. An unmeasured value draws the word unmeasured and its reason, never 0 and never an empty bar.
- **Controls on the bottom.** A slider switch for start and stop, then Restart, Steer, Mint, Archive. A verb the row's `verbs` list does not carry is drawn disabled with the server's `verb_why` as its hover text; the client derives nothing.
- **Multi-select.** Each card has a checkbox; a selected card is outlined; a selection bar at the top of the tab names the selected seats and offers a verb only when every selected row lists it.
- **Phone.** Everything below the card's header collapses behind a Details expander; the four verbs collapse behind a hamburger menu; the start-stop switch stays visible. The selection bar's verbs sit behind a hamburger too. No horizontal page scroll at 375 px.
- **Live.** A card updates from the seats frame without a repaint of the tab, and an open expander, an open menu, or a half-typed steer survives the frame.

### 3.1 Desktop, 1180 px

![The Seats tab at 1180 px: four role groups, cards side by side, info on top and controls on the bottom of each card, two cards selected with the selection bar above](mockups/seat-card-desktop.png)

### 3.2 Phone, 375 px

<img src="mockups/seat-card-phone.png" width="375" alt="The Seats tab at 375 px: cards stacked, each with a Details expander and a hamburger for the verbs, the start-stop switch visible, one card expanded with its menu open">

## 4. Tabs still to mock up

Health, Board, Review, Priorities, Gauges, Settings, Logs, Attached sessions. Each lands here with a desktop and a phone image before its stories are built ([the user stories, section 1, dashboard and UI](mike-user-stories.md#1-dashboard-and-ui-stories)).
