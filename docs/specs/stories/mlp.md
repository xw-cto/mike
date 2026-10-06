# The MLP build order

The MLP is the cheapest Mike that Tig will love and that teaches us something: one instance, one project, one worker and one reviewer on one cloud runtime, Tig steering by hand, and four dashboard tabs on his phone ([mike.md §13.1, the MLP](../mike.md#131-the-mlp)). These are the stories with `Urgency: high`, in the order to build them; each phase proves something the next one stands on. The words and the other releases: [mike.md §13, the cut](../mike.md#13-the-cut-mlp-v1-backlog); rules and verdicts: [the user stories index](README.md).

## Phase 1: package, config, store, records, log, fake runtime

Proves Mike installs as one package, keeps one store and one log, records before it acts, and runs its unit and component suites with no vendor.

1. [MS-110, One install command](operate.md#ms-110-one-install-command) · one install command, no factory checkout
2. [MS-156, One source for each fact](configure.md#ms-156-one-source-for-each-fact) · one config file, shipped defaults, live state outside git
3. [MS-121, Secrets outside live state](operate.md#ms-121-secrets-outside-live-state) · the vendor secret is named in config, kept outside live state
4. [MS-120, Vendor keys stored safely](operate.md#ms-120-vendor-keys-stored-safely) · the one vendor key is stored mode 600 and its account checked
5. [MS-157, One locked store owner](configure.md#ms-157-one-locked-store-owner) · one locked process owns the store
6. [MS-042, Unreadable config store said](configure.md#ms-042-unreadable-config-store-said) · an unreadable config store is said, never read as empty
7. [MS-043, Every tunable read each tick](configure.md#ms-043-every-tunable-read-each-tick) · every tunable is read from the store each tick
8. [MS-155, Settings applied live](configure.md#ms-155-settings-applied-live) · a saved setting applies live by the smallest action
9. [MS-061, Settings history by version](diagnose.md#ms-061-settings-history-by-version) · every settings save is a new version with its actor
10. [MS-178, Stale settings write refused](diagnose.md#ms-178-stale-settings-write-refused) · a save on an old version is refused
11. [MS-150, One record shape per actuation](seats.md#ms-150-one-record-shape-per-actuation) · mint, archive and restart write one record shape
12. [MS-073, Record every steer first](steer.md#ms-073-record-every-steer-first) · apply refuses an unrecorded steer
13. [MS-060, Every command recorded with identity](diagnose.md#ms-060-every-command-recorded-with-identity) · every command is recorded with identity and outcome
14. [MS-105, One structured log](diagnose.md#ms-105-one-structured-log) · one rotated, redacted structured log
15. [MS-138, ISO 8601 times on the wire](diagnose.md#ms-138-iso-8601-times-on-the-wire) · every time on the wire is ISO 8601 with offset
16. [MS-148, One actuator interface](seats.md#ms-148-one-actuator-interface) · one Runtime API for every driver
17. [MS-186, Mike ships a fake runtime](testing.md#ms-186-mike-ships-a-fake-runtime) · the fake runtime runs the control plane with no vendor
18. [MS-188, Worker and reviewer tested alone](testing.md#ms-188-worker-and-reviewer-tested-alone) · the worker and reviewer component suites pass from a synthetic steer

## Phase 2: the cloud driver and its conformance suite

Proves one real driver mints, steers with confirmed delivery, and reports its session log and usage, alone, before the control plane uses it.

19. [MS-185, A driver passes conformance alone](testing.md#ms-185-a-driver-passes-conformance-alone) · the cloud driver passes conformance with no control plane
20. [MS-149, Every steer confirmed or not](seats.md#ms-149-every-steer-confirmed-or-not) · every steer is confirmed by an event id or reported not confirmed
21. [MS-172, Session log from every runtime](seats.md#ms-172-session-log-from-every-runtime) · the session event stream is the seat's session log
22. [MS-111, Cloud setup installs the delta](operate.md#ms-111-cloud-setup-installs-the-delta) · a cloud session boots with the pinned tools
23. [MS-068, Tokens per seat and fleet](operate.md#ms-068-tokens-per-seat-and-fleet) · tokens since mint, unmeasured never zero
24. [MS-069, Context fullness per seat](operate.md#ms-069-context-fullness-per-seat) · context fullness per seat

## Phase 3: webhooks, the tick, the gates, two seats, routing

Proves the loop: an assigned issue reaches the worker, a ready pull request the reviewer, a send-back the worker, a Merge verdict Tig, every step gated and recorded.

25. [MS-165, Control plane detects every change](steer.md#ms-165-control-plane-detects-every-change) · signed webhooks and the store diff detect each change
26. [MS-107, Skip reads below budget reserve](diagnose.md#ms-107-skip-reads-below-budget-reserve) · reads are skipped below the reserve
27. [MS-158, Failed reads are unmeasured](configure.md#ms-158-failed-reads-are-unmeasured) · a failed read is unmeasured, not no work
28. [MS-112, One non-overlapping tick timer](operate.md#ms-112-one-non-overlapping-tick-timer) · one tick timer, never overlapping
29. [MS-019, Steer only owner-assigned work](steer.md#ms-019-steer-only-owner-assigned-work) · the owner gate on `gh_user`
30. [MS-142, Unlisted repositories refused](configure.md#ms-142-unlisted-repositories-refused) · the project gate
31. [MS-074, No worker steer onto urgency:no](steer.md#ms-074-no-worker-steer-onto-urgencyno) · the urgency floor
32. [MS-151, One pending steer per seat](seats.md#ms-151-one-pending-steer-per-seat) · one pending steer per seat
33. [MS-075, No action on unmeasured liveness](steer.md#ms-075-no-action-on-unmeasured-liveness) · no action on an unmeasured seat
34. [MS-035, One Running or Paused switch](configure.md#ms-035-one-running-or-paused-switch) · Running or Paused, a human switch
35. [MS-014, Stop keeps the session](steer.md#ms-014-stop-keeps-the-session) · seat Stop, the other human switch
36. [MS-091, Reviewers cannot push](review.md#ms-091-reviewers-cannot-push) · reviewer independence: no push by a reviewer
37. [MS-096, No merge verb](review.md#ms-096-no-merge-verb) · no merge verb, with a test
38. [MS-122, No seat acts as a human](operate.md#ms-122-no-seat-acts-as-a-human) · no seat acts as the human merger
39. [MS-152, Seat tokens act only as self](operate.md#ms-152-seat-tokens-act-only-as-self) · the seat token acts only as its seat
40. [MS-077, GitHub writes through Mike](steer.md#ms-077-github-writes-through-mike) · seat writes go through Mike, recorded first
41. [MS-124, Fixed writer, owner, addressee marks](operate.md#ms-124-fixed-writer-owner-addressee-marks) · `To: Name` and `seat:` are the fixed marks
42. [MS-023, Mint a seat with no session](seats.md#ms-023-mint-a-seat-with-no-session) · the two seats minted wait-only with an assignment
43. [MS-099, Mint wait-only](seats.md#ms-099-mint-wait-only) · a mint gives no permission to pick work
44. [MS-100, First steer rendered from config](seats.md#ms-100-first-steer-rendered-from-config) · the first steer is rendered from config
45. [MS-034, Remint carries the assignment](seats.md#ms-034-remint-carries-the-assignment) · a remint carries the assignment
46. [MS-098, Remint keeps one agent per name](seats.md#ms-098-remint-keeps-one-agent-per-name) · a remint keeps one session per seat name
47. [MS-033, No double actuation](seats.md#ms-033-no-double-actuation) · no double mint or restart while one is pending
48. [MS-012, Set or clear an assignment](steer.md#ms-012-set-or-clear-an-assignment) · Tig sets or clears an assignment as a label
49. [MS-168, Human issues reach the board](steer.md#ms-168-human-issues-reach-the-board) · an issue assigned to `gh_user` reaches the worker
50. [MS-169, Addressed comments become steers](steer.md#ms-169-addressed-comments-become-steers) · a `To: Name` comment from Tig becomes a steer
51. [MS-171, Unlisted users are contributors](steer.md#ms-171-unlisted-users-are-contributors) · an unlisted user's comment binds nothing
52. [MS-166, Changes routed as steers](steer.md#ms-166-changes-routed-as-steers) · the four routes: assigned, ready, send-back, Merge
53. [MS-082, Draft early, ready when clean](review.md#ms-082-draft-early-ready-when-clean) · the worker opens a draft and marks ready when clean
54. [MS-176, Self-review with the runtime's code-review tool](review.md#ms-176-self-review-with-the-runtimes-code-review-tool) · the worker self-reviews with its code-review tool
55. [MS-083, Self-review in one shape](review.md#ms-083-self-review-in-one-shape) · the self-review counts only in one shape on the head
56. [MS-092, Gates pinned to head sha](review.md#ms-092-gates-pinned-to-head-sha) · every gate is pinned to the head sha
57. [MS-085, One independent reviewer each](review.md#ms-085-one-independent-reviewer-each) · a ready pull request gets the independent reviewer
58. [MS-088, Review in one fixed shape](review.md#ms-088-review-in-one-fixed-shape) · the reviewer's verdict parses from one shape
59. [MS-093, Send-back returns to author](review.md#ms-093-send-back-returns-to-author) · a send-back returns the pull request to the worker
60. [MS-095, Request merge when gates pass](review.md#ms-095-request-merge-when-gates-pass) · a Merge verdict on the head assigns Tig
61. [MS-062, Hard Reboot the fleet](operate.md#ms-062-hard-reboot-the-fleet) · Hard reboot and Reset defaults start the pair clean
62. [MS-065, Fleet commands never collide](operate.md#ms-065-fleet-commands-never-collide) · a seat verb during a fleet command is refused

## Phase 4: the API and the four tabs, phone-first

Proves Tig sees and steers both seats from his phone over the version, health, seats, settings, logs and jobs parts.

63. [MS-154, Humans are verified bearers](operate.md#ms-154-humans-are-verified-bearers) · Tig is a verified bearer
64. [MS-137, Job ids for every command](diagnose.md#ms-137-job-ids-for-every-command) · every command returns a job id at once
65. [MS-177, Command outcome on the changed row](diagnose.md#ms-177-command-outcome-on-the-changed-row) · a job's outcome lands on the row it changed
66. [MS-054, Four distinct connection failures](diagnose.md#ms-054-four-distinct-connection-failures) · signed out, not allowed, unreachable and wrong version differ
67. [MS-006, Page updates by itself](observe.md#ms-006-page-updates-by-itself) · an open tab updates by itself
68. [MS-041, Typing survives live frames](configure.md#ms-041-typing-survives-live-frames) · a frame never eats an edit
69. [MS-180, One seat card component everywhere](observe.md#ms-180-one-seat-card-component-everywhere) · one seat card component
70. [MS-181, Cards grouped by role, responsive](observe.md#ms-181-cards-grouped-by-role-responsive) · cards stacked on a phone
71. [MS-182, Seat card info block](observe.md#ms-182-seat-card-info-block) · the seat card's info fields
72. [MS-001, One table of every seat](observe.md#ms-001-one-table-of-every-seat) · the Seats tab lists both seats
73. [MS-002, Liveness in four words](observe.md#ms-002-liveness-in-four-words) · liveness in four words
74. [MS-009, Runtime and host per row](observe.md#ms-009-runtime-and-host-per-row) · the driver on each card
75. [MS-004, Assignment shown per seat](observe.md#ms-004-assignment-shown-per-seat) · the assignment, linked
76. [MS-021, Reviewer links its pull request](review.md#ms-021-reviewer-links-its-pull-request) · the reviewer's card links its pull request
77. [MS-005, Last confirmed steer shown](observe.md#ms-005-last-confirmed-steer-shown) · the last confirmed steer
78. [MS-013, Pending steer shown apart](steer.md#ms-013-pending-steer-shown-apart) · the queued steer, apart
79. [MS-183, Seat card controls](observe.md#ms-183-seat-card-controls) · start-stop and the four verbs on the card
80. [MS-184, Phone card: expander and hamburger](observe.md#ms-184-phone-card-expander-and-hamburger) · Details expander and hamburger on a phone
81. [MS-140, Every seat verb by tap](observe.md#ms-140-every-seat-verb-by-tap) · every seat verb by tap
82. [MS-010, Steer one seat from its page](steer.md#ms-010-steer-one-seat-from-its-page) · steer one seat from its card
83. [MS-027, Verb buttons explain themselves](seats.md#ms-027-verb-buttons-explain-themselves) · a disabled verb carries the server's reason
84. [MS-028, Verbs offered by the control plane](seats.md#ms-028-verbs-offered-by-the-control-plane) · verbs only as the control plane lists them
85. [MS-024, Restart a stuck seat](seats.md#ms-024-restart-a-stuck-seat) · Restart keeps the assignment
86. [MS-025, Archive any seat's session](seats.md#ms-025-archive-any-seats-session) · Archive keeps the name
87. [MS-044, Health first with snapshot age](diagnose.md#ms-044-health-first-with-snapshot-age) · Health with its snapshot age
88. [MS-056, Health from the tick snapshot](diagnose.md#ms-056-health-from-the-tick-snapshot) · Health from the tick snapshot, stale said
89. [MS-046, Loop heartbeat and timer rows](diagnose.md#ms-046-loop-heartbeat-and-timer-rows) · the Loop section: heartbeat, mode, switch, timer
90. [MS-047, Header names a stopped loop](diagnose.md#ms-047-header-names-a-stopped-loop) · a stopped loop named on every tab
91. [MS-109, Each loop-down reason named](diagnose.md#ms-109-each-loop-down-reason-named) · each loop-down reason named
92. [MS-045, Needs attention groups faults](diagnose.md#ms-045-needs-attention-groups-faults) · Problems grouped worst first
93. [MS-052, Platform faults named](diagnose.md#ms-052-platform-faults-named) · read budget, vendor account and store faults named
94. [MS-050, Unconfirmed steers counted per seat](diagnose.md#ms-050-unconfirmed-steers-counted-per-seat) · unconfirmed steers counted per seat
95. [MS-058, Filterable log in the URL](diagnose.md#ms-058-filterable-log-in-the-url) · the Logs tab's full filter in the URL
96. [MS-036, Live or dry-run loop mode](configure.md#ms-036-live-or-dry-run-loop-mode) · live or dry-run with its confirm
97. [MS-037, Loop cadence from 1 to 60 minutes](configure.md#ms-037-loop-cadence-from-1-to-60-minutes) · cadence from 1 to 60 minutes
98. [MS-038, Settings show unit, actor and version](configure.md#ms-038-settings-show-unit-actor-and-version) · each setting with unit, actor and version
99. [MS-039, Schema check before save](configure.md#ms-039-schema-check-before-save) · a bad value fails before save
100. [MS-139, Every tab fits a phone](observe.md#ms-139-every-tab-fits-a-phone) · the four tabs fit a phone
101. [MS-191, Dashboard tested at every tier](testing.md#ms-191-dashboard-tested-at-every-tier) · the dashboard tested at the component and integration tiers

## Phase 5: the end-to-end run and the numbers

Proves the seams agree on a real repository with a real model, and records what the MLP set out to learn.

102. [MS-189, Control plane tick against fakes](testing.md#ms-189-control-plane-tick-against-fakes) · a full tick passes against fakes before the real run
103. [MS-190, One end-to-end run, on demand, recorded](testing.md#ms-190-one-end-to-end-run-on-demand-recorded) · one end-to-end run on demand, recorded

Record on [tig/mike#3, the spec issue](https://github.com/tig/mike/issues/3) before v1 starts: how many pull requests Tig merged glad, the cost of a wait-only mint and of a steer, the undelivered-steer count, and whether the Seats and Health tabs were enough on his phone.

## Counts

| File | critical | high | normal | no |
|---|---|---|---|---|
| [configure.md](configure.md) | 0 | 13 | 6 | 0 |
| [diagnose.md](diagnose.md) | 0 | 18 | 9 | 1 |
| [observe.md](observe.md) | 0 | 13 | 13 | 0 |
| [operate.md](operate.md) | 0 | 13 | 22 | 1 |
| [retired.md](retired.md) | 0 | 0 | 0 | 1 |
| [review.md](review.md) | 0 | 11 | 12 | 0 |
| [seats.md](seats.md) | 0 | 15 | 12 | 0 |
| [steer.md](steer.md) | 0 | 14 | 12 | 0 |
| [testing.md](testing.md) | 0 | 6 | 1 | 0 |
| **Total** | **0** | **103** | **87** | **3** |
