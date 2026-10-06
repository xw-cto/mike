# Mike user stories: diagnose

The stories for diagnosis and health, audit records, job ids for commands, and the dashboard API contract. Rules, verdicts and the other files: [the user stories index](README.md).

## Diagnose and health

#### MS-044 Health first with snapshot age
As a human (Tig today), I want Health as the first tab with the snapshot age ticking, so that I see at a glance whether the data is fresh.
Evidence: [factory dashboard app.js line 606, the Health tab](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L606); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: "updated Ns ago" changes every second from the ISO `snapshot_at`; with none it reads "update time not recorded".
Verdict: CHANGE: the field is `snapshot_at` on the `health` part ([Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes)).
Urgency: high · Health with its snapshot age is an MLP tab

#### MS-045 Needs attention groups faults
As a human (Tig today), I want a Needs attention block that groups every fault by kind, worst first, with counts and links, so that I triage in one read.
Evidence: [factory dashboard app.js line 640, the Needs attention block](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L640); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: the summary reads "N not ok, M unmeasured" or "Nothing needs attention."; not-ok groups precede unmeasured.
Verdict: KEEP.
Urgency: high · Health's Problems section groups faults worst first

#### MS-046 Loop heartbeat and timer rows
As a human (Tig today), I want loop rows for heartbeat, mode, Running/Paused and timer, with the heartbeat stamped only by the loop, so that a stopped loop never reads as a Paused or healthy one.
Evidence: [factory dashboard rules.mjs line 635, the loop rows](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L635); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: a hand run of a verb leaves the heartbeat unchanged; timer not active is marked fault; Paused is marked paused.
Verdict: CHANGE: no row for a poke heartbeat or a tick verb list; one loop, one heartbeat.
Urgency: high · Health's Loop section shows heartbeat, mode, switch and timer

#### MS-047 Header names a stopped loop
As a human (Tig today), I want the header to read "Loop Paused: <reason>" or "Loop timer not active" on every tab, so that I never miss a stopped loop.
Evidence: [factory dashboard rules.mjs line 969, the header loop status](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L969).
Acceptance: the line is on all tabs while Paused and absent while Running with the timer active.
Verdict: KEEP.
Urgency: high · Tig must not miss a stopped loop on any MLP tab

