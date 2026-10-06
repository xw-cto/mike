# Mike user stories: operate

The stories for operating an instance: install and recover, identity and secrets, scoped tokens, attached sessions, and cost. Rules, verdicts and the other files: [the user stories index](README.md).

## Install and recover

#### MS-062 Hard Reboot the fleet
As a human (Tig today), I want Hard Reboot (archive and remint every seat, restart the control plane), optionally with Reset Defaults, so that I can start the fleet clean.
Evidence: [factory dashboard rules.mjs line 1290, Hard Reboot](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1290); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: one confirm (`confirm` equals the mode); the record names a human actor; after `reset-defaults` every seat ends idle and 0 `seat:` labels remain, written as one record; a seat token is refused.
Verdict: CHANGE: Reset Defaults is its own fleet mode `reset-defaults`, run as a separate job beside `hard-reboot` ([Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands)).

#### MS-063 Orchestrator Reboot starts fresh
As Arthur (arbiter), I want an Orchestrator Reboot to archive and remint K and me with idle assignments, so that a confused orchestrator starts fresh.
Evidence: [factory dashboard rules.mjs line 1291, Orchestrator Reboot](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1291); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: only the `arbiter` and `tpm` role seats are reminted; both read idle afterwards.
Verdict: KEEP.

#### MS-064 Fill-Missing closes gaps
As a human (Tig today), I want Fill-Missing to adopt or mint every absent pool seat and leave live ones alone, capped per window, so that gaps close in one click.
Evidence: [factory dashboard rules.mjs line 1293, Fill-Missing](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1293); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: 0 responding or unmeasured seats are reminted ([gate 7, one session per seat name](../mike.md#33-gates-mike-enforces-for-every-caller)); at most `max_creates` per seat per `window_minutes`; the confirm states the mint count and the vendor each bills.
Verdict: CHANGE: adopt, not claim; never a lane-PE; the cost line comes from vendor config, not fixed text.

#### MS-065 Fleet commands never collide
As a human (Tig today), I want a running fleet command shown as progress, and the server to refuse any command that collides with it, so that two commands cannot collide.
Evidence: [factory dashboard rules.mjs line 1005, the fleet command progress](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1005); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: "<mode>: step N of M, started by <actor>" shows to every viewer; the server answers 409 to a colliding seat verb or fleet mode.
Verdict: CHANGE: factory's seat verbs have no server busy check, only a client lock ([mike.md §10 item 21, dashboard patches](../mike.md#10-what-mike-does-not-re-create)).

#### MS-066 Restart the control plane
As a human (Tig today), I want to restart the control plane process from the page, even while Paused, so that I recover a stuck API without SSH.
Evidence: [factory dashboard rules.mjs line 1294, the control plane restart](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1294); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: one confirm; the stream reconnects in under 10 s; 0 seats reminted.
Verdict: KEEP.

#### MS-110 One install command
As a human (Tig today), I want one command that installs the tool stack on Linux or Windows, so that a fresh machine reaches ready without a package list in my head.
Evidence: [factory agent-harness install.sh line 2, the install script](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/install.sh#L2).
Acceptance: the check exits 0 with every must-have present, exits 1 naming the installer to run; `--check-only` changes nothing.
Verdict: KEEP.

#### MS-111 Cloud setup installs the delta
As a seat host, I want a cloud setup script that installs only the delta over the vendor image and never fails the session, so that cloud seats boot with pinned tools.
Evidence: [factory agent-harness cloud-environment.sh line 2, the cloud setup script](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/cloud-environment.sh#L2).
Acceptance: exits 0 on every run in under 5 minutes; a second run on the same machine is a no-op.
Verdict: KEEP.

#### MS-112 One non-overlapping tick timer
As the loop, I want one timer that starts a tick 60 s after the last one finished and never overlaps it, so that two ticks never act at once.
Evidence: [factory agent-harness deploy/control-plane/hgl-control-loop.timer line 7, the tick timer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/deploy/control-plane/hgl-control-loop.timer#L7).
Acceptance: over 24 hours, 0 tick start times fall inside another tick's run; one loop per instance.
Verdict: KEEP.

#### MS-113 Narrow-helper control plane deploy
As a human (Tig today), I want the control plane deployed from the instance's checkout and restarted by a narrow root helper, so that a deploy needs no shell on the control-plane host.
Evidence: [factory agent-harness deploy/control-plane/apply-unit.sh line 1, the apply-unit helper](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/deploy/control-plane/apply-unit.sh#L1).
Acceptance: the restart action neither fetches nor installs; the helper never starts or stops the loop timer.
Verdict: KEEP.

#### MS-114 End-to-end proof on a host
As a human (Tig today), I want an end-to-end proof on a real seat host for event routing, gauges and confirmed steer delivery, posted on the pull request before ready, so that a green contract test is not mistaken for a working host.
Evidence: [factory agent-harness e2e-box.md line 1, the end-to-end proof](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/e2e-box.md#L1).
Acceptance: stdout has one line per part, each a number, an id, or `unmeasured`; the pull request carries the output before ready.
Verdict: CHANGE: the retarget and ladder lines go; one delivery line per runtime comes in.

#### MS-115 Remint seats when main moves
As the loop, I want seats running code that a `main` move changed reminted, and all actuation stopped when the loop's own checkout lacks the fetched `main`, so that a broken fetch cannot steer live seats with old code.
Evidence: [factory harness main_restart.py line 1, main-restart](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/main_restart.py#L1).
Acceptance: a docs-only `main` move remints 0 seats; with the checkout behind, the tick records 0 seat actions and one refusal.
Verdict: CHANGE: the preserve and remint name lists go; what a seat runs is read from config.

#### MS-116 Restart control plane on drift
As the loop, I want the control plane restarted once, recorded first, when the commit it serves differs from the instance checkout, so that a merged fix reaches the API.
Evidence: [factory harness serve_restart.py line 1, serve-restart](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/serve_restart.py#L1).
Acceptance: the decision record precedes the restart; a missing unit or helper refuses by name; unreadable health is `unmeasured`.
Verdict: KEEP.

#### MS-117 Discard stale actuation backlog
As a lane-PE, I want a stale pending actuation backlog discarded without touching claimed ones, so that a returning seat host does not replay old steers.
Evidence: [factory harness __main__.py line 3196, the backlog discard](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L3196).
Acceptance: matching pending rows become refused with `why: stale-backlog`; claimed rows are unchanged.
Verdict: CHANGE: the store expires a pending actuation after a configured age as well, so a discard is rarely needed.

#### MS-118 Dismiss grok usage-limit dialogs
As a seat host, I want a vendor usage-limit dialog on a grok-tmux pane dismissed with that dialog's own key, so that a seat stuck on a modal resumes.
Evidence: [factory harness tmux.py line 188, the usage-limit dialog key](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/tmux.py#L188).
Acceptance: dismissed only when the heading and the `Shift+x:dismiss` footer are both on the pane; a sign-in prompt gets 0 keys; not retried.
Verdict: CHANGE: lives in the grok-tmux runtime driver under the Mike Runtime API, not in core ([mike.md §4, runtimes](../mike.md#4-runtimes)).

#### MS-119 Reap expired branches
As the loop, I want expired reserved-prefix branches deleted, and a no-op run still recorded, so that throwaway branches do not pile up and silence does not mean "did not run".
Evidence: [factory harness reap.py line 1, the branch reaper](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/reap.py#L1).
Acceptance: a branch without the prefix or younger than `max_age_days` is untouched; each run writes one record.
Verdict: KEEP.

## Identity and secrets

#### MS-067 Microsoft sign-in renews silently
As a human (Tig today), I want to sign in with Microsoft, renew silently, and be told when a renewal needs me, so that a long session does not just die.
Evidence: [factory dashboard client.mjs line 158, the sign-in renewal](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/client.mjs#L158); [Mike dashboard API §2, identity](../mike-dashboard-api.md#2-identity).
Acceptance: a silent renewal shows "Your sign-in renewed silently." for 10 s; an interactive need redirects with a notice.
Verdict: CHANGE: identity provider, base path and origins are instance config ([mike.md §7, the dashboard](../mike.md#7-the-dashboard), [tig/mike#1, the dashboard rewrite](https://github.com/tig/mike/issues/1)).

#### MS-120 Vendor keys stored safely
As a human (Tig today), I want a vendor key stored by hidden prompt, mode 600, and its account checked against config, so that a key is never in history and spend lands on the right account.
Evidence: [factory harness __main__.py line 2093, the hidden key prompt](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L2093).
Acceptance: file mode 600; the key is in no log, record or argv; a key on the wrong account is a Health fault and mint refuses.
Verdict: CHANGE: one check per vendor, not Cursor only.

#### MS-121 Secrets outside live state
As a lane-PE, I want secrets kept in a directory outside live state and referenced by name, so that wiping live state does not drop credentials.
Evidence: [factory agent-harness load-secrets.sh line 2, the secrets loader](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/load-secrets.sh#L2).
Acceptance: after deleting live state, the next verb finds its credentials; 0 secret values in logs, records or check-ins.
Verdict: CHANGE: the config store names each secret; no wrapper exports all of them into every verb's environment.

#### MS-122 No seat acts as a human
As a human (Tig today), I want no seat able to post, review, push or run GitHub calls as a human merger, and Arthur's GitHub token read-only, so that a waiver or approval in my name cannot be forged.
Evidence: [factory AGENTS.md line 59, the no-human-account rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L59).
Acceptance: a write as the merger account from Mike raises; `waive:` is honored only from that account.
Verdict: KEEP.

#### MS-123 Host tokens name one host
As a seat host, I want a host token that names one host and a verified bearer on every pull, check-in and result, so that a compromised host can act only for itself.
Evidence: [factory harness __main__.py line 3387, the host token check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L3387).
Acceptance: a check-in naming another host is refused; signature, iss, aud, tid, exp and nbf are all checked; the identity read lists roles with no secret.
Verdict: KEEP.

#### MS-124 Fixed writer, owner, addressee marks
As a seat (any), I want writer, owner and addressee carried by fixed marks, so that nobody is ambiguous across GitHub accounts.
Evidence: [factory AGENTS.md line 48, the address marks](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L48).
Acceptance: gate parsers accept an optional `[Name] ` prefix and nothing else; `To: Name` at the start of the body (after the prefix, if any) is the address; 0 open titles carry a `[Name]` or `Name:` prefix; ownership reads only the label.
```
[Name] <text>              written by seat Name
To: Name. <text>           addressed to seat Name (a human writes this with no prefix)
[Name] To: Other. <text>   written by Name, addressed to Other
seat:<name>                label: the seat that owns this issue or pull request
```
Verdict: CHANGE: `To: Name` is the address, the email header word; factory's `Name:` form retires because it means the speaker in a transcript and the addressee on IRC ([mike.md §2.1, humans](../mike.md#21-humans), [mike.md §9 rule 15, the address contract](../mike.md#9-what-mike-keeps)).

## Seat and host scoped tokens

#### MS-152 Seat tokens act only as self
As a seat (any), I want my token to name me and act only as me, so that a leaked seat token cannot steer or mint another seat.
Evidence: [factory agent-harness seats.yaml line 57, caller matrix](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/seats.yaml#L57); [mike.md §4, runtimes](../mike.md#4-runtimes), [mike.md §9 rule 12, the caller matrix](../mike.md#9-what-mike-keeps); [Mike dashboard API §2, identity](../mike-dashboard-api.md#2-identity).
Acceptance: a seat token used on any other seat's self-verb is refused with a record; Arthur's and lane-PE steers pass only the matrix rows for their role.
Verdict: NEW.

#### MS-153 No master secret on hosts
As a seat host, I want no shared master secret on my machine and no inbound path or SSH key from the control plane, so that a compromised host cannot mint tokens for other seats.
Evidence: [factory docs/host.md line 258, the host secret](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/host.md#L258), [factory#1413, host secret mints any token](https://github.com/excaliwire/factory/issues/1413); [mike.md §4, runtimes](../mike.md#4-runtimes).
Acceptance: a scan of each seat host finds 0 files that can mint a token for another seat; the control-plane host holds 0 SSH keys to seat hosts.
Verdict: NEW.

#### MS-154 Humans are verified bearers
As a human (Tig today), I want to be a verified bearer, not a header any local process can set, so that a local script cannot act as me.
Evidence: [factory dashboard serve.py line 418, adds `X-HGL-Email`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/serve.py#L418); [mike.md §4, runtimes](../mike.md#4-runtimes), [mike.md §10 item 8, a shared secret and a header gate](../mike.md#10-what-mike-does-not-re-create); [Mike dashboard API §2, identity](../mike-dashboard-api.md#2-identity).
Acceptance: a request with only an email header and no verified bearer is refused 401 on every human-only route.
Verdict: NEW.

## Attached sessions

#### MS-159 Revocable attached session tokens
As a human (Tig today), I want to issue a named, revocable session token to a session I drive (Infra Fable, Factory Fable, my portal), so that it can act through Mike without a seat and without my own credentials.
Evidence: [mike.md §2.2, attached sessions](../mike.md#22-attached-sessions-non-seats-that-act-through-mike) and [mike.md §4, runtimes](../mike.md#4-runtimes) (Identity); factory has only a seat token minted from a shared secret, [factory hgl-auth agent_token.py line 54, the shared-secret seat token](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/host/hgl-auth/agent_token.py#L54); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: the token carries the session name and its verb list; a revoked token is refused on the next call with a record; no shared secret can mint one.
Verdict: NEW.

#### MS-160 Attached sessions write through Mike
As an attached session, I want every repository interaction (issue create, label, urgency, comment, pull ready, request merge) to go through Mike's verbs with my token, so that each is recorded first and written under Mike's account with my `[Name]` prefix.
Evidence: [mike.md §2.2, attached sessions](../mike.md#22-attached-sessions-non-seats-that-act-through-mike), [mike.md §5, the control plane](../mike.md#5-the-control-plane) (GitHub), [mike.md §9 rule 3, one choke point for GitHub writes](../mike.md#9-what-mike-keeps), [mike.md §9 rule 15, the address contract](../mike.md#9-what-mike-keeps).
Acceptance: one decision record per call with `actor` = the session name; the GitHub write is by Mike's account and starts `[Name] `; a call with no record is refused.
Verdict: NEW.

#### MS-161 Attached sessions read the board
As an attached session, I want to read the board, sessions, health and priorities over the same API a seat reads, so that my judgment uses the operator's view.
Evidence: [mike.md §2.2, attached sessions](../mike.md#22-attached-sessions-non-seats-that-act-through-mike), [mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share); seats read the same API in [MS-008, Arthur reads the same API](observe.md#ms-008-arthur-reads-the-same-api); [Mike dashboard API §5, reads](../mike-dashboard-api.md#5-reads).
Acceptance: `GET {base}/api/seats` and `GET {base}/api/board` answer a session token with the same rows the page draws.
Verdict: NEW.

#### MS-162 Attached sessions steer through gates
As an attached session whose config row allows it, I want to steer a seat through Mike bound by every gate, so that I can direct work at night without a comment Arthur must notice.
Evidence: [mike.md §2.2, attached sessions](../mike.md#22-attached-sessions-non-seats-that-act-through-mike), [mike.md §3.3, gates for every caller](../mike.md#33-gates-mike-enforces-for-every-caller); [factory#1336 comment 2026-10-05 05:18 UTC, the harness redesign](https://github.com/excaliwire/factory/issues/1336) (steers delivered as `Arthur:` comments); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: a steer from the session passes [gates 1 to 6, owner gate through record before act](../mike.md#33-gates-mike-enforces-for-every-caller) or is refused with a record naming the gate; a session whose row lacks `steer` gets 403 and a refused record.
Verdict: NEW.

#### MS-163 Attached sessions listed apart
As a human (Tig today), I want attached sessions listed on the dashboard with last call and token age, apart from the Seats tab, so that I can see who is acting through Mike and revoke one.
Evidence: [mike.md §2.2, attached sessions](../mike.md#22-attached-sessions-non-seats-that-act-through-mike), [mike.md §7, the dashboard](../mike.md#7-the-dashboard); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: one row per token with name, verbs, last call time, issued-at; a Revoke verb with one confirm; the Seats tab shows no attached session.
Verdict: NEW.

#### MS-164 Attaching is optional
As an attached session, I want attaching to be optional, so that a session with no token works as today and Mike sees it only through GitHub.
Evidence: [mike.md §2.2, attached sessions](../mike.md#22-attached-sessions-non-seats-that-act-through-mike).
Acceptance: with no token set, the CLI's Mike verbs refuse and name the token; the session's direct GitHub comments carry no actor record and raise no Health row.
Verdict: NEW.

## Cost

#### MS-068 Tokens per seat and fleet
As a human (Tig today), I want tokens per seat since its last mint and a fleet total that never counts unmeasured as zero, so that I see spend.
Evidence: [factory dashboard app.js line 530, the token columns](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L530); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: the total reads "incomplete" with an unmeasured count when any seat is unmeasured; each bar is that seat's percent of the measured total.
Verdict: KEEP.

#### MS-069 Context fullness per seat
As a human (Tig today), I want each seat's context fullness, fullest first, so that I can remint a seat before it summarizes.
Evidence: [factory dashboard rules.mjs line 414, the context fullness column](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L414); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: measured seats sorted by percent descending; "summarized" marked; unmeasured seats last with their reason.
Verdict: KEEP.

#### MS-070 Vendor included pools shown
As a human (Tig today), I want each vendor's included pools with percent used, age and overage, so that I know when we start paying more.
Evidence: [factory dashboard app.js line 363, the included pools gauges](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L363); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: one row per configured pool reading "N% used, <age>" or "unmeasured, <reason>"; a pool with no gauge source is named as not shown.
Verdict: CHANGE: pools come from vendor config, not two fixed Cursor names and a code tuple.

#### MS-125 Gauges read unmeasured, not guessed
As the loop, I want every gauge to read `unmeasured` with a reason rather than a guessed percent, and a reading older than its stale window treated as `unmeasured`, so that no decision runs on stale or invented data.
Evidence: [factory harness write_meters.py line 1, the meter writer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/write_meters.py#L1).
Acceptance: every absent source yields the literal `unmeasured` and a `why`; a `5% left` line parses to 95 used; text without a percent is `unparsed`.
Verdict: CHANGE: gauge sources are config; a vendor usage API is preferred over a screen scrape ([mike.md §10 item 19, screen-scraped meters](../mike.md#10-what-mike-does-not-re-create)).

#### MS-126 Price spend before it runs
As a seat (any), I want to price a spend before it runs and report cost unasked, so that a human only says yes to money he can see.
Evidence: [factory AGENTS.md line 117, the cost rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L117).
Acceptance: model-call spend under USD 100 needs no ask and is reported; any other spend, or over USD 100, waits for a yes; the price is a number from a measurement.
Verdict: KEEP.

#### MS-127 One pull request read per project
As the loop, I want one read of open pull requests and one of open issues per project per tick, with urgency and lane read from labels, so that a 60 s tick fits the GitHub rate limit.
Evidence: [factory agent-harness retarget-loop.sh line 64, the tick reads](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/retarget-loop.sh#L64).
Acceptance: GitHub reads per tick equal 1 pull-request page plus 1 issue page per project and 0 Priority field reads; a failed page is not reused.
Verdict: CHANGE: per project across the instance; urgency is a label, so the Priority field connection goes ([mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share)); webhook events cut the reads further.
