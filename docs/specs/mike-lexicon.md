# Mike lexicon carry-over

**Status:** plan. Written before the code, as the companion to [mike.md §8, the lexicon](mike.md#8-lexicon).

**What this is.** Every factory harness term, each with a verdict for Mike: KEEP, RENAME, NARROW, RETIRE, or CHALLENGE. A human edits this file; a CHALLENGE row stays open until he does. The lexicon is config, so once Mike has code a change to this file is test-first: a test fails on the old text and passes on the new. **Binds** test names in [section 3, Mike entries](#3-mike-entries) are the tests to write; none exists yet.

**Source pin:** excaliwire/factory [factory commit bb2bf4c6](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8) (2026-10-05). Every source link names its file and line at this commit; "agent-harness spec" is `docs/specs/agent-harness.md`. Input: the lexicon audit (194 rows, 309 terms). Where the audit and [mike.md §8, the lexicon](mike.md#8-lexicon) or [mike.md §11, decisions](mike.md#11-decisions) disagree, mike.md wins, and [section 2.1, audit disagreements](#21-where-the-audit-and-mikemd-disagree-mikemd-followed) lists each one.

## 1. Rules Mike keeps for its lexicon

1. **An entry is a heading.** One heading per term, 2 to 5 sentences, an owner link first; headings are anchors other files link to, so a rename keeps the old word on an `Also:` line.
2. **No second copy of a rule.** An entry links to the gate, threshold, or CLI; it does not restate it. Factory's Steer, Assignment, Config store and Harness-gh-user entries break this today.
3. **Aliases** go on one `Also:` line, extracted to the machine lexicon, never as separate headings.
4. **Banned terms are one list.** One table, one phrase per cell, a scope only from the registered qualifiers; `mint`, `steer` and `poke` attach the packet and never embed the list.
5. **Machine copy equals prose.** The Geas instance equals the extract of this file; a test fails when they differ.
6. **Geas lint.** Every outbound prompt and every write is linted against banned terms as whole strings; backticks and fenced blocks are mentions; a run that read nothing refuses.
7. **The lexicon is config.** A term change is test-first, like code, schema and briefs.
8. **A new term needs a human.** The candidate is argued, a human picks, and the term lands with its schema in one change.
9. **No pick history in an entry.** No "who named it" or dates; factory's test misses 5 such entries today.
10. **Use the words.** A clearer synonym is still the wrong word; a code appears once, in parentheses, as a bridge.
11. **Names are config.** Seat and role display names live in instance config; code classifies by role key, never by a display name.
12. **The review checks lexicon drift.** Drift across code, tests, docs, UI text, titles and commits is a blocking finding, not a fixed `Lexicon: Clear` line.
13. **US English, English names.** An OEM number or code is provenance, not a name. A project's domain words come from its hook, not from Mike.

## 2. Carry-over table

205 rows: the audit's 186 single-term rows, plus 6 terms [mike.md §8, the lexicon](mike.md#8-lexicon) decides that the audit has no row for (harness seat field, retarget loop, meter, Lexicon: Clear, lane owner, runtime kind names), plus 13 terms new in Mike (urgency, access method, driver, Mike Runtime API, self code review, independent code review, session log, dashboard API, part, frame, job, command, session token). Gate numbers are [mike.md §3.3, the gates](mike.md#33-gates-mike-enforces-for-every-caller). Ordered by verdict, then alphabetically.

| Verdict | Rows |
|---|---|
| KEEP | 107 |
| RENAME | 21 |
| NARROW | 33 |
| RETIRE | 46 |
| CHALLENGE | 0 |

| Term | Factory meaning (one line) | Source | Mike verdict | Mike term or why |
|---|---|---|---|---|
| Access method | None; new in Mike | [mike.md §4, runtimes](mike.md#4-runtimes) | KEEP | New in Mike: `cloud` (vendor APIs) or `tmux` (send-keys and screen reading), both under the Mike Runtime API |
| Actuation | Unit a seat host pulls: paste, restart, kill, liveness, meter | [agent-harness spec line 300, Actuation](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L300) | KEEP | Add a heading; `meter` kind reads a gauge source |
| Address | `seat:<name>` owns, `[Name] ` writes, `Name:` addresses | [agent-harness spec line 357, Address](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L357) | KEEP | `To: Name` addresses a seat (the email header word; several as `To: Name, Other`); `[Name]` at the start of a comment is the writer's prefix; factory's `Name:` form and the briefly proposed `[Name]:` both retire ([mike.md §9 rule 15, the address contract](mike.md#9-what-mike-keeps), [§2.1, humans](mike.md#21-humans)) |
| app principal | Banned; write agent principal | [lexicon.md line 1144, app principal](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1144) | KEEP | Ban stays |
| Applied / undelivered | Delivery outcomes; applied does not mean the seat acted | [agent-harness spec line 86, Applied / undelivered](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L86) | KEEP | An unconfirmed steer is not a steer |
| Archive | End a seat's Cursor session so it reads `not-minted` | [lexicon.md line 245, Archive](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L245) | KEEP | Runtime-neutral; writes a decision record |
| Artifact | Throwaway reproduction on a reserved-prefix branch; reaped past max age | [agent-harness spec line 127, Artifact](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L127) | KEEP | Same |
| Artificer | Factory's display name for a worker | [lexicon.md line 195, Artificer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L195) | KEEP | Default display name in instance config, not a core word |
| Caller matrix | Who may call which verb; arbiter steers; lane-PE steers its own lane | [agent-harness spec line 102, Caller matrix](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L102) | KEEP | Keeps lane-PE own-lane steer ([mike.md §9 rule 12, the caller matrix](mike.md#9-what-mike-keeps)); knows director and human |
| Check-in | A seat or host tells the control plane it is alive | [lexicon.md line 329, Check-in](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L329) | KEEP | Same |
| Command | None; new in Mike | [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands) | KEEP | New in Mike: a POST to the dashboard API; answers 202 with a job id at once |
| Config store | Often-changed settings outside git; one writer; versioned | [lexicon.md line 343, Config store](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L343) | KEEP | Schema, append-only, human-only, logged |
| Control plane | Holds desired state, reads live state, acts on the difference; refuses what policy forbids | [lexicon.md line 61, Control plane](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L61) | KEEP | Code, not a seat; the arbiter is separate |
| Current main | Seats remint and steer on current main | [agent-harness spec line 186, Current main](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L186) | KEEP | Same |
| Dashboard | A view, never the source of truth for policy | [agent-harness spec line 238, Dashboard](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L238) | KEEP | One client of [Mike's dashboard API](mike-dashboard-api.md), a full rewrite; factory's page and API were the starting point ([mike.md §7, the dashboard](mike.md#7-the-dashboard)) |
| Dashboard API | None; new in Mike (factory's dashboard API was the starting point) | [Mike's dashboard API](mike-dashboard-api.md) | KEEP | New in Mike: Mike's own versioned contract between the control plane and every client |
| Data plane | The seats doing the work; must not reach around the control plane | [lexicon.md line 139, Data plane](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L139) | KEEP | Same |
| Decision record | Seen, decided, why, written before the side effect; refusals recorded | [lexicon.md line 155, Decision record](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L155) | KEEP | [Gate 6, record before act](mike.md#33-gates-mike-enforces-for-every-caller); TPM clause follows [Q3, two orchestrator seats](#q3-two-orchestrator-seats-or-tpm-merged-into-arthur) |
| dispatch | Banned; write steer or poke | [lexicon.md line 1122, dispatch](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1122) | KEEP | Ban stays |
| Draft-sent-back | Convert a ready pull request to draft on `send_back` | [agent-harness spec line 406, Draft-sent-back](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L406) | KEEP | Same |
| Driver | None; new in Mike | [mike.md §4, runtimes](mike.md#4-runtimes) | KEEP | New in Mike: one runtime's implementation of the Mike Runtime API, enabled or installed by config |
| Dry run | Plans and records; does not act | [lexicon.md line 355, Dry run](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L355) | KEEP | Same |
| farm | Banned; write steer | [lexicon.md line 1121, farm](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1121) | KEEP | Ban stays |
| Fill-missing | Fleet mode: claim a live same-name session, else mint | [lexicon.md line 275, Fill-missing](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L275) | KEEP | Adopt, else mint; scope follows [Q1, standing names or a pool](#q1-standing-names-or-pool-slots) |
| Finding | The permanent result; goes on the issue | [agent-harness spec line 125, Finding](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L125) | KEEP | Non-blocking review findings become issues |
| Fleet mode | The reboot commands: hard, orchestrator, worker, fill-missing | [agent-harness spec line 102, Fleet mode](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L102) | KEEP | Adds `restart-control-plane` and `reset-defaults`; one at a time, a collision is 409; each a [job](#job) ([Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands)) |
| Fleet read | Vendor listing against the roster: untracked, missing, duplicates | [agent-harness spec line 190, Fleet read](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L190) | KEEP | Same |
| Frame | None; new in Mike | [Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream) | KEEP | New in Mike: one server-sent event carrying one part, with `version`, `part`, `written_at` |
| Gauge | Measured reading of one budget; no probe is unmeasured | [agent-harness spec line 148, Gauge](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L148) | KEEP | Mint-threshold input and dashboard usage, declared per runtime ([mike.md §4, runtimes](mike.md#4-runtimes)); gauge list is config |
| Geas | Binding on words; schema `excaliwire.geas/v1`; instance `geas.yaml` | [lexicon.md line 465, Geas](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L465) | KEEP | Mike's machine lexicon; lints every outbound prompt |
| Hard reboot | Archive every standing seat, mint again, restart the control plane | [lexicon.md line 281, Hard reboot](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L281) | KEEP | First steer is the carried assignment |
| Health | Loop ticking, seats live, gauges unmeasured; one log `harness.jsonl` | [agent-harness spec line 169, Health](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L169) | KEEP | Log is `mike.jsonl`; shows target versus actual share; served as the `health` [part](#part) ([Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes)) |
| Heartbeat | Loop stamp each tick, before any refusal, only from the loop | [agent-harness spec line 155, Heartbeat](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L155) | KEEP | Same |
| Independent code review | None; new in Mike (factory: Independent review) | [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back) | KEEP | New in Mike: a review by a seat, an attached session, or a human other than the assigned seat; at least one per pull request |
| Independent review | Line 1 `[Name] Recommendation: Merge on <sha>.` | [agent-harness spec line 406, Independent review](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L406) | KEEP | 12-line review ([mike.md §6, the pull request lifecycle](mike.md#6-the-pull-request-lifecycle)); from a seat, an attached session, or a human; see independent code review |
| Initial steer | Code-rendered first steer after a mint | [agent-harness spec line 192, Initial steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L192) | KEEP | Same |
| Job | None; new in Mike | [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands) | KEEP | New in Mike: one command's outcome, `pending` then `applied`, `refused` or `cancelled`, with why and actor |
| Lane-PE | Expensive judgment seat for one lane; no merge, no mint | [lexicon.md line 173, Lane-PE](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L173) | KEEP | Decided 2026-10-05: role stays, wait-only, human or loop mint behind a confirmed setting ([decision 12, the lane-PE role](mike.md#11-decisions)) |
| Last mint | A time, `not-minted`, or `unmeasured`; never a liveness word | [agent-harness spec line 108, Last mint](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L108) | KEEP | Same |
| Live state | Who is on what now, session ids, meter readings, live tier; not in git | [lexicon.md line 149, Live state](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L149) | KEEP | The store; readings are gauges |
| Liveness | `not-minted`, `responding`, `not-responding`, `unmeasured`; not assignment | [lexicon.md line 257, Liveness](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L257) | KEEP | No fifth word; busy and idle are activity |
| Loop cadence | Minutes between acting ticks, 1 to 60 | [lexicon.md line 361, Loop cadence](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L361) | KEEP | Config store |
| Loop mode | `live` or `dry-run`; an unreadable store reads `dry-run` | [lexicon.md line 349, Loop mode](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L349) | KEEP | Same |
| loop off | Banned; write Paused | [lexicon.md line 1147, loop off](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1147) | KEEP | Ban stays |
| Loop window | How old the loop's own record may be: `stale_after_minutes` plus cadence | [settings.py line 1049, Loop window](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L1049) | KEEP | Add a heading; [gate 5, one pending steer](mike.md#33-gates-mike-enforces-for-every-caller) |
| Main-restart | When main moves, remint the seats whose code changed | [agent-harness spec line 186, Main-restart](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L186) | KEEP | Same |
| Master plan | Issue with sub-issues; done when all are done | [agent-harness spec line 385, Master plan](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L385) | KEEP | Its hold reason retires |
| Merge-gate | Names the merge step and what is missing, per head; no merge action | [agent-harness spec line 447, Merge-gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L447) | KEEP | Same |
| Mike Runtime API | None; new in Mike (factory's session API was Cursor-shaped) | [mike.md §4, runtimes](mike.md#4-runtimes) | KEEP | New in Mike: the vendor-neutral driver layer; every runtime fills it or reports `unmeasured` |
| Mint | Create a seat; the only verb that brings a seat into being | [lexicon.md line 219, Mint](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L219) | KEEP | Cause a session to be created for a seat; wait-only, every role; no token or turn budget |
| mountain seat | Banned; write worker | [lexicon.md line 1119, mountain seat](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1119) | KEEP | Ban stays |
| mountain worker | Banned; write worker | [lexicon.md line 1118, mountain worker](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1118) | KEEP | Ban stays |
| Names must say the job | A name a human can say aloud and know the job; no codes | [lexicon.md line 9, Names must say the job](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L9) | KEEP | [section 1 rules 10 and 13, names](#1-rules-mike-keeps-for-its-lexicon) |
| Needs IR (`needs_ir`) | Ready and waiting for independent review | [agent-harness README, Needs IR](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md) | KEEP | Same |
| Orchestrator cooldown | Minimum minutes before the same board steers an orchestrator again | [agent-harness spec line 161, Orchestrator cooldown](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L161) | KEEP | Trigger follows [decision 1, change-driven steering](mike.md#11-decisions) |
| Orchestrator reboot | Archive TPM and arbiter, reset their assignments, restart, mint both | [lexicon.md line 293, Orchestrator reboot](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L293) | KEEP | TPM half follows [Q3, two orchestrator seats](#q3-two-orchestrator-seats-or-tpm-merged-into-arthur) |
| Orchestrator seat | Arbiter or TPM; must not be one chat | [lexicon.md line 459, Orchestrator seat](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L459) | KEEP | Decided 2026-10-05: two seats stay; K measured for a week ([decision 13, Arthur and K stay two](mike.md#11-decisions)) |
| Owner self-review | `Self-Review: Done` naming `Head: <sha>` | [agent-harness spec line 402, Owner self-review](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L402) | KEEP | Merge step 2, done with the seat's runtime code-review tool ([mike.md §6, the pull request lifecycle](mike.md#6-the-pull-request-lifecycle)); see self code review |
| Part | None; new in Mike | [Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream) | KEEP | New in Mike: one named slice of state (`seats`, `board`, `jobs`, ...), sent as a frame and served as a read |
| Paste | tmux steer delivery; delivered when the pane shows it | [agent-harness spec line 96, Paste](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L96) | KEEP | Pane echo is delivery confirmation |
| Paste hold | Pastes and restarts to a pane are held while a human controls it | [agent-harness spec line 230, Paste hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L230) | KEEP | A human pane lock, not a planner hold |
| Paused | No tick acts; carries a reason; an unreadable store reads Paused | [lexicon.md line 89, Paused](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L89) | KEEP | Human switch, [gate 8, the human switches](mike.md#33-gates-mike-enforces-for-every-caller) |
| PE seat | Banned; write lane-PE | [lexicon.md line 1120, PE seat](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1120) | KEEP | Ban stays; moot if [Q2, the lane-PE role](#q2-does-the-lane-pe-role-exist-in-mike) drops lane-PE |
| pr-check | Mechanical pull request rules: one seat label, no owner prefix | [agent-harness spec line 449, pr-check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L449) | KEEP | Same |
| Program | The repositories in `seats.yaml` `program` | [agent-harness spec line 76, Program](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L76) | KEEP | The instance's set of projects, `program.repositories` ([mike.md §1.2, multi-repository](mike.md#12-multi-repository-one-instance)); [gate 2, the project gate](mike.md#33-gates-mike-enforces-for-every-caller) |
| Ready | Out of draft only with clean self-review and green CI on one head | [agent-harness spec line 405, Ready](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L405) | KEEP | Same |
| Refusal | A recorded no with its reason (no heading) | [agent-harness spec line 80, Refusal](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L80) | KEEP | Add a heading; the one outcome word |
| Remint | Applied create or restart for one seat; carries the assignment | [agent-harness spec line 84, Remint](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L84) | KEEP | A mint of a seat that already had a session; carries the assignment; add a heading |
| Report-focus | A seat tells the control plane what it is working on | [lexicon.md line 321, Report-focus](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L321) | KEEP | Drift check: focus versus assignment |
| Reset defaults | Reboot option: assignments idle, auto-steer on, seat labels removed, a record per seat | [lexicon.md line 287, Reset defaults](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L287) | KEEP | One recorded write clears every assignment and label ([mike.md §3.2, mint, remint, steer](mike.md#32-mint-remint-steer)) |
| Restart control plane | Bounce the control-plane process only | [lexicon.md line 305, Restart control plane](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L305) | KEEP | Resumes from the store |
| Retired name | A name in `seats.yaml` `retired`; never minted again | [agent-harness spec line 45, Retired name](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L45) | KEEP | Same |
| Reviewer | Seat that independently reviews a ready pull request it did not write | [lexicon.md line 201, Reviewer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L201) | KEEP | Role key `reviewer`; Warden is factory's name for it, not a Mike default ([decision 9, role keys are names](mike.md#11-decisions)); how it operates is [mike.md §3.6, how reviewers operate](mike.md#36-how-reviewers-operate) |
| Reviewer grant | `reviewer: <Name>` from `tig` | [agent-harness spec line 422, Reviewer grant](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L422) | KEEP | From a human merger account (config) |
| Row verbs | A Sessions row lists the verbs that fit liveness; others refused | [agent-harness spec line 102, Row verbs](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L102) | KEEP | The page's only verb source; the server also sends `verb_why` per verb ([Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes)) |
| Running | Loop state in which each tick acts; the one config-store switch | [lexicon.md line 83, Running](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L83) | KEEP | Same |
| Runtime kind names | `cursor-cloud`, `grok-tmux`, `claude-tmux`, `codex-tmux`, `claude-cloud` | [seats.yaml line 147, Runtime kind names](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/seats.yaml#L147) | KEEP | Each is a runtime, a driver under the Mike Runtime API ([mike.md §4, runtimes](mike.md#4-runtimes)) |
| Seat actuator | One interface for mint, stop, steer, archive, restart, claim; Cursor only | [lexicon.md line 269, Seat actuator](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L269) | KEEP | The Mike Runtime API: one interface, one record shape, every runtime |
| Seat card | none; factory draws a seat as a table row | [mike.md §7.1, the Seats tab and the seat card](mike.md#71-the-seats-tab-and-the-seat-card) | KEEP | new in Mike: the one component that draws a seat ([entry](#seat-card)) |
| Seat host | Agent on a machine that hosts seats; pulls actuations, pushes check-in | [lexicon.md line 95, Seat host](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L95) | KEEP | Pulls with a host token; no inbound path |
| Seat type | Seats of one role sharing vendor, runtime and model; no per-seat override | [lexicon.md line 453, Seat type](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L453) | KEEP | Remint on change |
| Self code review | None; new in Mike (factory: Owner self-review) | [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back) | KEEP | New in Mike: the assigned seat's review with its runtime code-review tool, posted as the self-review block |
| Session log | None; new in Mike | [mike.md §4, runtimes](mike.md#4-runtimes) | KEEP | New in Mike: a runtime capability; inputs and responses, from which the last steer and the latest response are read |
| Session token | None; new in Mike | [Mike dashboard API §2, identity](mike-dashboard-api.md#2-identity) | KEEP | New in Mike: the bearer a human issues to an attached session; revocable; shown once |
| Stale | Older than the window, by arithmetic | [agent-harness spec line 302, Stale](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L302) | KEEP | Same |
| stall | Banned; write Paused | [lexicon.md line 1145, stall](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1145) | KEEP | Ban stays |
| stalled | Banned; write Paused | [lexicon.md line 1146, stalled](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1146) | KEEP | Ban stays |
| Sync-tip | Control plane fast-forwards and restarts on tip | [agent-harness spec line 117, Sync-tip](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L117) | KEEP | Same |
| Temporary seat | Seat a human mints for one conversation; not counted against the cap | [agent-harness spec line 51, Temporary seat](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L51) | KEEP | Proof is its mint record, not the retired board ([mike.md §8, the lexicon](mike.md#8-lexicon)) |
| Terminal ticket | Single-use ticket bound to an email and a session | [agent-harness spec line 220, Terminal ticket](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L220) | KEEP | Not in Mike's API 1.0.0; the seat host's terminal contract carries it later ([Mike dashboard API §8, what changed and the terminal deferral](mike-dashboard-api.md#8-what-changed-from-the-starting-point)) |
| Test-first | The test fails on the old code and passes on the new | [agent-harness spec line 403, Test-first](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L403) | KEEP | Reviewer verb runs it both sides |
| Tick | One control-loop pass, `run_tick`, 10 verbs today (no heading) | [agent-harness spec line 155, Tick](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L155) | KEEP | Add a heading; also names the loop (see retarget loop) |
| Tier | How capable and expensive a seat's model is | [lexicon.md line 167, Tier](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L167) | KEEP | Property of a seat type's model; the ladder use retires ([mike.md §8, the lexicon](mike.md#8-lexicon)) |
| Title ownership | Which roles own which titles and development paths | [agent-harness spec line 66, Title ownership](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L66) | KEEP | Same |
| TPM (Kay) | Roster and briefs; direction into issues; classification judgment | [agent-harness spec line 39, TPM](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L39) | KEEP | Decided 2026-10-05: stays as K; measured for a week ([decision 13, Arthur and K stay two](mike.md#11-decisions)) |
| Tree gate | A tick reaches no live seat unless the tree is confirmed | [agent-harness spec line 167, Tree gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L167) | KEEP | Same |
| Unmeasured | A reading not taken; an answer; the path refuses to act (no heading) | [agent-harness spec line 74, Unmeasured](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L74) | KEEP | Add a heading; never 0, never ok |
| Urgency | None; new in Mike (factory: severity) | [mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share) | KEEP | New in Mike: `critical`, `high`, `normal`, `no` as labels `urgency:<level>`; no label is `urgency:no` |
| vendor-hook framework | Banned; write Geas | [lexicon.md line 1143, vendor-hook framework](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1143) | KEEP | Ban stays |
| Wait-only mint | Mint with `MINT_WAIT`; the first steer is the assignment | [agent-harness spec line 192, Wait-only mint](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L192) | KEEP | Every role, lane-PE included ([factory#1755, the lane-PE mint cost](https://github.com/excaliwire/factory/issues/1755)) |
| Waiver | `waive: <gate>` from the `tig` account, pinned to a sha | [agent-harness spec line 416, Waiver](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L416) | KEEP | From a human merger account (config) |
| Warden | Factory's display name for a reviewer | [lexicon.md line 207, Warden](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L207) | KEEP | Default display name in instance config |
| Web terminal | Watch and take control of a tmux pane; human only | [agent-harness spec line 210, Web terminal](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L210) | KEEP | Deferred from Mike's API 1.0.0; served by the seat host over a two-way channel, added as a minor bump ([Mike dashboard API §8, what changed and the terminal deferral](mike-dashboard-api.md#8-what-changed-from-the-starting-point)) |
| Work type | Feature, Bug, Task; not priority | [agent-harness spec line 383, Work type](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L383) | KEEP | Same |
| Worker | Builds one assigned issue to a ready pull request, then waits | [lexicon.md line 187, Worker](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L187) | KEEP | Role key `worker`; its send-backs return to it |
| Worker reboot | Archive and mint workers and reviewers; no control-plane restart | [lexicon.md line 299, Worker reboot](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L299) | KEEP | Same |
| Agent harness | Code-owned control plane for agent sessions; `agent-harness/` | [lexicon.md line 45, Agent harness](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L45) | RENAME | **Mike**; harness carried 2 meanings |
| Assign Tig | Merge step: assign `tig`; `pull assign-tig` | [agent-harness spec line 407, Assign Tig](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L407) | RENAME | **request merge**; the merger is config |
| Claim | Attach a live same-name vendor session to its seat; not a mint | [lexicon.md line 251, Claim](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L251) | RENAME | **adopt**; claim stays for a host claiming an actuation |
| Direction | A human's lane rows `{lane, note}` in the store; on enabled, off starved | [lexicon.md line 379, Direction](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L379) | RENAME | **priorities list**; one ranked row per lane, each with a share; the API command is `priorities`, not `direction` ([Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands)) |
| Droplet | The host that runs the control plane (used 20+ times, no heading) | [agent-harness spec line 86, Droplet](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L86) | RENAME | **control-plane host**; Mike runs on any host |
| Excaliwire PgM (director) | A human's portal session; not a seat; caller kind `operator` | [agent-harness spec line 47, Excaliwire PgM](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L47) | RENAME | **director**; PgM is the instance's display name |
| harness (seat field) | A seat's run kind, `harness: grok-tmux` | [lexicon.md line 131, harness](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L131) | RENAME | **runtime** ([mike.md §8, the lexicon](mike.md#8-lexicon), [decision 7, harness renamed runtime](mike.md#11-decisions)) |
| Harness account | One account per harness, named by secret file | [agent-harness spec line 347, Harness account](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L347) | RENAME | **vendor account**; the vendor bills ([mike.md §4, runtimes](mike.md#4-runtimes)); new word, [Q12, the new words](#q12-accept-the-new-words-this-file-proposes-beyond-mikemd-section-8) |
| Harness-gh-user | GitHub user whose assigned issues and pull requests may be steered | [lexicon.md line 373, Harness-gh-user](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L373) | RENAME | **gh_user**; same [gate 1, the owner gate](mike.md#33-gates-mike-enforces-for-every-caller) |
| High | `sev2`; hours; steer class `elevate` | [lexicon.md line 429, High](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L429) | RENAME | **`urgency:high`**; sort order only |
| Live map | `main_restart` reading: active, idle, unmeasured; not liveness | [agent-harness spec line 191, Live map](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L191) | RENAME | **activity** (busy, idle, unmeasured); new word, [Q12, the new words](#q12-accept-the-new-words-this-file-proposes-beyond-mikemd-section-8) |
| Low | Default; not planned; never steered onto a worker or Warden | [lexicon.md line 441, Low](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L441) | RENAME | **`urgency:no`**: no label is `urgency:no`; nothing runs on it; worker steer refused ([gate 4, the urgency floor](mike.md#33-gates-mike-enforces-for-every-caller)) |
| Medium | Ordinary work; `sev3`; steer class `feed` | [lexicon.md line 435, Medium](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L435) | RENAME | **`urgency:normal`**; drop `feed` |
| Meter | A scraped reading of one vendor budget; `write-meters` | [meters.py line 16, Meter](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/meters.py#L16) | RENAME | **gauge source**; the gauge is the reading |
| Retarget loop | `retarget-loop.sh` and `run_tick`, the loop's name | [retarget-loop.sh line 2, Retarget loop](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/retarget-loop.sh#L2) | RENAME | **tick**; `retarget-pe` retires with the host ladder |
| Sessions tab | Who is on what now, and the last poke | [agent-harness spec line 246, Sessions tab](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L246) | RENAME | **Seats tab**: every seat as one [seat card](#seat-card) ([mike.md §7.1, the Seats tab and the seat card](mike.md#71-the-seats-tab-and-the-seat-card)) |
| Severity | Urgent, High, Medium, Low, plus steer class and SLA | [lexicon.md line 413, Severity](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L413) | RENAME | **urgency**: `urgency:<level>` labels order work inside a lane; no steer class ([mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share)) |
| Severity floor | `severity floor: Low is never steered` (no heading) | [lexicon.md line 441, Severity floor](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L441) | RENAME | **urgency floor**; add a heading; [gate 4, the urgency floor](mike.md#33-gates-mike-enforces-for-every-caller) |
| Steer-idle | Tick verb: planner for idle workers plus orchestrator follow-up | [agent-harness spec line 159, Steer-idle](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RENAME | **follow-up**; the planner is not re-created |
| Tig | A human: merges, owns spend, only waiver source | [lexicon.md line 31, Tig](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L31) | RENAME | **humans** (plural): instance config lists them by login; Mike text says a human or humans; Tig is factory's config ([Q6, the word for a human](#q6-which-word-names-a-human), [mike.md §2.1, humans](mike.md#21-humans)) |
| Urgent | Blocking; `sev1`; steer class `interrupt` | [lexicon.md line 423, Urgent](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L423) | RENAME | **`urgency:critical`**: sorts first, never preempts; the `interrupt` steer class retires ([decision 14, `urgency:critical` never preempts](mike.md#11-decisions)) |
| `seat:<name>` label | That seat owns the work; routes a poke | [agent-harness spec line 365, `seat:<name>` label](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L365) | NARROW | Marks the seat's one assignment |
| Agent principal | Entra ID identity per machine trust boundary | [lexicon.md line 107, Agent principal](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L107) | NARROW | Identity per trust boundary: seat token, host token; Entra is an implementation |
| App role | Entra role checked per route: 4 roles | [lexicon.md line 115, App role](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L115) | NARROW | Keep the 4 roles; drop Entra |
| Arbiter | Seat that owns the control plane, orders work, owns assignment | [lexicon.md line 213, Arbiter](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L213) | NARROW | Judgment from the board; acts only through verbs |
| Arthur | Display name of the control-plane seat; spec title "harness aka Arthur" | [agent-harness spec line 1, Arthur](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L1) | NARROW | Default display name of the arbiter only |
| Assignment | The work a seat is on; actuator stores it; label marks it | [lexicon.md line 263, Assignment](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L263) | NARROW | Exactly one; the label is the truth, the store caches |
| At prompt | tmux pane reading: empty prompt is idle, spinner is busy | [agent-harness spec line 82, At prompt](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L82) | NARROW | The tmux source of activity |
| Board | Follow-up input: open issues, priorities list, unassigned-urgent | [agent-harness spec line 161, Board](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L161) | NARROW | Arthur's whole input, each idle seat's last completed assignment included ([mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share)); pages say page or tab |
| Board lane rule | Policy text: priorities list is ordered lanes, on or off | [agent-harness spec line 192, Board lane rule](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L192) | NARROW | Moves into the arbiter brief and the priorities list entry; one row per lane |
| Control loop | Both one pass and the process that is Running or Paused | [lexicon.md line 75, Control loop](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L75) | NARROW | The process, one per instance; one pass is a tick |
| Desired state | `seats.yaml`: names, harness, owner, tier, cap, `pe_retarget` | [lexicon.md line 145, Desired state](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L145) | NARROW | Instance config; drop owner and `pe_retarget` |
| Lane | Domain named by a repo label; `policy.lanes` maps it to an owning lane-PE | [lexicon.md line 181, Lane](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L181) | NARROW | A large architectural body of work in the program; one lane label per issue, one priorities row per lane; no owner ([mike.md §3, the seat model](mike.md#3-the-seat-model)) |
| no-work-above-low | Hold: only Low work is open | [idle_steer.py line 47, the no-work-above-low hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L47) | NARROW | Refusal text of [gate 4, the urgency floor](mike.md#33-gates-mike-enforces-for-every-caller) only |
| not assigned to harness-gh-user | none-eligible reason ([factory#1598, steer only gh-user work](https://github.com/excaliwire/factory/issues/1598)) | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | NARROW | Refusal text of [gate 1, the owner gate](mike.md#33-gates-mike-enforces-for-every-caller): `not assigned to gh_user` |
| Packet | Control plane assembles it from notifications for TPM | [agent-harness spec line 61, Packet](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L61) | NARROW | Folded into the board |
| Poke | Wake a seat, no instruction; about work this seat owns | [lexicon.md line 311, Poke](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L311) | NARROW | About its assignment or its pull request |
| Prioritization | Putting a few items at the top | [lexicon.md line 389, Prioritization](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L389) | NARROW | The act only; the list is the priorities list |
| priority list unreadable | none-eligible reason and steer refusal ([factory#1407, remove the lane gate](https://github.com/excaliwire/factory/issues/1407)) | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | NARROW | [Gate 3, the lane gate](mike.md#33-gates-mike-enforces-for-every-caller) refusal; the reading is unmeasured |
| Program priorities | The page `/dashboard/priorities` | [agent-harness spec line 247, Program priorities](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L247) | NARROW | Priorities tab: edits the list, shows target versus actual share |
| repository-not-allowed | none-eligible reason ([factory#897, idle feed finds no work](https://github.com/excaliwire/factory/issues/897)) | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | NARROW | Refusal text of [gate 2, the project gate](mike.md#33-gates-mike-enforces-for-every-caller) only |
| Review-idle | Pair an idle reviewer with the oldest `needs_ir` pull request; holds | [agent-harness README, Review-idle](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md) | NARROW | One reviewer per ready pull request, in parallel; no holds |
| Seat | An agent session the harness manages | [lexicon.md line 161, Seat](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L161) | NARROW | Owns one assignment or nothing |
| Seat cap (`max_seats`) | Worker cap in `seats.yaml`; control seats exempt | [agent-harness spec line 49, Seat cap](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L49) | NARROW | Cap per role; reviewers `ceil(workers / 3)` ([decision 3, the reviewer cap](mike.md#11-decisions)) |
| Send-back | Merge-gate outcome: findings return to the owner | [agent-harness spec line 406, Send-back](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L406) | NARROW | An independent reviewer's signal (seat, attached session, or human); the owner seat's next assignment; nothing held |
| Sign-in gate | Front door in front of the API: `hgl-auth` or `oauth2-proxy` | [lexicon.md line 121, Sign-in gate](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L121) | NARROW | Concept stays; product is config; a human is a verified bearer |
| Standing seat | A seat named in `seats.yaml` | [agent-harness spec line 45, Standing seat](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L45) | NARROW | Decided 2026-10-05: the pool is a cap and a name list; a standing seat is a name in that list ([decision 11, the seat pool](mike.md#11-decisions)) |
| Steer | Wake and instruct; the entry restates 3 gates and the loop window | [lexicon.md line 227, Steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L227) | NARROW | Next assignment or inside it; never across open work in the first cut; an idle seat may be steered onto related work |
| Steer record | Record of a steer; in the planner it holds seat and issue | [agent-harness AGENTS.md line 113, Steer record](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/AGENTS.md#L113) | NARROW | A record only |
| Steer rules | Config-store steering settings, 11 listed | [lexicon.md line 367, Steer rules](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L367) | NARROW | Gate and share parameters only; rest is Fleet |
| Stop | Pause a seat, keep its session; auto-steer off | [lexicon.md line 239, Stop](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L239) | NARROW | Human switch; a human or Arthur clears it ([mike.md gate 8, the human switches](mike.md#33-gates-mike-enforces-for-every-caller)) |
| Unassigned-urgent | Set of unassigned Urgent issues; a Health row | [agent-harness spec line 161, Unassigned-urgent](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L161) | NARROW | A board column of unassigned `urgency:critical` issues |
| unmeasured-liveness | Hold: the seat's reading is unmeasured | [idle_steer.py line 55, the unmeasured-liveness hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L55) | NARROW | Refusal text of [gate 7, no mint over a live seat](mike.md#33-gates-mike-enforces-for-every-caller) only |
| Vendor | System that runs a seat's session; truth for alive; also the biller | [lexicon.md line 127, Vendor](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L127) | NARROW | Who bills a runtime: Claude, Grok, Cursor ([mike.md §4, runtimes](mike.md#4-runtimes)); what runs it is the runtime, how Mike reaches it is the access method |
| `--allow-lower-severity` | Override flag for `higher_unassigned` | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Already removed ([factory#1763, Low refused, higher_unassigned removed](https://github.com/excaliwire/factory/issues/1763)) |
| already-assigned | none-eligible reason ([factory#897, idle feed finds no work](https://github.com/excaliwire/factory/issues/897)) | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| Auto-steer | Seat eligibility for loop steering; stop sets it off | [agent-harness spec line 104, Auto-steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L104) | RETIRE | Stop replaces it |
| awaiting-response | Hold: a seat with a pull request awaiting response is not idle | [idle_steer.py line 42, the awaiting-response hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L42) | RETIRE | Send-back is the next assignment ([mike.md §8, the lexicon](mike.md#8-lexicon)) |
| Conflict-steer | Ready conflicting PR steers its owner, or an idle worker | [agent-harness spec line 163, Conflict-steer](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L163) | RETIRE | Decided 2026-10-05: not a verb; a conflict is a change kind the control plane routes to the author seat ([decision 5, conflicts are change kinds](mike.md#11-decisions)) |
| Copilot-findings | Copilot threads steer the owner; a busy owner yields to an idle worker | [agent-harness spec line 406, Copilot-findings](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L406) | RETIRE | Decided 2026-10-05: not a verb; unresolved Copilot threads are a change kind routed to the author seat ([decision 5, conflicts are change kinds](mike.md#11-decisions)) |
| Harness-state | Git branch that seeds the direction list | [lexicon.md line 337, Harness-state](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L337) | RETIRE | Config store is the source |
| higher_unassigned | Steer refusal: a higher severity in the lane is unassigned | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Already removed ([factory#1763, Low refused, higher_unassigned removed](https://github.com/excaliwire/factory/issues/1763)) |
| Hold | Planner outcome that plans nothing and names why | [agent-harness spec line 159, Hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | A gate outcome is a refusal |
| Hold streak | Fault holds past a threshold become a Health row | [agent-harness AGENTS.md, Hold streak](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/AGENTS.md) | RETIRE | A refusal streak is a log line |
| Host ladder | Lane-PE moves to cheaper hosts at a gauge threshold; one way | [agent-harness spec line 137, Host ladder](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L137) | RETIRE | Gauges with a mint threshold replace it ([mike.md §4, runtimes](mike.md#4-runtimes), [§8, the lexicon](mike.md#8-lexicon)) |
| in-flight:open-pull-request | none-eligible reason ([factory PR 913, in-flight work is taken](https://github.com/excaliwire/factory/pull/913)) | [agent-harness spec line 159, in-flight:open-pull-request](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | Planner reason |
| in-flight:pending-assignment | Hold: a pending create for the seat | [idle_steer.py line 56, the in-flight:pending-assignment hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L56) | RETIRE | Planner hold |
| in-flight:steer-record | none-eligible reason ([factory PR 913, in-flight work is taken](https://github.com/excaliwire/factory/pull/913)) | [agent-harness spec line 159, in-flight:steer-record](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | Planner reason |
| Lane owner | `policy.lanes` maps a lane label to its owning lane-PE | [lexicon.md line 181, Lane owner](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L181) | RETIRE | [mike.md §8, the lexicon](mike.md#8-lexicon); a lane-PE steers its lane, owns nothing |
| lane-owner-busy | Hold: lane owner busy (never used) | [idle_steer.py line 45, the lane-owner-busy hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L45) | RETIRE | Planner hold |
| lane-starved | Hold and steer refusal: lane not on the list | [idle_steer.py line 46, the lane-starved hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L46) | RETIRE | Every lane is on the priorities list; [gate 3, the lane gate](mike.md#33-gates-mike-enforces-for-every-caller) refuses only a missing or unknown lane ([mike.md §8, the lexicon](mike.md#8-lexicon)) |
| Lexicon: Clear | Line 2 of the old 4-line review block | [test_comment_limits_1741.py line 17, Lexicon: Clear](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/tests/test_comment_limits_1741.py#L17) | RETIRE | Retired by [factory#1741, terse comment limits](https://github.com/excaliwire/factory/issues/1741); drift is a blocking finding |
| master-plan (reason) | none-eligible: the issue has sub-issues | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| no-candidate-work | Hold: no open candidate issue | [idle_steer.py line 40, the no-candidate-work hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L40) | RETIRE | Planner hold |
| no-free-seat | none-eligible reason ([factory#1197, the none-eligible hold with idle workers](https://github.com/excaliwire/factory/issues/1197)) | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| no-idle-seat | Hold: no idle seat | [idle_steer.py line 39, the no-idle-seat hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L39) | RETIRE | Planner hold |
| no-lane-label | Hold: issue has no lane label (never shown) | [idle_steer.py line 43, the no-lane-label hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L43) | RETIRE | Planner hold |
| no-lane-owner | Hold: lane has no owner (never shown) | [idle_steer.py line 44, the no-lane-owner hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L44) | RETIRE | Planner hold |
| no-matching-seat | none-eligible reason ([factory#897, idle feed finds no work](https://github.com/excaliwire/factory/issues/897)) | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| none-eligible | Hold: candidates exist, none eligible; 1 of 12 reasons | [idle_steer.py line 41, the none-eligible hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L41) | RETIRE | Planner hold ([mike.md §8, the lexicon](mike.md#8-lexicon)) |
| Owned work (`owned_work`) | Roles whose steer prepends what the seat name owns | [agent-harness spec line 192, Owned work](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L192) | RETIRE | A seat owns only its assignment |
| owned-by-live | none-eligible reason: a live seat owns the issue | [agent-harness spec line 159, owned-by-live](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | Planner reason |
| owner-unmeasured | none-eligible reason ([factory#1197, the none-eligible hold with idle workers](https://github.com/excaliwire/factory/issues/1197)) | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| Principal SDE | A worker at a capable tier; `psde.md` | [lexicon.md line 449, Principal SDE](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L449) | RETIRE | Seat types allow no per-seat model |
| Priority (GitHub field) | The issue field whose meaning is severity | [lexicon.md line 397, Priority](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L397) | RETIRE | Replaced by the `urgency:<level>` label, which the GitHub mobile app can set ([mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share)) |
| Program board | Retired 2026-09-16 | [agent-harness spec line 312, Program board](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L312) | RETIRE | Already retired |
| Reboot redelivery | Planner redelivers labelled issues after a reboot | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | The remint carries the assignment |
| reboot-redelivery-held | none-eligible reason ([factory#1744, reboot keeps seat labels](https://github.com/excaliwire/factory/issues/1744)) | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| Redeliver tries | Requeue a queued steer refused at delivery up to N | [agent-harness spec line 86, Redeliver tries](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L86) | RETIRE | No second queue ([mike.md §10 item 7, machine-local queues](mike.md#10-what-mike-does-not-re-create)); unconfirmed delivery says so |
| redelivery-refused | Hold: refused redelivery not replanned in the window | [idle_steer.py line 49, the redelivery-refused hold](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L49) | RETIRE | Planner hold |
| Resume | Tick verb that resumes stood-down seats | [agent-harness spec line 78, Resume](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L78) | RETIRE | With stand-down |
| Rung | One step on the lane-PE host ladder | [lexicon.md line 67, Rung](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L67) | RETIRE | The ladder retires ([mike.md §8, the lexicon](mike.md#8-lexicon)) |
| Seat-assignments board | Retired dashboard board | [agent-harness spec line 261, Seat-assignments board](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L261) | RETIRE | Already retired; remove references |
| SLA | How soon a severity must move; 0 code readers | [lexicon.md line 407, SLA](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L407) | RETIRE | Decided 2026-10-05: retired for the first cut; 0 code readers; age per urgency is a log line first if wanted ([Q7, SLA retired](#q7-sla-measure-or-drop)) |
| Stand-down | Live-state hold until a gate `name#N` clears | [agent-harness spec line 78, Stand-down](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L78) | RETIRE | Arthur steers "wait for #N" ([mike.md §8, the lexicon](mike.md#8-lexicon)) |
| Steer class | Per severity: `interrupt`, `elevate`, `feed`, `never` | [seats.yaml line 682, Steer class](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/seats.yaml#L682) | RETIRE | Only `never` acted; the urgency floor replaces it |
| Steer debt | Planner bookkeeping of refused or 409 steers | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | No planner |
| Taken (in-flight) | Issue taken by open PR, title, steer record, or pending create | [agent-harness spec line 159, Taken](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | Assignment is the one source |
| The box | Shared machine at `/home/box` hosting the harness and tmux seats | [lexicon.md line 53, The box](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L53) | RETIRE | 3 hosts now; name by job: control-plane host, seat host |
| Worker planner | `plan`, `hold_why`, `_feed_key`: picks seat and issue | [factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Arthur decides |

**PROJECT terms (123, not in the table).** The audit's 8 grouped rows hold 90 Excaliwire domain headings and 33 domain bans at [lexicon.md lines 471 to 1142, the project terms](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L471): factory stages (12), Scabbard (7), quality checks (12), canon (33), presentation (10), originals (14), people and product (2), domain bans (33). They stay in factory's own lexicon and reach Mike only through the factory project's hook, which loads them as that project's Geas scope. Mike keeps the general rule ([section 1 rule 10, use the words](#1-rules-mike-keeps-for-its-lexicon)) and the scoped-ban mechanism, not the words. One pattern carries over: Model-call record's "unknown is recorded as unknown, never as zero" is the gauge rule.

**New in Mike, no factory term:** instance, project, share, pool, and the 13 KEEP rows marked new in Mike above. Board is the NARROW row above; runtime is the RENAME of the harness seat field. Entries are in [section 3, Mike entries](#3-mike-entries).

### 2.1 Where the audit and mike.md disagree (mike.md followed)

- Agent harness: audit keeps "harness" for the runtime kind; [mike.md §8, the lexicon](mike.md#8-lexicon) renames it runtime.
- Harness-gh-user: audit KEEP; [mike.md §8, the lexicon](mike.md#8-lexicon) RENAME to gh_user.
- Rung, Host ladder: audit CHALLENGE; [mike.md §8, the lexicon](mike.md#8-lexicon) retires the ladder.
- Reviewer: audit CHALLENGE on the role word; [mike.md §2, roles](mike.md#2-roles) settles it (role key `reviewer`; Warden is factory's instance name).
- Direction: audit CHALLENGE; [mike.md §8, the lexicon](mike.md#8-lexicon) renames it priorities list.
- Board: audit CHALLENGE; [mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share) defines it.
- Temporary seat: audit CHALLENGE; [mike.md §8, the lexicon](mike.md#8-lexicon) keeps it.
- Excaliwire PgM: audit RENAME to Operator; [mike.md §2, roles](mike.md#2-roles) and [§8, the lexicon](mike.md#8-lexicon) say director.
- Vendor: audit moves the billing sense out; [mike.md §4, runtimes](mike.md#4-runtimes) makes billing the whole meaning.
- Harness account: audit KEEP; [mike.md §8, the lexicon](mike.md#8-lexicon) drops "harness" from the vocabulary, so it renames.
- Tier: audit narrows it to the ladder; [mike.md §8, the lexicon](mike.md#8-lexicon) keeps tier and retires the ladder.
- Redeliver tries: audit keeps a transport retry; [mike.md §10 item 7, machine-local queues](mike.md#10-what-mike-does-not-re-create) drops `redeliver_tries`.
- Caller matrix: audit drops the lane-PE own-lane steer; [mike.md §9 rule 12, the caller matrix](mike.md#9-what-mike-keeps) keeps it.
- Stop: audit says only a person clears it; [mike.md gate 8, the human switches](mike.md#33-gates-mike-enforces-for-every-caller) lets Arthur undo a Stop.
- Reset defaults: audit one record per seat; [mike.md §3.2, mint, remint, steer](mike.md#32-mint-remint-steer) one recorded write.
- Low: audit refuses a worker or Warden steer; [mike.md gate 4, the urgency floor](mike.md#33-gates-mike-enforces-for-every-caller) names the worker steer onto `urgency:no` only.
- Gate count: audit counts 7 gates ([factory#1336, the harness redesign](https://github.com/excaliwire/factory/issues/1336) section 4); [mike.md §3.3, the gates](mike.md#33-gates-mike-enforces-for-every-caller) has 10. Gates 1 to 7 number the same; this file cites mike.md.
- Lane-PE, TPM: audit asks whether they go or merge into Arthur; [mike.md decision 12, the lane-PE role](mike.md#11-decisions) and [decision 13, Arthur and K stay two](mike.md#11-decisions) keep both; [section 4, questions for a human](#4-questions-for-a-human) records the decisions.

## 3. Mike entries

Factory style: owner link first, what it is, what it is not, then **Binds**. Thresholds and gate lists stay in [mike.md, the Mike spec](mike.md) ([rule 2, no second copy](#1-rules-mike-keeps-for-its-lexicon)).

### Mike

Owner: [mike.md §1, what Mike is](mike.md#1-what-mike-is). The system: code and tests that run a swarm of AI agent seats on GitHub repositories. It mints seats, steers them, records every decision before it acts, holds the merge gate, and serves one [dashboard API](#dashboard-api). It is not a seat, not a runtime, and not a merger: it has no merge verb. Factory called it the agent harness. **Binds:** [gate 10, no merge verb](mike.md#33-gates-mike-enforces-for-every-caller), test `test_no_merge_verb`.

### Instance

Owner: [mike.md §1.2, multi-repository](mike.md#12-multi-repository-one-instance). One running Mike: one control plane, one loop, one store, one dashboard, one priorities list, managing a list of projects. There is no Mike deploy per repository. Not a vendor instance (factory's word for one vendor session); Mike says session. **Binds:** test `test_two_projects_one_instance` ([mike.md §12, done when](mike.md#12-done-when)).

### Project

Owner: [mike.md §1.2, multi-repository](mike.md#12-multi-repository-one-instance). One GitHub repository an instance manages, named `owner/repo` on the instance's project list. Every verb that touches GitHub names its project; a repository not on the list is refused before any call runs. A project's domain words come from its own lexicon through its hook. The set of projects is the program (`program.repositories`). **Binds:** [gate 2, the project gate](mike.md#33-gates-mike-enforces-for-every-caller), test `test_steer_refuses_repository_not_on_project_list`.

### Runtime

Owner: [mike.md §4, runtimes](mike.md#4-runtimes). What a seat runs on: one [driver](#driver) under the [Mike Runtime API](#mike-runtime-api), such as `cursor-cloud`, `grok-tmux`, `claude-tmux`, `codex-tmux`, `claude-cloud`. Each runtime provides mint, confirmed steer, stop, restart, archive, liveness, usage and a [session log](#session-log), or reports `unmeasured` with a reason. Not the vendor, which bills it, and not the [access method](#access-method), which is how Mike reaches it. Factory carried it as a seat's `harness:` field. **Binds:** the actuator contract test run once per runtime; config key `runtime` ([decision 7, harness renamed runtime](mike.md#11-decisions)).

### Vendor

Owner: [mike.md §4, runtimes](mike.md#4-runtimes). Who bills a runtime: for example Claude, Grok, or Cursor. Mint picks the next vendor when a runtime's [gauge](#gauge) crosses its mint threshold. Not the runtime, not the [access method](#access-method), and not the source of liveness, which the runtime reports. **Binds:** gauge mint-threshold refusal, test `test_mint_refuses_on_unmeasured_gauge`.

### Mike Runtime API

Owner: [mike.md §4, runtimes](mike.md#4-runtimes). The driver-like layer that gives Mike vendor-neutral access to agent sessions from any vendor through either [access method](#access-method). Every runtime is a [driver](#driver) under it; new drivers are enabled or installed through config. Not factory's session API, which was Cursor-shaped. **Binds:** the actuator contract test, run once per driver; one record shape for every runtime.

### Driver

Owner: [mike.md §4, runtimes](mike.md#4-runtimes). One runtime's implementation of the [Mike Runtime API](#mike-runtime-api), for one vendor and one access method. It fills every capability or reports `unmeasured` with a reason. Not a vendor and not a seat. **Binds:** config enables or installs it; the actuator contract test per driver.

### Access method

Owner: [mike.md §4, runtimes](mike.md#4-runtimes). How Mike reaches a vendor's sessions: `cloud`, through the vendor's APIs, or `tmux`, through send-keys and screen reading that emulate an API. Both sit under the [Mike Runtime API](#mike-runtime-api). Not the vendor and not the runtime, which pairs one vendor with one access method. **Binds:** config field per driver; a `tmux` steer is confirmed by pane echo.

### Session log

Owner: [mike.md §4, runtimes](mike.md#4-runtimes). A runtime capability: the stream of inputs and responses from one session, from which the last input (the last steer) and the most recent response can be identified. Not `mike.jsonl`, which is Mike's own log. **Binds:** the actuator contract test reads the last steer back from the session log.

### gh_user

Owner: [mike.md §3.3, the gates](mike.md#33-gates-mike-enforces-for-every-caller). The GitHub user, per instance, whose assigned issues and pull requests Mike may steer. Empty or unmeasured refuses every steer. Not a human merger; Mike never writes as the merger. Factory: harness-gh-user. **Binds:** [gate 1, the owner gate](mike.md#33-gates-mike-enforces-for-every-caller), refusal text `not assigned to gh_user`.

### Seat card

Owner: [mike.md §7.1, the Seats tab and the seat card](mike.md#71-the-seats-tab-and-the-seat-card). The one component that draws a seat: info on top (name, role, liveness LED with its word, driver, last mint, assignment and its time, last steer and its time, context pressure gauge, tokens since mint) and controls on the bottom (start-stop switch, Restart, Steer, Mint, Archive). Responsive by its container; on a phone the info sits behind an expander and the verbs behind a hamburger. Not a table row, and not a tab: the Seats tab is where cards are grouped by role. **Binds:** one component rendered on the Seats tab, the board and the review surface; test that a 375 px render has no horizontal scroll.

### Seat

Owner: [mike.md §2, roles](mike.md#2-roles). A named agent session Mike manages, with one role. A worker or reviewer seat is in the pool and owns nothing beyond its current assignment: no lane, no issue history, no second label. The director, a session a human opens for himself, and a human-driven engineer session are not seats. **Binds:** caller matrix (anyone not a human or director is a seat or refused).

### Pool

Owner: [mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share). The worker and reviewer seats together, each owning only its assignment. Its size is a cap per role in instance config; reviewers are sized from workers ([decision 3, the reviewer cap](mike.md#11-decisions)). Whether its seats are standing names or minted names is [Q1, standing names or a pool](#q1-standing-names-or-pool-slots). Not the orchestrator seats or lane-PEs. **Binds:** mint refuses past the role cap.

### Assignment

Owner: [mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share). The one piece of work a seat is on: idle, or one issue or one pull request. A seat owns nothing beyond it. The `seat:<name>` label is the truth and Mike's store caches it; a remint carries it, a send-back is the author seat's next assignment, and Reset Defaults clears all of them in one recorded write. Not liveness, and not desired state. **Binds:** test `test_remint_carries_assignment`.

### Steer

Owner: [mike.md §3.3, the gates](mike.md#33-gates-mike-enforces-for-every-caller). Give an idle seat its next assignment, or tell a seat something inside the assignment it already has. In the first cut a steer never moves a seat to other work while its assignment is open; a remint keeps it on the same work. The architecture lets Arthur steer an idle seat onto related work where its context helps ([mike.md §3.2, mint, remint, steer](mike.md#32-mint-remint-steer)). Delivery is confirmed by a run id, a pane echo, or an event id, or it is not a steer. `steer` refuses what the gates forbid, for every caller, and the refusal is a decision record. **Binds:** [gates 1 to 5, owner through one pending steer](mike.md#33-gates-mike-enforces-for-every-caller), test `test_steer_refuses_across_open_work`.

### Board

Owner: [mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share). What the arbiter reads: idle seats, each seat's assignment and its last completed assignment, send-backs with the owner seat, ready pull requests per seat, the priorities list with its notes, and target versus actual share per row. Mike builds it, and the dashboard shows the same board to a human. Not a dashboard page or tab, and not a GitHub Discussion board. **Binds:** the follow-up prompt carries the board; test `test_follow_up_carries_board`.

### Share

Owner: [mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share). The percent of workers the lane at a priorities rank gets; the config store holds one share per rank. Defaults follow the rule in mike.md for any number of lanes (60, 30, 10 for three), and a human may override them; overrides sum to 100. A row with no open work above `urgency:no` gives its share to the next row. Target share is config; actual share is the arbiter's judgment, and Health shows both. **Binds:** config-store schema field per rank, test that overrides sum to 100; Health target-versus-actual row.

### Urgency

Also: severity

Owner: [mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share). How soon work must move: `critical`, `high`, `normal`, `no`, carried as the label `urgency:<level>`, because a label can be set from the GitHub mobile app and the Priority field cannot. It orders work inside a lane, oldest first inside an urgency; no label is [`urgency:no`, the floor](#urgencyno). Factory's Urgent, High, Medium and Low map onto the four levels in order. Not a lane, and it has no steer class. **Binds:** [gate 4, the urgency floor](mike.md#33-gates-mike-enforces-for-every-caller); board sort-order test.

### `urgency:no`

Also: Low

Owner: [mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share). The lowest urgency and the default: an issue with no urgency label is `urgency:no`. Nothing runs on it; a worker steer onto it is refused at the urgency floor. Not "not planned": there is no planner. **Binds:** [gate 4, the urgency floor](mike.md#33-gates-mike-enforces-for-every-caller), refusal text `urgency floor: nothing runs on urgency:no`; factory's pin [test_lane_rows_1407.py line 376, "not planned" on Low](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/tests/test_lane_rows_1407.py#L376) moves from "not planned" to "Nothing runs on `urgency:no`".

### Lane

Owner: [mike.md §3, the seat model](mike.md#3-the-seat-model). A large architectural body of work within the program; a program has one or more, and each issue carries exactly one lane label. Every lane has one row on the priorities list, which is how it gets workers. A lane has no owner and binds no seat; a lane-PE steers in its lane through the caller matrix. **Binds:** [gate 3, the lane gate](mike.md#33-gates-mike-enforces-for-every-caller), refusing a missing or unknown lane label; `lane-starved` is retired.

### Priorities list

Owner: [mike.md §3.1, pool, assignment, share](mike.md#31-pool-assignment-share). What a human decided about prioritization: an ordered list in the config store with one row per lane, so every lane is ranked, each row carrying an optional note. A row's rank sets its [share](#share) of workers. The note is a human's intent in a sentence: it goes on the board and into every steer to that lane's lane-PE, and binds nothing. Not the GitHub Priority field, which retires for the [urgency](#urgency) label. Fields: `lane`, `note`. Factory called it direction. **Binds:** [gate 3, the lane gate](mike.md#33-gates-mike-enforces-for-every-caller); the API command is `priorities` and Mike's API has no `direction` ([Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands), [decision 8, priorities list replaces direction](mike.md#11-decisions)); factory pin [test_direction.py, the direction tests](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/tests/test_direction.py) moves.

### Arbiter

Owner: [mike.md §2, roles](mike.md#2-roles). The role of the seat that reads the board and decides who does what: which seat takes which issue, the share each priorities row actually gets, when to remint and when to reuse an idle seat, the order of send-backs, and recovery after a reboot. It acts only through Mike's verbs, and the gates bind it like any caller. It is judgment, not the control plane, which is code. One per instance; the name is the role key unless the instance overrides it; Arthur on factory. **Binds:** caller matrix `arbiter`; [gates 1 to 5, owner through one pending steer](mike.md#33-gates-mike-enforces-for-every-caller).

### Steer rules

Owner: [mike.md §5, the control plane](mike.md#5-the-control-plane). The config-store settings that parameterize the gates and the shares: the share per rank, the loop window, the reviewer ratio, the per-role seat caps, and the orchestrator cooldown. A rule the store does not hold reads `unmeasured`. Fill-missing cap, paste limits, poke stale window, main-restart lists and the GitHub read reserve are Fleet settings, not steer rules. **Binds:** config-store schema; test that an absent rule reads `unmeasured`.

### Mint

Owner: [mike.md §3.2, mint, remint, steer](mike.md#32-mint-remint-steer). Cause an agent session to be created for a seat on its runtime. A mint is wait-only for every role, lane-PEs included: the seat reads its brief and stops at "Wait for the first steer". It writes a decision record; wait-only mints and the [gauges](#gauge) hold its cost down, not a token or turn budget. Mike mints no seat over one whose liveness is responding or unmeasured. **Binds:** [gate 7, no mint over a live seat](mike.md#33-gates-mike-enforces-for-every-caller); test `test_mint_prompt_is_wait_only` for every role.

### Remint

Owner: [mike.md §3.2, mint, remint, steer](mike.md#32-mint-remint-steer). A mint of a seat that already had a session; it carries the assignment, so the first steer after a remint is the same work. In the first cut it is how a seat with open work gets a fresh session; a steer does not move it across open work. Not a mint of a new name. **Binds:** test `test_remint_carries_assignment`; one decision record per remint.

### Liveness

Owner: [mike.md §4, runtimes](mike.md#4-runtimes). Whether a seat's session answers: `not-minted`, `responding`, `not-responding`, or `unmeasured` with a reason, the same 4 words for every runtime. Busy and idle are activity, not liveness, and liveness is not assignment. **Binds:** schema refuses a fifth value; Sessions row verbs.

### Decision record

Owner: [mike.md §5, the control plane](mike.md#5-the-control-plane). Who saw what, decided what, why, and the outcome (pending, applied, refused, cancelled), with actor and caller, written before the side effect. Every verb writes one, mint, archive, restart and kill included; a refusal is a record with its why. **Binds:** [gate 6, record before act](mike.md#33-gates-mike-enforces-for-every-caller); `apply` refuses an unrecorded decision.

### Send-back

Owner: [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back). An independent reviewer's signal, from a seat, an attached session, or a human, that the pull request goes back to its owner: it returns to draft and the owner seat gets it as its next assignment after the work it is on. Nothing else is held, and a ready pull request does not hold its owner. Not an awaiting-response hold. **Binds:** `draft-sent-back`; test `test_send_back_is_author_next_assignment`.

### Self code review

Owner: [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back). A review by the seat a pull request is assigned to, done with that seat's runtime code-review tool and posted as the self-review block on the head ([mike.md §6, the pull request lifecycle](mike.md#6-the-pull-request-lifecycle)). Every pull request needs at least one. Not an independent review. Factory: owner self-review. **Binds:** merge step 2; a new commit voids it.

### Independent code review

Owner: [mike.md §3.4, review and send-back](mike.md#34-review-and-send-back). A review by a seat, an attached session, or a human that is not the seat assigned to the pull request; every pull request needs at least one. A reviewer seat's review takes the 12-line shape, and a human's or attached session's counts when config says so ([mike.md §3.6, how reviewers operate](mike.md#36-how-reviewers-operate)). Its `Send back` is a [send-back](#send-back). Factory: independent review. **Binds:** [gate 9, reviewer independence](mike.md#33-gates-mike-enforces-for-every-caller); config `human_review_counts`.

### Gauge

Owner: [mike.md §4, runtimes](mike.md#4-runtimes). A measured reading of one usage pool or window a runtime declares: a vendor pool percent, a window such as Claude's 5-hour limit, tokens since mint, context pressure. Each carries a mint threshold, and mint picks the next vendor when one crosses it; the dashboard shows the same readings to humans. No probe means `unmeasured`, never 0, and a mint that depends on an unmeasured gauge is refused. A gauge source is how a reading is taken (factory: meter); the gauge list is config. **Binds:** mint-threshold refusal; test that an unprobed gauge reads `unmeasured`.

### Tick

Owner: [mike.md §5, the control plane](mike.md#5-the-control-plane). One pass of the control loop: read desired state, read live state, decide, act. A tick does not overlap the previous one. The loop is the process that is Running or Paused; a tick is one pass of it. Factory: retarget-loop. **Binds:** loop lock test (no overlap); one heartbeat per tick.

### Control plane

Owner: [mike.md §5, the control plane](mike.md#5-the-control-plane). Mike's code: it holds desired state, reads live state, acts on the difference, and refuses what the gates forbid. It holds no inbound path and no SSH key to a seat host. Not a seat: the arbiter is judgment, the control plane is mechanism. It runs on the control-plane host (factory: droplet). **Binds:** [gates 1 to 10, every gate](mike.md#33-gates-mike-enforces-for-every-caller).

### Dashboard API

Owner: [Mike's dashboard API](mike-dashboard-api.md). Mike's own versioned contract between the control plane and every client: the dashboard, the CLI, a seat, an attached session. It carries [parts](#part) as [frames](#frame) on one stream and as plain reads, and takes [commands](#command) that each return a [job](#job). Factory's dashboard API was its starting point, not its definition; nothing in Mike refers to factory's contract as law. Not the [Mike Runtime API](#mike-runtime-api), which faces vendors. **Binds:** the version-gate and second-client tests in [Mike dashboard API §9, where this is tested](mike-dashboard-api.md#9-where-this-is-tested).

### Part

Owner: [Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream). One named slice of state the control plane serves: `version`, `health`, `seats`, `board`, `priorities`, `review`, `gauges`, `settings`, `attached-sessions`, `logs`, `jobs`. Each part is one read and one stream event name; one the loop has not written is `absent`, one it cannot read is `unmeasured`. Not a dashboard tab, though a tab usually draws one. **Binds:** the opening-frames and pushed-frames tests in [Mike dashboard API §9, where this is tested](mike-dashboard-api.md#9-where-this-is-tested).

### Frame

Owner: [Mike dashboard API §4, the stream](mike-dashboard-api.md#4-the-stream). One server-sent event that carries one [part](#part), with `version`, `part`, `written_at` and `state`. A new stream gets one frame per readable part, then a frame only when that part changes; `logs` frames carry new lines only. Not a keep-alive, which is a comment. **Binds:** every frame validates against its shape in [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes).

### Command

Owner: [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands). A POST to the [dashboard API](#dashboard-api): fleet mode, seat verb, priorities, settings, attached sessions, issue. It answers 202 with a [job](#job) id and a record id at once, the record written first. Not a seat verb alone, and there is no merge command. **Binds:** the commands test in [Mike dashboard API §9, where this is tested](mike-dashboard-api.md#9-where-this-is-tested); [gate 10, no merge verb](mike.md#33-gates-mike-enforces-for-every-caller).

### Job

Owner: [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands). The outcome of one [command](#command): `pending`, then `applied`, `refused` or `cancelled`, with why, actor, and one outcome per seat for a seat verb. It arrives on the `jobs` [part](#part) and on the jobs read however long it took. Not a [decision record](#decision-record), which it names. **Binds:** `jobRow` in [Mike dashboard API §7, payload shapes](mike-dashboard-api.md#7-payload-shapes); a slow verb's outcome lands on its job row.

### Seat host

Owner: [mike.md §4, runtimes](mike.md#4-runtimes). The agent on a machine that runs tmux seats: it checks in, pulls its own actuations from the control-plane store with a host token, runs them, and reports results. A stale seat host makes its seats `unmeasured`. Not the control-plane host, and it holds no shared master secret and no second, machine-local queue. **Binds:** test that a host token pulls only its own actuations.

### Attached session

Owner: [mike.md §2.2, attached sessions](mike.md#22-attached-sessions-non-seats-that-act-through-mike). A session a human drives (Infra Fable, Factory Fable, the director) that holds a session token and acts through Mike's verbs for every repository and Mike interaction. Not a seat: never minted, steered, assigned, or counted against the cap. Recorded as its own actor; writes under Mike's account with its `[Name]` prefix; bound by every gate; rights per its config row. Attaching is optional. Word confirmed by a human 2026-10-05 ([Q14, the attached-session word](#q14-the-word-for-a-non-seat-session-that-acts-through-mike)). **Binds:** caller matrix `attached`; test that a session token cannot mint and cannot act as a human.

### Session token

Owner: [Mike dashboard API §2, identity](mike-dashboard-api.md#2-identity). The bearer a human issues to an [attached session](#attached-session), naming the session and the verbs it may run. Its text appears once, in the issue answer, and never on a frame, read, record or log line; a revoke takes effect on its next call. Not a seat token or a host token. **Binds:** `POST attached-sessions` in [Mike dashboard API §6, commands](mike-dashboard-api.md#6-commands); test that a revoked token is 401 with a record.

### Humans

Owner: [mike.md §2.1, humans](mike.md#21-humans). The people Mike serves, several, listed in instance config by GitHub login. They act on GitHub as themselves: create and edit issues, comment, review, assign, merge. The control plane watches that activity and routes it: an assignment to `gh_user` hands an issue with a lane label to Mike, a `To: Name` comment steers that seat (`[Name]` with no colon is a prefix, not an address), a change request on a ready pull request is a send-back, `waive:` and `reviewer:` bind the gates. Any listed human may merge, issue a session token, and edit priorities and settings; the record names which one. A user not on the list is a contributor: seen, shown, routed nowhere until a listed human or K triages it. Not a seat, not an attached session, not one person: Tig is factory's config. **Binds:** caller matrix `human`; the change router; test that a contributor's `waive:` binds nothing.

### Director

Owner: [mike.md §2, roles](mike.md#2-roles). The attached session a human uses as his portal (Excaliwire PgM on factory). It is not a seat and holds no assignment; the caller matrix knows it by name beside a human. Authority runs human, director, TPM, lane-PE, then worker or reviewer. Not a human: only a human merges, waives a gate, or grants a reviewer. **Binds:** caller matrix `director`; test that a seat token cannot act as the director.

## 4. Questions for a human

Each CHALLENGE row, plus the [mike.md §11, decisions](mike.md#11-decisions) this file depends on. Recommendations match mike.md. A decided question says so.

### Q1. Standing names or pool slots?

(Standing seat, Fill-missing, Seat cap.) Factory has 13 standing rows; 100 workers would be 100 `seats.yaml` rows.

Decided, Tig, 2026-10-05: pool, a cap plus a name list ([decision 11, the seat pool](mike.md#11-decisions)).

### Q2. Does the lane-PE role exist in Mike?

(Lane-PE, PE seat.) A mint that was not wait-only read 4.2M and 5.0M tokens in 30 minutes ([factory#1755, the lane-PE mint cost](https://github.com/excaliwire/factory/issues/1755)).

Decided, Tig, 2026-10-05: keep the role; Mike may mint it behind a human-confirmed setting; wait-only; no ladder ([decision 12, the lane-PE role](mike.md#11-decisions)).

### Q3. Two orchestrator seats, or TPM merged into Arthur?

(Orchestrator seat, TPM.) Classification and "who should own this" overlap the arbiter's judgment.

Decided, Tig, 2026-10-05: keep two; measure K for a week, then decide ([decision 13, Arthur and K stay two](mike.md#11-decisions)).

### Q4. Does SEV1 (Urgent) preempt an open assignment?

(Urgent.) Its steer class `interrupt` is reported, never acted on.

Decided, Tig, 2026-10-05: `urgency:critical` sorts first, never preempts; a human may Stop a seat by hand ([decision 14, `urgency:critical` never preempts](mike.md#11-decisions)).

### Q5. Priorities list form: lanes or free text, per instance or per project?

(Priorities list, Lane.) Free text drops the lane gate.

Decided, Tig, 2026-10-05: a lane plus an optional note shared with the lane-PE as context ([decision 2, a lane plus a note](mike.md#11-decisions)). Per instance or per project is still [decision 6, one list per instance](mike.md#11-decisions).

### Q6. Which word names a human?

(Tig.) "Tig", "operator" and "director" are all in use; mike.md writes "a human".

Decided, Tig, 2026-10-05: humans, plural. The system holds a list of humans in instance config; text says a human or humans; the name is config ([mike.md §2.1, humans](mike.md#21-humans)).

### Q7. SLA: measure or drop?

(SLA.) 0 code readers today; prose and `seats.yaml` only.

Decided, Tig, 2026-10-05: retire for the first cut.

### Q8. Conflict-steer: keep?

(Conflict-steer.) "Or an idle worker" steers a non-author across work.

Decided by [decision 1, change-driven steering](mike.md#11-decisions), 2026-10-05: not a verb; a change kind the control plane routes to the author seat.

### Q9. Copilot-findings: keep?

(Copilot-findings.) A busy owner yields to an idle worker, the same cross-work steer.

Decided by [decision 1, change-driven steering](mike.md#11-decisions), 2026-10-05: same as [Q8, conflict-steer](#q8-conflict-steer-keep).

### Q10. Rename the seat field `harness` to `runtime`?

(harness seat field.)

Decided, Tig, 2026-10-05: yes ([decision 7, harness renamed runtime](mike.md#11-decisions)).

### Q11. Replace `direction` everywhere, the API command included?

(Direction.)

Decided, Tig, 2026-10-05: yes, at the major bump [tig/mike#1, the dashboard rewrite](https://github.com/tig/mike/issues/1) already needs ([decision 8, priorities list replaces direction](mike.md#11-decisions)). Done: Mike's own contract starts at 1.0.0 with `priorities` and no `direction` ([Mike dashboard API §8, what changed and the terminal deferral](mike-dashboard-api.md#8-what-changed-from-the-starting-point)).

### Q12. Accept the new words this file proposes beyond mike.md section 8?

Activity (Live map), vendor account (Harness account); [mike.md §8, the lexicon](mike.md#8-lexicon) decides the rest, and program stays ([mike.md §1.2, multi-repository](mike.md#12-multi-repository-one-instance)).

Recommend: accept; each lands with its schema in one change ([rule 8, a new term needs a human](#1-rules-mike-keeps-for-its-lexicon)).

### Q13. Retire stand-down, resume, the hold words, the host ladder, rung, and retarget?

Decided, Tig, 2026-10-05: yes ([decision 15, the hold words retire](mike.md#11-decisions)). The RETIRE rows for them in [section 2, the carry-over table](#2-carry-over-table) are closed.

### Q14. The word for a non-seat session that acts through Mike?

(Attached session, new.) Factory says only "not a seat"; Tig asked for the capability on 2026-10-05.

Decided, Tig, 2026-10-05: attached session; the director is one; default rights issue and pull verbs like a seat, steer like a lane-PE, no mint ([decision 16, attached session](mike.md#11-decisions)).

