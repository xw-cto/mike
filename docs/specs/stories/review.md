# Mike user stories: review

The stories for review and merge: self-review, verdicts, send-back, merge, and the review surface. Rules, verdicts and the other files: [the user stories index](README.md).

## Review and merge

#### MS-020 Conflicting pull requests listed
As a human (Tig today), I want ready pull requests in merge conflict listed with their author seat, so that each becomes a send-back.
Evidence: [factory harness attention.py line 136, the merge-conflict finding](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/attention.py#L136).
Acceptance: one row per conflicting ready pull request with `owner/repo#N` and the author seat, linked.
Verdict: CHANGE: shown on the review surface ([MS-128, review surface lists ready pulls](#ms-128-review-surface-lists-ready-pulls)), routed as a send-back ([decision 5, conflicts are changes, not verbs](../mike.md#11-decisions)).

#### MS-021 Reviewer links its pull request
As a human (Tig today), I want a reviewer whose assignment is a pull request to link to that pull request, so that I open the review in one click.
Evidence: [factory harness api.py line 2024, the pull request assignment link](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/api.py#L2024).
Acceptance: the assignment URL ends in `/pull/N` when the item is a pull request.
Verdict: KEEP.

#### MS-022 Point a reviewer at a pull request
As a human (Tig today), I want to point a reviewer at a pull request by typing it as the reviewer's assignment with a steer, so that a review starts now.
Evidence: [factory dashboard verbs.mjs line 109, the reviewer assignment](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/verbs.mjs#L109).
Acceptance: the reviewer row shows `#N` on the next sessions frame; the steer is refused when the reviewer wrote the pull request or has another without a verdict.
Verdict: CHANGE: reviewer independence and one-pull-request-per-reviewer are gates ([gate 9, reviewer independence](../mike.md#33-gates-mike-enforces-for-every-caller), [mike.md §3.6, how reviewers operate](../mike.md#36-how-reviewers-operate)).

#### MS-082 Draft early, ready when clean
As a worker (Artificer), I want to open my pull request as a draft early, labelled `seat:<name>`, and mark it ready only with a self-review done with my runtime's code-review tool and green CI on the same sha, so that other seats see which files I hold.
Evidence: [factory AGENTS.md line 105, the draft-early rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L105).
Acceptance: `pull create` opens a draft by default; `pull ready` is refused unless self-review and CI name the current head.
Verdict: KEEP.

#### MS-083 Self-review in one shape
As a worker (Artificer), I want my self-review counted only in this exact shape, written by me, naming the head sha, so that a review of an old commit or prose about a review never passes the gate.
Evidence: [factory harness pr_state.py line 41, the self-review parser](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L41).
Acceptance: the gate matches `^\s*(\[[^\]\n]+\]\s*)?Self-Review:\s*Done\b`, finds the head sha (7 to 40 hex) in the comment, and the `[Name]` prefix equals the `seat:` owner; anything else does not count.
```
[Name] Self-Review: Done
Head: <sha>
```
Verdict: CHANGE: the old four-line form (`Lexicon: Clear.` and the rest) is refused by the gate, not only banned in briefs; the review behind it is the runtime's code-review tool ([MS-176, self-review with the runtime's code-review tool](#ms-176-self-review-with-the-runtimes-code-review-tool)).

#### MS-084 pr-check names rule breaks
As a worker (Artificer), I want `pr-check` to name mechanical rule breaks (one `seat:` label naming a real seat, no `[Name]` or `Name:` title, `Closes` in the same project, no development pull request from an orchestrator or lane-PE), so that review time is not spent on them.
Evidence: [factory harness __main__.py line 2149, the pr-check verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L2149).
Acceptance: `--strict` exits 1 on any finding; a cross-repository `Closes` is a finding.
Verdict: KEEP.

#### MS-085 One independent reviewer each
As the loop, I want each ready pull request given one reviewer, urgency first then oldest ready, never its author and never a reviewer already holding a pull request without a verdict, so that every ready pull request gets an independent review in parallel.
Evidence: [factory harness review.py line 123, the reviewer assignment](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/review.py#L123).
Acceptance: two ready pull requests and three idle reviewers give exactly two steers; with one reviewer idle, a `critical` pull request is steered before an older `normal` one; mergeable `UNKNOWN` read twice is `unmeasured` naming the pull request.
Verdict: CHANGE: urgency orders review before age; no reviewer waits behind a busy one ([factory#1759, reviewer queued behind a busy one](https://github.com/excaliwire/factory/issues/1759)); Arthur may order it, Mike enforces independence ([mike.md §3.4, review and send-back](../mike.md#34-review-and-send-back), [mike.md §3.6, how reviewers operate](../mike.md#36-how-reviewers-operate)).

#### MS-086 Review pinned to the head
As a reviewer (Warden), I want `review <pr>` to print one results table naming the head and refuse when the head moved or a read failed, so that my review is of this commit only.
Evidence: [factory harness review.py line 96, the review verb](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/review.py#L96).
Acceptance: the table contains `| head | <sha> |`; a review without that table for the head does not clear the gate.
Verdict: KEEP.

#### MS-087 Fails on main, passes on head
As a reviewer (Warden), I want new tests copied onto a `main` worktree and run there and on the head, so that "fails on main, passes on head" is measured for code, config, schema and briefs.
Evidence: [factory brief reviewer.md line 17, the main worktree test rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/reviewer.md#L17).
Acceptance: the table has one main result and one head result per new test; a behavior finding without a failing test is not blocking.
Verdict: KEEP.

#### MS-088 Review in one fixed shape
As a reviewer (Warden), I want my review in one fixed shape of at most 12 lines, so that a human reads it on a phone and the gate parses it.
Evidence: [factory brief reviewer.md line 27, the review shape](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/reviewer.md#L27).
Acceptance: line 1 matches the verdict pattern with a head sha; verdict is `Merge`, `Send back` or `Hold`; one line per blocking finding as `file:line, what is wrong, the fix`; one `Ran:` line; at most 12 lines outside `<details>`; non-blocking findings become issues, not comment text.
```
[Name] Recommendation: Send back on 1a2b3c4.
tools/board.py:42: skips the last row. Fix: iterate to n.
Ran: `review 1741`: new test fails on main, passes on head.
<details><summary>Review results</summary>

(the verb's table)

</details>
Next: <Seat> fixes tools/board.py:42.
```
Verdict: KEEP.

#### MS-089 Comments end with next steps
As a seat (any), I want every comment to end with its next steps, one line each, each naming who does it, so that nobody has to infer the hand-off.
Evidence: [factory brief psde.md line 34, the Next line rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/psde.md#L34).
Acceptance: the last non-blank lines of every seat comment match `^Next: \S+ .+\.$`, and no non-`Next:` line follows them (test on a sample of 50 comments).
```
Next: <Seat> <does X>.
```
Verdict: KEEP.

#### MS-090 Comment length caps
As a human (Tig today), I want seat comments capped at 12 lines for a review, 20 for a pull request body, and 6 for any other comment, so that I read the fleet on a phone.
Evidence: [factory AGENTS.md line 104, the comment limits](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/AGENTS.md#L104).
Acceptance: each loaded brief states the three limits (test); a pull request body has change, `Fixes #N` or `Advances #N`, test-first in one line, verdicts, merge order, follow-ups, and at most 20 lines.
Verdict: KEEP.

#### MS-091 Reviewers cannot push
As a reviewer (Warden), I want to be unable to push a fix or open a development pull request, so that review stays independent.
Evidence: [factory brief reviewer.md line 23, the reviewer no-push rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/briefs/reviewer.md#L23).
Acceptance: 0 commits by a reviewer seat on a development path; a bug a reviewer finds becomes 1 issue with an `urgency:` label and a steer to a worker.
Verdict: CHANGE: a push by a reviewer seat token is refused by mechanism, not only by the brief ([gate 9, reviewer independence](../mike.md#33-gates-mike-enforces-for-every-caller), [mike.md §3.6, how reviewers operate](../mike.md#36-how-reviewers-operate)).

#### MS-092 Gates pinned to head sha
As a human (Tig today), I want every gate pinned to the head sha, so that a new commit voids self-review, CI and review.
Evidence: [factory harness merge_gate.py line 1, the merge gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/merge_gate.py#L1).
Acceptance: pushing one commit after a `Merge` review moves the pull request's next step back to self-review within one tick.
Verdict: KEEP.

#### MS-093 Send-back returns to author
As a worker (Artificer), I want a send-back from any independent reviewer (a seat, an attached session or a human) to return my pull request to draft and come back to me as my next assignment, so that the fix lands on the seat that has the context and nobody else waits.
Evidence: [factory harness draft_sent_back.py line 1, draft on send-back](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/draft_sent_back.py#L1).
Acceptance: after `Send back` on the head from a reviewer seat, an attached session or a listed human, the pull request is draft within one tick and the author seat's next assignment is that pull request; a send-back naming an older sha does nothing.
Verdict: CHANGE: send-back is a first-class state on the board, and no seat waits on it ([mike.md §3.4, review and send-back](../mike.md#34-review-and-send-back)).

#### MS-094 Conflicts and Copilot threads sent back
As a worker (Artificer), I want a ready pull request that turns conflicting, or gets unresolved Copilot threads on its head, sent back to me once, so that I fix it without a human polling.
Evidence: [factory harness conflict_steer.py line 243, the conflict steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/conflict_steer.py#L243).
Acceptance: one send-back per pull request per head per cause; the prompt names the cause and says "Merge origin/main. Never rebase on a shared branch."
Verdict: CHANGE: kept as wakes until the planner is gone, then routed as send-backs ([decision 5, conflicts are changes, not verbs](../mike.md#11-decisions)).

#### MS-095 Request merge when gates pass
As a human (Tig today), I want Mike to request merge from the configured merger exactly when self-review, CI, ready and an independent `Merge` review (seat, attached session or human) all name the same head, so that my assignment list is my merge queue.
Evidence: [factory harness assign_tig.py line 1, assign-tig](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/assign_tig.py#L1).
Acceptance: a draft never gets a request; a pull request already assigned to the merger is not re-requested; the merger login comes from config.
Verdict: CHANGE: request merge, not assign-tig.

#### MS-096 No merge verb
As a human (Tig today), I want Mike to have no merge verb, so that only a human merges.
Evidence: [factory harness merge_gate.py line 5, the no-merge rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/merge_gate.py#L5).
Acceptance: a test fails if any verb, route or GitHub call that merges is added.
Verdict: KEEP.

#### MS-097 Waive and grant by comment
As a human (Tig today), I want to waive a gate with a comment and grant a reviewer with a comment, honored only from my account, so that I unblock without editing code.
Evidence: [factory harness pr_state.py line 89, the waive and reviewer comments](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L89).
Acceptance: a waiver or grant from any seat is ignored and recorded; an unpinned waiver expires on the next commit; each honored waiver is a record.
```
waive: <self_review|ci|ready|ir|all> [sha]
reviewer: <Name>
```
Verdict: CHANGE: honored from the configured merger account, not a hard-coded `tig`.

## Review surface

#### MS-128 Review surface lists ready pulls
As a human (Tig today), I want a review surface listing every ready pull request, the reviewer assigned to each, and each verdict on the current head, so that I see review state without opening GitHub.
Evidence: [factory dashboard rules.mjs line 57, the router has no review route](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L57); [mike.md §7, the dashboard](../mike.md#7-the-dashboard); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: the rows equal the open non-draft pull requests across all projects; each shows reviewer or `none`, and `Merge`, `Send back`, `Hold` or `pending` for the head sha.
Verdict: NEW.

#### MS-129 Review surface by urgency then age
As a human (Tig today), I want the review surface ordered by urgency, then by the time each pull request went ready, oldest first, with send-backs and their author seats listed apart, so that the most urgent, oldest wait is on top.
Evidence: [factory harness review.py line 123, the reviewer assignment](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/review.py#L123); [mike.md §3.4, review and send-back](../mike.md#34-review-and-send-back); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: row order is `critical`, `high`, `normal`, `no`, then ascending ready time from GitHub events inside each; each send-back row names the author seat and its next-assignment state.
Verdict: NEW.

#### MS-130 Reviewer pool sized to workers
As the loop, I want the reviewer pool sized at `ceil(workers / 3)`, with one reviewer per ready pull request inside it, so that review keeps pace with work.
Evidence: [factory#1336 section 1 point 5, the harness redesign](https://github.com/excaliwire/factory/issues/1336); [decision 3, the reviewer pool cap](../mike.md#11-decisions), [mike.md §3.6, how reviewers operate](../mike.md#36-how-reviewers-operate).
Acceptance: with 9 workers the pool cap is 3; with 2 ready pull requests and 3 idle reviewers, 2 are steered.
Verdict: NEW.

#### MS-176 Self-review with the runtime's code-review tool
As a worker (Artificer), I want my self-review done with my runtime's code-review tool on the head, so that the self-review is a review, not a stamp, before an independent reviewer spends time.
Evidence: [factory harness pr_state.py line 41, the self-review parser checks shape only](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/pr_state.py#L41); [mike.md §3.4, review and send-back](../mike.md#34-review-and-send-back), [mike.md §6 step 2, owner self-review](../mike.md#6-the-pull-request-lifecycle).
Acceptance: every runtime's config names its code-review tool (test); the worker brief says to run it on the head before posting the self-review block ([MS-083, self-review in one shape](#ms-083-self-review-in-one-shape)); a pull request with no self-review on the head is not marked ready.
Verdict: NEW.
