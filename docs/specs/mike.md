# Mike

**Status:** plan. Written before the code. This is the contract for moms (the Mike rewrite). The factory agent-harness tree is reference, not law, for anything in this file. Where this file and factory disagree, this file wins for Mike.

**Sources read:** excaliwire/factory at [`bb2bf4c6`](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8) (2026-10-05): `agent-harness/`, `docs/specs/agent-harness.md`, `docs/specs/dashboard-api.md`, `docs/lexicon.md`; [factory#1336](https://github.com/excaliwire/factory/issues/1336) (the seat model) and its comments; [factory#1501](https://github.com/excaliwire/factory/issues/1501) (the extraction call, 2026-10-01); [#1](https://github.com/tig/mike/issues/1), [#2](https://github.com/tig/mike/issues/2). Tracking issue: [#3](https://github.com/tig/mike/issues/3).

**Companion files:** [`mike-user-stories.md`](mike-user-stories.md) (what each role needs, with the factory evidence for each) and [`mike-lexicon.md`](mike-lexicon.md) (every factory term: kept, renamed, retired, or challenged).

## 1. What Mike is

Mike is an operating system for a swarm of AI agents that work on GitHub repositories. One Mike instance runs the swarm for several repositories at once. It mints seats on vendors, steers them onto issues and pull requests, records every decision before it acts, holds the merge gate, and shows the operator one dashboard. Mike never merges. A human merges.

Mike is a clean-sheet rewrite of the factory agent harness. It keeps the harness's hard-won rules (section 9) and does not re-create its accidental complexity (section 10). The seat model is factory#1336, not the model on factory `main` today.

### 1.1 Three homes for a statement

Mechanism is code and tests. Behavior a seat must choose is the brief. Shape and intent are this spec. A rule that only one chat remembers is not a rule.

### 1.2 Multi-repository, one instance

An **instance** is one running Mike: one control plane, one loop, one store, one dashboard, one priorities list. A **project** is one repository the instance manages. An instance manages a set of projects; factory calls that set the program (`program.repositories`). Every verb that touches GitHub names the project. A repository not on the instance's list is refused before any call runs. There is no Mike deploy per repository (#2).

First-wave projects (#2): `excaliwire/web`, `excaliwire/app`, `tig/mike`, `tig/silico`, `kindel/kindelwww` and the Kindel apps. factory#1501 names `tig/goalie` as the first external target. The reference pattern is factory plus `Holy-Grail-Labs/squire` on one harness today.

## 2. Roles

A seat has a name and a role. What it does comes from the role. Mike ships no display names: a role's name is its role key (`arbiter`, `tpm`, `lane-pe`, `worker`, `reviewer`) unless the instance config overrides it, and an override touches no runtime code (factory#1164 proved that). The Arthurian names below are factory's instance config, not Mike's (decision 9).

| Role key | Factory's name | What it does | Mints how |
|---|---|---|---|
| `arbiter` | Arthur | Judgment. Reads the board, decides which seat takes which issue, sets severity, orders send-backs, decides when to remint. Acts only through Mike's verbs. | By a human or the loop; one per instance. |
| `tpm` | K (Kay today) | Keeps briefs and the roster current, turns a human's direction into issues with a severity, audits technical direction across lanes. Writes no development pull request. | By a human or the loop; one per instance. |
| `lane-pe` | Factory PE, Presentation PE, Infrastructure PE | Technical judgment for one lane. Files issues with a severity and steers workers. Writes no development pull request. Minted wait-only (factory#1755). | By a human, or by the loop when the role's fill-missing setting is on; that setting asks a human before it turns on. |
| `worker` | Artificer | Takes one assignment to a ready pull request, then waits. Owns nothing beyond its assignment. | By the loop, from the pool. |
| `reviewer` | Warden | Independent review of one ready pull request it did not write. Never pushes. | By the loop, from the pool. |

### 2.1 Humans

Mike serves humans, plural. Several humans create issues, comment on issues and pull requests, review, assign, and merge, each as themselves on GitHub, not through Mike. Instance config lists them by GitHub login. Mike text and the dashboard say "a human" or "humans"; a name (Tig on factory) is instance config.

What a listed human's GitHub activity means to Mike, each routed by the control plane as a change (section 5, rule 22):

- An issue a listed human creates or edits is on the board once it carries a lane and is assigned to `gh_user`. Assigning it is the handoff: before that it is theirs, after that it is Mike's. The severity they set is the severity; none set is Low.
- A comment addressed `Name:` on an issue or pull request is a steer to that seat, carrying the comment. A comment with no address is context on the board, not a steer.
- A review verdict or a review comment from a listed human on a ready pull request is a send-back to the author seat when it asks for a change, and counts as the independent review when it says Merge (config: `human_review_counts`).
- `waive: <gate> [sha]` and `reviewer: <Name>` from a listed human bind the gates. From anyone else they are text.
- Any listed human may merge, issue a session token, and edit the priorities list and the config store. The record names which human acted.

A GitHub user not on the list is a contributor. Their issues and comments are shown on the board and routed nowhere; a listed human or K triages them (assigns, sets severity, addresses a seat). A human is a verified bearer on the API, never a header. A human is not a seat and not an attached session; where a human drives an agent session that should act through Mike, that session attaches (2.2).

### 2.2 Attached sessions: non-seats that act through Mike

A session a human drives (Infra Fable and Factory Fable today, the director's portal session, Excaliwire PgM) is not a seat. Mike does not mint it, steer it, assign it, or count it against the cap. It may still be **attached** to Mike, and then every repository and Mike interaction it makes goes through Mike's verbs, the same door a seat uses:

- A human issues it a named, revocable **session token** from the dashboard or CLI. The token names the session (its `[Name]` prefix) and the verbs it may run. It is not a seat token and not a human's token. There is no shared secret to derive it from.
- With the token it runs the same CLI as a seat: issue and pull verbs (create, label, severity, comment, request merge), read the board, sessions, health and priorities, and, when its config row allows, steer a seat. Every call records first with the session as `actor`, writes through Mike's GitHub choke point under Mike's account with the `[Name]` prefix, and is bound by every gate in 3.3. It never writes as a human, never merges, never mints.
- The dashboard shows attached sessions on their own list, with last call and token age, not on the Sessions tab.
- Attaching is optional and per session. A session that is not attached works as it does today, and Mike sees it only through GitHub; its comments carry no actor record. The brief tells a human-driven session to attach when the token is present.

The **director** is the attached session a human uses as his portal (Excaliwire PgM today). The caller matrix knows a human, the director, attached sessions, and seats; everything else is refused.

The arbiter brief on factory `main` says "I am mechanism, not judgment" ([`briefs/arbiter.md:19`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/arbiter.md)). That is the model factory#1336 replaces. In Mike, Arthur is judgment and Mike is mechanism. Harness engineering never lives in an orchestrator seat.

Authority: humans > director > TPM > lane-PE > worker or reviewer. An attached session that is not the director has the authority its config row gives it, by default that of a lane-PE for steers and of any seat for issue and pull verbs. Only a human merges, waives a gate, or grants a reviewer.

## 3. The seat model (factory#1336)

### 3.1 Pool, assignment, share

- Seats are a **pool**. A worker or reviewer seat owns nothing beyond its current **assignment**: one issue or one pull request, or idle. The durable form of an assignment is the `seat:<name>` label on the issue or pull request. Mike's store caches it; the label is the truth.
- The **priorities list** has at most 3 rows, ordered. Each row names a lane and may carry a **note**: a human's intent for that row in a sentence. Mike puts the note on the board Arthur reads and in every steer to that lane's lane-PE, as context. The note binds nothing; the lane does. The config store holds a **share** per rank: top 60, second 30, third 10 percent of workers. A human adjusts the shares. A row with no open non-Low work gives its share to the next row.
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

**Budgets.** Each vendor declares its pools, windows (such as Claude's 5-hour limit), a probe, and a mint threshold. Mint picks the next vendor when one crosses its threshold (factory#1501: at 75 percent of Claude's 5-hour limit, stop minting Claude seats and shift new seats to xAI Grok; decision 10). An unmeasured gauge stays unmeasured, never 0, and a mint that depends on an unmeasured gauge is refused. The gauge list is config, not a tuple in code (factory `meters.GAUGES`).

**Seat hosts pull.** A machine that runs tmux seats checks in and claims actuations from the store. The control plane holds no inbound path and no SSH key to a seat host. Every steer goes through the control plane store, from any caller on any machine. There is no second, machine-local queue.

**Identity.** A seat token names one seat and acts only as that seat. A session token names one attached session (2.2) and acts only as that session, with the verbs its config row lists. A host token names one host and pulls only its own actuations. There is no shared master secret on a seat host (factory#1413, host.md:258). A human is a verified bearer, not a header any local process can set.

## 5. The control plane

- **The control plane is the only watcher.** It takes GitHub events by signed webhook and diffs its own store each tick: an issue assigned, a pull request from draft to ready, a review verdict, a send-back, a conflict, unresolved Copilot threads, a seat gone idle. Each change is routed to the seat it concerns as a recorded steer bound by the gates: Arthur gets the board when the board changed or a seat went idle; the author seat gets its send-back, conflict or Copilot findings; a reviewer gets a ready pull request. No seat polls GitHub. No vendor scheduler or routine-fire watches anything for Mike. Nothing fires on a timer except the tick itself.
- **Control loop.** One tick: read desired state, read live state, decide, act. One loop per instance, from a checkout the instance owns. A tick does not overlap the previous one. Loop cadence, Running/Paused, and live/dry-run are config-store settings.
- **Desired state** is instance config: roles, roster, projects, lanes and labels, hosts, vendors and budgets, briefs. Shipped defaults and instance config are separate files. Changing desired state is a pull request on the instance's config repository.
- **Live state** is the store: assignments, session ids, liveness, gauges, records, settings versions. Never in git. The store is one process's responsibility, locked, and append-only where it is a log.
- **Config store.** Validated against a schema, versioned, append-only history, human-only writes, one log line per change with actor and from-to. Secrets by name only. A change applies live: reload, remint the affected seats, or swap a key, whichever is smallest (factory#1524).
- **Decision records.** Schema: who saw what, decided what, why, outcome (pending, applied, refused, cancelled), actor, caller. Every verb writes one. Health reads them. A refusal is a record.
- **One log.** `mike.jsonl`, rotated, structured, secrets redacted. A new signal is a log line first; a Health row only when a human needs to act on it.
- **GitHub.** One module runs `gh` or the API. A write as a human merger is refused. A read that fails is unmeasured, never empty. Reads are budgeted: below the reserve, the tick holds every GitHub-reading verb. Events arrive by signed webhook; polling a human's notifications is a fallback, not the design.

## 6. The pull request lifecycle

1. The worker opens the pull request as a draft early, labelled `seat:<name>`.
2. Owner self-review on the head commit: a comment `Self-Review: Done` naming `Head: <sha>`, written by the owner's `[Name]` prefix. Anything else does not count.
3. CI green on that head. The worker marks the pull request ready only then.
4. One reviewer is steered onto it. The review is at most 12 lines: line 1 `[Name] Recommendation: Merge|Send back|Hold on <sha>.`, one line per blocking finding as `file:line, what is wrong, the fix`, one `Ran:` line, the results table collapsed, `Next:` lines last. Non-blocking findings become issues, not comment text.
5. A new commit voids self-review, CI, and review. Every gate is per head sha.
6. Send back: the pull request returns to draft and the author's seat gets it as its next assignment.
7. Merge: self-review, CI, ready, and a `Merge` review on the same head. Mike assigns a human merger (config, `tig` on factory). The merger's assignment list is the merge queue. Mike never merges.
8. A human may waive a gate with `waive: <gate> [sha]` and grant a reviewer with `reviewer: <Name>`. No seat may write either.

Tests must fail on main and pass on the head. The reviewer's verb copies new tests onto a `main` worktree and runs them both sides, so "fails on main" is measured, not claimed.

## 7. The dashboard

The API contract moves unchanged from factory: [`docs/specs/dashboard-api.md`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/dashboard-api.md), the schema, `api_version` (6.6.1 at the read; the spec text there still describes 2.0.0 and omits the `settings` frame and route, which the code has), and the contract tests. A breaking change is a major bump. The page stops on a different major. Base path, origins and auth are config (#1).

The dashboard is one client of that API. It is rebuilt from a clean slate against the contract (#1). The stories it must satisfy are in [`mike-user-stories.md`](mike-user-stories.md), section 1. What the rewrite adds beyond today's page:

- A **review surface**: ready pull requests, which reviewer holds each, and each verdict. Today there is none.
- **Target versus actual share** per priority row (factory#1336 section 4).
- The **board** Arthur reads, as a human sees it.
- A **phone layout** for every tab. Today Sessions has 8 columns and no breakpoint, and single-seat verbs need a right-click.
- A **job id** for every command, so an answer after the 30-second timeout still lands on a row a human can see.
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
| direction, direction list | **priorities list** | factory#1336 and a human say priorities. One word. |
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

New term, confirmed by a human 2026-10-05: **attached session** (2.2). The audit had no word for a human-driven session that acts through Mike; factory says only "not a seat".

Terms kept as-is include: seat, role, mint, remint, steer, stop, archive, restart, assignment, liveness and its four words, decision record, record before act, control plane, control loop, seat host, data plane, desired state, live state, config store, fleet mode, hard reboot, orchestrator reboot, worker reboot, fill-missing, reset defaults, loop window, Running, Paused, live, dry-run, send-back, severity, lane, gauge, tier, temporary seat, director, Geas, banned term, address contract (`seat:<name>` owns, `[Name] ` writes, `Name:` addresses). Full table and the open challenges are in the lexicon file.

## 9. What Mike keeps

Each is a rule factory paid for. Evidence is the factory file at `bb2bf4c6` unless an issue is named.

1. Record before act. `records.py:1-14`.
2. Unmeasured is an answer. Never invent a percent, a liveness, a severity, a board. `liveness.py:1-24`.
3. One choke point for GitHub writes; never as a human; no merge verb. `gh.py:100-133`.
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
21. Talking to humans: measurement not adjective, bad news first, recommendation not menu, decisions then merges then next, cost unasked. Root `AGENTS.md:84-96`.
22. The control plane is the only watcher; a change is routed to the seat it concerns as a steer; no seat polls and no vendor watches (section 5). Tig, 2026-10-05.

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

## 11. Decisions

All 16 decided by Tig on 2026-10-05. Decisions 1 to 6 are factory#1336 section 7 and are repeated here because Mike's cut depends on them. Decision 4 closes when factory#1778 posts its number.

1. **Decided, Tig, 2026-10-05.** The control plane detects every change (section 5, rule 22) and steers Arthur when the board changed or a seat went idle. Never on a timer. No seat or vendor watches.
2. **Decided, Tig, 2026-10-05: a lane plus an optional note.** The lane binds the gate and the share; the note is a human's intent, shared with Arthur on the board and with that lane's lane-PE as context (3.1).
3. **Decided, Tig, 2026-10-05.** `ceil(workers / 3)` caps the reviewer pool; inside it, one reviewer per ready pull request, all in parallel.
4. **Decided, Tig, 2026-10-05: measure first, on the existing harness.** [factory#1778](https://github.com/excaliwire/factory/issues/1778): 5 wait-only mints left 1 hour, tokens, turns, dollars and first-steer cost per seat. The number closes this decision; the remint-not-steer rule is built on it.
5. **Decided by decision 1, 2026-10-05.** conflict-steer and copilot-findings are not verbs. A conflict and an unresolved Copilot thread set are two change kinds the control plane routes to the author seat as a steer.
6. **Decided, Tig, 2026-10-05: per instance.** One list across every project the instance manages. A lane may belong to any project.
7. **Decided, Tig, 2026-10-05: yes.** The system is Mike, not the harness, and the seat's run-kind field is renamed from `harness` to `runtime`.
8. **Decided, Tig, 2026-10-05: yes.** The priorities list replaces the word direction everywhere, including the API's `direction` command, at the major bump #1 already needs.
9. **Decided, Tig, 2026-10-05: role keys are the names unless overridden.** Mike ships no display names. The Arthurian names are factory's instance config (section 2).
10. **Decided, Tig, 2026-10-05: xAI Grok.** The budget rule in factory#1501 shifts new seats to xAI Grok, the vendor the workers and reviewers run on, not Groq.
11. **Decided, Tig, 2026-10-05: pool.** Config holds a cap and a list of names. Mike mints a name when the pool is below target and kills one only when stale or at the cap (factory#1336 section 1, point 6).
12. **Decided, Tig, 2026-10-05: keep the role, and Mike may mint it.** One PE per lane, wait-only, no ladder. The loop mints a missing lane-PE when the role's fill-missing setting is on; turning it on asks a human first, because each mint spends money. A project may configure zero lane-PEs.
13. **Decided, Tig, 2026-10-05: keep two, measure a week.** Arthur and K stay separate roles. Mike measures K's follow-ups per hour for one week after the first cut, recorded on #3, then a human decides whether K merges into Arthur.
14. **Decided, Tig, 2026-10-05: sorts first, never preempts.** SEV1 takes the next idle seat. No seat is steered across open work. A human may Stop a seat by hand.
15. **Decided, Tig, 2026-10-05: yes.** Stand-down and resume, the hold words, the PE ladder and its rungs, and `retarget` retire (section 8 table; lexicon section 2).
16. **Decided, Tig, 2026-10-05: yes.** The word is **attached session**; the director is one. Default rights: issue and pull verbs like a seat, steer like a lane-PE, no mint.

## 12. Done when

- The user stories in `mike-user-stories.md` each name a test or a measurement, and the LEGACY ones are not built.
- `mike-lexicon.md` has a verdict on every factory term and a human has edited it.
- moms passes the ported contract tests with an empty `PINNED` list, from an install with no factory checkout, managing two projects from one instance.
- A tick with idle workers writes no planner row; Arthur's steers pass the section 3.3 gates; Health shows target versus actual share.