#### MS-048 Hosts table shows host health
As a human (Tig today), I want a Hosts table with reachability, seat count, check-in age, checkout commit and pending actuations, so that I see which seat host is down.
Evidence: [factory dashboard rules.mjs line 775, the Hosts table](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L775); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: a host with a stale check-in is red with a note row; a host with 0 seats that never checked in is not in the payload.
Verdict: CHANGE: the server omits never-used hosts; the page filters nothing ([mike.md §10 item 21, dashboard patches](../mike.md#10-what-mike-does-not-re-create)).
Urgency: normal · seat hosts are v1

#### MS-049 Served commit and checkout lag
As a human (Tig today), I want the commit this control plane serves and how far the loop checkout is behind `main`, linked, so that I know whether a merge is live.
Evidence: [factory dashboard rules.mjs line 577, the served commit row](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L577); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: "serving <branch · sha8>, started <ISO time>"; the loop checkout item says "N behind".
Verdict: KEEP.
Urgency: normal · checkout lag matters with self-deploy; the MLP's version part names the version

#### MS-050 Unconfirmed steers counted per seat
As a human (Tig today), I want steers not confirmed counted per seat with a link to the matching log lines, so that I see lost deliveries.
Evidence: [factory harness attention.py line 271, the steers not confirmed finding](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L271).
Acceptance: the count equals the not-confirmed steer records in the window, for every runtime; "Show in log" opens a log view with exactly those lines.
Verdict: CHANGE: one delivery result for every runtime, not tmux pastes only.
Urgency: high · undelivered steers per seat is one of the MLP's numbers

#### MS-051 Mint anomaly named
As a human (Tig today), I want a mint anomaly named from the mint records, so that runaway minting is visible.
Evidence: [factory harness attention.py line 119, the mint anomaly finding](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L119).
Acceptance: Health shows "no seat minted twice for one issue" as ok or names each seat and issue; a vendor session with no mint record is one red item.
Verdict: CHANGE: one check over mint records replaces six detectors for past defects ([mike.md §10 item 21, dashboard patches](../mike.md#10-what-mike-does-not-re-create)).
Urgency: normal · two standing seats and the session gate stop runaway minting

#### MS-052 Platform faults named
As a human (Tig today), I want platform faults named (GitHub read budget, vendor account, store not writable, another loop on this store, runtime launcher missing on a seat host, process and tree disagree), so that I fix the platform before the fleet.
Evidence: [factory harness attention.py line 212, the platform faults](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L212).
Acceptance: each fault appears as its own labelled group when not ok and clears on the next snapshot after the fault clears.
Verdict: CHANGE: the account check is per vendor, not Cursor only.
Urgency: high · MLP part: read budget, vendor account and store faults; seat-host faults wait for v1

#### MS-053 Refusal streaks named
As a human (Tig today), I want a verb that refused N times in a row named, with each refusal's reason in its record, so that a broken verb shows and one cause is not buried under hundreds of rows.
Evidence: [factory harness api.py line 606, the refusal streak](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L606).
Acceptance: "<verb> refusing (N in a row): <why>" appears at the threshold inside the window; a later applied record clears it.
Verdict: CHANGE: refusal streaks only; Mike has no holds ([mike.md §10 item 1, the steer-idle planner](../mike.md#10-what-mike-does-not-re-create)).
Urgency: normal · refusals show in the Logs tab; streak detection waits for v1

#### MS-054 Four distinct connection failures
As a human (Tig today), I want signed out, not allowed, unreachable and wrong version each said differently, so that a refusal never looks like a dead control plane.
Evidence: [factory dashboard app.mjs line 108, the connection error states](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.mjs#L108); [Mike dashboard API §3, version](../mike-dashboard-api.md#3-version), [Mike dashboard API §4, the stream](../mike-dashboard-api.md#4-the-stream).
Acceptance: four distinct texts; 401 and 403 do not retry; other failures retry every 3 s.
Verdict: KEEP.
Urgency: high · Tig must tell signed out from down on his phone

#### MS-055 Live stream recovers itself
As a human (Tig today), I want the live stream to recover by itself after sleep, a proxy drop or a control plane restart, so that an open tab stays true.
Evidence: [factory dashboard app.mjs line 280, the stream reconnect](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.mjs#L280); [Mike dashboard API §4, the stream](../mike-dashboard-api.md#4-the-stream).
Acceptance: 45 s with no bytes, or a return to the tab, opens a new stream that resends every opening frame.
Verdict: KEEP.
Urgency: normal · the MLP polls the JSON reads every few seconds; the stream and its recovery are v1

#### MS-056 Health from the tick snapshot
As a human (Tig today), I want Health built from a snapshot the tick wrote, and a stale snapshot said on open pages, so that polling the page costs nothing and silence never reads as healthy.
Evidence: [factory harness api.py line 3995, the Health snapshot read](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L3995); [Mike dashboard API §4, the stream](../mike-dashboard-api.md#4-the-stream).
Acceptance: a Health request makes 0 vendor and 0 GitHub calls (test); within one keep-alive after the loop window passes, one `health` frame has `stale` true and the item "health snapshot stale", even with a log frame in the same pass.
Verdict: CHANGE: the stale signal is `stale` true on one `health` frame per stale period ([Mike dashboard API §4, the stream](../mike-dashboard-api.md#4-the-stream)).
Urgency: high · Health is built from the tick snapshot

#### MS-057 Watch and drive a tmux pane
As a human (Tig today), I want to watch a tmux seat's pane in the browser and take control to type, one human at a time, so that I can unstick it without SSH.
Evidence: [factory dashboard app.js line 2451, the browser terminal](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2451).
Acceptance: view mode sends 0 keys; keys reach the pane only after Take control; the seat host defers steers and restarts while a human has control and runs each once after.
Verdict: CHANGE: deferred from API 1.0.0; served by the seat host over a two-way channel and added later as a minor bump ([Mike dashboard API §8, what changed and the terminal deferral](../mike-dashboard-api.md#8-what-changed-from-the-starting-point)).
Urgency: no · terminal control from the browser is backlog

#### MS-105 One structured log
As a lane-PE, I want one structured log, rotated, secrets redacted, with every verb's start and end, so that I can rebuild a miss a week later.
Evidence: [factory harness harness_log.py line 1, the harness log](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/harness_log.py#L1).
Acceptance: every verb logs start and end with exit code and ms; a failure leaves a line even at exit 0; a scan of 7 days finds 0 secret values.
Verdict: CHANGE: the file is `mike.jsonl`; a new signal is a log line first ([mike.md §5, the control plane](../mike.md#5-the-control-plane)).
Urgency: high · one log is MLP

#### MS-106 Written path to one cause
As a lane-PE, I want a written path from "it did not fire" to one cause, so that I answer it without reading code.
Evidence: [factory agent-harness README.md line 240, the did-not-fire guide](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md#L240).
Acceptance: each branch (no event line, dry-run, `error=`, event id absent, gauge `unmeasured`) maps to exactly one cause.
Verdict: CHANGE: starts from the webhook event and the decision record, not the notification poll.
Urgency: normal · a written diagnosis path waits for the loop to be trusted

#### MS-107 Skip reads below budget reserve
As the loop, I want every GitHub-reading verb skipped for the tick when the read budget is below the reserve, so that polling cannot exhaust the token.
Evidence: [factory harness read_budget.py line 1, the read budget](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/read_budget.py#L1).
Acceptance: with remaining below `read_budget_reserve`, the tick records the number and makes 0 GitHub reads beyond the budget read.
Verdict: KEEP.
Urgency: high · the read reserve is MLP

#### MS-108 Remints counted per seat
As a lane-PE, I want remints per seat counted between two times from the records, so that I can measure churn.
Evidence: [factory harness __main__.py line 705, the remint count](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L705).
Acceptance: the count writes nothing and equals the applied mint and remint records for that seat in the range.
Verdict: KEEP.
Urgency: normal · records hold remints; a churn count waits for v1

#### MS-109 Each loop-down reason named
As a human (Tig today), I want each reason the loop cannot run named as its own token, so that I never read healthy for a loop that does not run.
Evidence: [factory agent-harness README.md line 208, the loop health tokens](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md#L208).
Acceptance: timer absent, timer inactive, another loop on the store, and checkout off branch each read as a distinct Health value; an unreadable scheduler reads `unmeasured`, never empty.
Verdict: CHANGE: one timer unit per instance and a store lock replace cron-line repair.
Urgency: high · Health must name why the one loop is down

## Audit records

#### MS-058 Filterable log in the URL
As a human (Tig today), I want the log under Health, filterable by level and up, component, seat, command, project and text, with the filter in the URL, so that I can share or reload a filtered view.
Evidence: [factory dashboard app.js line 1767, the log filters](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1767); [Mike dashboard API §5, reads](../mike-dashboard-api.md#5-reads).
Acceptance: the URL carries `log_*` keys; Back and Forward restore the filter; Clear empties every field.
Verdict: CHANGE: adds a project filter ([mike.md §1.2, multi-repository, one instance](../mike.md#12-multi-repository-one-instance)).
Urgency: high · the Logs tab's full filter, in the URL

#### MS-059 Since view reads whole window
As a human (Tig today), I want a "since" log view that reads the whole window up to 2000 rows, so that a count on Health matches the lines I see.
Evidence: [factory dashboard rules.mjs line 1151, the since log view](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1151); [Mike dashboard API §5, reads](../mike-dashboard-api.md#5-reads).
Acceptance: a since query sends `limit=2000`; rereads come at most every 30 s, one in flight.
Verdict: KEEP.
Urgency: normal · a log detail the MLP's two seats do not need

#### MS-060 Every command recorded with identity
As a human (Tig today), I want every dashboard command recorded with my identity and its outcome, so that I can audit who did what.
Evidence: [factory harness api.py line 4717, the command record](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L4717); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: one record per command, pending then applied, refused or cancelled, with `actor` and the job id.
Verdict: KEEP.
Urgency: high · every command is a recorded job with its actor

#### MS-061 Settings history by version
As a human (Tig today), I want every settings change stored as a new version with actor, and a history I can list, so that "who changed what" needs no pull request.
Evidence: [factory harness api.py line 5131, the settings versions](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L5131); [Mike dashboard API §5, reads](../mike-dashboard-api.md#5-reads).
Acceptance: the answer says "saved as version N"; one log line names key, actor, from and to; `settings history` lists every version.
Verdict: KEEP.
Urgency: high · versioned saves of the config store are MLP

## Job ids for commands

#### MS-137 Job ids for every command
As a human (Tig today), I want every command to return a job id at once, and its answer to land on a row I can see whenever it finishes, so that an answer after 30 s is not lost.
Evidence: [factory harness api.py line 4726, synchronous `run_verb`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L4726); [mike.md §7, the dashboard](../mike.md#7-the-dashboard); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: every command POST answers in under 1 s with a job id; a verb that takes 120 s shows its outcome on that job's row.
Verdict: NEW.
Urgency: high · commands as jobs are MLP

#### MS-138 ISO 8601 times on the wire
As a human (Tig today), I want every time on the wire in ISO 8601 with offset, so that the page never parses prose or guesses a year.
Evidence: [factory harness api.py line 478, `format_for_human`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L478); [mike.md §7, the dashboard](../mike.md#7-the-dashboard); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: a schema test finds 0 time fields not matching ISO 8601 with offset; the page has 0 time-zone tables.
Verdict: NEW.
Urgency: high · the MLP API parts carry ISO 8601 times

## Dashboard API contract

#### MS-177 Command outcome on the changed row
As a human (Tig today), I want a command's outcome shown on the row it changed, however long it took, so that I see the result where I acted.
Evidence: [mike.md §7, the dashboard](../mike.md#7-the-dashboard); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands), [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: each seat's outcome from `jobRow.seats` shows on that seat's card on the Seats tab; a steer that takes 120 s shows its outcome there with no reload; a stream reopen restores it from the opening `jobs` frame; `GET {base}/api/jobs?job=<id>` answers the same row.
Verdict: NEW.
Urgency: high · a job's outcome shows on the seat card it changed

#### MS-178 Stale settings write refused
As a human (Tig today), I want a settings save based on an old version refused, so that I never overwrite a change someone made after my page loaded.
Evidence: [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands); [MS-061, settings history by version](#ms-061-settings-history-by-version).
Acceptance: a `POST settings` whose `expected_version` is not the current `store_version` answers 409 and writes no version; the page says the setting changed and shows the new value; the save with the current version is applied.
Verdict: NEW.
Urgency: high · versioned saves refuse a stale write

#### MS-179 Open streams capped per caller
As a human (Tig today), I want each caller's open streams capped by config, so that a leaking app or a looping seat cannot exhaust the control plane.
Evidence: [Mike dashboard API §4, the stream](../mike-dashboard-api.md#4-the-stream).
Acceptance: with the cap at N, the caller's open N+1 answers 429 and the first N stay open; the page says the stream cap is reached, not that the control plane is down.
Verdict: NEW.
Urgency: normal · two seats and one human do not exhaust streams
