# Mike

**Status:** plan. Written before the code. This is the contract for moms (the Mike rewrite). The factory agent-harness tree is reference, not law, for anything in this file. Where this file and factory disagree, this file wins for Mike.

**Sources read:** excaliwire/factory at [`bb2bf4c6`](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8) (2026-10-05): `agent-harness/`, `docs/specs/agent-harness.md`, `docs/specs/dashboard-api.md`, `docs/lexicon.md`; [factory#1336](https://github.com/excaliwire/factory/issues/1336) (the seat model) and its comments; [factory#1501](https://github.com/excaliwire/factory/issues/1501) (the extraction call, 2026-10-01); [#1](https://github.com/tig/mike/issues/1), [#2](https://github.com/tig/mike/issues/2). Tracking issue: [#3](https://github.com/tig/mike/issues/3).

**Companion files:** [`mike-user-stories.md`](mike-user-stories.md) (what each role needs, with the factory evidence for each) and [`mike-lexicon.md`](mike-lexicon.md) (every factory term: kept, renamed, retired, or challenged).

## 1. What Mike is

Mike is an operating system for a swarm of AI agents that work on GitHub repositories. One Mike instance runs the swarm for several repositories at once. It mints seats on vendors, steers them onto issues and pull requests, records every decision before it acts, holds the merge gate, and shows the operator one dashboard. Mike never merges. The human merges.

Mike is a clean-sheet rewrite of the factory agent harness. It keeps the harness's hard-won rules (section 9) and does not re-create its accidental complexity (section 10). The seat model is factory#1336, not the model on factory `main` today.

### 1.1 Three homes for a statement

Mechanism is code and tests. Behavior a seat must choose is the brief. Shape and intent are this spec. A rule that only one chat remembers is not a rule.

### 1.2 Multi-repository, one instance

An **instance** is one running Mike: one control plane, one loop, one store, one dashboard, one priorities list. A **project** is one repository the instance manages. An instance manages a set of projects; factory calls that set the program (`program.repositories`). Every verb that touches GitHub names the project. A repository not on the instance's list is refused before any call runs. There is no Mike deploy per repository (#2).

First-wave projects (#2): `excaliwire/web`, `excaliwire/app`, `tig/mike`, `tig/silico`, `kindel/kindelwww` and the Kindel apps. factory#1501 names `tig/goalie` as the first external target. The reference pattern is factory plus `Holy-Grail-Labs/squire` on one harness today.

## 2. Roles

A seat has a name and a role. What it does comes from the role. Names are instance config; Mike ships these defaults, and an instance may rename any of them without a code change (factory#1164 proved a rename touches no runtime code).

| Role key | Default name | What it does | Mints how |
|---|---|---|---|
| `arbiter` | Arthur | Judgment. Reads the board, decides which seat takes which issue, sets severity, orders send-backs, decides when to remint. Acts only through Mike's verbs. | By the human or the loop; one per instance. |
| `tpm` | K (Kay today) | Keeps briefs and the roster current, turns the human's direction into issues with a severity, audits technical direction across lanes. Writes no development pull request. | By the human or the loop; one per instance. |
| `lane-pe` | Factory PE, Presentation PE, Infrastructure PE | Technical judgment for one lane. Files issues with a severity and steers workers. Writes no development pull request. Minted wait-only (factory#1755). | Only by the human. |
| `worker` | Artificer | Takes one assignment to a ready pull request, then waits. Owns nothing beyond its assignment. | By the loop, from the pool. |
| `reviewer` | Warden | Independent review of one ready pull request it did not write. Never pushes. | By the loop, from the pool. |

### 2.1 Attached sessions: non-seats that act through Mike

A session the human drives (Infra Fable and Factory Fable today, the director's portal session, Excaliwire PgM) is not a seat. Mike does not mint it, steer it, assign it, or count it against the cap. It may still be **attached** to Mike, and then every repository and Mike interaction it makes goes through Mike's verbs, the same door a seat uses:

- The human issues it a named, revocable **session token** from the dashboard or CLI. The token names the session (its `[Name]` prefix) and the verbs it may run. It is not a seat token and not the human's token. There is no shared secret to derive it from.
- With the token it runs the same CLI as a seat: issue and pull verbs (create, label, severity, comment, request merge), read the board, sessions, health and priorities, and, when its config row allows, steer a seat. Every call records first with the session as `actor`, writes through Mike's GitHub choke point under Mike's account with the `[Name]` prefix, and is bound by every gate in 3.3. It never writes as the human, never merges, never mints.
- The dashboard shows attached sessions on their own list, with last call and token age, not on the Sessions tab.
- Attaching is optional and per session. A session that is not attached works as it does today, and Mike sees it only through GitHub; its comments carry no actor record. The brief tells a human-driven session to attach when the token is present.

The **director** is the attached session the human uses as his portal (Excaliwire PgM today). The caller matrix knows the human, the director, attached sessions, and seats; everything else is refused.

The arbiter brief on factory `main` says "I am mechanism, not judgment" ([`briefs/arbiter.md:19`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/arbiter.md)). That is the model factory#1336 replaces. In Mike, Arthur is judgment and Mike is mechanism. Harness engineering never lives in an orchestrator seat.

Authority: human > director > TPM > lane-PE > worker or reviewer. An attached session that is not the director has the authority its config row gives it, by default that of a lane-PE for steers and of any seat for issue and pull verbs. Only the human merges, waives a gate, or grants a reviewer.

## 3. The seat model (factory#1336)

### 3.1 Pool, assignment, share

- Seats are a **pool**. A worker or reviewer seat owns nothing beyond its current **assignment**: one issue or one pull request, or idle. The durable form of an assignment is the `seat:<name>` label on the issue or pull request. Mike's store caches it; the label is the truth.
- The **priorities list** has at most 3 rows, ordered. Each row names a lane. The config store holds a **share** per rank: top 60, second 30, third 10 percent of workers. The human adjusts the shares. A row with no open non-Low work gives its share to the next row.
- **Severity** orders work inside a lane: SEV1 (Urgent), High, Medium, then oldest first inside a severity. The GitHub field that carries severity is instance config (`Priority` on factory).
- **Nothing runs on Low.** An issue with no severity is Low.
- The **board** is what Arthur reads: idle seats, each seat's assignment, send-backs with the author seat, ready pull requests per seat, and target versus actual share per row. Mike builds it; today's orchestrator follow-up carries no board (factory `idle_steer.py:1279-1293`), so this is new.
- Arthur decides who does what. Mike enforces the gates in 3.3 for every caller, Arthur included, and shows target versus actual share on Health so a bad judgment is visible.

### 3.2 Mint, remint, steer

- A **mint** is wait-only and cheap: the seat reads its brief and stops at "Wait for the first steer". Work reaches a seat only through a **steer**. This holds for every role, lane-PEs included (factory#1755 measured 4.2M and 5.0M tokens in 30 minutes from a lane-PE mint that was not wait-only).
- A **remint** carries the assignment. The first steer after a remint is the same work. A seat is never steered across open work; it is reminted onto the same work. Reset Defaults clears every assignment and every `seat:` label in one recorded write.
- A mint run has a token and turn budget. A run over budget is cancelled with a record.
- Mint, archive, restart, and kill each write a decision record. Today the actuator writes only log lines for these (factory `seat_actuator.py:1499-1549`); Health cannot then show "no seat is minted twice for one issue".
- Mike mints no seat over one whose liveness is responding or unmeasured.

### 3.3 Gates Mike enforces for every caller

These are mechanism. They refuse with a recorded reason and the caller sees the why.

1. **Owner gate.** Only an issue or pull request assigned to Mike's GitHub user (`gh_user`; harness-gh-user today) may be steered. An empty or unmeasured setting refuses every steer.
2. **Project gate.** The repository is on the instance's project list. Today `cmd_steer` does not check this (factory `__main__.py:121, 1425`); Mike does.
3. **Lane gate.** A worker steer onto a lane that is not on the priorities list is refused.
4. **Severity floor.** A worker steer onto Low, or onto an issue with no severity, is refused.
5. **One pending steer.** No second steer to a seat while one is pending inside the loop window, for every caller and for every runtime, queued included. Today it holds only for the loop caller and only for `applied` rows (factory `__main__.py:1054-1080`).
6. **Record before act.** Every side effect has a decision record before it happens. `apply` refuses an unrecorded decision. A refusal is a record with its why.
7. **No mint over a seat whose liveness is responding or unmeasured.**
8. **Human switches.** Loop Paused and seat Stop are the two human switches. The loop acts on neither until a human changes them. Arthur may undo a Stop; nothing else may.
9. **Reviewer independence.** A reviewer never reviews its own pull request, and never pushes.
10. **No merge verb.** There is none. A test fails if one is added.

Everything else that factory's tick evaluates today, 45 holds and gates counted in factory#1336 section 2, is not re-created (section 10).

### 3.4 Review and send-back

- One reviewer per ready pull request. All reviewers review in parallel. A reviewer with a pull request does not take a second until it posts a verdict.
- A **send-back** goes to the author's seat as its next assignment. Nothing else is held. A ready pull request does not hold its author.
- Pull requests needing review are ordered by the time they went ready, oldest first.

### 3.5 What is judgment

Which seat takes which issue. The share actually given to each row this tick. When to remint. The order of send-backs. Recovery after a reboot. Whether a cross-lane theme maps onto a severity. These are Arthur's, with the board as input and Mike's verbs as the only output.

## 4. Runtimes and vendors

A seat runs on a **runtime** (factory calls this the seat's `harness`: `cursor-cloud`, `grok-tmux`, `claude-tmux`, `codex-tmux`, `claude-cloud`). A **vendor** is who bills it. Mike treats every runtime the same at its core:

| Capability | Every runtime must provide |
|---|---|
| mint | create a session for a seat, wait-only, returning a session id |
| steer | deliver one prompt and **confirm delivery** (a run id, a pane echo, or an event id). A steer that is not confirmed is not a steer, and the verb says so. |
| stop, restart, archive | each with a record |
| liveness | one of `not-minted`, `responding`, `not-responding`, `unmeasured` with a reason. No fifth word. Busy and idle are not liveness. |
| usage | tokens since mint, context pressure, and the vendor's included-pool percent, each `unmeasured` with a reason when not read |

Today the actuator is Cursor-shaped: mint steps are Cursor creates, grok-tmux has no archive, claude-cloud liveness is always unmeasured, and Health clears a row only on the Cursor record shape (factory#1336 comments, learnings 6, 9, 11; factory#1418). Mike has one actuator interface and one record shape, and each runtime fills it or reports unmeasured.

**Budgets.** Each vendor declares its pools, windows (such as Claude's 5-hour limit), a probe, and a mint threshold. Mint picks the next vendor when one crosses its threshold (factory#1501: at 75 percent of Claude's 5-hour limit, stop minting Claude seats). An unmeasured gauge stays unmeasured, never 0, and a mint that depends on an unmeasured gauge is refused. The gauge list is config, not a tuple in code (factory `meters.GAUGES`).

**Seat hosts pull.** A machine that runs tmux seats checks in and claims actuations from the store. The control plane holds no inbound path and no SSH key to a seat host. Every steer goes through the control plane store, from any caller on any machine. There is no second, machine-local queue.

**Identity.** A seat token names one seat and acts only as that seat. A session token names one attached session (2.1) and acts only as that session, with the verbs its config row lists. A host token names one host and pulls only its own actuations. There is no shared master secret on a seat host (factory#1413, host.md:258). The human is a verified bearer, not a header any local process can set.

## 5. The control plane

- **Control loop.** One tick: read desired state, read live state, decide, act. One loop per instance, from a checkout the instance owns. A tick does not overlap the previous one. Loop cadence, Running/Paused, and live/dry-run are config-store settings.
- **Desired state** is instance config: roles, roster, projects, lanes and labels, hosts, vendors and budgets, briefs. Shipped defaults and instance config are separate files. Changing desired state is a pull request on the instance's config repository.
- **Live state** is the store: assignments, session ids, liveness, gauges, records, settings versions. Never in git. The store is one process's responsibility, locked, and append-only where it is a log.
- **Config store.** Validated against a schema, versioned, append-only history, human-only writes, one log line per change with actor and from-to. Secrets by name only. A change applies live: reload, remint the affected seats, or swap a key, whichever is smallest (factory#1524).
- **Decision records.** Schema: who saw what, decided what, why, outcome (pending, applied, refused, cancelled), actor, caller. Every verb writes one. Health reads them. A refusal is a record.
- **One log.** `mike.jsonl`, rotated, structured, secrets redacted. A new signal is a log line first; a Health row only when a human needs to act on it.
- **GitHub.** One module runs `gh` or the API. A write as the human merger is refused. A read that fails is unmeasured, never empty. Reads are budgeted: below the reserve, the tick holds every GitHub-reading verb. Events arrive by signed webhook; polling the human's notifications is a fallback, not the design.

## 6. The pull request lifecycle

1. The worker opens the pull request as a draft early, labelled `seat:<name>`.
2. Owner self-review on the head commit: a comment `Self-Review: Done` naming `Head: <sha>`, written by the owner's `[Name]` prefix. Anything else does not count.
3. CI green on that head. The worker marks the pull request ready only then.
4. One reviewer is steered onto it. The review is at most 12 lines: line 1 `[Name] Recommendation: Merge|Send back|Hold on <sha>.`, one line per blocking finding as `file:line, what is wrong, the fix`, one `Ran:` line, the results table collapsed, `Next:` lines last. Non-blocking findings become issues, not comment text.
5. A new commit voids self-review, CI, and review. Every gate is per head sha.
6. Send back: the pull request returns to draft and the author's seat gets it as its next assignment.
7. Merge: self-review, CI, ready, and a `Merge` review on the same head. Mike assigns the human merger (config, `tig` on factory). The merger's assignment list is the merge queue. Mike never merges.
8. The human may waive a gate with `waive: <gate> [sha]` and grant a reviewer with `reviewer: <Name>`. No seat may write either.

Tests must fail on main and pass on the head. The reviewer's verb copies new tests onto a `main` worktree and runs them both sides, so "fails on main" is measured, not claimed.

## 7. The dashboard

The API contract moves unchanged from factory: [`docs/specs/dashboard-api.md`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/dashboard-api.md), the schema, `api_version` (6.6.1 at the read; the spec text there still describes 2.0.0 and omits the `settings` frame and route, which the code has), and the contract tests. A breaking change is a major bump. The page stops on a different major. Base path, origins and auth are config (#1).

The dashboard is one client of that API. It is rebuilt from a clean slate against the contract (#1). The stories it must satisfy are in [`mike-user-stories.md`](mike-user-stories.md), section 1. What the rewrite adds beyond today's page:

- A **review surface**: ready pull requests, which reviewer holds each, and each verdict. Today there is none.
- **Target versus actual share** per priority row (factory#1336 section 4).
- The **board** Arthur reads, as the human sees it.
- A **phone layout** for every tab. Today Sessions has 8 columns and no breakpoint, and single-seat verbs need a right-click.
- A **job id** for every command, so an answer after the 30-second timeout still lands on a row the human can see.
- Times on the wire are ISO 8601 with offset. The page never parses human prose.

The page derives no verb from any field. The row's `verbs` list is the only source. It draws unmeasured, never 0 and never ok, for a part the loop has not written.

## 8. Lexicon

Mike keeps the discipline: the lexicon is config, a term change is test-first, an outbound prompt is linted against the banned-terms table (Geas), and every review checks lexicon drift. The word list for a project comes from that project's hook, not from Mike.

The carry-over table, one row per factory term, is [`mike-lexicon.md`](mike-lexicon.md). The decisions that change a word:

| Factory term | Mike | Why |
|---|---|---|
| agent harness, the harness (the system) | **Mike** | The system has a name. "Harness" was also the per-seat run kind, so one word carried two meanings. |
| harness (a seat's `harness:` field) | **runtime** | The seat runs on a runtime; the vendor bills it. |
| harness-gh-user | **gh_user** | Follows the system rename. Same gate. |
| retarget, retarget-loop, retarget-pe, the ladder | **tick** for the loop; the ladder retires | The loop's name was a verb it rarely ran. Vendor budgets replace the ladder (section 4). |
| direction, direction list | **priorities list** | factory#1336 and the human say priorities. One word. |
| hold, hold word, none-eligible reason | retired | The planner that produced them is not re-created. |
| awaiting-response, lane owner, lane-starved as a hold | retired | Nothing is held but the gates in 3.3. lane-starved survives only as the lane gate's refusal text. |
| stand-down, resume | retired | A seat waiting on a gate is a steer Arthur writes ("wait for #N"), not a parallel hold mechanism. |
| meter | **gauge source** | A gauge is the reading; a meter was one way to scrape it. |
| arbiter = mechanism | arbiter = **judgment** | factory#1336. |
| board (new) | **board** | What Arthur reads each tick, section 3.1. |
| share (new) | **share** | Percent of workers a priority row gets. |
| pool (new) | **pool** | The worker and reviewer seats together. |
| runtime kind names (`cursor-cloud`, `grok-tmux`, `claude-cloud`) | kept | Each is a runtime. |
| droplet | **control-plane host** | Mike runs on any host. |
| claim (a vendor session) | **adopt** | Claim collides with a seat host claiming an actuation. |
| assign-tig, Assign Tig | **request merge** | The merger is config. |
| steer-idle (the verb) | **follow-up** | Only the orchestrator follow-up survives; the planner does not. |
| Lexicon: Clear (review line) | retired | Already retired on factory by #1741; the review's line 1 verdict carries it. |

New term, for the human to confirm: **attached session** (2.1). The audit had no word for a human-driven session that acts through Mike; factory says only "not a seat".

Terms kept as-is include: seat, role, mint, remint, steer, stop, archive, restart, assignment, liveness and its four words, decision record, record before act, control plane, control loop, seat host, data plane, desired state, live state, config store, fleet mode, hard reboot, orchestrator reboot, worker reboot, fill-missing, reset defaults, loop window, Running, Paused, live, dry-run, send-back, severity, lane, gauge, tier, temporary seat, director, Geas, banned term, address contract (`seat:<name>` owns, `[Name] ` writes, `Name:` addresses). Full table and the open challenges are in the lexicon file.

## 9. What Mike keeps

Each is a rule factory paid for. Evidence is the factory file at `bb2bf4c6` unless an issue is named.

1. Record before act. `records.py:1-14`.
2. Unmeasured is an answer. Never invent a percent, a liveness, a severity, a board. `liveness.py:1-24`.
3. One choke point for GitHub writes; never as the human; no merge verb. `gh.py:100-133`.
4. The merge path is a head-pinned state machine reading structured blocks, not prose. `merge_gate.py`, `pr_state.py:39-95`.
5. A test must fail on main and pass on the head, for code, config, schema, and briefs. Root `AGENTS.md:132-140`.
6. The lexicon is config; Geas lints every outbound prompt. `geas.py`.
7. One liveness vocabulary for every runtime; liveness is not assignment. `liveness.py:1-44`.
8. Delivery is confirmed, not assumed from enqueue. `seat_host.py:934`, factory#1630.
9. Mint is wait-only; remint carries the assignment; never steer across open work. factory#1336 section 3.
10. Stop and Paused are human switches. `seats.yaml:70`.
11. Config store: validated, versioned, append-only, human-only, logged. `settings.py:1258-1370`.
12. Caller matrix: seats do not mint; the arbiter steers; a lane-PE steers its own lane; a seat token acts on itself. `seats.yaml:59-77`.
13. Seat hosts pull; no inbound path on the control plane. `docs/host.md:258`.
14. One log; a new signal is a log line. `harness_log.py`.
15. Address contract: `seat:<name>` owns, `[Name] ` writes, `Name:` addresses. `poke.py:30-33`.
16. Names, roles, lanes, caps, repositories, hosts, vendors are config, not code. `policy.py:214-281`.
17. Health shows target versus actual share. factory#1336 section 4.
18. API contract versioned with a schema-digest test; the health read makes no vendor or GitHub call.
19. Secrets by name only: never in git, records, logs, or argv. `local.py:559`.
20. Comment limits: review 12 lines, pull request body 20, other 6, `Next:` last. `test_comment_limits_1741.py`.
21. Talking to the human: measurement not adjective, bad news first, recommendation not menu, decisions then merges then next, cost unasked. Root `AGENTS.md:84-96`.

## 10. What Mike does not re-create

Each is accidental complexity or a defect on factory `main`, with the evidence.

1. The steer-idle worker planner and its 45 holds and gates: 12 hold words, 12 none-eligible reasons, 9 wordless gates, 8 steer refusals beyond section 3.3, 4 review-idle holds. `idle_steer.py:39-56, 1628, 1834`; factory#1336 section 2.
2. Two deciders on one roster: a planner beside the arbiter, disagreeing (factory#1365).
3. Ten verbs per tick that can each steer or mint the same seat, patched by `_loop_steer_hold`. `retarget-loop.sh:79-100`.
4. Holds that strand capacity: awaiting-response, an idle reviewer held behind a busy one, a ready pull request holding its author. factory#1759, #1761, #1762.
5. Assignment in three places (label, actuator cache, steer records) with "taken" inferred from titles and pending creates.
6. A single-vendor actuator with per-runtime special paths. factory#1336 learnings 6, 11.
7. Machine-local steer queues and a second queue (`assignments.jsonl`, `assign`, `redeliver_tries`). learnings 7, 10.
8. A shared master secret on the seat host; a human gate that is a header. factory#1413; `host.md:99` versus `:258`.
9. Health that assumes one runtime's record shape, back-patched with a synthetic record. factory#1418.
10. Mint and archive that write no record.
11. Invariants that hold only for the loop caller.
12. Lane-PE mints that are not wait-only. factory#1755.
13. An orchestrator follow-up on a timer rhythm that carries no board. factory#1743.
14. A GitHub Discussion board publisher kept for retired boards (`dashboards.py`, 1300 dead lines).
15. An unlocked file store with newest-row-wins and whole-file scans per decision. `store.py:3-6, 597-789`.
16. Settings seeded from four places plus a self-healing migration.
17. Cursor busy/idle leaking as a third liveness reading.
18. Stand-down and resume as a parallel hold mechanism.
19. Screen-scraped vendor meters as the budget source where a usage API exists.
20. One-shot migration verbs kept in the product (retitle, seat-rename). A stable seat id makes rename a config edit.
21. Dashboard behaviors that patch the above: parsing server prose and human time strings, a 30-second command timeout with no job id, full repaint per log frame, a banned-word dodge in source (`rules.mjs:330`), hover text that re-derives a verb rule the server already answers.

## 11. Open decisions for the human

Each with a recommendation. Decisions 1 to 6 are factory#1336 section 7 and are repeated here because Mike's cut depends on them. A decided item says so and is closed.

1. Arthur each tick, or on each board change and each newly idle seat. Recommend: board change or idle seat.
2. Priority rows are lanes, or free text. Recommend: lanes.
3. Reviewer count: `ceil(workers / 3)` sizes the pool; inside it, one reviewer per ready pull request. Recommend that.
4. Mint cost is unmeasured. Recommend: measure 5 wait-only mints for 1 hour before the pool relies on remints.
5. conflict-steer and copilot-findings: keep as wakes until the planner is gone, then route each as a send-back. Recommend that.
6. The one priorities list is per instance, not per project. Lanes may belong to any project. Recommend per instance: the human has one attention.
7. **Decided, Tig, 2026-10-05: yes.** The system is Mike, not the harness, and the seat's run-kind field is renamed from `harness` to `runtime`.
8. **Decided, Tig, 2026-10-05: yes.** The priorities list replaces the word direction everywhere, including the API's `direction` command, at the major bump #1 already needs.
9. Shipped default names stay Arthurian (Arthur, K, Artificer, Warden). Recommend yes; an instance renames.
10. Which vendor the budget rule in factory#1501 means by "Groq": the call notes say Groq; the seats run xAI Grok. Needs the human's word.
11. Standing names or pool slots. Today every seat is a named row in `seats.yaml` (13 standing). Recommend: the pool is a cap and a list of names in config; Mike mints a name when the pool is below target and kills one only when stale or at the cap (factory#1336 section 1, point 6).
12. Does the lane-PE role exist in Mike. factory#1501 names one PE per lane; factory#1755 measured the cost of a mint that was not wait-only. Recommend: keep the role, human-minted only, wait-only, no ladder.
13. Two orchestrator seats (Arthur, K) or one. The control-versus-noticing split is documented on factory; factory#1336 gives Arthur the judgment. Recommend: keep two for the first cut, measure K's follow-ups for one week, then decide.
14. Does SEV1 (Urgent) preempt an open assignment. Its steer class on factory is `interrupt`, which steers a busy seat across work, and factory#1336 forbids that. Recommend: SEV1 sorts first and takes the next idle seat; it never preempts. The human may Stop a seat by hand.
15. **Decided, Tig, 2026-10-05: yes.** Stand-down and resume, the hold words, the PE ladder and its rungs, and `retarget` retire (section 8 table; lexicon section 2).
16. The word for a non-seat session that acts through Mike (2.1). Recommend **attached session**; the director is one. Its default rights: issue and pull verbs like a seat, steer like a lane-PE, no mint. Tig asked for the capability on 2026-10-05; the word and the default rights are his.

## 12. Done when

- The user stories in `mike-user-stories.md` each name a test or a measurement, and the LEGACY ones are not built.
- `mike-lexicon.md` has a verdict on every factory term and the human has edited it.
- moms passes the ported contract tests with an empty `PINNED` list, from an install with no factory checkout, managing two projects from one instance.
- A tick with idle workers writes no planner row; Arthur's steers pass the section 3.3 gates; Health shows target versus actual share.
