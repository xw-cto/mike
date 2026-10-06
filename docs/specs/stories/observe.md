# Mike user stories: observe

The stories for observing the fleet: the seat table, the seat card, the phone layout, the board, and target versus actual share. Rules, verdicts and the other files: [the user stories index](README.md).

## Observe the fleet

#### MS-001 One table of every seat
As a human (Tig today), I want one table of every seat with its name and role, so that I see who exists without reading config files.
Evidence: [factory dashboard app.js line 1646, the seats table](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1646).
Acceptance: row count equals the configured role seats plus the minted pool names; order is arbiter, TPM, lane-PEs, workers, reviewers; each row reads "Name - Role".
Verdict: CHANGE: rows come from role config and the pool ([mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share), [decision 11, the pool model](../mike.md#11-decisions)), not 13 standing names in `seats.yaml`.

#### MS-002 Liveness in four words
As a human (Tig today), I want each seat's liveness as one of four words with the reason on hover, identical for every runtime, so that "no session" and "session not responding" never look alike.
Evidence: [factory dashboard rules.mjs line 878, the liveness cell](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L878); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: for cursor-cloud, claude-cloud and grok-tmux seats the word is one of `not-minted`, `responding`, `not-responding`, `unmeasured`; every non-responding word has a non-empty reason; one function computes it (test).
Verdict: KEEP.

#### MS-003 Liveness opens the vendor session
As a human (Tig today), I want the liveness cell to open the vendor session when a seat is minted, so that I can watch it in one click.
Evidence: [factory dashboard rules.mjs line 898, the liveness link](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L898); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: a link exists if and only if the word is `responding` or `not-responding` and the URL is http(s).
Verdict: KEEP.

#### MS-004 Assignment shown per seat
As a human (Tig today), I want each seat's assignment as a linked `owner/repo#N` with its title, or idle, so that I see what each seat is on and in which project.
Evidence: [factory dashboard rules.mjs line 840, the assignment cell](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L840); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: the cell matches the `seat:<name>` label on GitHub for 100% of rows in a 20-row sample; a pull request links to `/pull/N`.
Verdict: CHANGE: the label is the truth and the store a cache ([mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share)); the project is named on the cell.

#### MS-005 Last confirmed steer shown
As a human (Tig today), I want each seat's last confirmed steer, clipped, with the full text on hover, so that I know what it was last told.
Evidence: [factory dashboard app.js line 1691, the last steer cell](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1691).
Acceptance: at most 40 characters shown; the full prompt is in the title when longer.
Verdict: KEEP.

#### MS-006 Page updates by itself
As a human (Tig today), I want an open page to update by itself when state changes, so that I never reload.
Evidence: [factory dashboard app.js line 2685, the live update stream](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2685); [Mike dashboard API §4, the stream](../mike-dashboard-api.md#4-the-stream).
Acceptance: a store change reaches an open page in under 2 s plus network time.
Verdict: KEEP.

#### MS-007 Seat page for diagnosis
As a human (Tig today), I want a seat page with liveness, last mint, last steer, pending steer, and the stored session log, so that I can diagnose one seat.
Evidence: [factory dashboard app.js line 2502, the seat page](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2502); [Mike dashboard API §5, reads](../mike-dashboard-api.md#5-reads).
Acceptance: `/sessions/<seat>` shows all 5 blocks; a missing log reads `unmeasured`.
Verdict: KEEP.

#### MS-008 Arthur reads the same API
As Arthur (arbiter), I want the seat list, verbs, assignments and Health over the same API with my seat token, so that my decisions use a human's view.
Evidence: [factory dashboard rules.mjs line 7, the shared row rules](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L7); [Mike dashboard API §5, reads](../mike-dashboard-api.md#5-reads).
Acceptance: the sessions read with a seat token returns rows byte-identical to the rows the page draws.
Verdict: KEEP.

#### MS-009 Runtime and host per row
As a human (Tig today), I want each row to name the seat's runtime and host, so that I know where a seat runs without expecting it to carry a control-plane key.
Evidence: [factory harness api.py line 2210, the runtime and host fields](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L2210); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: every row shows a runtime from the config list and a host or `cloud`; 0 rows carry the per-seat "acts through the control plane" text.
Verdict: CHANGE: every seat acts through the control plane ([mike.md §4, runtimes](../mike.md#4-runtimes)), so the special-case marker goes.

#### MS-071 Talk to humans by measurement
As a seat (any), I want to talk to a human by measurement, bad news first, with one recommendation, ordered decisions then merges then next, and cost unasked, so that a human reads one message and acts.
Evidence: [factory AGENTS.md line 84, talking to humans](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L84).
Acceptance: each loaded brief contains the five rules (test); a report with a cost has a number and a unit.
Verdict: KEEP.

#### MS-072 Focus stored in detail
As a seat (any), I want my reported focus and check-in stored in the record's `detail`, never its `why`, so that the Seats tab shows focus without hiding a refusal reason.
Evidence: [factory harness __main__.py line 3024, the check-in detail field](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L3024).
Acceptance: `detail.focus` and `detail.checked_in` written, `detail.present_keys` holds names only; `why` unchanged.
Verdict: KEEP.

## The Seats tab and the seat card

#### MS-180 One seat card component everywhere
As a human, I want every seat drawn as the same seat card wherever it appears, so that I learn one shape and read it the same on every tab.
Evidence: [the dashboard spec §3, the Seats tab and the seat card](../mike-dashboard.md#3-the-seats-tab-and-the-seat-card); [the approved mockup](../mike-dashboard.md#3-the-seats-tab-and-the-seat-card).
Acceptance: the Seats tab, the board, and the review surface render a seat through one component; a change to the card's markup appears on all three without a second edit.
Verdict: NEW.

#### MS-181 Cards grouped by role, responsive
As a human, I want cards grouped as orchestrators, lane-PEs, workers and reviewers, side by side on a desktop and stacked on a phone, so that I find a seat by its job on any screen.
Evidence: [the dashboard spec §3, the Seats tab and the seat card](../mike-dashboard.md#3-the-seats-tab-and-the-seat-card).
Acceptance: at 1180 px a group shows at least 2 cards per row; at 375 px one per row with no horizontal page scroll; the card's inner grid goes from two columns to one by its own container width.
Verdict: NEW.

#### MS-182 Seat card info block
As a human, I want each card to show name, role, liveness LED with its word, driver, last mint, assignment with its time, last steer with its time, context pressure as a bar gauge, and tokens since mint, so that one glance answers who, what, how long, and how full.
Evidence: [the dashboard spec §3, the Seats tab and the seat card](../mike-dashboard.md#3-the-seats-tab-and-the-seat-card); [MS-002, liveness in four words](#ms-002-liveness-in-four-words).
Acceptance: all nine fields present on every card; the LED color always has its word beside it; an unmeasured field reads unmeasured plus its reason and draws no bar; the gauge fill changes to warning at 60 percent and critical at 80 percent.
Verdict: NEW.

#### MS-183 Seat card controls
As a human, I want a start-stop switch and Restart, Steer, Mint and Archive at the bottom of each card, with a verb disabled and explained when the seat's row does not list it, so that I act on one seat without a menu hunt.
Evidence: [the dashboard spec §3, the Seats tab and the seat card](../mike-dashboard.md#3-the-seats-tab-and-the-seat-card); [MS-027, verb buttons explain themselves](seats.md#ms-027-verb-buttons-explain-themselves).
Acceptance: the five controls are present on every card; a control not in the row's `verbs` is disabled with `verb_why` as its hover text; a click posts one command and the card shows the job outcome.
Verdict: NEW.

#### MS-184 Phone card: expander and hamburger
As a human on a phone, I want the card's info behind a Details expander and its verbs behind a hamburger, with the start-stop switch still visible, so that the tab stays short and every verb has a touch path.
Evidence: [the dashboard spec §3, the Seats tab and the seat card](../mike-dashboard.md#3-the-seats-tab-and-the-seat-card); [MS-005, last confirmed steer shown](#ms-005-last-confirmed-steer-shown).
Acceptance: at 375 px a closed card is at most 3 lines tall; the expander and the hamburger each open with one tap; the switch is reachable without opening either; an open expander or menu survives a sessions frame.
Verdict: NEW.

## Phone layout

#### MS-139 Every tab fits a phone
As a human (Tig today), I want every tab readable on a phone, so that I run the fleet away from my desk.
Evidence: [factory dashboard app.css line 125, no breakpoint for the 8-column Sessions table](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.css#L125).
Acceptance: at 375 px width, 0 tabs need horizontal page scroll.
Verdict: CHANGE: today factory's Sessions tab fails; Mike lays out every tab, review surface and board included.

#### MS-140 Every seat verb by tap
As a human (Tig today), I want every single-seat verb reachable by tap, so that I need no right-click.
Evidence: [factory dashboard app.js line 1598, context menu, no touch path](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1598).
Acceptance: on a touch device each of the 5 seat verbs is reachable within 2 taps from the seat card.
Verdict: CHANGE: today the per-row menu needs a right-click.

## The board

#### MS-131 Arthur reads the board
As Arthur (arbiter), I want the board on each board change or newly idle seat (idle seats, each seat's assignment and last completed assignment, send-backs with owner seat, ready pull requests per seat, the priorities list with its notes, target and actual share per row), so that I decide who does what from one read.
Evidence: [factory harness idle_steer.py line 1279, the follow-up carries no board](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L1279); [mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share), [decision 1, Arthur steered on change](../mike.md#11-decisions).
Acceptance: the [factory#1761, send-back held awaiting-response](https://github.com/excaliwire/factory/issues/1761) state yields a board naming the 3 send-backs as next assignments; a tick with idle workers writes 0 planner rows.
Verdict: NEW.

#### MS-132 Board Arthur read is shown
As a human (Tig today), I want the board Arthur last read shown on the dashboard with its tick time, so that I can judge his choices against the same input.
Evidence: [factory dashboard rules.mjs line 57, no board view](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L57); [mike.md §7, the dashboard](../mike.md#7-the-dashboard); [Mike dashboard API §5, reads](../mike-dashboard-api.md#5-reads).
Acceptance: the page payload's board equals, byte for byte, the board in Arthur's last follow-up record.
Verdict: NEW.

#### MS-133 No steer across open work
As a worker (Artificer), I want Mike to refuse any steer that moves me off an open assignment, so that I keep my context; a replaced session is reminted onto the same work.
Evidence: [factory#1336 section 3, the harness redesign](https://github.com/excaliwire/factory/issues/1336) (Avalon lost context 4 times on 2026-09-26); [mike.md §3.2, mint, remint, steer](../mike.md#32-mint-remint-steer).
Acceptance: a steer naming a different item than the seat's open assignment is a refused record; a remint onto the same item is applied.
Verdict: NEW. The rule for the first cut; once the assignment closes the seat may be reused ([MS-174, Arthur reuses an idle seat](#ms-174-arthur-reuses-an-idle-seat)).

#### MS-134 Role names renamable in config
As Arthur (arbiter), I want the instance's role names renamable in config, so that renaming a seat needs no code change and no migration verb.
Evidence: [factory#1164, the hardened control-plane API](https://github.com/excaliwire/factory/pull/1164); [factory harness policy.py line 214, the role name policy](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/policy.py#L214); [mike.md §2, roles](../mike.md#2-roles).
Acceptance: renaming the `arbiter` default in config changes 0 code files and every record keeps the stable seat id.
Verdict: NEW.

#### MS-174 Arthur reuses an idle seat
As Arthur (arbiter), I want to steer an idle seat onto work related to its last completed assignment instead of minting a fresh seat, so that its context is not thrown away.
Evidence: [factory#1336 section 3, the harness redesign](https://github.com/excaliwire/factory/issues/1336) (Avalon lost context 4 times on 2026-09-26); [mike.md §3.2, mint, remint, steer](../mike.md#32-mint-remint-steer).
Acceptance: a steer from Arthur to a seat with no open assignment is applied with a record naming the seat's last completed assignment; tokens per assignment are recorded for reused and freshly minted seats so the saving is measured, not assumed.
Verdict: NEW.

#### MS-175 Board shows last completed assignment
As Arthur (arbiter), I want the board to show each idle seat's last completed assignment, so that I can pick a seat whose context fits the next issue.
Evidence: [factory harness idle_steer.py line 1279, the follow-up carries no board](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L1279); [mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share), [mike.md §3.2, mint, remint, steer](../mike.md#32-mint-remint-steer); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: each idle seat's board row names `owner/repo#N` of the last item whose `seat:<name>` label it held when the item closed, or `none`; the dashboard's board view shows the same.
Verdict: NEW.

## Target versus actual share

#### MS-135 Configurable share per rank
As a human (Tig today), I want a share per priority rank in the config store, defaulting by the number of lanes (1: 100; 2: 75, 25; 3: 60, 30, 10; 4: 50, 30, 15, 5 percent of workers), that I can override, with an empty row's share passed to the next, so that I set the split, not each assignment.
Evidence: [factory#1336 section 3, the harness redesign](https://github.com/excaliwire/factory/issues/1336); [mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share).
Acceptance: with no override, n lanes get weights T(n − i + 1) normalized, T(k) = k(k + 1) / 2 (test for n = 1 to 4); an override set not summing to 100 is refused; a row with 0 open issues above `urgency:no` shows target 0 and the next row's target rises by its share.
Verdict: NEW.

#### MS-136 Target versus actual share
As a human (Tig today), I want Health to show target versus actual share per priority row, so that a bad judgment by Arthur is visible.
Evidence: [factory#1336 section 4, the harness redesign](https://github.com/excaliwire/factory/issues/1336); [mike.md §9 rule 17, Health shows target versus actual share](../mike.md#9-what-mike-keeps); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: each row shows target percent and actual percent of assigned workers from labels; a gap over 20 points for 3 ticks is one attention item.
Verdict: NEW.
