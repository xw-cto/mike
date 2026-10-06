# Mike

**Status:** plan. Written before the code. This is the contract for moms (the Mike rewrite). The factory agent-harness tree is reference, not law, for anything in this file. Where this file and factory disagree, this file wins for Mike.

**Sources read:** excaliwire/factory at [factory at commit bb2bf4c6, the tree this spec read](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8) (2026-10-05): `agent-harness/`, `docs/specs/agent-harness.md`, `docs/specs/dashboard-api.md`, `docs/lexicon.md`; [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) and its comments; [factory#1501, the extraction call of 2026-10-01](https://github.com/excaliwire/factory/issues/1501); [tig/mike#1, the dashboard rewrite](https://github.com/tig/mike/issues/1); [tig/mike#2, the master plan](https://github.com/tig/mike/issues/2). Tracking issue: [tig/mike#3, this spec](https://github.com/tig/mike/issues/3).

**Companion files:** [`stories/`, the user stories by job: what each role needs](stories/README.md) with the factory evidence for each; [`mike-lexicon.md`, every factory term kept, renamed, retired or challenged](mike-lexicon.md); [`mike-dashboard.md`, the dashboard with its mockups](mike-dashboard.md); [`mike-dashboard-api.md`, the dashboard API contract](mike-dashboard-api.md).

**Self-contained.** These files define Mike completely. A link to factory is provenance, where a rule or a story came from, never a definition a reader must go and fetch. Factory's specs are not Mike's contract.

## 1. What Mike is

Mike is an operating system for a swarm of AI agents that work on GitHub repositories. One Mike instance runs the swarm for several repositories at once. It mints seats on any AI vendor's harness, either through APIs or by controlling a terminal session via tmux. Mike steers those seats onto issues and pull requests, records every decision before it acts, ensures the criteria for making a pull request ready to merge are met, and provides a rich dashboard for monitoring and controlling the operating system. To ensure a human is "on the loop", Mike never merges pull requests; instead it assigns a pull request that has been deemed ready to merge to a human.

Mike is a clean-sheet rewrite of the Excaliwire factory agent harness. It keeps the harness's hard-won rules ([section 9, what Mike keeps](#9-what-mike-keeps)) and does not re-create its accidental complexity ([section 10, what Mike does not re-create](#10-what-mike-does-not-re-create)). The seat model is the one in [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336), not the model on factory `main` today.

### 1.1 Where each kind of rule lives

Mike's rules live in three places, and each place holds one kind of rule:

- **Code and tests** hold what Mike enforces. If Mike refuses an action, the refusal is code, and a test proves it.
- **The brief** a seat reads at mint holds what a seat must decide for itself and Mike cannot check: how to review, when to ask a human, how to write a comment.
- **This spec** holds what Mike is for and the shape it must have. It is what the code is tested against.

A rule written anywhere else, in a chat, a pull request comment, or one agent's memory, is not a rule. If it matters, it moves into one of the three places.

### 1.2 Multi-repository, one instance

An **instance** is one running Mike: one control plane, one loop, one store, one dashboard, one priorities list. A **project** is one repository the instance manages. An instance manages a set of projects; the set of projects is called the **program** (`program.repositories`). Every verb that touches GitHub names the project.

You run one Mike for all of your repositories. You do not install or run a separate Mike for each repository ([tig/mike#2, the master plan, "cross-repo requirement"](https://github.com/tig/mike/issues/2)).

### 1.3 Overlapping instances

Two Mike instances may manage the same repository, for example a project that two organizations each run a swarm on, or a staging Mike beside a production one. Mike does not solve for this in the first cut. This section says how the overlap shows and what keeps it harmless.

GitHub is the shared surface. Everything an instance reads from a repository, another instance can also read, write, or claim.

| Where they overlap | How a conflict shows | What keeps it harmless |
|---|---|---|
| **`gh_user`**, the owner gate. Each instance steers only issues and pull requests assigned to its own GitHub user. | Two instances with the same `gh_user` both see every assigned issue, both route it to a seat, and the issue ends with two `seat:` labels and two pull requests. | Each instance has its own GitHub user. A human assigns an issue to one of them. An issue assigned to two Mike users is a human's mistake, and the first cut does not detect it. |
| **Seat names**, in `seat:<name>` labels, `[Name]` writer prefixes, `To: Name` addresses, branch names and tmux session names. | Two instances that both have an Avalon each read `seat:Avalon` as their own, both route `To: Avalon` as a steer, and on a shared seat host both try to own one tmux session. | Seat names are unique across every instance that touches a repository, orchestrator names included: instance config renames any role, so one instance's Arthur is another's Merlin. |
| **Unknown labels and names.** An instance meets `seat:` labels, `[Name]` prefixes and `To:` addresses it did not issue. | Treated as anomalies, they turn Health red for the other instance's normal work; treated as steers, they misfire. | An instance treats a seat label or name it does not know the way it treats a contributor's: shown on the board as another owner's work, routed nowhere, never a finding. |
| **Webhooks and reads.** Every instance receives every event for the repository and reads the same issues. | Each instance's GitHub read budget is spent on the other's events; the reserve trips sooner. | Each instance drops at ingress every event that names no seat, label or user of its own. The budget is per instance, so the cost is load, not a wrong action. |
| **Lanes and urgency labels.** Both instances read the same label set. | An issue whose lane is one instance's and not the other's is simply refused by the other's lane gate. No conflict, as long as `gh_user` differs. | Lane labels may be shared or disjoint; the urgency labels are one vocabulary and are shared. |
| **The human merger.** Both instances assign ready pull requests to the same human. | One merge queue holds two instances' work with no mark of which. | The `[Name]` prefix and the `seat:` label name the instance's seat, and unique names make the source readable. |
| **Grants.** `waive:` and `reviewer:` are text in the repository that both instances read. | A grant naming the other instance's seat is read by both. | A grant binds only a gate the reading instance holds; one naming an unknown seat is text to it. |

The one case the mitigations do not cover is two instances that share a `gh_user` or a seat name; that produces the first two rows and the first cut does not detect it. A later cut may let an instance list its peers so it can refuse an issue assigned to two Mike users and flag a duplicate name; that is a decision for then.

## 2. Roles

A seat has a name and a role. What it does comes from the role. Mike ships no display names: a role's name is its role key (`arbiter`, `tpm`, `lane-pe`, `worker`, `reviewer`) unless the instance config overrides it, and an override touches no runtime code. The Arthurian names below are factory's instance config, not Mike's.

| Role key | Factory's name | What it does | Mints how |
|---|---|---|---|
| `arbiter` | Arthur | Judgment. Reads the board, decides which seat takes which issue, sets urgency, orders send-backs, decides when to remint. Acts only through Mike's verbs. | By a human or the loop; one per instance. |
| `tpm` | K (Kay today) | Keeps briefs and the roster current, turns a human's direction into issues with an urgency, audits technical direction across lanes. Writes no development pull request. | By a human or the loop; one per instance. |
| `lane-pe` | Factory PE, Presentation PE, Infrastructure PE | Technical judgment for one lane. Files issues with an urgency and steers workers. Writes no development pull request. Minted wait-only. | By a human, or by the loop when the role's fill-missing setting is on; that setting asks a human before it turns on. |
| `worker` | Artificer | Takes one assignment to a ready pull request, then waits. Owns nothing beyond its assignment. | By the loop, from the pool. |
| `reviewer` | Warden | Independent review of one ready pull request it did not write. Never pushes. | By the loop, from the pool. |

### 2.1 Humans

Mike serves humans, plural. Several humans create issues, comment on issues and pull requests, review, assign, and merge, each as themselves on GitHub, not through Mike. Instance config lists them by GitHub login. Mike text and the dashboard say "a human" or "humans"; a name (Tig on factory) is instance config.

What a listed human's GitHub activity means to Mike, each routed by the control plane as a change ([section 5, the control plane](#5-the-control-plane)):

- An issue a listed human creates or edits is on the board once it carries a lane label and is assigned to `gh_user`. Assigning it is the handoff: before that it is theirs, after that it is Mike's. The urgency label they set is the urgency; none set is `urgency:no`.
- A comment that starts `To: Name` (or `To: Name, Other`) on an issue or pull request is a steer to that seat, carrying the comment. A comment with no `To:` is context on the board, not a steer. `To:` is the email and Usenet header word; it is a word, not a glyph, so a phone keyboard cannot turn it into something else ([section 9, rule 15, the address contract](#9-what-mike-keeps)).
- A review verdict or a review comment from a listed human on a ready pull request is a send-back to the owner seat when it asks for a change, and counts as the independent review when it says Merge (config: `human_review_counts`).
- `waive: <gate> [sha]` and `reviewer: <Name>` from a listed human bind the gates. From anyone else they are text.
- Any listed human may merge, issue a session token, and edit the priorities list and the config store. The record names which human acted.

A GitHub user not on the list is a contributor. Their issues and comments are shown on the board and routed nowhere; a listed human or K triages them (assigns, sets urgency, addresses a seat). A human is a verified bearer on the API, never a header. A human is not a seat and not an attached session; where a human drives an agent session that should act through Mike, that session attaches ([section 2.2, attached sessions](#22-attached-sessions-non-seats-that-act-through-mike)).

### 2.2 Attached sessions: non-seats that act through Mike

A session a human drives (for example Infra Fable and Factory Fable today, or the director's portal session, Excaliwire PgM) is not a seat. Mike does not mint sessions, steer them, assign them, or count them against the cap. They may still be **attached** to Mike, and then every repository and Mike interaction a session makes goes through Mike's verbs, the same door a seat uses:

- A human issues it a named, revocable **session token** from the dashboard or CLI. The token names the session (its `[Name]` prefix) and the verbs it may run. It is not a seat token and not a human's token. There is no shared secret to derive it from.
- With the token it runs the same CLI as a seat: issue and pull verbs (create, label, urgency, comment, request merge), read the board, sessions, health and priorities, and, when its config row allows, steer a seat. Every call records first with the session as `actor`, writes through Mike's GitHub choke point under Mike's account with the `[Name]` prefix, and is bound by every gate in [section 3.3, the gates](#33-gates-mike-enforces-for-every-caller). It never writes as a human, never merges, never mints.
- The dashboard shows attached sessions on their own list, with last call and token age, not on the Seats tab.
- Attaching is optional and per session. A session that is not attached works as it does today, and Mike sees it only through GitHub; its comments carry no actor record. The brief tells a human-driven session to attach when the token is present.

The **director** is the attached session a human uses as a portal (Excaliwire PgM today). The caller matrix knows a human, the director, attached sessions, and seats; everything else is refused.

The arbiter brief on factory `main` says "I am mechanism, not judgment" ([factory `briefs/arbiter.md` line 19, the arbiter's self-description](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/arbiter.md#L19)). That is the model [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) replaces. In Mike, Arthur is judgment and Mike is mechanism. Harness engineering never lives in an orchestrator seat.

Authority: humans > director > TPM > lane-PE > worker or reviewer. An attached session that is not the director has the authority its config row gives it, by default that of a lane-PE for steers and of any seat for issue and pull verbs. Only a human merges, waives a gate, or grants a reviewer.

## 3. The seat model

The model is the one in [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336), as amended by the review of this file.

**Lanes.** A **lane** is a large architectural body of work within the program, the set of projects one instance manages. A program has one or more lanes; factory has three (Infrastructure, Factory, Presentation). An issue belongs to exactly one lane, marked by its lane label. Lanes, their labels and their order are instance config.

### 3.1 Pool, assignment, share

- Seats are a **pool**. A worker or reviewer seat owns nothing beyond its current **assignment**: one issue or one pull request, or idle. The durable form of an assignment is the `seat:<name>` label on the issue or pull request. Mike's store caches it; the label is the truth.
- The **priorities list** has one row per lane, ordered, so every lane of the program has a rank. Each row names its lane and may carry a **note**: a human's intent for that row in a sentence. Mike puts the note on the board Arthur reads and in every steer to that lane's lane-PE, as context. The note binds nothing; the lane does.
- The config store holds a **share** per rank: the percent of workers the lane at that rank gets. The default shares come from one rule for any number of lanes: rank *i* of *n* gets the weight *T(n − i + 1)*, where *T(k) = k(k + 1) / 2*, divided by the sum of the weights. A human may override any share; overrides must sum to 100. A row with no open work above `urgency:no` gives its share to the next row.

  | Lanes | Default shares, top rank first |
  |---|---|
  | 1 | 100 |
  | 2 | 75, 25 |
  | 3 | 60, 30, 10 |
  | 4 | 50, 30, 15, 5 |

- **Urgency** orders work inside a lane: `critical`, `high`, `normal`, then oldest first inside an urgency. Urgency is a label, `urgency:<level>`, because a label can be set from the GitHub mobile app and the GitHub Priority field cannot. Factory's Priority field values map onto it when factory is migrated: Urgent to `critical`, High to `high`, Medium to `normal`, Low to `no`.
- **Nothing runs on `urgency:no`.** An issue with no urgency label is `urgency:no`.
- The **board** is what Arthur reads: idle seats, each seat's assignment and its last completed assignment, send-backs with the owner seat, ready pull requests per seat, the priorities list with its notes, and target versus actual share per row. Mike builds it; today's orchestrator follow-up carries no board ([factory `idle_steer.py` lines 1279 to 1293, the follow-up prompt](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L1279-L1293)), so this is new.
- Arthur decides who does what. Mike enforces the gates in [section 3.3](#33-gates-mike-enforces-for-every-caller) for every caller, Arthur included, and shows target versus actual share on Health so a bad judgment is visible.

### 3.2 Mint, remint, steer

- **Mint** means to cause an agent session to be created for a seat. A mint is wait-only and cheap: the seat reads its brief and stops at "Wait for the first steer". Work reaches a seat only through a **steer**. This holds for every role.
- A **remint** is a mint of a seat that already had a session, and it carries the assignment: the first steer after a remint is the same work. Reset Defaults clears every assignment and every `seat:` label in one recorded write.
- **A seat with an open assignment is not steered onto other work**; if its session must be replaced, it is reminted onto the same work. This is the rule for the first cut. The architecture must allow seat reuse: when a seat's assignment closes, Arthur may steer that same seat onto related work where its context helps, instead of reminting a fresh seat. The board shows each idle seat's last completed assignment so Arthur can make that call. Whether reuse saves tokens is measured, not assumed.
- Mint, archive, restart, and kill each write a decision record. Today the actuator writes only log lines for these ([factory `seat_actuator.py` lines 1499 to 1549, the mint and archive steps](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_actuator.py#L1499-L1549)); Health cannot then show "no seat is minted twice for one issue".
- **One session per seat name.** Before a mint, Mike reads the seat's liveness. If the seat already has a responding session, Mike refuses the mint; a human or Arthur archives that session first. If Mike cannot read the liveness, it refuses and says why, rather than guess and risk two sessions under one name.

### 3.3 Gates Mike enforces for every caller

These are mechanism. They refuse with a recorded reason and the caller sees the why.

1. **Owner gate.** Only an issue or pull request assigned to Mike's GitHub user (`gh_user`; harness-gh-user today) may be steered. An empty or unmeasured setting refuses every steer.
2. **Project gate.** The repository is on the instance's project list. Today factory's steer does not check this ([factory `__main__.py` line 121, the create path's repository check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L121)); Mike does.
3. **Lane gate.** A worker steer onto an issue that has no lane label, or whose lane is not one of the program's lanes, is refused.
4. **Urgency floor.** A worker steer onto `urgency:no`, or onto an issue with no urgency label, is refused.
5. **One pending steer.** No second steer to a seat while one is pending inside the loop window, for every caller and for every runtime, queued included. Today it holds only for the loop caller and only for `applied` rows ([factory `__main__.py` lines 1054 to 1080, the loop steer hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1054-L1080)).
6. **Record before act.** Every side effect has a decision record before it happens. `apply` refuses an unrecorded decision. A refusal is a record with its why.
7. **One session per seat name.** No mint over a seat whose liveness is responding or unmeasured ([section 3.2](#32-mint-remint-steer)).
8. **Human switches.** Loop Paused and seat Stop are the two human switches. The loop acts on neither until a human changes them. Arthur may undo a Stop; nothing else may.
9. **Reviewer independence.** A reviewer does not review its own pull request, and never pushes.
10. **No merge verb.** There is none. A test fails if one is added.

Everything else that factory's tick evaluates today, 45 holds and gates counted in [factory#1336 section 2, what a tick evaluates](https://github.com/excaliwire/factory/issues/1336), is not re-created ([section 10](#10-what-mike-does-not-re-create)).

### 3.4 Review and send-back

- Every pull request a seat creates, or that is created elsewhere and assigned to a seat, must have:
  - at least one **self code review**: a review by the seat the pull request is assigned to, done with that seat's runtime code-review tool and posted as the self-review block ([section 6, step 2](#6-the-pull-request-lifecycle));
  - at least one **independent code review**: a review by a seat, an attached session, or a human that is not the seat assigned to the pull request.
- A **send-back** is an independent reviewer's signal, from a seat, an attached session, or a human, that the pull request must go back to its owner to address the review. On a send-back Mike returns the pull request to draft and steers the owner seat onto it as that seat's next work. Nothing else waits: while a pull request sits in review its owner may take new work, and a send-back then becomes the owner's next assignment after the work it is on.
- Pull requests needing review are ordered by urgency first, then by the time they went ready, oldest first.

### 3.5 What is judgment

Which seat takes which issue. The share actually given to each lane this tick. When to remint, and when to reuse an idle seat instead. The order of send-backs. Recovery after a reboot. Whether a cross-lane theme maps onto an urgency. These are Arthur's, with the board as input and Mike's verbs as the only output.

### 3.6 How reviewers operate

- One reviewer per ready pull request. All reviewers review in parallel. A reviewer holding a pull request takes no second one until it posts a verdict.
- A reviewer never reviews its own pull request and never pushes ([gate 9](#33-gates-mike-enforces-for-every-caller)).
- The reviewer pool is capped at `ceil(workers / 3)` ([decision 3, the reviewer count](#11-decisions)).
- A review has one shape, [section 6, step 4](#6-the-pull-request-lifecycle). A human's or an attached session's review counts as the independent review when config says so ([section 2.1, humans](#21-humans)).

## 4. Runtimes

A seat runs on a **runtime** (factory calls this the seat's `harness`: `cursor-cloud`, `grok-tmux`, `claude-tmux`, `codex-tmux`, `claude-cloud`).

Mike has an abstraction layer that gives it access to agent sessions from multiple **vendors** (for example Claude, Grok, or Cursor) through different **access methods** (`cloud` and `tmux`). This abstraction layer is a driver-like API called the **Mike Runtime API**. Each runtime is a driver, and the API allows new drivers to be developed over time and enabled or installed through config.

Cloud access is through the vendor's APIs. `tmux` access uses send-keys and screen reading to emulate API access. Both access methods sit architecturally under the Mike Runtime API. (Factory's session API was Cursor-shaped because when factory was written the Cursor API was the most mature.)

The Runtime API provides Mike with consistent access to the following capabilities, in a vendor-neutral manner:

| Capability | Every runtime must provide |
|---|---|
| mint | create a session for a seat, wait-only, returning a session id |
| steer | deliver one prompt and **confirm delivery** (a run id, a pane echo, or an event id). A steer that is not confirmed is not a steer, and the verb says so. |
| stop, restart, archive | each with a record |
| liveness | one of `not-minted`, `responding`, `not-responding`, `unmeasured` with a reason. No fifth word. Busy and idle are not liveness. |
| usage | tokens since mint, context pressure, and the vendor's included-pool percent, each `unmeasured` with a reason when not read |
| session log | a stream of inputs and responses from the session, from which the last input (the last steer) and the most recent response can be identified |

Factory's runtime API is Cursor-shaped: mint steps are Cursor creates, grok-tmux has no archive, claude-cloud liveness is always unmeasured, and Health clears a row only on the Cursor record shape ([factory#1336 comments, learnings 6, 9 and 11 on the single-vendor actuator](https://github.com/excaliwire/factory/issues/1336); [factory#1418, Health assuming a Cursor steer](https://github.com/excaliwire/factory/issues/1418)). Mike has one actuator interface and one record shape, and each runtime fills it or reports unmeasured.

**Gauges.** Each runtime declares its pools, windows (such as Claude's 5-hour limit), a probe, and a mint threshold. Mint picks the next vendor when one crosses its threshold ([factory#1501, the extraction call](https://github.com/excaliwire/factory/issues/1501): at 75 percent of Claude's 5-hour limit, stop minting Claude seats and shift new seats to xAI Grok; [decision 10](#11-decisions)). These are called gauges because they serve two purposes: they let Mike redirect new seats to runtimes that have usage available, and they show usage to humans in the dashboard. An unmeasured gauge stays unmeasured, never 0, and a mint that depends on an unmeasured gauge is refused. Which gauges exist is config.

**Seat hosts pull.** A machine that runs tmux seats checks in and claims actuations from the store. The control plane holds no inbound path and no SSH key to a seat host. Every steer goes through the control plane store, from any caller on any machine. There is no second, machine-local queue.

**Identity.** A seat token names one seat and acts only as that seat. A session token names one attached session ([section 2.2](#22-attached-sessions-non-seats-that-act-through-mike)) and acts only as that session, with the verbs its config row lists. A host token names one host and pulls only its own actuations. There is no shared master secret on a seat host ([factory#1413, the shared session secret](https://github.com/excaliwire/factory/issues/1413)). A human is a verified bearer, not a header any local process can set.

## 5. The control plane

The **control plane** is the mechanism that detects changes on the board (GitHub plus Mike's own state) and maps those changes to actions that steer seats.

- **The control plane is the only watcher.** It takes GitHub events by signed webhook and diffs its own store each tick: an issue assigned, a pull request from draft to ready, a review verdict, a send-back, a conflict, unresolved Copilot threads, a seat gone idle. Each change is routed to the seat it concerns as a recorded steer bound by the gates: Arthur gets the board when the board changed or a seat went idle; the owner seat gets its send-back, conflict or Copilot findings; a reviewer gets a ready pull request. No seat polls GitHub. No vendor scheduler or routine-fire watches anything for Mike. Nothing fires on a timer except the tick itself.
- **Control loop.** One tick: read desired state, read live state, decide, act. One loop per instance, from a checkout the instance owns. A tick does not overlap the previous one. Loop cadence, Running/Paused, and live/dry-run are config-store settings.
- **Desired state** is instance config: roles, roster, projects, lanes and labels, hosts, runtimes and gauges, briefs. Shipped defaults and instance config are separate files. Changing desired state is a pull request on the instance's config repository.
- **Live state** is the store: assignments, session ids, liveness, gauges, records, settings versions. Never in git. The store is one process's responsibility, locked, and append-only where it is a log.
- **Config store.** Validated against a schema, versioned, append-only history, human-only writes, one log line per change with actor and from-to. Secrets by name only. A change applies live: reload, remint the affected seats, or swap a key, whichever is smallest ([factory#1524, config outside git with a Settings tab](https://github.com/excaliwire/factory/issues/1524)).
- **Decision records.** Schema: who saw what, decided what, why, outcome (pending, applied, refused, cancelled), actor, caller. Every verb writes one. Health reads them. A refusal is a record.
- **One log.** `mike.jsonl`, rotated, structured, secrets redacted. A new signal is a log line first; a Health row only when a human needs to act on it.
- **GitHub.** One module runs `gh` or the API. A write as a human merger is refused. A read that fails is unmeasured, never empty. Reads respect GitHub's rate limit: below a reserve, the tick holds every GitHub-reading verb. Events arrive by signed webhook; polling a human's notifications is a fallback, not the design.

## 6. The pull request lifecycle

1. The worker opens the pull request as a draft early, labelled `seat:<name>`.
2. Owner self-review on the head commit, done with the seat's runtime code-review tool: a comment `Self-Review: Done` naming `Head: <sha>`, written by the owner's `[Name]` prefix. Anything else does not count.
3. CI green on that head. The worker marks the pull request ready only then.
4. One reviewer is steered onto it. The review is at most 12 lines: line 1 `[Name] Recommendation: Merge|Send back|Hold on <sha>.`, one line per blocking finding as `file:line, what is wrong, the fix`, one `Ran:` line, the results table collapsed, `Next:` lines last. Non-blocking findings become issues, not comment text.
5. A new commit voids self-review, CI, and review. Every gate is per head sha.
6. Send back: the pull request returns to draft and the owner's seat gets it as its next assignment ([section 3.4](#34-review-and-send-back)).
7. Merge: self-review, CI, ready, and a `Merge` review on the same head. Mike assigns a human merger (config, `tig` on factory). The merger's assignment list is the merge queue. Mike never merges.
8. A human may waive a gate with `waive: <gate> [sha]` and grant a reviewer with `reviewer: <Name>`. No seat may write either.

Tests must fail on main and pass on the head. The reviewer's verb copies new tests onto a `main` worktree and runs them both sides, so "fails on main" is measured, not claimed.

## 7. The dashboard

The dashboard is how humans see and control Mike. It has its own spec, [`mike-dashboard.md`, the dashboard](mike-dashboard.md): what the app is, what each tab shows, and the approved mockup for each tab, inline. Its API is Mike's own contract, [`mike-dashboard-api.md`, the dashboard API](mike-dashboard-api.md); factory's dashboard API was a starting point, not law. The app is a full rewrite; factory's dashboard is not evolved, imported, or copied from.

## 8. Lexicon

Mike keeps the discipline: the lexicon is config, a term change is test-first, an outbound prompt is linted against the banned-terms table (Geas), and every review checks lexicon drift. The word list for a project comes from that project's hook, not from Mike.

The carry-over table, one row per factory term, is [the lexicon carry-over table](mike-lexicon.md#2-carry-over-table). The decisions that change a word:

| Factory term | Mike | Why |
|---|---|---|
| agent harness, the harness (the system) | **Mike** | The system has a name. "Harness" was also the per-seat run kind, so one word carried two meanings. |
| harness (a seat's `harness:` field) | **runtime** | The seat runs on a runtime; the vendor bills it. |
| harness-gh-user | **gh_user** | Follows the system rename. Same gate. |
| retarget, retarget-loop, retarget-pe, the ladder | **tick** for the loop; the ladder retires | The loop's name was a verb it rarely ran. Vendor budgets replace the ladder ([section 4, runtimes](#4-runtimes)). |
| direction, direction list | **priorities list** | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) and a human say priorities. One word. |
| hold, hold word, none-eligible reason | retired | The planner that produced them is not re-created. |
| awaiting-response, lane owner, lane-starved as a hold | retired | Nothing is held but the gates in [section 3.3](#33-gates-mike-enforces-for-every-caller). lane-starved retires with it: every lane is on the priorities list, so the lane gate refuses only an unknown or missing lane. |
| stand-down, resume | retired | A seat waiting on a gate is a steer Arthur writes ("wait for #N"), not a parallel hold mechanism. |
| meter | **gauge source** | A gauge is the reading; a meter was one way to scrape it. |
| arbiter = mechanism | arbiter = **judgment** | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336). |
| board (new) | **board** | What Arthur reads each tick, [section 3.1](#31-pool-assignment-share). |
| share (new) | **share** | Percent of workers a priority row gets. |
| pool (new) | **pool** | The worker and reviewer seats together. |
| severity; Urgent, High, Medium, Low; the GitHub Priority field | **urgency**: `critical`, `high`, `normal`, `no`, as labels `urgency:<level>` | Tig, 2026-10-05 review: a label can be set from the GitHub mobile app, the Priority field cannot. Factory maps Urgent, High, Medium, Low onto the four levels. |
| harness (a seat's run kind), vendor | **runtime** (a driver under the Mike Runtime API), **vendor** (who bills), **access method** (`cloud` or `tmux`) | [Section 4](#4-runtimes). |
| budget (mint token or turn budget) | retired | Came from [factory#1755, the lane-PE remint token burn](https://github.com/excaliwire/factory/issues/1755)'s done-when, written by Infra Fable, not from Tig. The control on mint cost is wait-only mints and the gauges. |
| Sessions tab | **Seats tab** | The tab shows seats, each as a seat card ([the dashboard spec, the Seats tab and the seat card](mike-dashboard.md#3-the-seats-tab-and-the-seat-card)). |
| `Name:` (address) | **`To: Name`** addresses a seat, as in an email header; **`[Name]`** at the start of a comment is the writer's prefix, unchanged | Tig, 2026-10-06. `Name:` means the speaker in a transcript and the addressee on IRC, so it was ambiguous; `[Name]:` differed from the writer prefix by one character. |
| runtime kind names (`cursor-cloud`, `grok-tmux`, `claude-cloud`) | kept | Each is a runtime. |
| droplet | **control-plane host** | Mike runs on any host. |
| claim (a vendor session) | **adopt** | Claim collides with a seat host claiming an actuation. |
| assign-tig, Assign Tig | **request merge** | The merger is config. |
| steer-idle (the verb) | **follow-up** | Only the orchestrator follow-up survives; the planner does not. |
| Lexicon: Clear (review line) | retired | Already retired on factory by [factory#1741, the terse comment guidance](https://github.com/excaliwire/factory/issues/1741); the review's line 1 verdict carries it. |

New term, confirmed by a human 2026-10-05: **attached session** ([section 2.2, attached sessions](#22-attached-sessions-non-seats-that-act-through-mike)). The audit had no word for a human-driven session that acts through Mike; factory says only "not a seat".

Terms kept as-is include: seat, role, mint, remint, steer, stop, archive, restart, assignment, liveness and its four words, decision record, record before act, control plane, control loop, seat host, data plane, desired state, live state, config store, fleet mode, hard reboot, orchestrator reboot, worker reboot, fill-missing, reset defaults, loop window, Running, Paused, live, dry-run, send-back, lane, gauge, tier, temporary seat, director, Geas, banned term, address contract (`seat:<name>` owns, `[Name] ` writes, `To: Name` addresses). Full table and the open challenges are in [the lexicon file](mike-lexicon.md).

## 9. What Mike keeps

Each is a rule factory paid for. Evidence is the factory file at [factory commit bb2bf4c6, the tree this spec read](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8) unless an issue is named.

1. Record before act. [factory records.py lines 1 to 14, record before act](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/records.py#L1-L14).
2. Unmeasured is an answer. Never invent a percent, a liveness, an urgency, a board. [factory liveness.py lines 1 to 24, unmeasured is an answer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/liveness.py#L1-L24).
3. One choke point for GitHub writes; never as a human; no merge verb. [factory gh.py lines 100 to 133, the one choke point for GitHub writes](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/gh.py#L100-L133).
4. The merge path is a head-pinned state machine reading structured blocks, not prose. [factory merge_gate.py, the head-pinned merge path](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/merge_gate.py), [factory pr_state.py lines 39 to 95, the structured-block reader](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L39-L95).
5. A test must fail on main and pass on the head, for code, config, schema, and briefs. [factory root AGENTS.md lines 132 to 140, test-first](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md?plain=1#L132-L140).
6. The lexicon is config; Geas lints every outbound prompt. [factory geas.py, the Geas prompt lint](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/geas.py).
7. One liveness vocabulary for every runtime; liveness is not assignment. [factory liveness.py lines 1 to 44, one liveness vocabulary](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/liveness.py#L1-L44).
8. Delivery is confirmed, not assumed from enqueue. [factory seat_host.py line 934, delivery confirmed](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/seat_host.py#L934), [factory#1630, the grok paste never delivered](https://github.com/excaliwire/factory/issues/1630).
9. Mint is wait-only; remint carries the assignment; never steer across open work. [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336), section 3.
10. Stop and Paused are human switches. [factory seats.yaml line 70, the Stop prompt](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/seats.yaml#L70).
11. Config store: validated, versioned, append-only, human-only, logged. [factory settings.py lines 1258 to 1370, the config store write](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L1258-L1370).
12. Caller matrix: seats do not mint; the arbiter steers; a lane-PE steers its own lane; a seat token acts on itself. [factory seats.yaml lines 59 to 77, the caller matrix](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/seats.yaml#L59-L77).
13. Seat hosts pull; no inbound path on the control plane. [factory docs/host.md line 258, seat hosts pull](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/host.md?plain=1#L258).
14. One log; a new signal is a log line. [factory harness_log.py, the one log](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/harness_log.py).
15. Address contract: `seat:<name>` owns, `[Name] ` at the start of a comment writes, `To: Name` addresses, several as `To: Name, Other`. A seat writes `[Avalon] To: Arthur. ...`; a human, whom GitHub already names, writes `To: Arthur. ...`. A bare `Name:` or `[Name]:` addresses nobody, and the lint says so. [factory poke.py lines 30 to 33, the address contract](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/poke.py#L30-L33) is the shape, with `Name:` as its address form.
16. Names, roles, lanes, caps, repositories, hosts, vendors are config, not code. [factory policy.py lines 214 to 281, roles and names as config](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/policy.py#L214-L281).
17. Health shows target versus actual share. [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336), section 4.
18. The dashboard API is a versioned contract with a schema-digest test, and a health read makes no vendor or GitHub call ([section 7, the dashboard](#7-the-dashboard)). The contract is Mike's own.
19. Secrets by name only: never in git, records, logs, or argv. [factory local.py line 559, secret redaction](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/local.py#L559).
20. Comment limits: review 12 lines, pull request body 20, other 6, `Next:` last. [factory test_comment_limits_1741.py, the comment limits test](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/tests/test_comment_limits_1741.py).
21. Talking to humans: measurement not adjective, bad news first, recommendation not menu, decisions then merges then next, cost unasked. [factory root AGENTS.md lines 84 to 96, talking to Tig](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md?plain=1#L84-L96).
22. The control plane is the only watcher; a change is routed to the seat it concerns as a steer; no seat polls and no vendor watches ([section 5, the control plane](#5-the-control-plane)). Tig, 2026-10-05.
23. Every test names its tier of the test pyramid, and every part is covered at the unit and component tiers with nothing else running; only an end-to-end test needs the whole system ([section 12, how Mike is tested](#12-how-mike-is-tested)). Tig, 2026-10-06.

## 10. What Mike does not re-create

Each is accidental complexity or a defect on factory `main`, with the evidence.

1. The steer-idle worker planner and its 45 holds and gates: 12 hold words, 12 none-eligible reasons, 9 wordless gates, 8 steer refusals beyond [section 3.3, the gates](#33-gates-mike-enforces-for-every-caller), 4 review-idle holds. [factory idle_steer.py lines 39 to 56, the hold words](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L39-L56), [line 1628, hold_why](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L1628) and [line 1834, the planner](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L1834); [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336), section 2.
2. Two deciders on one roster: a planner beside the arbiter, disagreeing ([factory#1365, steer-idle redelivery refused every tick](https://github.com/excaliwire/factory/issues/1365)).
3. Ten verbs per tick that can each steer or mint the same seat, patched by `_loop_steer_hold`. [factory retarget-loop.sh lines 79 to 100, the verbs per tick](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/retarget-loop.sh#L79-L100).
4. Holds that strand capacity: awaiting-response, an idle reviewer held behind a busy one, a ready pull request holding its author. [factory#1759, ready PR queued behind busy Warden](https://github.com/excaliwire/factory/issues/1759), [factory#1761, send-back seat held awaiting-response](https://github.com/excaliwire/factory/issues/1761), [factory#1762, no cap on ready pull requests](https://github.com/excaliwire/factory/issues/1762).
5. Assignment in three places (label, actuator cache, steer records) with "taken" inferred from titles and pending creates.
6. A single-vendor actuator with per-runtime special paths. [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336), learnings 6, 11.
7. Machine-local steer queues and a second queue (`assignments.jsonl`, `assign`, `redeliver_tries`). [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336), learnings 7, 10.
8. A shared master secret on the seat host; a human gate that is a header. [factory#1413, seats can read the session secret](https://github.com/excaliwire/factory/issues/1413); [factory docs/host.md line 99, the header gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/host.md?plain=1#L99) versus [line 258, seat hosts pull](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/host.md?plain=1#L258).
9. Health that assumes one runtime's record shape, back-patched with a synthetic record. [factory#1418, Health red for every tmux seat](https://github.com/excaliwire/factory/issues/1418).
10. Mint and archive that write no record.
11. Invariants that hold only for the loop caller.
12. Lane-PE mints that are not wait-only. [factory#1755, the lane-PE remint token burn](https://github.com/excaliwire/factory/issues/1755).
13. An orchestrator follow-up on a timer rhythm that carries no board. [factory#1743, follow-up only on real board change](https://github.com/excaliwire/factory/issues/1743).
14. A GitHub Discussion board publisher kept for retired boards ([factory dashboards.py, the Discussion board publisher](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/dashboards.py), 1300 dead lines).
15. An unlocked file store with newest-row-wins and whole-file scans per decision. [factory store.py lines 3 to 6, the file store](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/store.py#L3-L6) and [lines 597 to 789, the whole-file scans](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/store.py#L597-L789).
16. Settings seeded from four places plus a self-healing migration.
17. Cursor busy/idle leaking as a third liveness reading.
18. Stand-down and resume as a parallel hold mechanism.
19. Screen-scraped vendor meters as the gauge source where a usage API exists.
20. One-shot migration verbs kept in the product (retitle, seat-rename). A stable seat id makes rename a config edit.
21. Dashboard behaviors that patch the above: parsing server prose and human time strings, a 30-second command timeout with no job id, full repaint per log frame, a banned-word dodge in source ([factory rules.mjs line 330, the banned-word dodge](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L330)), hover text that re-derives a verb rule the server already answers.

## 11. Decisions

All 16 decided by Tig on 2026-10-05. Decisions 1 to 6 are [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336), section 7 and are repeated here because Mike's cut depends on them. Decision 4 closes when [factory#1778, the wait-only mint measurement](https://github.com/excaliwire/factory/issues/1778) posts its number.

1. **Decided, Tig, 2026-10-05.** The control plane detects every change ([section 5, the control plane](#5-the-control-plane), [rule 22, the control plane is the only watcher](#9-what-mike-keeps)) and steers Arthur when the board changed or a seat went idle. Never on a timer. No seat or vendor watches.
2. **Decided, Tig, 2026-10-05: a lane plus an optional note.** The lane binds the gate and the share; the note is a human's intent, shared with Arthur on the board and with that lane's lane-PE as context. Amended in the 2026-10-05 review: the list has one row per lane, so every lane is ranked, and the shares follow the rule in [section 3.1](#31-pool-assignment-share) for any number of lanes.
3. **Decided, Tig, 2026-10-05.** `ceil(workers / 3)` caps the reviewer pool; inside it, one reviewer per ready pull request, all in parallel.
4. **Decided, Tig, 2026-10-05: measure first, on the existing harness.** [factory#1778, the wait-only mint measurement](https://github.com/excaliwire/factory/issues/1778): 5 wait-only mints left 1 hour, tokens, turns, dollars and first-steer cost per seat. The number closes this decision; the remint-not-steer rule is built on it.
5. **Decided by [decision 1, change-driven steers](#11-decisions), 2026-10-05.** conflict-steer and copilot-findings are not verbs. A conflict and an unresolved Copilot thread set are two change kinds the control plane routes to the author seat as a steer.
6. **Decided, Tig, 2026-10-05: per instance.** One list across every project the instance manages. A lane may belong to any project.
7. **Decided, Tig, 2026-10-05: yes.** The system is Mike, not the harness, and the seat's run-kind field is renamed from `harness` to `runtime`.
8. **Decided, Tig, 2026-10-05: yes.** The priorities list replaces the word direction everywhere, including the API's `direction` command, at the major bump [tig/mike#1, the dashboard rewrite](https://github.com/tig/mike/issues/1) already needs.
9. **Decided, Tig, 2026-10-05: role keys are the names unless overridden.** Mike ships no display names. The Arthurian names are factory's instance config ([section 2, roles](#2-roles)).
10. **Decided, Tig, 2026-10-05: xAI Grok.** The vendor-shift rule in [factory#1501, the extraction call of 2026-10-01](https://github.com/excaliwire/factory/issues/1501) shifts new seats to xAI Grok, the vendor the workers and reviewers run on, not Groq.
11. **Decided, Tig, 2026-10-05: pool.** Config holds a cap and a list of names. Mike mints a name when the pool is below target and kills one only when stale or at the cap ([factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336), section 1, point 6).
12. **Decided, Tig, 2026-10-05: keep the role, and Mike may mint it.** One PE per lane, wait-only, no ladder. The loop mints a missing lane-PE when the role's fill-missing setting is on; turning it on asks a human first, because each mint spends money. A project may configure zero lane-PEs.
13. **Decided, Tig, 2026-10-05: keep two, measure a week.** Arthur and K stay separate roles. Mike measures K's follow-ups per hour for one week after the first cut, recorded on [tig/mike#3, this spec](https://github.com/tig/mike/issues/3), then a human decides whether K merges into Arthur.
14. **Decided, Tig, 2026-10-05: sorts first, never preempts.** `urgency:critical` (SEV1, Urgent on factory) takes the next idle seat. No seat is steered across open work. A human may Stop a seat by hand.
15. **Decided, Tig, 2026-10-05: yes.** Stand-down and resume, the hold words, the PE ladder and its rungs, and `retarget` retire ([section 8, the lexicon table](#8-lexicon); [the lexicon carry-over table](mike-lexicon.md#2-carry-over-table)).
16. **Decided, Tig, 2026-10-05: yes.** The word is **attached session**; the director is one. Default rights: issue and pull verbs like a seat, steer like a lane-PE, no mint.

## 12. How Mike is tested

Factory's harness could be tested only whole: a verb needed the repository checkout, the live roster, a running loop, a live vendor, and often a second seat before anything could be observed ([factory#1501, the extraction call, "suggested first steps"](https://github.com/excaliwire/factory/issues/1501) tells a newcomer to run nothing with `--apply` and to set a temp state directory first). Mike uses the standard test taxonomy, the test pyramid ([Fowler, "The Practical Test Pyramid"](https://martinfowler.com/articles/practical-test-pyramid.html)), and every test names its tier.

### 12.1 The tiers

| Tier | What is under test | What is real | What is faked | Runs |
|---|---|---|---|---|
| 1. **Unit** | one function or class | the code | everything it calls | CI, every change, milliseconds |
| 2. **Component** | one part behind its seam: a runtime driver, a seat role's behavior, the API server, the store, the board builder | the part | every other part, the vendor, GitHub, the clock | CI; the real-model and real-vendor variants on demand |
| 3. **Contract** | an interface both sides depend on: the Runtime API, the dashboard API, the GitHub interface | the contract and one implementation at a time | the other side | CI against fakes; against the real vendor or GitHub sandbox on demand |
| 4. **Integration** | several real parts together, for example a whole control-plane tick | the control plane, the store, the router, the gates, the API | the runtime (fake runtime), GitHub (fake), the clock | CI, no network |
| 5. **End-to-end** | the whole system live | a real driver, a sandbox repository, a real tick, a real model | nothing | on demand; result, duration and cost recorded on the issue that asked |

**The rule.** Every part has a seam and is covered at tiers 1 and 2 with nothing else running: no control plane, no vendor, no GitHub, no second seat. Tiers 3 and 4 may start real parts of Mike but never a live vendor or live GitHub; they run in CI with no network. Only tier 5 needs the whole system, and it is the proof that the seams agree, not the way a part is tested. A part that can be tested only at tier 4 or 5 is not done.

### 12.2 The seams the architecture must provide

- The [Mike Runtime API](#4-runtimes) is an interface. Mike ships a **fake runtime** that implements it in memory and records every call, loaded by the same path as a real driver.
- GitHub is behind one interface with a fake that serves fixture repositories and accepts fixture webhook deliveries.
- The clock is injected. The store runs on any directory. The API server runs in-process against a fixture store.
- The brief renderer, the board builder, the share rule, the gates, the address parser and the urgency sort are pure functions: input in, output out, no I/O.
- A seat's judgment is reachable without the control plane: the brief plus a **synthetic board** plus a stub of Mike's verbs that records calls and applies the gates.

### 12.3 The suites each tier must hold

- **Tier 2, driver conformance.** One suite every runtime driver must pass through the Runtime API alone: load config; mint wait-only and return a session id; steer and confirm delivery; stop; restart; archive; liveness in exactly the four words; usage and context pressure, unmeasured with a reason when unread; session log with the last steer and latest response identifiable. It runs against the fake runtime in CI and, as its tier 3 contract variant, against the real vendor in a sandbox account on demand, where it records cost. A driver that does not pass is not installable through config.
- **Tier 2, seat behavior.** One suite per role, with no control plane and no other seat, from synthetic inputs. Arthur alone: given a synthetic board and the verb stub, it produces the expected steers and no refused ones, for example the three send-back steers for the state factory measured on 2026-10-05, and never a steer onto `urgency:no`. A worker alone: given a steer onto an issue in a fixture repository, it opens a draft, posts the self-review block on the head, and marks ready only after CI is green. A reviewer alone: given a ready pull request, it posts a verdict in the 12-line shape. A replay of recorded model turns runs in CI; the real model runs on demand and on every brief change, because a brief is config and a brief change is test-first against this suite.
- **Tier 3, contracts.** The dashboard API's schema-digest and frame tests ([the dashboard API, where this is tested](mike-dashboard-api.md#9-where-this-is-tested)); the Runtime API conformance against each real vendor; the GitHub fake checked against recorded real responses.
- **Tier 4, the tick.** A full tick against the fake runtime, the fake GitHub and the injected clock: routing of every change kind, every gate, record before act, the API frames, the jobs.
- **Tier 5, live.** One real driver, one sandbox repository, one real tick, one real model turn, on demand.

### 12.4 The dashboard

The app is tested at the same tiers, with a headless browser as the runner where layout matters. It is not a sixth tier.

- **Unit.** The page's pure rules (verb enablement from a row's `verbs`, age and time formatting from ISO 8601, share and gauge arithmetic) as functions with fixtures.
- **Component.** Each UI component rendered alone from fixture payloads, the seat card first ([the dashboard spec, the Seats tab and the seat card](mike-dashboard.md#3-the-seats-tab-and-the-seat-card)): at 1180 px and at 375 px, no horizontal overflow, the LED word present beside the color, a disabled verb carrying `verb_why`, an unmeasured field drawn as the word and no bar. A screenshot per component and width is kept as a visual baseline, and a change to it is a reviewed diff, not a surprise.
- **Contract.** The app fed the dashboard API's fixture frames draws without error, and the command bodies it builds equal the API's command examples byte for byte ([the dashboard API, where this is tested](mike-dashboard-api.md#9-where-this-is-tested)).
- **Integration.** The page in a headless browser against the in-process API server with the fake runtime and a fixture store: a pushed frame updates one card without a repaint, a half-typed steer and an open expander survive the frame, a command shows its job outcome on the row, the stream reopens after a cut, a major-version mismatch stops the page with "must update". No network beyond loopback.
- **End-to-end.** The live run in tier 5 is driven through the page once, on a phone-width viewport and a desktop one.

**What a test must still do.** Fail on main and pass on the head ([rule 7](#9-what-mike-keeps)). Name its tier and the seam it uses. Say the measurement it makes.

## 13. The cut: MLP, v1, backlog

Factory's failure was building too much at once, up front. Mike is cut into three releases, and every user story carries an urgency that says which one it is in, in the same four words issues use ([section 3.1, urgency](#31-pool-assignment-share)):

| Urgency | Means | Stories |
|---|---|---|
| `critical` | blocks progress on the current release | none today; a story becomes critical when it blocks the MLP |
| `high` | in the **MLP** | the minimum lovable product, [section 13.1](#131-the-mlp) |
| `normal` | in **v1**, after the MLP works end to end | [section 13.2](#132-v1) |
| `no` | **backlog**, not planned | [section 13.3](#133-backlog) |

The MLP is the cheapest Mike that Tig will love and that teaches us something: one seat pair working one project end to end, Tig steering by hand, with the least complexity and the least fragility. Every story's `Urgency:` line is in [the user stories, by file](stories/README.md), and [`stories/mlp.md`, the MLP build order](stories/mlp.md) lists the `high` stories in the order to build them.

### 13.1 The MLP

**What it is.** One instance, one project, two seats on one cloud runtime, and Tig. Tig assigns an issue to `gh_user` or writes `To: <worker>` on it; Mike steers the worker; the worker opens a draft, self-reviews, gets CI green, marks ready; Mike steers the reviewer; the reviewer posts a verdict; a send-back steers the worker back; a Merge verdict assigns Tig; Tig merges. Tig watches it on his phone.

**What is in.**

- **Seats:** one worker and one reviewer, both standing names in config. No arbiter, no TPM, no lane-PE. Tig is the judgment: he steers by `To: Name` on GitHub or from the seat card. The control plane routes only what needs no judgment: an issue assigned to `gh_user` goes to the worker when the worker is idle, oldest first by urgency, else it waits; a ready pull request goes to the reviewer; a send-back goes back to the worker; a Merge verdict assigns the human merger.
- **Runtime:** the fake runtime and **one cloud driver**. Recommend the Claude cloud driver ([factory#1372, the claude-cloud seat harness](https://github.com/excaliwire/factory/issues/1372)): an API with queued messages, a session event stream that confirms delivery and is the session log, and no screen reading. tmux drivers, seat hosts and host tokens are v1; they are where factory's fragility lived.
- **Gates:** owner (`gh_user`), project, urgency floor, one pending steer, record before act, one session per seat name, the two human switches, reviewer independence, no merge verb. The lane gate is v1 with lanes.
- **Mint:** wait-only; remint carries the assignment; Reset defaults.
- **Humans:** one listed human. `To: Name` addressing from a human comment. No attached sessions, no contributors handling beyond ignoring them, no `waive:` or `reviewer:` grants.
- **Control plane:** signed webhook ingestion, the tick, the store, decision records, one log, the config store with versioned saves and reload-on-change, the read reserve.
- **Dashboard:** phone-first from the start, with four tabs: Seats (the seat card), Health (Instance, Control plane, Loop, Problems; the rollups only as far as two seats need them), Logs (the full filter, no scenario presets), Settings (the two switches, `gh_user`, cadence; seat types stay in the config file). API parts: version, health, seats, settings, logs, jobs, read by **polling** every few seconds; the live stream is v1. Commands as jobs. Identity: a human bearer token issued at install and a seat token; identity-provider sign-in is v1.
- **Testing:** unit; component suites for the one driver (against the fake and the vendor), the worker and the reviewer; the integration tick against fakes; one end-to-end run. The dashboard at the component and integration tiers.
- **Install:** one package, one config file, no factory checkout.

**What we learn.** Whether one cloud worker and one reviewer, steered by hand, merge work Tig is glad to merge. What a wait-only mint and a steer cost. Whether confirmed delivery over a cloud API removes the undelivered-steer class of failure. Whether the seat card and Health are enough on a phone. Each is a number on [tig/mike#3, the spec issue](https://github.com/tig/mike/issues/3) before v1 starts.

### 13.2 v1

Everything the seat model adds once the loop is trusted: the live stream and its recovery, identity-provider sign-in, the JSON editor and the full Settings groups; Arthur and the board, K, lane-PEs, the pool with shares, lanes and the priorities list with notes, SEV ordering across seats, send-back ordering, seat reuse. More runtimes: tmux drivers, seat hosts, host tokens, per-runtime gauges and the mint threshold. Several humans, attached sessions, `waive:` and `reviewer:` grants, contributor triage, conflict and Copilot change kinds. Several projects per instance. The Board, Priorities, Gauges and Attached sessions tabs; Logs scenarios; the full Settings groups. The seat-behavior suite for Arthur.

### 13.3 Backlog

Terminal control from the browser. Overlapping-instance detection. Vendor-to-vendor shifting beyond the mint threshold. Visual regression baselines beyond the seat card. Anything else no story in `high` or `normal` names.

## 14. Done when

- The user stories in [the user stories index](stories/README.md) each name a test or a measurement, and the LEGACY ones are not built.
- [The lexicon carry-over table](mike-lexicon.md#2-carry-over-table) has a verdict on every factory term and a human has edited it.
- moms passes its own contract tests ([`mike-dashboard-api.md`, the dashboard API](mike-dashboard-api.md)) with an empty `PINNED` list, from an install with no factory checkout, managing two projects from one instance.
- A tick with idle workers writes no planner row; Arthur's steers pass the [section 3.3, the gates](#33-gates-mike-enforces-for-every-caller); Health shows target versus actual share.
