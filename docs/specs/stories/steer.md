# Mike user stories: steer

The stories for steering and assigning seats, what the control plane watches, and humans acting on GitHub. Rules, verdicts and the other files: [the user stories index](README.md).

## Steer and assign

#### MS-010 Steer one seat from its page
As a human (Tig today), I want to type a steer on a seat's page and send it, so that I can redirect one seat fast.
Evidence: [factory dashboard app.js line 2513, the seat page steer box](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2513); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: one POST `{verb:steer, seats:[name], prompt}` answered 202 with a job id; the button is disabled unless the row's `verbs` lists steer; the job's outcome names confirmed or not confirmed.
Verdict: CHANGE: 202 with a job id; the outcome arrives on the `jobs` part, not in a synchronous answer ([Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands)).

#### MS-011 Steer several seats at once
As a human (Tig today), I want to steer several checked seats at once with one prompt and an optional assignment, so that I can redirect a group.
Evidence: [factory dashboard app.js line 1377, the multi-seat steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1377); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: one POST with `seats` equal to every checked name; refused before sending when prompt and assignment are both empty.
Verdict: KEEP.

#### MS-012 Set or clear an assignment
As a human (Tig today), I want to set a seat's assignment (`owner/repo#N`) while minting, steering or restarting, and clear it with `idle`, so that I own the durable assignment.
Evidence: [factory dashboard verbs.mjs line 106, the assignment input](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L106); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: after a save the `seat:<name>` label is on that issue within one tick; empty input changes nothing; `idle` removes the label.
Verdict: CHANGE: the write is the label in the named project, recorded first.

