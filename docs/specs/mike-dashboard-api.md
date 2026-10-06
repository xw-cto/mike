# Mike dashboard API

**Status:** draft for Tig's edit, written before the code. This file is the contract between Mike's control plane and every dashboard client. It defines version `1.0.0` of Mike's API.

**Starting point.** [Factory's dashboard API at commit bb2bf4c6, the starting point](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/docs/specs/dashboard-api.md) was the starting point for this file and is not referenced as law. A reader needs nothing from factory to read or implement it.

**Companion files.** [`mike.md`, the spec](mike.md) defines the domain: [humans](mike.md#21-humans), [attached sessions](mike.md#22-attached-sessions-non-seats-that-act-through-mike), [the seat model](mike.md#3-the-seat-model), [runtimes and gauges](mike.md#4-runtimes), [the control plane](mike.md#5-the-control-plane), and [the dashboard spec](mike-dashboard.md). The dashboard and UI stories and the stories the spec requires, [indexed by job in the user stories](stories/README.md), are the acceptance tests the client and this contract answer to.

Routes below are written relative to `{base}`, the instance's configured base path.

## 1. Two processes

- The **control plane** serves the API (`{base}/api/...`) and the stream (`{base}/events`). It does not serve the page. A GET of any other path under `{base}` answers 404 with `the dashboard app serves this page`.
- The **dashboard app** serves the page and its static files under `{base}`. It holds no state, no token store, and no route to GitHub or a vendor.
- Both sit behind the instance's gate (a reverse proxy that terminates TLS). The gate splits `{base}/api` and `{base}/events` to the control plane and everything else to the app.
- Base path, the API origin, allowed origins, and both listen ports are instance config. Each process binds to loopback unless config says otherwise.
- Neither process is public. The gate is the only listener on a public interface.
- The page may be served from another origin than the API. It then reads the API origin from its own config file. An API origin must be https, except loopback.

## 2. Identity

Four callers exist. Each carries its own token as `Authorization: Bearer <token>` on every call, the stream included. A token never rides in a URL.

| Caller | Token | Verified how | Acts as |
|---|---|---|---|
| `human` | bearer from the instance's identity provider | signature against the provider's published keys; `iss`, `aud`, `exp`, `nbf`; login on the instance's humans list ([humans](mike.md#21-humans)) | that human |
| `session` | session token, issued by a human ([attached sessions](mike.md#22-attached-sessions-non-seats-that-act-through-mike)) | lookup of its hash in the store; not revoked | that attached session, with the verbs its row lists |
| `seat` | seat token, issued at mint | lookup of its hash; names one seat | that seat only ([MS-152, seat tokens act only as self](stories/operate.md#ms-152-seat-tokens-act-only-as-self)) |
| `host` | host token, one per seat host | lookup of its hash; names one host | that host only |

- Each route declares which callers it accepts. The tables in [section 5](#5-reads) and [section 6](#6-commands) are that declaration, and the server's route table is generated from the same source.
- No header names a caller. An email header, a forwarded-user header, or a query parameter is ignored for identity ([MS-154, humans are verified bearers](stories/operate.md#ms-154-humans-are-verified-bearers)).
- No token or a token that fails verification: 401, body `{error}`. A human-only route refuses a session, seat, or host token with 403.
- A verified caller the caller matrix refuses: 403, body `{error, record_id}`. The matrix is [the gates](mike.md#33-gates-mike-enforces-for-every-caller) plus the role rows in instance config.
- Every refusal, 401 and 403 included, writes a decision record with caller kind, the token's subject when one was read, route, and why. A 401 record holds no token text.
- A host token reaches only `version` and `health` on this contract. Check-in and claim belong to the seat-host protocol, not to this file.
- **CORS.** The control plane answers a cross-origin call only from an origin in config. It names that origin, never `*`, and varies on `Origin`. A preflight from any other origin is 403. A POST whose `Origin` is present and not an allowed origin is 403 before it runs. A POST with no `Origin` (the CLI, a seat) is not checked for origin. The webhook route gets no CORS header.
- The page renews a human bearer without the human where the provider allows it, and says so ([MS-067, sign-in renews silently](stories/operate.md#ms-067-microsoft-sign-in-renews-silently)). The identity provider, its tenant, client id and scope are instance config.

## 3. Version

- `GET {base}/api/version` answers `versionFrame`. The version is semantic: `major.minor.patch`. A human writes it.
- An added field, part, route, or enum value a client may ignore is a minor bump. An old client ignores a field it does not know.
- A removed or renamed field, a changed meaning, a changed type, or a changed event name is a major bump.
- A wording change in a description is a patch bump.
- A client reads the version before it opens the stream, and again from every frame. On a major it was not built for it stops and says it must be updated. It draws no half-compatible page.
- The contract's machine form (a schema file generated from [section 7](#7-payload-shapes)) carries a digest. A test fails on any edit of that file whose digest is not recorded beside a new version.

## 4. The stream

`GET {base}/events` is one server-sent event stream. It is one-way: a client never publishes on it. Callers: `human`, `session`, `seat`.

- A new connection receives one frame of each part, in this order: `version`, `health`, `seats`, `board`, `priorities`, `review`, `gauges`, `settings`, `attached-sessions`, `logs`, `jobs`. A part the caller may not read is omitted, and the `version` frame lists the parts this stream will carry.
- After the opening frames the control plane sends a frame for a part only when that part changes. A write to one part sends no other part.
- The SSE event name is the part name. Every frame carries `version`, `part`, and `written_at`, the time the part was last written.
- A part the loop has not written arrives as a frame with `state` `absent` and no rows. A part that cannot be read arrives with `state` `unmeasured` and a `reason`. The client says which; it never draws ok or 0 for either.
- `seats`, `board`, `review`, `gauges`, `attached-sessions` and `jobs` frames carry the whole part. `logs` frames carry only the new lines since the last frame, oldest first.
- An idle stream writes the comment `: keep-alive` every `api.keepalive_seconds` (config, default 15). The client draws nothing for it.
- A client drops a stream with no bytes for three keep-alive intervals and opens a new one. It also reopens when its tab becomes visible again. A reopen receives every opening frame, so a reopen is a full read ([MS-055, live stream recovers itself](stories/diagnose.md#ms-055-live-stream-recovers-itself)).
- The open's status decides the client's next step: 200 reads on, 401 asks for sign-in, 403 says the caller is refused, anything else retries every 3 seconds. 401 and 403 are not retried ([MS-054, four distinct connection failures](stories/diagnose.md#ms-054-four-distinct-connection-failures)).
- At each keep-alive the control plane compares the health snapshot's age with the loop window. When the loop has stopped writing, it sends one `health` frame with `stale` true and the attention item `health snapshot stale`, once per stale period. A log frame in the same pass does not suppress it ([MS-056, health from the tick snapshot](stories/diagnose.md#ms-056-health-from-the-tick-snapshot)).
- A store change reaches an open stream in under 2 seconds ([MS-006, page updates by itself](stories/observe.md#ms-006-page-updates-by-itself)).
- Open streams are capped per caller by config. An open over the cap answers 429.
- There is no message broker. A client that cannot hold a stream polls the reads.

## 5. Reads

Every read answers JSON, the payload named. The `Callers` column is the route's declaration. `own` means a session or seat sees only rows it is the actor of.

| Route | Payload | Serves | Callers |
|---|---|---|---|
| `GET {base}/api/version` | `versionFrame` | API version, parts, served commit | all four |
| `GET {base}/api/health` | `health` | the loop's last snapshot | all four |
| `GET {base}/api/seats` | `seatsFrame` | one `seatRow` per seat ([MS-001, one table of every seat](stories/observe.md#ms-001-one-table-of-every-seat)) | human, session, seat |
| `GET {base}/api/seats/{seat}` | `seatDetail` | that seat's row, its records, pending steer, vendor link ([MS-007, seat page for diagnosis](stories/observe.md#ms-007-seat-page-for-diagnosis)) | human, session, seat |
| `GET {base}/api/seats/{seat}/log` | `sessionLog` | the runtime's session log: inputs and responses, last steer, latest response ([MS-172, session log from every runtime](stories/seats.md#ms-172-session-log-from-every-runtime)) | human, session, seat (`own` seat) |
| `GET {base}/api/board` | `boardFrame` | the board Arthur read on his last follow-up ([MS-132, board Arthur read is shown](stories/observe.md#ms-132-board-arthur-read-is-shown)) | human, session, seat |
| `GET {base}/api/priorities` | `prioritiesFrame` | the priorities list, one `priorityRow` per lane | human, session, seat |
| `GET {base}/api/review` | `reviewFrame` | open ready pull requests across all projects ([MS-128, review surface lists ready pulls](stories/review.md#ms-128-review-surface-lists-ready-pulls)) | human, session, seat |
| `GET {base}/api/gauges` | `gaugesFrame` | one `gaugeRow` per runtime pool and window | human, session, seat |
| `GET {base}/api/settings` | `settingsFrame` | every setting, secrets by name only | human, session |
| `GET {base}/api/settings/history` | `settingsHistory` | every version, key, from, to, actor ([MS-061, settings history by version](stories/diagnose.md#ms-061-settings-history-by-version)) | human |
| `GET {base}/api/attached-sessions` | `attachedSessionsFrame` | one `attachedSessionRow` per token, never the token | human |
| `GET {base}/api/jobs` | `jobsFrame` | recent jobs, newest first; `?job=<id>` for one | human; session, seat `own` |
| `GET {base}/api/logs` | `logsFrame` | log lines, filtered | human, session, seat |

`logs` filters, all optional: `level` (this level and above), `component` (comma list), `seat`, `project`, `command`, `text` (substring), `since` (ISO 8601 with offset: every match back to that time, no scan budget), `limit` (1 to 2000, default 200). The client keeps these in its URL ([MS-058, filterable log in the URL](stories/diagnose.md#ms-058-filterable-log-in-the-url)) and rereads a `since` view at most every 30 seconds, one read in flight ([MS-059, since view reads whole window](stories/diagnose.md#ms-059-since-view-reads-whole-window)).

Rules for every read:

- A read makes no vendor call, no GitHub call, and no subprocess. It serves what the loop and the store last wrote. A test proves it for every route.
- A read writes nothing except, for a refusal, its decision record.
- A read with a seat or session token answers the same rows, byte for byte, as the page draws ([MS-008, Arthur reads the same API](stories/observe.md#ms-008-arthur-reads-the-same-api), [MS-161, attached sessions read the board](stories/operate.md#ms-161-attached-sessions-read-the-board)).
- An absent part is `state` `absent`; the client says so. Unmeasured is `null` with a reason, never 0.
- The session log read serves what the seat host or the cloud runtime last delivered to the store. A runtime that cannot read its log answers `unmeasured` with a reason.

## 6. Commands

A command is a POST with a JSON body. Every command answers 202 at once with `{job_id, record_id, state: "pending"}`. The record is written before the 202. The outcome arrives on the `jobs` frame and on `GET {base}/api/jobs?job=<id>`, as `applied`, `refused` or `cancelled`, with `why` and `actor` ([MS-137, job ids for every command](stories/diagnose.md#ms-137-job-ids-for-every-command), [MS-060, every command recorded with identity](stories/diagnose.md#ms-060-every-command-recorded-with-identity)).

| Route | Body | Who may |
|---|---|---|
| `POST {base}/api/fleet-mode` | `{mode, confirm}`; `mode` one of `hard-reboot`, `orchestrator-reboot`, `worker-reboot`, `fill-missing`, `restart-control-plane`, `reset-defaults`; `confirm` equals `mode` | human |
| `POST {base}/api/seat-verb` | `{verb, seats, prompt?, assignment?, confirm?}`; `verb` one of `mint`, `steer`, `stop`, `restart`, `archive`; `seats` one or more names; `assignment` is `owner/repo#N` or `idle` (steer only); `confirm` equals `verb` for `restart` and `archive` | human; seat per the caller matrix; session when its row lists the verb |
| `POST {base}/api/priorities` | exactly one of `{order}` (every lane key, new order) or `{lane, note}` (note text, empty clears) | human |
| `POST {base}/api/settings` | `{key, value, expected_version, confirm?}`; `confirm` equals `key` for keys config marks confirm-first | human |
| `POST {base}/api/attached-sessions` | `{action: "issue", name, verbs}` or `{action: "revoke", name, confirm}` | human |
| `POST {base}/api/issue` | `{project, number, urgency?, lane?}`; `urgency` one of `critical`, `high`, `normal`, `no`; `lane` a configured lane key | human; session when its row lists `issue`; seat per the caller matrix |

- **Fleet mode.** One fleet mode runs at a time. A second fleet mode, or a seat verb on a seat a running fleet mode will touch, answers 409 with the running job's id and writes a refused record ([MS-065, fleet commands never collide](stories/operate.md#ms-065-fleet-commands-never-collide)). `reset-defaults` clears every assignment and every `seat:` label in one recorded write ([mint, remint, steer](mike.md#32-mint-remint-steer)). `restart-control-plane` persists its job; the outcome is on the first `jobs` frame after the reconnect.
- **Seat verb.** One job covers every named seat; the job's `seats` list carries one outcome per seat. A verb fits a seat only when that seat's `seatRow.verbs` lists it. The server refuses a verb that does not fit, with a record, even when a client sends it ([MS-028, verbs offered by the control plane](stories/seats.md#ms-028-verbs-offered-by-the-control-plane)). A steer with `prompt` and `assignment` both empty is 400. With an assignment, `Assignment: <work>` leads the delivered prompt on its own line. A steer's outcome names `confirmed` with the runtime's delivery id or `not confirmed` with a reason. A steer passes every [gate](mike.md#33-gates-mike-enforces-for-every-caller) or is refused naming the gate.
- **Priorities.** Rows come from the lanes in instance config: one row per lane. A body that adds, deletes, or omits a lane is 400 and names the lanes config ([MS-015, edit the priorities list](stories/steer.md#ms-015-edit-the-priorities-list), [MS-016, rows follow configured lanes](stories/steer.md#ms-016-rows-follow-configured-lanes)). Each accepted edit is one config-store version.
- **Settings.** Loop Running or Paused, live or dry-run, and loop cadence are setting keys. The server validates the value against the one settings schema the page also reads. A value that fails is 400 with `<key> must be <type>` and writes no version ([MS-039, schema check before save](stories/configure.md#ms-039-schema-check-before-save)). An `expected_version` that is not the current version is 409. A write of the value already stored is applied with why `already <value>`. A secret key takes a secret name, never a secret value.
- **Attached-session token.** `issue` is the one answer that carries a secret: the 202 body adds `token`, once. The token is never on a frame, a read, a record, or a log line. `revoke` takes effect on the token's next call, which is 401 with a record ([MS-159, revocable attached session tokens](stories/operate.md#ms-159-revocable-attached-session-tokens)).
- **Issue.** Sets the `urgency:<level>` label or the lane label on one issue in a listed project, through Mike's issue verb and its GitHub choke point. An unlisted project is refused with 0 GitHub calls.
- **No merge command exists.** A test fails if a route or verb named merge is added ([gate 10, no merge verb](mike.md#33-gates-mike-enforces-for-every-caller)).
- A body that fails the schema is 400 with `error` and a record. A 401 or 403 answers before a job exists; both still write a record.

## 7. Payload shapes

Every time is ISO 8601 with offset, or `null` when not recorded. Durations are whole seconds. Unmeasured is `null` plus a `reason`, never 0. Liveness words are exactly `not-minted`, `responding`, `not-responding`, `unmeasured`. Urgency values are exactly `critical`, `high`, `normal`, `no`. Every frame also carries the envelope `version`, `part`, `written_at`, `state` (`ok`, `absent`, `unmeasured`), `reason`.

**versionFrame**

| Field | Type | Meaning |
|---|---|---|
| `version` | string | `major.minor.patch` |
| `parts` | string list | parts this stream carries for this caller |
| `commit` | string | commit the control plane serves |
| `started_at` | time | when the control plane process started |

**health**

| Field | Type | Meaning |
|---|---|---|
| `snapshot_at` | time | when the loop wrote the snapshot; the client counts ages from it ([MS-044, health first with snapshot age](stories/diagnose.md#ms-044-health-first-with-snapshot-age)) |
| `stale` | bool | true when `snapshot_at` is older than the loop window |
| `loop` | object | `state` `Running` or `Paused`, `mode` `live` or `dry-run`, `paused_by`, `paused_why`, `last_tick_at`, `cadence_seconds` |
| `attention` | list | groups, worst first: `not-ok` then `unmeasured`; each `{kind, severity, count, items}`, each item `{text, seat?, project?, url?}` ([MS-045, needs attention groups faults](stories/diagnose.md#ms-045-needs-attention-groups-faults)) |
| `hosts` | list | `{name, last_checkin_at, state, seats, note}` per seat host that runs a seat or was ever checked in ([MS-048, hosts table shows host health](stories/diagnose.md#ms-048-hosts-table-shows-host-health)) |
| `process` | object | control plane `commit`, `branch`, `started_at` |
| `tree` | object | loop checkout `commit`, `behind` count or `null` with `reason` ([MS-049, served commit and checkout lag](stories/diagnose.md#ms-049-served-commit-and-checkout-lag)) |

**seatRow**, one per seat, ordered arbiter, tpm, lane-pe, worker, reviewer, then name.

| Field | Type | Meaning |
|---|---|---|
| `seat` | string | stable seat name |
| `role` | string | role key |
| `role_name` | string | display name from instance config, else the role key |
| `runtime` | string | runtime driver name |
| `vendor` | string | who bills the runtime |
| `access` | string | `cloud` or `tmux` |
| `host` | string | seat host name, or `cloud` |
| `liveness` | string | one of the four words ([MS-002, liveness in four words](stories/observe.md#ms-002-liveness-in-four-words)) |
| `liveness_reason` | string | required for `not-responding` and `unmeasured` |
| `liveness_source` | string | where the word came from, such as a vendor read or a host check-in |
| `session_url` | string or null | link to the live vendor session |
| `assignment` | object or null | `{project, number, kind (issue or pull), url, title}` from the `seat:` label; null is idle |
| `last_completed` | object or null | same shape, the last item that closed under this seat ([MS-175, board shows last completed assignment](stories/observe.md#ms-175-board-shows-last-completed-assignment)) |
| `last_steer` | object or null | `{prompt, at, actor, delivery: confirmed or not-confirmed, delivery_id, reason}` |
| `queued_steer` | object or null | the one pending steer: `{prompt, at, actor, why_pending}` ([MS-013, pending steer shown apart](stories/steer.md#ms-013-pending-steer-shown-apart)) |
| `stopped` | bool | the human Stop switch |
| `tokens` | object | since mint: `{input, output, cache_write, cache_read, total, read_at, reason}`; counts `null` when unmeasured ([MS-068, tokens per seat and fleet](stories/operate.md#ms-068-tokens-per-seat-and-fleet)) |
| `context` | object | `{used, window, percent, summarized, read_at, reason}`; `null` counts when unmeasured ([MS-069, context fullness per seat](stories/operate.md#ms-069-context-fullness-per-seat)) |
| `verbs` | string list | the seat verbs that fit this seat now; the client enables a verb only when every selected row lists it |
| `verb_why` | object | verb to the server's one-line text for its button, for all five verbs ([MS-027, verb buttons explain themselves](stories/seats.md#ms-027-verb-buttons-explain-themselves)) |
| `minted` | time or null | last mint; null with `reason` `never minted` or `unmeasured` |

**seatDetail** is the `seatRow` plus `records` (the seat's last 50 decision records) and `pending_job` (job id or null). **sessionLog** is `{state, reason, entries, last_steer, latest_response}`; each entry `{at, kind (input or response), text, latest}`.

**boardFrame**, the board as Arthur read it ([MS-131, Arthur reads the board](stories/observe.md#ms-131-arthur-reads-the-board)).

| Field | Type | Meaning |
|---|---|---|
| `follow_up_record` | string | the record id of the follow-up that carried this board |
| `idle_seats` | list | `{seat, role, last_completed}` |
| `assignments` | list | `{seat, project, number, kind, urgency, lane, since}` |
| `send_backs` | list | `{project, number, owner_seat, reviewer, at}` |
| `ready_pulls` | list | `{seat, pulls}`, ready pull requests per owner seat |
| `lanes` | list | `priorityRow` per lane, rank order |

**priorityRow** ([MS-136, target versus actual share](stories/observe.md#ms-136-target-versus-actual-share))

| Field | Type | Meaning |
|---|---|---|
| `lane` | string | lane key from config |
| `rank` | integer | 1 is top |
| `note` | string or null | a human's intent for the row |
| `target_share` | number | percent of workers by rule or override ([pool, assignment, share](mike.md#31-pool-assignment-share)) |
| `actual_share` | number or null | percent of assigned workers from labels; null with reason when labels were not read |

`prioritiesFrame` is `{rows, lanes_source, store_version}`.

**reviewRow**, ordered by urgency then `ready_since`, oldest first ([MS-129, review surface by urgency then age](stories/review.md#ms-129-review-surface-by-urgency-then-age)).

| Field | Type | Meaning |
|---|---|---|
| `pull` | object | `{project, number, url, title, head_sha}` |
| `project` | string | `owner/repo` |
| `urgency` | string | one of the four values |
| `ready_since` | time | when it went ready, from GitHub events |
| `reviewer` | string or null | seat, session, or human holding it; null is none |
| `verdict` | string | `Merge`, `Send back`, `Hold`, or `pending`, for `head_sha` |
| `send_back_owner` | string or null | owner seat on a send-back, with its next-assignment state |
| `conflict` | bool | the pull request conflicts with its base |

**gaugeRow** ([gauges](mike.md#4-runtimes), [MS-146, no mint on unmeasured gauge](stories/seats.md#ms-146-no-mint-on-unmeasured-gauge))

| Field | Type | Meaning |
|---|---|---|
| `runtime` | string | runtime driver |
| `vendor` | string | who bills it |
| `pool` | string | pool name from config |
| `window` | string | window name, such as `5h` |
| `percent_used` | number or null | null when unmeasured |
| `reason` | string | why unmeasured; empty otherwise |
| `mint_threshold` | number | percent at which mint picks the next vendor |
| `read_at` | time or null | when the gauge source was read |

**settingRow** ([MS-038, settings show source and actor](stories/configure.md#ms-038-settings-show-source-and-actor))

| Field | Type | Meaning |
|---|---|---|
| `key` | string | store key |
| `value` | any | value Mike reads now; a secret holds its name |
| `source` | string | `default`, `instance`, `store`, or `unmeasured` |
| `changed_by` | string or null | actor of the last change |
| `changed_at` | time or null | when |
| `version` | integer | store version that wrote it |

`settingsFrame` is `{store_version, rows, schema_digest}`.

**attachedSessionRow** ([MS-163, attached sessions listed apart](stories/operate.md#ms-163-attached-sessions-listed-apart))

| Field | Type | Meaning |
|---|---|---|
| `name` | string | the session's `[Name]` |
| `verbs` | list | verbs the token may run |
| `issued_at` | time | when |
| `issued_by` | string | the human who issued it |
| `last_call_at` | time or null | null before the first call |
| `revoked_at` | time or null | null while live |

**jobRow**

| Field | Type | Meaning |
|---|---|---|
| `job_id` | string | id returned with the 202 |
| `command` | string | route and verb or mode |
| `actor` | string | human login, session name, or seat |
| `caller` | string | `human`, `session`, `seat`, or `host` |
| `state` | string | `pending`, `applied`, `refused`, `cancelled` |
| `why` | string | one line for the human |
| `seats` | list | per-seat `{seat, state, why}` for a seat verb |
| `started_at` | time | when accepted |
| `finished_at` | time or null | null while pending |
| `record_id` | string | the decision record |

**logLine**, secrets redacted.

| Field | Type | Meaning |
|---|---|---|
| `at` | time | when |
| `level` | string | `debug`, `info`, `warning`, `error`, `critical` |
| `component` | string | Mike component that wrote it |
| `seat` | string or null | seat it concerns |
| `project` | string or null | project it concerns |
| `command` | string or null | job command it belongs to |
| `event` | string | stable event name |
| `fields` | object | named values |

## 8. What changed from the starting point

| Factory shape | Mike shape | Why |
|---|---|---|
| settings event outside the written contract | `settings` part, read, and command in the contract | a part a client relies on is versioned |
| `direction` command and list | `priorities` command; reorder and note only | one row per lane ([decision 8, priorities replace direction](mike.md#11-decisions)) |
| GitHub Priority field (Urgent, High, Medium, Low) | `urgency:<level>` label, four values | a label is settable from the GitHub mobile app |
| synchronous command result, 30-second wait | 202 with job id; outcome on `jobs` | a slow answer still lands ([MS-029, commands shown as notifications](stories/seats.md#ms-029-commands-shown-as-notifications)) |
| human time strings (`minted`, ages) | ISO 8601 with offset everywhere | the client parses no prose ([MS-138, ISO 8601 times on the wire](stories/diagnose.md#ms-138-iso-8601-times-on-the-wire)) |
| `X-HGL-Email` header, `?token=` query | verified bearer for every caller | a header any process can set is not identity |
| health `boards` and per-defect detector fields | dropped; findings are `attention` items | one shape for every finding |
| `droplet` joined not-ok string | dropped; `attention` groups | one reader, one source |
| `harness`, `surface`, `state`, `watch` on a row | `runtime`, `vendor`, `access`, `liveness_source` | [runtimes](mike.md#4-runtimes) |
| `verbs` list plus hover text the client derived | `verbs` list plus server `verb_why` | the server explains; the client derives nothing |
| `sessions` part, `sessionRow`, `/sessions` routes | `seats` part, `seatRow`, `/seats` routes | the row is a seat; a session is what the runtime holds for it ([the Seats tab](mike-dashboard.md#3-the-seats-tab-and-the-seat-card)) |
| none | `board`, `review`, `gauges` per runtime, `attached-sessions`, `jobs`, session log | parts [the dashboard spec](mike-dashboard.md) requires |
| terminal ticket and WebSocket messages | **deferred** | see below |

Terminal control ([MS-057, watch and drive a tmux pane](stories/diagnose.md#ms-057-watch-and-drive-a-tmux-pane)) is deferred to its own contract. It is served by the seat host, not the control plane, it is tmux-only, and it is a two-way WebSocket, which this one-way contract does not carry. Version `1.0.0` holds no terminal field. Adding a terminal URL and control holder to `seatRow` later is a minor bump.

## 9. Where this is tested

The contract tests ship with Mike and run in CI. Each names a story or a section. They run the API server in-process against a fixture store with the fake runtime, with no control plane loop, no vendor and no GitHub ([mike.md §12, how Mike is tested](mike.md#12-how-mike-is-tested), tier 4).

- **Version gate.** A schema edit without a recorded digest and a new version fails ([section 3](#3-version)).
- **Opening frames.** Every opening frame, for each caller kind, validates against its shape, absent and unmeasured parts included.
- **Pushed frames.** A write to each part pushes exactly that part, and the frame validates.
- **Reads.** Every read validates, and makes 0 vendor calls, 0 GitHub calls, and 0 subprocesses ([MS-056, health from the tick snapshot](stories/diagnose.md#ms-056-health-from-the-tick-snapshot)).
- **Commands.** Every command example in the fixtures is accepted with 202, a job id, and a record written before the answer; a seat verb not in `verbs` is refused with a record; no merge route exists.
- **401/403 matrix.** Every route against no token, a bad token, and each caller kind answers the declared status, and every refusal writes a record.
- **CORS.** A listed origin is named, never `*`; a preflight or POST from another origin is 403; the webhook carries no CORS header.
- **Keep-alive and stale snapshot.** An idle stream sends a keep-alive inside one interval; a stopped loop yields one stale `health` frame even when a log line lands in the same pass.
- **Second client.** A CLI or text client that imports nothing from the page reads every part and runs every command through this contract ([MS-008, Arthur reads the same API](stories/observe.md#ms-008-arthur-reads-the-same-api)).
- **Phone.** Out of contract scope; the client's own component and integration tests hold [MS-139, every tab fits a phone](stories/observe.md#ms-139-every-tab-fits-a-phone) and [MS-191, dashboard tested at every tier](stories/testing.md#ms-191-dashboard-tested-at-every-tier) ([mike.md §12.4, the dashboard](mike.md#124-the-dashboard)).
