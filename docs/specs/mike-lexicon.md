# Mike lexicon carry-over

**Status:** plan. Written before the code, as the companion to [`mike.md`](mike.md#8-lexicon).

**What this is.** Every factory harness term, each with a verdict for Mike: KEEP, RENAME, NARROW, RETIRE, or CHALLENGE. A human edits this file; a CHALLENGE row stays open until he does. The lexicon is config, so once Mike has code a change to this file is test-first: a test fails on the old text and passes on the new. Test names on **Binds** lines in section 3 are the tests to write; none exists yet.

**Source pin:** excaliwire/factory [`bb2bf4c6`](https://github.com/excaliwire/factory/tree/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8) (2026-10-05). A `lex:<n>` source is `https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L<n>`; `spec:<n>` is `docs/specs/agent-harness.md#L<n>` at the same commit; other sources name their file. Input: the lexicon audit (194 rows, 309 terms). Where the audit and [`mike.md`](mike.md) sections 8 and 11 disagree, mike.md wins, and section 2.1 lists each disagreement.

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

192 rows: the audit's 186 single-term rows plus 6 terms mike.md section 8 decides that the audit has no row for (harness seat field, retarget loop, meter, Lexicon: Clear, lane owner, runtime kind names). Gate numbers are mike.md 3.3. Ordered by verdict, then alphabetically.

| Verdict | Rows |
|---|---|
| KEEP | 95 |
| RENAME | 15 |
| NARROW | 38 |
| RETIRE | 44 |
| CHALLENGE | 0 |

| Term | Factory meaning (one line) | Source | Mike verdict | Mike term or why |
|---|---|---|---|---|
| Actuation | Unit a seat host pulls: paste, restart, kill, liveness, meter | [spec:300](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L300) | KEEP | Add a heading; `meter` kind reads a gauge source |
| Address | `seat:<name>` owns, `[Name] ` writes, `Name:` addresses | [spec:357](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L357) | KEEP | Address contract (mike.md 9.15) |
| app principal | Banned; write agent principal | [lex:1144](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1144) | KEEP | Ban stays |
| Applied / undelivered | Delivery outcomes; applied does not mean the seat acted | [spec:86](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L86) | KEEP | An unconfirmed steer is not a steer |
| Archive | End a seat's Cursor session so it reads `not-minted` | [lex:245](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L245) | KEEP | Runtime-neutral; writes a decision record |
| Artifact | Throwaway reproduction on a reserved-prefix branch; reaped past max age | [spec:127](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L127) | KEEP | Same |
| Artificer | Factory's display name for a worker | [lex:195](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L195) | KEEP | Default display name in instance config, not a core word |
| Caller matrix | Who may call which verb; arbiter steers; lane-PE steers its own lane | [spec:102](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L102) | KEEP | Keeps lane-PE own-lane steer (mike.md 9.12); knows director and human |
| Check-in | A seat or host tells the control plane it is alive | [lex:329](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L329) | KEEP | Same |
| Config store | Often-changed settings outside git; one writer; versioned | [lex:343](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L343) | KEEP | Schema, append-only, human-only, logged |
| Control plane | Holds desired state, reads live state, acts on the difference; refuses what policy forbids | [lex:61](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L61) | KEEP | Code, not a seat; the arbiter is separate |
| Current main | Seats remint and steer on current main | [spec:186](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L186) | KEEP | Same |
| Dashboard | A view, never the source of truth for policy | [spec:238](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L238) | KEEP | One client of the API |
| Data plane | The seats doing the work; must not reach around the control plane | [lex:139](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L139) | KEEP | Same |
| Decision record | Seen, decided, why, written before the side effect; refusals recorded | [lex:155](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L155) | KEEP | Gate 6; TPM clause follows Q3 |
| dispatch | Banned; write steer or poke | [lex:1122](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1122) | KEEP | Ban stays |
| Draft-sent-back | Convert a ready pull request to draft on `send_back` | [spec:406](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L406) | KEEP | Same |
| Dry run | Plans and records; does not act | [lex:355](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L355) | KEEP | Same |
| farm | Banned; write steer | [lex:1121](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1121) | KEEP | Ban stays |
| Fill-missing | Fleet mode: claim a live same-name session, else mint | [lex:275](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L275) | KEEP | Adopt, else mint; scope follows Q1 |
| Finding | The permanent result; goes on the issue | [spec:125](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L125) | KEEP | Non-blocking review findings become issues |
| Fleet mode | The reboot commands: hard, orchestrator, worker, fill-missing | [spec:102](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L102) | KEEP | Same |
| Fleet read | Vendor listing against the roster: untracked, missing, duplicates | [spec:190](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L190) | KEEP | Same |
| Gauge | Measured reading of one budget; no probe is unmeasured | [spec:148](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L148) | KEEP | Mint budget input; gauge list is config |
| Geas | Binding on words; schema `excaliwire.geas/v1`; instance `geas.yaml` | [lex:465](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L465) | KEEP | Mike's machine lexicon; lints every outbound prompt |
| Hard reboot | Archive every standing seat, mint again, restart the control plane | [lex:281](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L281) | KEEP | First steer is the carried assignment |
| Health | Loop ticking, seats live, gauges unmeasured; one log `harness.jsonl` | [spec:169](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L169) | KEEP | Log is `mike.jsonl`; shows target versus actual share |
| Heartbeat | Loop stamp each tick, before any refusal, only from the loop | [spec:155](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L155) | KEEP | Same |
| Independent review | Line 1 `[Name] Recommendation: Merge on <sha>.` | [spec:406](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L406) | KEEP | 12-line review (mike.md 6) |
| Initial steer | Code-rendered first steer after a mint | [spec:192](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L192) | KEEP | Same |
| Lane-PE | Expensive judgment seat for one lane; no merge, no mint | [lex:173](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L173) | KEEP | Decided 2026-10-05: role stays, wait-only, human or loop mint behind a confirmed setting (decision 12) |
| Last mint | A time, `not-minted`, or `unmeasured`; never a liveness word | [spec:108](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L108) | KEEP | Same |
| Live state | Who is on what now, session ids, meter readings, live tier; not in git | [lex:149](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L149) | KEEP | The store; readings are gauges |
| Liveness | `not-minted`, `responding`, `not-responding`, `unmeasured`; not assignment | [lex:257](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L257) | KEEP | No fifth word; busy and idle are activity |
| Loop cadence | Minutes between acting ticks, 1 to 60 | [lex:361](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L361) | KEEP | Config store |
| Loop mode | `live` or `dry-run`; an unreadable store reads `dry-run` | [lex:349](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L349) | KEEP | Same |
| loop off | Banned; write Paused | [lex:1147](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1147) | KEEP | Ban stays |
| Loop window | How old the loop's own record may be: `stale_after_minutes` plus cadence | [settings:1049](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L1049) | KEEP | Add a heading; gate 5 |
| Main-restart | When main moves, remint the seats whose code changed | [spec:186](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L186) | KEEP | Same |
| Master plan | Issue with sub-issues; done when all are done | [spec:385](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L385) | KEEP | Its hold reason retires |
| Medium | Ordinary work; `sev3`; steer class `feed` | [lex:435](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L435) | KEEP | Drop `feed` |
| Merge-gate | Names the merge step and what is missing, per head; no merge action | [spec:447](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L447) | KEEP | Same |
| Mint | Create a seat; the only verb that brings a seat into being | [lex:219](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L219) | KEEP | Wait-only and budgeted, every role |
| mountain seat | Banned; write worker | [lex:1119](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1119) | KEEP | Ban stays |
| mountain worker | Banned; write worker | [lex:1118](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1118) | KEEP | Ban stays |
| Names must say the job | A name a human can say aloud and know the job; no codes | [lex:9](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L9) | KEEP | Section 1, rules 10 and 13 |
| Needs IR (`needs_ir`) | Ready and waiting for independent review | [README](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md) | KEEP | Same |
| Orchestrator cooldown | Minimum minutes before the same board steers an orchestrator again | [spec:161](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L161) | KEEP | Trigger follows decision 1 |
| Orchestrator reboot | Archive TPM and arbiter, reset their assignments, restart, mint both | [lex:293](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L293) | KEEP | TPM half follows Q3 |
| Orchestrator seat | Arbiter or TPM; must not be one chat | [lex:459](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L459) | KEEP | Decided 2026-10-05: two seats stay; K measured for a week (decision 13) |
| Owner self-review | `Self-Review: Done` naming `Head: <sha>` | [spec:402](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L402) | KEEP | Merge step 2 (mike.md 6) |
| Paste | tmux steer delivery; delivered when the pane shows it | [spec:96](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L96) | KEEP | Pane echo is delivery confirmation |
| Paste hold | Pastes and restarts to a pane are held while a human controls it | [spec:230](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L230) | KEEP | A human pane lock, not a planner hold |
| Paused | No tick acts; carries a reason; an unreadable store reads Paused | [lex:89](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L89) | KEEP | Human switch, gate 8 |
| PE seat | Banned; write lane-PE | [lex:1120](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1120) | KEEP | Ban stays; moot if Q2 drops lane-PE |
| pr-check | Mechanical pull request rules: one seat label, no owner prefix | [spec:449](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L449) | KEEP | Same |
| Priority (GitHub field) | The issue field whose meaning is severity | [lex:397](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L397) | KEEP | Field name is instance config (`Priority` on factory) |
| Ready | Out of draft only with clean self-review and green CI on one head | [spec:405](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L405) | KEEP | Same |
| Refusal | A recorded no with its reason (no heading) | [spec:80](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L80) | KEEP | Add a heading; the one outcome word |
| Remint | Applied create or restart for one seat; carries the assignment | [spec:84](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L84) | KEEP | Add a heading |
| Report-focus | A seat tells the control plane what it is working on | [lex:321](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L321) | KEEP | Drift check: focus versus assignment |
| Reset defaults | Reboot option: assignments idle, auto-steer on, seat labels removed, a record per seat | [lex:287](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L287) | KEEP | One recorded write clears every assignment and label (mike.md 3.2) |
| Restart control plane | Bounce the control-plane process only | [lex:305](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L305) | KEEP | Resumes from the store |
| Retired name | A name in `seats.yaml` `retired`; never minted again | [spec:45](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L45) | KEEP | Same |
| Reviewer | Seat that independently reviews a ready pull request it did not write | [lex:201](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L201) | KEEP | Role key `reviewer`; Warden is factory's name for it, not a Mike default (decision 9) |
| Reviewer grant | `reviewer: <Name>` from `tig` | [spec:422](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L422) | KEEP | From a human merger account (config) |
| Row verbs | A Sessions row lists the verbs that fit liveness; others refused | [spec:102](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L102) | KEEP | The page's only verb source |
| Running | Loop state in which each tick acts; the one config-store switch | [lex:83](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L83) | KEEP | Same |
| Runtime kind names | `cursor-cloud`, `grok-tmux`, `claude-tmux`, `codex-tmux`, `claude-cloud` | [seats.yaml:147](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/seats.yaml#L147) | KEEP | Each is a runtime (mike.md 8) |
| Seat actuator | One interface for mint, stop, steer, archive, restart, claim; Cursor only | [lex:269](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L269) | KEEP | One interface, one record shape, every runtime |
| Seat host | Agent on a machine that hosts seats; pulls actuations, pushes check-in | [lex:95](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L95) | KEEP | Pulls with a host token; no inbound path |
| Seat type | Seats of one role sharing vendor, runtime and model; no per-seat override | [lex:453](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L453) | KEEP | Remint on change |
| Sessions tab | Who is on what now, and the last poke | [spec:246](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L246) | KEEP | Adds a phone layout |
| Severity floor | `severity floor: Low is never steered` (no heading) | [lex:441](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L441) | KEEP | Add a heading; gate 4 |
| Stale | Older than the window, by arithmetic | [spec:302](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L302) | KEEP | Same |
| stall | Banned; write Paused | [lex:1145](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1145) | KEEP | Ban stays |
| stalled | Banned; write Paused | [lex:1146](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1146) | KEEP | Ban stays |
| Sync-tip | Control plane fast-forwards and restarts on tip | [spec:117](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L117) | KEEP | Same |
| Temporary seat | Seat a human mints for one conversation; not counted against the cap | [spec:51](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L51) | KEEP | Proof is its mint record, not the retired board (mike.md 8) |
| Terminal ticket | Single-use ticket bound to an email and a session | [spec:220](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L220) | KEEP | Same |
| Test-first | The test fails on the old code and passes on the new | [spec:403](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L403) | KEEP | Reviewer verb runs it both sides |
| Tick | One control-loop pass, `run_tick`, 10 verbs today (no heading) | [spec:155](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L155) | KEEP | Add a heading; also names the loop (see retarget loop) |
| Tier | How capable and expensive a seat's model is | [lex:167](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L167) | KEEP | Property of a seat type's model; the ladder use retires (mike.md 8) |
| Title ownership | Which roles own which titles and development paths | [spec:66](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L66) | KEEP | Same |
| TPM (Kay) | Roster and briefs; direction into issues; classification judgment | [spec:39](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L39) | KEEP | Decided 2026-10-05: stays as K; measured for a week (decision 13) |
| Tree gate | A tick reaches no live seat unless the tree is confirmed | [spec:167](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L167) | KEEP | Same |
| Unmeasured | A reading not taken; an answer; the path refuses to act (no heading) | [spec:74](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L74) | KEEP | Add a heading; never 0, never ok |
| vendor-hook framework | Banned; write Geas | [lex:1143](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L1143) | KEEP | Ban stays |
| Wait-only mint | Mint with `MINT_WAIT`; the first steer is the assignment | [spec:192](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L192) | KEEP | Every role, lane-PE included (#1755) |
| Waiver | `waive: <gate>` from the `tig` account, pinned to a sha | [spec:416](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L416) | KEEP | From a human merger account (config) |
| Warden | Factory's display name for a reviewer | [lex:207](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L207) | KEEP | Default display name in instance config |
| Web terminal | Watch and take control of a tmux pane; human only | [spec:210](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L210) | KEEP | Same |
| Work type | Feature, Bug, Task; not priority | [spec:383](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L383) | KEEP | Same |
| Worker | Builds one assigned issue to a ready pull request, then waits | [lex:187](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L187) | KEEP | Role key `worker`; its send-backs return to it |
| Worker reboot | Archive and mint workers and reviewers; no control-plane restart | [lex:299](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L299) | KEEP | Same |
| Agent harness | Code-owned control plane for agent sessions; `agent-harness/` | [lex:45](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L45) | RENAME | **Mike**; harness carried 2 meanings |
| Assign Tig | Merge step: assign `tig`; `pull assign-tig` | [spec:407](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L407) | RENAME | **request merge**; the merger is config |
| Claim | Attach a live same-name vendor session to its seat; not a mint | [lex:251](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L251) | RENAME | **adopt**; claim stays for a host claiming an actuation |
| Direction | A human's lane rows `{lane, note}` in the store; on enabled, off starved | [lex:379](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L379) | RENAME | **priorities list**; at most 3 ranked rows, each with a share |
| Droplet | The host that runs the control plane (used 20+ times, no heading) | [spec:86](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L86) | RENAME | **control-plane host**; Mike runs on any host |
| Excaliwire PgM (director) | A human's portal session; not a seat; caller kind `operator` | [spec:47](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L47) | RENAME | **director**; PgM is the instance's display name |
| harness (seat field) | A seat's run kind, `harness: grok-tmux` | [lex:131](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L131) | RENAME | **runtime** (mike.md 8, decision 7) |
| Harness account | One account per harness, named by secret file | [spec:347](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L347) | RENAME | **vendor account**; the vendor bills (mike.md 4); new word, Q12 |
| Harness-gh-user | GitHub user whose assigned issues and pull requests may be steered | [lex:373](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L373) | RENAME | **gh_user**; same gate 1 |
| Live map | `main_restart` reading: active, idle, unmeasured; not liveness | [spec:191](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L191) | RENAME | **activity** (busy, idle, unmeasured); new word, Q12 |
| Meter | A scraped reading of one vendor budget; `write-meters` | [meters:16](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/meters.py#L16) | RENAME | **gauge source**; the gauge is the reading |
| Program | The repositories in `seats.yaml` `program` | [spec:76](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L76) | RENAME | **project list**: the instance's projects; gate 2 |
| Retarget loop | `retarget-loop.sh` and `run_tick`, the loop's name | [retarget-loop:2](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/retarget-loop.sh#L2) | RENAME | **tick**; `retarget-pe` retires with the host ladder |
| Steer-idle | Tick verb: planner for idle workers plus orchestrator follow-up | [spec:159](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RENAME | **follow-up**; the planner is not re-created |
| Tig | A human: merges, owns spend, only waiver source | [lex:31](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L31) | RENAME | **humans** (plural): instance config lists them by login; Mike text says a human or humans; Tig is factory's config (Q6, mike.md 2.1) |
| `seat:<name>` label | That seat owns the work; routes a poke | [spec:365](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L365) | NARROW | Marks the seat's one assignment |
| Agent principal | Entra ID identity per machine trust boundary | [lex:107](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L107) | NARROW | Identity per trust boundary: seat token, host token; Entra is an implementation |
| App role | Entra role checked per route: 4 roles | [lex:115](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L115) | NARROW | Keep the 4 roles; drop Entra |
| Arbiter | Seat that owns the control plane, orders work, owns assignment | [lex:213](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L213) | NARROW | Judgment from the board; acts only through verbs |
| Arthur | Display name of the control-plane seat; spec title "harness aka Arthur" | [spec:1](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L1) | NARROW | Default display name of the arbiter only |
| Assignment | The work a seat is on; actuator stores it; label marks it | [lex:263](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L263) | NARROW | Exactly one; the label is the truth, the store caches |
| At prompt | tmux pane reading: empty prompt is idle, spinner is busy | [spec:82](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L82) | NARROW | The tmux source of activity |
| Board | Follow-up input: open issues, priorities list, unassigned-urgent | [spec:161](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L161) | NARROW | Arthur's whole input (mike.md 3.1); pages say page or tab |
| Board lane rule | Policy text: priorities list is ordered lanes, on or off | [spec:192](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L192) | NARROW | Moves into the arbiter brief and the priorities list entry |
| Control loop | Both one pass and the process that is Running or Paused | [lex:75](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L75) | NARROW | The process, one per instance; one pass is a tick |
| Desired state | `seats.yaml`: names, harness, owner, tier, cap, `pe_retarget` | [lex:145](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L145) | NARROW | Instance config; drop owner and `pe_retarget` |
| High | `sev2`; hours; steer class `elevate` | [lex:429](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L429) | NARROW | Sort order only |
| Lane | Domain named by a repo label; `policy.lanes` maps it to an owning lane-PE | [lex:181](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L181) | NARROW | Label = priorities row; no owner |
| lane-starved | Hold and steer refusal: lane not on the list | [idle_steer:46](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L46) | NARROW | Refusal text of gate 3 only (mike.md 8) |
| Low | Default; not planned; never steered onto a worker or Warden | [lex:441](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L441) | NARROW | Nothing runs on Low; worker steer refused (gate 4) |
| no-work-above-low | Hold: only Low work is open | [idle_steer:47](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L47) | NARROW | Refusal text of gate 4 only |
| not assigned to harness-gh-user | none-eligible reason (#1598) | [#1336](https://github.com/excaliwire/factory/issues/1336) | NARROW | Refusal text of gate 1: `not assigned to gh_user` |
| Packet | Control plane assembles it from notifications for TPM | [spec:61](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L61) | NARROW | Folded into the board |
| Poke | Wake a seat, no instruction; about work this seat owns | [lex:311](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L311) | NARROW | About its assignment or its pull request |
| Prioritization | Putting a few items at the top | [lex:389](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L389) | NARROW | The act only; the list is the priorities list |
| priority list unreadable | none-eligible reason and steer refusal (#1407) | [#1336](https://github.com/excaliwire/factory/issues/1336) | NARROW | Gate 3 refusal; the reading is unmeasured |
| Program priorities | The page `/dashboard/priorities` | [spec:247](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L247) | NARROW | Priorities tab: edits the list, shows target versus actual share |
| repository-not-allowed | none-eligible reason (#897) | [#1336](https://github.com/excaliwire/factory/issues/1336) | NARROW | Refusal text of gate 2 only |
| Review-idle | Pair an idle reviewer with the oldest `needs_ir` pull request; holds | [README](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md) | NARROW | One reviewer per ready pull request, in parallel; no holds |
| Seat | An agent session the harness manages | [lex:161](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L161) | NARROW | Owns one assignment or nothing |
| Seat cap (`max_seats`) | Worker cap in `seats.yaml`; control seats exempt | [spec:49](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L49) | NARROW | Cap per role; reviewers `ceil(workers / 3)` (decision 3) |
| Send-back | Merge-gate outcome: findings return to the owner | [spec:406](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L406) | NARROW | The author seat's next assignment; nothing held |
| Severity | Urgent, High, Medium, Low, plus steer class and SLA | [lex:413](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L413) | NARROW | Orders work inside a lane; no steer class |
| Sign-in gate | Front door in front of the API: `hgl-auth` or `oauth2-proxy` | [lex:121](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L121) | NARROW | Concept stays; product is config; a human is a verified bearer |
| Standing seat | A seat named in `seats.yaml` | [spec:45](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L45) | NARROW | Decided 2026-10-05: the pool is a cap and a name list; a standing seat is a name in that list (decision 11) |
| Steer | Wake and instruct; the entry restates 3 gates and the loop window | [lex:227](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L227) | NARROW | Next assignment or inside it; never across work |
| Steer record | Record of a steer; in the planner it holds seat and issue | [AGENTS:113](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/AGENTS.md#L113) | NARROW | A record only |
| Steer rules | Config-store steering settings, 11 listed | [lex:367](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L367) | NARROW | Gate and share parameters only; rest is Fleet |
| Stop | Pause a seat, keep its session; auto-steer off | [lex:239](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L239) | NARROW | Human switch; a human or Arthur clears it (mike.md 3.3.8) |
| Unassigned-urgent | Set of unassigned Urgent issues; a Health row | [spec:161](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L161) | NARROW | A board column |
| unmeasured-liveness | Hold: the seat's reading is unmeasured | [idle_steer:55](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L55) | NARROW | Refusal text of gate 7 only |
| Urgent | Blocking; `sev1`; steer class `interrupt` | [lex:423](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L423) | NARROW | Decided 2026-10-05: SEV1 sorts first, never preempts; the `interrupt` steer class retires (decision 14) |
| Vendor | System that runs a seat's session; truth for alive; also the biller | [lex:127](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L127) | NARROW | Who bills a runtime (mike.md 4); what runs it is the runtime |
| `--allow-lower-severity` | Override flag for `higher_unassigned` | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Already removed (#1763) |
| already-assigned | none-eligible reason (#897) | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| Auto-steer | Seat eligibility for loop steering; stop sets it off | [spec:104](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L104) | RETIRE | Stop replaces it |
| awaiting-response | Hold: a seat with a pull request awaiting response is not idle | [idle_steer:42](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L42) | RETIRE | Send-back is the next assignment (mike.md 8) |
| Conflict-steer | Ready conflicting PR steers its owner, or an idle worker | [spec:163](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L163) | RETIRE | Decided 2026-10-05: not a verb; a conflict is a change kind the control plane routes to the author seat (decision 5) |
| Copilot-findings | Copilot threads steer the owner; a busy owner yields to an idle worker | [spec:406](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L406) | RETIRE | Decided 2026-10-05: not a verb; unresolved Copilot threads are a change kind routed to the author seat (decision 5) |
| Harness-state | Git branch that seeds the direction list | [lex:337](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L337) | RETIRE | Config store is the source |
| higher_unassigned | Steer refusal: a higher severity in the lane is unassigned | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Already removed (#1763) |
| Hold | Planner outcome that plans nothing and names why | [spec:159](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | A gate outcome is a refusal |
| Hold streak | Fault holds past a threshold become a Health row | [AGENTS](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/AGENTS.md) | RETIRE | A refusal streak is a log line |
| Host ladder | Lane-PE moves to cheaper hosts at a gauge threshold; one way | [spec:137](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L137) | RETIRE | Vendor budgets replace it (mike.md 4, 8) |
| in-flight:open-pull-request | none-eligible reason (PR #913) | [spec:159](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | Planner reason |
| in-flight:pending-assignment | Hold: a pending create for the seat | [idle_steer:56](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L56) | RETIRE | Planner hold |
| in-flight:steer-record | none-eligible reason (PR #913) | [spec:159](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | Planner reason |
| Lane owner | `policy.lanes` maps a lane label to its owning lane-PE | [lex:181](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L181) | RETIRE | mike.md 8; a lane-PE steers its lane, owns nothing |
| lane-owner-busy | Hold: lane owner busy (never used) | [idle_steer:45](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L45) | RETIRE | Planner hold |
| Lexicon: Clear | Line 2 of the old 4-line review block | [test_1741:17](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/tests/test_comment_limits_1741.py#L17) | RETIRE | Retired by #1741; drift is a blocking finding |
| master-plan (reason) | none-eligible: the issue has sub-issues | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| no-candidate-work | Hold: no open candidate issue | [idle_steer:40](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L40) | RETIRE | Planner hold |
| no-free-seat | none-eligible reason (#1197) | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| no-idle-seat | Hold: no idle seat | [idle_steer:39](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L39) | RETIRE | Planner hold |
| no-lane-label | Hold: issue has no lane label (never shown) | [idle_steer:43](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L43) | RETIRE | Planner hold |
| no-lane-owner | Hold: lane has no owner (never shown) | [idle_steer:44](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L44) | RETIRE | Planner hold |
| no-matching-seat | none-eligible reason (#897) | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| none-eligible | Hold: candidates exist, none eligible; 1 of 12 reasons | [idle_steer:41](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L41) | RETIRE | Planner hold (mike.md 8) |
| Owned work (`owned_work`) | Roles whose steer prepends what the seat name owns | [spec:192](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L192) | RETIRE | A seat owns only its assignment |
| owned-by-live | none-eligible reason: a live seat owns the issue | [spec:159](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | Planner reason |
| owner-unmeasured | none-eligible reason (#1197) | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| Principal SDE | A worker at a capable tier; `psde.md` | [lex:449](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L449) | RETIRE | Seat types allow no per-seat model |
| Program board | Retired 2026-09-16 | [spec:312](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L312) | RETIRE | Already retired |
| Reboot redelivery | Planner redelivers labelled issues after a reboot | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | The remint carries the assignment |
| reboot-redelivery-held | none-eligible reason (#1744) | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Planner reason |
| Redeliver tries | Requeue a queued steer refused at delivery up to N | [spec:86](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L86) | RETIRE | No second queue (mike.md 10.7); unconfirmed delivery says so |
| redelivery-refused | Hold: refused redelivery not replanned in the window | [idle_steer:49](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/idle_steer.py#L49) | RETIRE | Planner hold |
| Resume | Tick verb that resumes stood-down seats | [spec:78](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L78) | RETIRE | With stand-down |
| Rung | One step on the lane-PE host ladder | [lex:67](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L67) | RETIRE | The ladder retires (mike.md 8) |
| Seat-assignments board | Retired dashboard board | [spec:261](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L261) | RETIRE | Already retired; remove references |
| SLA | How soon a severity must move; 0 code readers | [lex:407](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L407) | RETIRE | Decided 2026-10-05: retired for the first cut; 0 code readers; age per severity is a log line first if wanted (Q7) |
| Stand-down | Live-state hold until a gate `name#N` clears | [spec:78](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L78) | RETIRE | Arthur steers "wait for #N" (mike.md 8) |
| Steer class | Per severity: `interrupt`, `elevate`, `feed`, `never` | [seats.yaml:682](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/seats.yaml#L682) | RETIRE | Only `never` acted; severity floor replaces it |
| Steer debt | Planner bookkeeping of refused or 409 steers | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | No planner |
| Taken (in-flight) | Issue taken by open PR, title, steer record, or pending create | [spec:159](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/agent-harness.md#L159) | RETIRE | Assignment is the one source |
| The box | Shared machine at `/home/box` hosting the harness and tmux seats | [lex:53](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L53) | RETIRE | 3 hosts now; name by job: control-plane host, seat host |
| Worker planner | `plan`, `hold_why`, `_feed_key`: picks seat and issue | [#1336](https://github.com/excaliwire/factory/issues/1336) | RETIRE | Arthur decides |

**PROJECT terms (123, not in the table).** The audit's 8 grouped rows hold 90 Excaliwire domain headings and 33 domain bans at [lex:471-1142](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/lexicon.md#L471): factory stages (12), Scabbard (7), quality checks (12), canon (33), presentation (10), originals (14), people and product (2), domain bans (33). They stay in factory's own lexicon and reach Mike only through the factory project's hook, which loads them as that project's Geas scope. Mike keeps the general rule (section 1, rule 10) and the scoped-ban mechanism, not the words. One pattern carries over: Model-call record's "unknown is recorded as unknown, never as zero" is the gauge rule.

**New in Mike, no factory term:** instance, project, share, pool. Board is the NARROW row above; runtime is the RENAME of the harness seat field. Entries are in section 3.

### 2.1 Where the audit and mike.md disagree (mike.md followed)

- Agent harness: audit keeps "harness" for the runtime kind; mike.md 8 renames it runtime.
- Harness-gh-user: audit KEEP; mike.md 8 RENAME to gh_user.
- Rung, Host ladder: audit CHALLENGE; mike.md 8 retires the ladder.
- Reviewer: audit CHALLENGE on the role word; mike.md 2 settles it (role key `reviewer`; Warden is factory's instance name).
- Direction: audit CHALLENGE; mike.md 8 renames it priorities list.
- Board: audit CHALLENGE; mike.md 3.1 defines it.
- Temporary seat: audit CHALLENGE; mike.md 8 keeps it.
- Excaliwire PgM: audit RENAME to Operator; mike.md 2 and 8 say director.
- Vendor: audit moves the billing sense out; mike.md 4 makes billing the whole meaning.
- Harness account: audit KEEP; mike.md 8 drops "harness" from the vocabulary, so it renames.
- Program: audit KEEP; mike.md 1.2 calls the set the instance's project list.
- Tier: audit narrows it to the ladder; mike.md 8 keeps tier and retires the ladder.
- Redeliver tries: audit keeps a transport retry; mike.md 10.7 drops `redeliver_tries`.
- Caller matrix: audit drops the lane-PE own-lane steer; mike.md 9.12 keeps it.
- Stop: audit says only a person clears it; mike.md 3.3.8 lets Arthur undo a Stop.
- Reset defaults: audit one record per seat; mike.md 3.2 one recorded write.
- Low: audit refuses a worker or Warden steer; mike.md 3.3.4 names the worker steer only.
- Gate count: audit counts 7 gates (#1336 section 4); mike.md 3.3 has 10. Gates 1 to 7 number the same; this file cites mike.md.
- Lane-PE, TPM: audit asks whether they go or merge into Arthur; mike.md decisions 12 and 13 recommend keeping both. Still CHALLENGE (section 4), with mike.md's recommendation.
- Not audit versus mike.md: mike.md 3.2 says no mint over liveness "responding or unmeasured", and 3.3.7 says "busy or unmeasured". This file uses 3.2's words; busy is activity, not liveness.

## 3. Mike entries

Factory style: owner link first, what it is, what it is not, then **Binds**. Thresholds and gate lists stay in mike.md (rule 2).

### Mike

Owner: [`mike.md` 1](mike.md#1-what-mike-is). The system: code and tests that run a swarm of AI agent seats on GitHub repositories. It mints seats, steers them, records every decision before it acts, holds the merge gate, and serves one dashboard API. It is not a seat, not a runtime, and not a merger: it has no merge verb. Factory called it the agent harness. **Binds:** gate 10, test `test_no_merge_verb`.

### Instance

Owner: [`mike.md` 1.2](mike.md#12-multi-repository-one-instance). One running Mike: one control plane, one loop, one store, one dashboard, one priorities list, managing a list of projects. There is no Mike deploy per repository. Not a vendor instance (factory's word for one vendor session); Mike says session. **Binds:** test `test_two_projects_one_instance` (mike.md 12).

### Project

Owner: [`mike.md` 1.2](mike.md#12-multi-repository-one-instance). One GitHub repository an instance manages, named `owner/repo` on the instance's project list. Every verb that touches GitHub names its project; a repository not on the list is refused before any call runs. A project's domain words come from its own lexicon through its hook. Factory called the list the program. **Binds:** gate 2, test `test_steer_refuses_repository_not_on_project_list`.

### Runtime

Owner: [`mike.md` 4](mike.md#4-runtimes-and-vendors). What a seat runs on: `cursor-cloud`, `grok-tmux`, `claude-tmux`, `codex-tmux`, `claude-cloud`. Each runtime provides mint, confirmed steer, stop, restart, archive, liveness and usage, or reports `unmeasured` with a reason. Not the vendor, which bills it. Factory carried it as a seat's `harness:` field. **Binds:** the actuator contract test run once per runtime; config key `runtime` (decision 7).

### Vendor

Owner: [`mike.md` 4](mike.md#4-runtimes-and-vendors). Who bills a runtime: Cursor, Anthropic, xAI on factory today. A vendor declares its pools, windows, probe and mint threshold, and mint moves to the next vendor when one crosses its threshold. Not the runtime, and not the source of liveness, which the runtime reports. **Binds:** mint budget refusal, test `test_mint_refuses_on_unmeasured_gauge`.

### gh_user

Owner: [`mike.md` 3.3](mike.md#33-gates-mike-enforces-for-every-caller). The GitHub user, per instance, whose assigned issues and pull requests Mike may steer. Empty or unmeasured refuses every steer. Not a human merger; Mike never writes as the merger. Factory: harness-gh-user. **Binds:** gate 1, refusal text `not assigned to gh_user`.

### Seat

Owner: [`mike.md` 2](mike.md#2-roles). A named agent session Mike manages, with one role. A worker or reviewer seat is in the pool and owns nothing beyond its current assignment: no lane, no issue history, no second label. The director, a session a human opens for himself, and a human-driven engineer session are not seats. **Binds:** caller matrix (anyone not a human or director is a seat or refused).

### Pool

Owner: [`mike.md` 3.1](mike.md#31-pool-assignment-share). The worker and reviewer seats together, each owning only its assignment. Its size is a cap per role in instance config; reviewers are sized from workers (decision 3). Whether its seats are standing names or minted names is Q1. Not the orchestrator seats or lane-PEs. **Binds:** mint refuses past the role cap.

### Assignment

Owner: [`mike.md` 3.1](mike.md#31-pool-assignment-share). The one piece of work a seat is on: idle, or one issue or one pull request. A seat owns nothing beyond it. The `seat:<name>` label is the truth and Mike's store caches it; a remint carries it, a send-back is the author seat's next assignment, and Reset Defaults clears all of them in one recorded write. Not liveness, and not desired state. **Binds:** test `test_remint_carries_assignment`.

### Steer

Owner: [`mike.md` 3.3](mike.md#33-gates-mike-enforces-for-every-caller). Give an idle seat its next assignment, or tell a seat something inside the assignment it already has. A steer never moves a seat to other work while its assignment is open; a remint does that. Delivery is confirmed by a run id, a pane echo, or an event id, or it is not a steer. `steer` refuses what the gates forbid, for every caller, and the refusal is a decision record. **Binds:** gates 1 to 5, test `test_steer_refuses_across_open_work`.

### Board

Owner: [`mike.md` 3.1](mike.md#31-pool-assignment-share). What the arbiter reads: idle seats, each seat's assignment, send-backs with their author seat, ready pull requests per seat, and target versus actual share per priorities row. Mike builds it, and the dashboard shows the same board to a human. Not a dashboard page or tab, and not a GitHub Discussion board. **Binds:** the follow-up prompt carries the board; test `test_follow_up_carries_board`.

### Share

Owner: [`mike.md` 3.1](mike.md#31-pool-assignment-share). The percent of workers a priorities row gets by rank; the config store holds one share per rank and a human sets them. A row with no open non-Low work gives its share to the next row. Target share is config; actual share is the arbiter's judgment, and Health shows both. **Binds:** config-store schema field per rank; Health target-versus-actual row.

### Severity

Owner: [`mike.md` 3.1](mike.md#31-pool-assignment-share). How soon work must move: SEV1 (Urgent), High, Medium, Low, carried by an issue field named in instance config (`Priority` on factory). It orders work inside a lane, oldest first inside a severity. Not a lane, and it has no steer class. **Binds:** gate 4; board sort-order test.

### Low

Owner: [`mike.md` 3.1](mike.md#31-pool-assignment-share). The default severity: an issue with no severity is Low. Nothing runs on Low; a worker steer onto it is refused at the severity floor. Not "not planned": there is no planner. **Binds:** gate 4, refusal text `severity floor: Low is never steered`; factory's pin `test_lane_rows_1407.py:376` moves from "not planned" to "Nothing runs on Low".

### Lane

Owner: [`mike.md` 3.1](mike.md#31-pool-assignment-share). A work domain named by a repository label; a priorities row names a lane, which is how a lane gets workers. A lane has no owner and binds no seat. A lane-PE steers in its lane through the caller matrix, not by owning it. **Binds:** gate 3, refusal text `lane-starved`.

### Priorities list

Owner: [`mike.md` 3.1](mike.md#31-pool-assignment-share). What a human decided about prioritization: an ordered list of at most 3 rows, each naming a lane and carrying an optional note, in the config store. A row's rank sets its share of workers; a lane not on the list gets no worker. The note is a human's intent in a sentence: it goes on the board and into every steer to that lane's lane-PE, and binds nothing. Not the GitHub Priority field, which is severity. Fields: `lane`, `note`. Factory called it direction. **Binds:** gate 3; the API's `direction` command renames at the next major (decision 8); factory pin `test_direction.py` moves.

### Arbiter

Owner: [`mike.md` 2](mike.md#2-roles). The role of the seat that reads the board and decides who does what: which seat takes which issue, the share each priorities row actually gets, when to remint, the order of send-backs, and recovery after a reboot. It acts only through Mike's verbs, and the gates bind it like any caller. It is judgment, not the control plane, which is code. One per instance; the name is the role key unless the instance overrides it; Arthur on factory. **Binds:** caller matrix `arbiter`; gates 1 to 5.

### Steer rules

Owner: [`mike.md` 5](mike.md#5-the-control-plane). The config-store settings that parameterize the gates and the shares: the share per rank, the loop window, the reviewer ratio, the per-role seat caps, and the orchestrator cooldown. A rule the store does not hold reads `unmeasured`. Fill-missing cap, paste limits, poke stale window, main-restart lists and read-budget reserve are Fleet settings, not steer rules. **Binds:** config-store schema; test that an absent rule reads `unmeasured`.

### Mint

Owner: [`mike.md` 3.2](mike.md#32-mint-remint-steer). Create a seat on a runtime. A mint is wait-only for every role, lane-PEs included: the seat reads its brief and stops at "Wait for the first steer". A mint run has a token and turn budget and writes a decision record. Mike mints no seat over one whose liveness is responding or unmeasured. **Binds:** gate 7; test `test_mint_prompt_is_wait_only` for every role.

### Remint

Owner: [`mike.md` 3.2](mike.md#32-mint-remint-steer). Replace a seat's session and carry its assignment: the first steer after a remint is the same work. It is the only way a seat leaves context; a steer never moves a seat across open work. Not a mint of a new name. **Binds:** test `test_remint_carries_assignment`; one decision record per remint.

### Liveness

Owner: [`mike.md` 4](mike.md#4-runtimes-and-vendors). Whether a seat's session answers: `not-minted`, `responding`, `not-responding`, or `unmeasured` with a reason, the same 4 words for every runtime. Busy and idle are activity, not liveness, and liveness is not assignment. **Binds:** schema refuses a fifth value; Sessions row verbs.

### Decision record

Owner: [`mike.md` 5](mike.md#5-the-control-plane). Who saw what, decided what, why, and the outcome (pending, applied, refused, cancelled), with actor and caller, written before the side effect. Every verb writes one, mint, archive, restart and kill included; a refusal is a record with its why. **Binds:** gate 6; `apply` refuses an unrecorded decision.

### Send-back

Owner: [`mike.md` 3.4](mike.md#34-review-and-send-back). A `Send back` review verdict on a head: the pull request returns to draft and the author's seat gets it as its next assignment. Nothing else is held, and a ready pull request does not hold its author. Not an awaiting-response hold. **Binds:** `draft-sent-back`; test `test_send_back_is_author_next_assignment`.

### Gauge

Owner: [`mike.md` 4](mike.md#4-runtimes-and-vendors). A measured reading of one budget: a vendor pool percent, a window, tokens since mint, context pressure. No probe means `unmeasured`, never 0, and a mint that depends on an unmeasured gauge is refused. A gauge source is how a reading is taken (factory: meter); the gauge list is config. **Binds:** mint budget refusal; test that an unprobed gauge reads `unmeasured`.

### Tick

Owner: [`mike.md` 5](mike.md#5-the-control-plane). One pass of the control loop: read desired state, read live state, decide, act. A tick does not overlap the previous one. The loop is the process that is Running or Paused; a tick is one pass of it. Factory: retarget-loop. **Binds:** loop lock test (no overlap); one heartbeat per tick.

### Control plane

Owner: [`mike.md` 5](mike.md#5-the-control-plane). Mike's code: it holds desired state, reads live state, acts on the difference, and refuses what the gates forbid. It holds no inbound path and no SSH key to a seat host. Not a seat: the arbiter is judgment, the control plane is mechanism. It runs on the control-plane host (factory: droplet). **Binds:** gates 1 to 10.

### Seat host

Owner: [`mike.md` 4](mike.md#4-runtimes-and-vendors). The agent on a machine that runs tmux seats: it checks in, pulls its own actuations from the control-plane store with a host token, runs them, and reports results. A stale seat host makes its seats `unmeasured`. Not the control-plane host, and it holds no shared master secret and no second, machine-local queue. **Binds:** test that a host token pulls only its own actuations.

### Attached session

Owner: [`mike.md` 2.2](mike.md#22-attached-sessions-non-seats-that-act-through-mike). A session a human drives (Infra Fable, Factory Fable, the director) that holds a session token and acts through Mike's verbs for every repository and Mike interaction. Not a seat: never minted, steered, assigned, or counted against the cap. Recorded as its own actor; writes under Mike's account with its `[Name]` prefix; bound by every gate; rights per its config row. Attaching is optional. Word confirmed by a human 2026-10-05 (Q14). **Binds:** caller matrix `attached`; test that a session token cannot mint and cannot act as a human.

### Humans

Owner: [`mike.md` 2.1](mike.md#21-humans). The people Mike serves, listed in instance config by GitHub login. Any listed human may merge, waive a gate, grant a reviewer, issue a session token, and edit the priorities list and the config store; the record names which one. A human is a verified bearer, never a header. Not a seat, not the director, and not one person: Tig is factory's config. **Binds:** caller matrix `human`; test that a seat token and a session token cannot act as a human.

### Director

Owner: [`mike.md` 2](mike.md#2-roles). The attached session a human uses as his portal (Excaliwire PgM on factory). It is not a seat and holds no assignment; the caller matrix knows it by name beside a human. Authority runs human, director, TPM, lane-PE, then worker or reviewer. Not a human: only a human merges, waives a gate, or grants a reviewer. **Binds:** caller matrix `director`; test that a seat token cannot act as the director.

## 4. Questions for a human

Each CHALLENGE row, plus the mike.md section 11 decisions this file depends on. Recommendations match mike.md 11. A decided question says so.

1. **Standing names or pool slots?** (Standing seat, Fill-missing, Seat cap.) Factory has 13 standing rows; 100 workers would be 100 `seats.yaml` rows.
    Decided, Tig, 2026-10-05: pool, a cap plus a name list (decision 11).
2. **Does the lane-PE role exist in Mike?** (Lane-PE, PE seat.) A mint that was not wait-only read 4.2M and 5.0M tokens in 30 minutes (#1755).
    Decided, Tig, 2026-10-05: keep the role; Mike may mint it behind a human-confirmed setting; wait-only; no ladder (decision 12).
3. **Two orchestrator seats, or TPM merged into Arthur?** (Orchestrator seat, TPM.) Classification and "who should own this" overlap the arbiter's judgment.
    Decided, Tig, 2026-10-05: keep two; measure K for a week, then decide (decision 13).
4. **Does SEV1 (Urgent) preempt an open assignment?** (Urgent.) Its steer class `interrupt` is reported, never acted on.
    Decided, Tig, 2026-10-05: sorts first, never preempts; a human may Stop a seat by hand (decision 14).
5. **Priorities list form: lanes or free text, per instance or per project?** (Priorities list, Lane.) Free text drops the lane gate.
    Decided, Tig, 2026-10-05: a lane plus an optional note shared with the lane-PE as context (decision 2). Per instance or per project is still decision 6.
6. **Which word names a human?** (Tig.) "Tig", "operator" and "director" are all in use; mike.md writes "a human".
    Decided, Tig, 2026-10-05: humans, plural. The system holds a list of humans in instance config; text says a human or humans; the name is config (mike.md 2.1).
7. **SLA: measure or drop?** (SLA.) 0 code readers today; prose and `seats.yaml` only.
    Decided, Tig, 2026-10-05: retire for the first cut.
8. **Conflict-steer: keep?** (Conflict-steer.) "Or an idle worker" steers a non-author across work.
    Decided by decision 1, 2026-10-05: not a verb; a change kind the control plane routes to the author seat.
9. **Copilot-findings: keep?** (Copilot-findings.) A busy owner yields to an idle worker, the same cross-work steer.
    Decided by decision 1, 2026-10-05: same as Q8.
10. **Rename the seat field `harness` to `runtime`?** (harness seat field.)
    Decided, Tig, 2026-10-05: yes (decision 7).
11. **Replace `direction` everywhere, the API command included?** (Direction.)
    Decided, Tig, 2026-10-05: yes, at the major bump #1 already needs (decision 8).
12. **Accept the new words this file proposes beyond mike.md 8:** activity (Live map), vendor account (Harness account), project list (Program)?
    Recommend: accept; each lands with its schema in one change (rule 8).
13. **Retire stand-down, resume, the hold words, the host ladder, rung, and retarget?**
    Decided, Tig, 2026-10-05: yes (decision 15). The RETIRE rows for them in section 2 are closed.
14. **The word for a non-seat session that acts through Mike?** (Attached session, new.) Factory says only "not a seat"; Tig asked for the capability on 2026-10-05.
    Decided, Tig, 2026-10-05: attached session; the director is one; default rights issue and pull verbs like a seat, steer like a lane-PE, no mint (decision 16).