#### MS-013 Pending steer shown apart
As a human (Tig today), I want a pending steer shown apart from the last confirmed one, with its age and why it waits, so that I know why a steer has not landed.
Evidence: [factory dashboard rules.mjs line 914, the pending steer cell](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L914); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: with the loop Paused and a steer pending, the cell reads "pending, not delivered: Paused, <age>" and a second steer to that seat is refused.
Verdict: CHANGE: at most one pending steer per seat ([gate 5, one pending steer](../mike.md#33-gates-mike-enforces-for-every-caller)) with a reason, replacing the separate "Assignments untouched" finding.

#### MS-014 Stop keeps the session
As a human (Tig today), I want Stop to set a seat idle and keep its session, and only me or Arthur to undo it, so that the loop leaves it alone.
Evidence: [factory dashboard verbs.mjs line 66, the Stop verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L66).
Acceptance: after Stop the cell reads "stopped"; 0 loop steer records target the seat until a record by a human or Arthur clears Stop.
Verdict: CHANGE: factory clears Stop on any human steer; Mike lets a human or Arthur clear it, nothing else ([gate 8, the human switches](../mike.md#33-gates-mike-enforces-for-every-caller)).

#### MS-015 Edit the priorities list
As a human (Tig today), I want a priorities list with one row per lane that I can reorder by tap or drag and give a note per row, so that I set what the fleet works on from phone or desk.
Evidence: [factory dashboard app.js line 2143, the priorities editor](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L2143); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: each reorder or note edit is one POST and one config-store version; the list always has exactly one row per configured lane; adding or deleting a row is refused and names the lanes config; up and down work without drag.
Verdict: CHANGE: priorities list, not direction; one row per lane, so every lane is ranked; rows change only when the lanes in config change ([mike.md §3, the seat model, lanes](../mike.md#3-the-seat-model), [mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share)); Mike's API has `POST priorities` (reorder or note) and no `direction` command ([Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands), [decision 8, priorities replace direction](../mike.md#11-decisions)).

#### MS-016 Rows follow configured lanes
As a human (Tig today), I want the priorities rows built from the configured lanes, not typed, so that the list cannot contain a typo or miss a lane.
Evidence: [factory dashboard rules.mjs line 1227, the lane picker](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1227); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: adding a lane in config adds one row at the bottom and removing one removes its row, each one config-store version; there is no lane picker and no free-text lane.
Verdict: CHANGE: factory's picker guards typed rows; Mike has no typed rows ([mike.md §3, the seat model, lanes](../mike.md#3-the-seat-model)).

#### MS-017 Priorities page names unreadable store
As a human (Tig today), I want the priorities page to say when it cannot read the store, so that an unreadable store does not look empty.
Evidence: [factory dashboard rules.mjs line 558, the unreadable store message](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L558).
Acceptance: with the store unreadable the page reads "unmeasured: <reason>", a save is refused, and every worker steer is refused.
Verdict: CHANGE: no seed file view; shipped defaults and instance config are separate files ([mike.md §5, the control plane](../mike.md#5-the-control-plane), [mike.md §10 item 16, settings seeded from four places](../mike.md#10-what-mike-does-not-re-create)).

#### MS-018 Arthur steers with his token
As Arthur (arbiter), I want to steer a seat with my seat token when the caller matrix allows it, and a denied attempt recorded with my name, so that I assign work without a click and a denial is evidence.
Evidence: [factory harness api.py line 4686, the seat-token steer check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L4686); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: an allowed call answers 202 and its job reads `actor=<seat>`; a denied one answers 403 and writes a record with `caller=<seat>`, outcome refused.
Verdict: CHANGE: every gate in [mike.md §3.3, gates for every caller](../mike.md#33-gates-mike-enforces-for-every-caller) applies to Arthur's steers as to the loop's; the actor is on the job row ([Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands)).

#### MS-019 Steer only owner-assigned work
As the loop, I want to steer only issues and pull requests assigned to `gh_user`, and a human to confirm any change to it, so that a wrong login cannot start spending.
Evidence: [factory harness harness_gh_user.py line 1, the harness-gh-user gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/harness_gh_user.py#L1).
Acceptance: changing `gh_user` opens a confirm; with it empty or unmeasured, 0 steers apply and each is a refused record.
Verdict: KEEP. Renamed from harness-gh-user.

#### MS-073 Record every steer first
As Arthur (arbiter), I want every steer recorded before it is sent, and apply to refuse an unrecorded decision, so that no steer exists without a trail.
Evidence: [factory harness __main__.py line 748, the record-before-act steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L748).
Acceptance: for 100% of steers the record's write time precedes the send; apply with no record id is refused.
Verdict: KEEP.

#### MS-074 No worker steer onto urgency:no
As a human (Tig today), I want any worker steer onto an `urgency:no` issue, or one with no urgency label, refused for every caller, so that spare capacity is never spent on work nobody marked urgent.
Evidence: [factory harness severity_floor.py line 1, the severity floor](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/severity_floor.py#L1).
Acceptance: the refusal reads `urgency floor: urgency:no is never steered` with a record; unreadable labels refuse as `unmeasured`; factory's Urgent, High, Medium and Low map to `critical`, `high`, `normal` and `no`.
Verdict: CHANGE: urgency is a label, `urgency:<level>`, not the GitHub Priority field, so a human sets it from the GitHub mobile app ([gate 4, the urgency floor](../mike.md#33-gates-mike-enforces-for-every-caller), [mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share)).

#### MS-075 No action on unmeasured liveness
As the loop, I want no mint, steer or restart decided on a seat whose liveness is unmeasured, so that a blind read cannot plan work over running seats.
Evidence: [factory harness liveness.py line 1, the liveness module](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/liveness.py#L1).
Acceptance: with a seat `unmeasured`, 0 mints and 0 loop steers target it; each attempt is a refused record naming the reason.
Verdict: KEEP.

#### MS-076 Lane-PE files, workers code
As a lane-PE, I want to file an issue with an `urgency:<level>` label and a lane label and steer it to a worker instead of writing code, so that judgment stays separate from development.
Evidence: [factory brief factory-pe.md line 79, the lane-PE file-and-steer rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/factory-pe.md#L79).
Acceptance: 0 development pull requests authored by Arthur, K or lane-PE seats; `pr-check` names one as a finding; a `[none]` title prefix does not bypass it; each filed issue carries one `urgency:` label and one lane label.
Verdict: CHANGE: urgency is set as a label, not the Priority field ([mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share)).

#### MS-077 GitHub writes through Mike
As a seat (any), I want issue and pull-request writes through Mike's verbs, recorded first, through one GitHub module, so that no seat runs raw `gh` and no write comes from a read-only account.
Evidence: [factory harness gh.py line 1, the GitHub write module](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/gh.py#L1).
Acceptance: only one module spawns `gh` or calls the API (test); a write as the read-only account raises; a GraphQL mutation counts as a write.
Verdict: KEEP.

#### MS-078 Geas lints every prompt
As the loop, I want every outbound steer, poke and mint prompt linted by Geas against the banned-terms table before sending, so that a banned word never reaches a seat.
Evidence: [factory harness geas.py line 1, Geas](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/geas.py#L1).
Acceptance: a prompt with a banned term is refused with 0 bytes sent; the table comes from the project's hook, not from Mike.
Verdict: KEEP.

#### MS-079 Events routed to the owner seat
As the loop, I want a GitHub event on an issue or pull request routed to the seat its `seat:<name>` label names, so that the owner hears about a comment or review without polling.
Evidence: [factory harness poke.py line 525, the event routing](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/poke.py#L525).
Acceptance: a signed webhook delivery produces one prompt of the form `[<owner>] GitHub poke (<reason>): <title>` within one tick; an unsigned delivery is refused.
Verdict: CHANGE: signed webhook is the design; polling a human's notifications is a fallback ([mike.md §5, the control plane](../mike.md#5-the-control-plane)).

#### MS-080 K nudges missing self-review
As K (TPM), I want to post one nudge when a ready pull request has no owner self-review on its head, so that the gate is met by the owner, not waived.
Evidence: [factory brief tpm.md line 55, K's self-review nudge](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/tpm.md#L55).
Acceptance: at most one nudge per pull request per head, in this shape:
```
[K (TPM)] <owner seat>, owner self-review is missing on <sha>.
```
Verdict: CHANGE: the name is the instance's TPM name; the sha is named.

#### MS-081 K follows up idle lane-PEs
As K (TPM), I want to send a follow-up once per idle stretch to a lane-PE idle past 30 minutes, with the measured idle time, 1 to 3 open items, and a reminder to use a cheaper model for grunt work, so that a stalled lane-PE moves without a human.
Evidence: [factory brief tpm.md line 57, K's idle follow-up](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/tpm.md#L57).
Acceptance: 0 or 1 follow-ups per lane-PE per idle stretch; each names idle minutes and a last-activity ISO time.
Verdict: CHANGE: delivered as a follow-up steer through Mike, gated like every steer.

## The control plane watches

#### MS-165 Control plane detects every change
As the loop, I want to detect every board change myself, from signed webhooks and a diff of my own store each tick, so that no seat polls GitHub and no vendor scheduler watches anything for Mike.
Evidence: [mike.md §5, the control plane](../mike.md#5-the-control-plane) and [mike.md §9 rule 22, the control plane is the only watcher](../mike.md#9-what-mike-keeps); factory polls a human's notifications in [factory harness poke.py line 1, polling a human's notifications](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/poke.py#L1) and seats read GitHub themselves.
Acceptance: with the webhook delivering, a tick makes 0 GitHub reads that are not the budgeted store refresh; a brief contains no instruction to poll or watch GitHub; a seat's own `gh` read of issue state is a refused record.
Verdict: NEW.

#### MS-166 Changes routed as steers
As the loop, I want each detected change routed to the seat it concerns as one recorded steer (Arthur for a board change or an idle seat; the author for a send-back, a conflict or Copilot findings; a reviewer for a ready pull request), so that a seat is told and never has to notice.
Evidence: [mike.md §5, the control plane](../mike.md#5-the-control-plane), [mike.md §3.4, review and send-back](../mike.md#34-review-and-send-back), [decision 1, Arthur steered on change](../mike.md#11-decisions) and [decision 5, conflicts are changes, not verbs](../mike.md#11-decisions); factory runs conflict-steer and copilot-findings as verbs ([MS-094, conflicts and Copilot threads sent back](review.md#ms-094-conflicts-and-copilot-threads-sent-back)).
Acceptance: one steer record per change with `why` naming the change kind and the GitHub event or diff that produced it; the same change produces 0 further steers; the steer passes the gates or is a refused record.
Verdict: NEW.

#### MS-167 Row note carried in steers
As a lane-PE, I want the note on my lane's priorities row carried in every steer I receive, so that a human's intent for the row is my context without a comment I must find.
Evidence: [mike.md §3.1, pool, assignment and share](../mike.md#31-pool-assignment-share), [decision 2, a lane plus a note](../mike.md#11-decisions).
Acceptance: a steer to a lane-PE whose lane has a row with a note contains that note verbatim; a row with no note adds nothing; the note appears on the board Arthur reads.
Verdict: NEW.

## Humans on GitHub

#### MS-168 Human issues reach the board
As a human, I want an issue I create to reach the board when I give it a lane label and assign it to `gh_user`, so that handing work to Mike is one GitHub action I already know.
Evidence: [mike.md §2.1, humans](../mike.md#21-humans); factory's harness-gh-user gate, [factory harness harness_gh_user.py line 1, the harness-gh-user gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/harness_gh_user.py#L1).
Acceptance: within one tick of the assignment webhook the issue is on the board with my `urgency:` label, or `urgency:no` if I set none; before the assignment it is not on the board.
Verdict: NEW.

#### MS-169 Addressed comments become steers
As a human, I want a comment I start with `To: Name` on an issue or pull request delivered to that seat as a steer, so that I direct a seat from GitHub on my phone without a dashboard.
Evidence: [mike.md §2.1, humans](../mike.md#21-humans), [mike.md §9 rule 15, the address contract](../mike.md#9-what-mike-keeps) (address contract); [factory#1336 comment 2026-10-05 05:18 UTC, the harness redesign](https://github.com/excaliwire/factory/issues/1336) (`Arthur:` comments as steers).
Acceptance: one steer record per addressed comment with `why` naming the comment id and my login; the steer passes the gates or is a refused record; an unaddressed comment, one starting only with a writer prefix `[Name]`, or one using factory's `Name:` or the retired `[Name]:` form produces 0 steers and one lint line.
Verdict: NEW.

#### MS-170 Human reviews count when configured
As a human, I want my change request on a ready pull request to be the send-back and my Merge verdict to count as the independent review when config says so, so that a review I did is not redone by a reviewer seat.
Evidence: [mike.md §2.1, humans](../mike.md#21-humans), [mike.md §3.4, review and send-back](../mike.md#34-review-and-send-back), [mike.md §3.6, how reviewers operate](../mike.md#36-how-reviewers-operate), [mike.md §6, the pull request lifecycle](../mike.md#6-the-pull-request-lifecycle); factory's `independent_review_writers` and `reviewer:` grant, [factory harness pr_state.py line 45, independent review writers](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L45).
Acceptance: a change request from a listed human is a send-back: it returns the pull request to draft and steers the owner seat; with `human_review_counts` on, a Merge verdict from a listed human satisfies the review gate for that head.
Verdict: NEW.

#### MS-171 Unlisted users are contributors
As a human, I want a GitHub user not on the instance's human list treated as a contributor, so that their issues and comments are seen but bind nothing.
Evidence: [mike.md §2.1, humans](../mike.md#21-humans).
Acceptance: a contributor's issue shows on the board as unassigned contributor work; their `waive:`, `reviewer:` and `To: Name` comments produce 0 records that act; a listed human's assignment of that issue puts it on the board.
Verdict: NEW.
