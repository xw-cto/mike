# Mike user stories: testing

The stories for the testing seams and the dashboard tested at every tier. Rules, verdicts and the other files: [the user stories index](README.md).

## Testing seams

#### MS-185 A driver passes conformance alone
As a human, I want every runtime driver to pass one conformance suite through the Runtime API with no control plane running, so that a driver is proven before it is installed and a vendor change is caught in one place.
Evidence: [mike.md §12.3, the suites each tier must hold](../mike.md#123-the-suites-each-tier-must-hold), component tier; [mike.md §4, runtimes](../mike.md#4-runtimes).
Acceptance: the suite covers config, mint, steer with confirmed delivery, stop, restart, archive, liveness, usage, session log; it runs as a component test against the fake runtime in CI and as a contract test against the vendor sandbox on demand with cost recorded; a driver failing any case cannot be enabled by config.
Verdict: NEW.

#### MS-186 Mike ships a fake runtime
As the loop, I want a fake runtime that implements the Runtime API in memory and records every call, so that the control plane and the seat suites run with no vendor.
Evidence: [mike.md §12.2, the seams](../mike.md#122-the-seams-the-architecture-must-provide).
Acceptance: the fake is loaded by the same driver path as a real driver; a control-plane tick against it makes 0 network calls; its recorded calls are asserted in integration tests.
Verdict: NEW.

#### MS-187 Arthur tested alone on a synthetic board
As a human, I want Arthur's behavior tested with no control plane and no other seat, from a synthetic board and a stub of Mike's verbs, so that a brief change is measured before it reaches the fleet.
Evidence: [mike.md §12.3, the suites each tier must hold](../mike.md#123-the-suites-each-tier-must-hold), component tier; [mike.md §3.5, what is judgment](../mike.md#35-what-is-judgment).
Acceptance: given the 2026-10-05 send-back board fixture, the stub records 3 send-back steers and 0 refusals; given a board with only `urgency:no` work, it records 0 steers; the suite runs against a replay of recorded model turns in CI and against a real model on demand.
Verdict: NEW.

#### MS-188 Worker and reviewer tested alone
As a human, I want a worker and a reviewer each tested alone from a synthetic steer in a fixture repository, so that the pull request lifecycle shape is proven per role.
Evidence: [mike.md §12.3, the suites each tier must hold](../mike.md#123-the-suites-each-tier-must-hold), component tier; [mike.md §6, the pull request lifecycle](../mike.md#6-the-pull-request-lifecycle).
Acceptance: the worker opens a draft, posts `Self-Review: Done` with the head sha, and marks ready only after a green CI fixture; the reviewer posts a verdict of at most 12 lines in the required shape; each failure names the lifecycle step.
Verdict: NEW.

#### MS-189 Control plane tick against fakes
As the loop, I want a full tick runnable as an integration test against the fake runtime, a fake GitHub and an injected clock, so that routing, gates, records and frames are tested without a network.
Evidence: [mike.md §12.1, the tiers](../mike.md#121-the-tiers), integration tier; [mike.md §5, the control plane](../mike.md#5-the-control-plane).
Acceptance: every change kind in section 5 has a tick test that asserts the routed steer and its record; every gate has a refusal test; the API's opening frames validate from the fixture store; 0 network calls.
Verdict: NEW.

#### MS-190 One end-to-end run, on demand, recorded
As a human, I want one end-to-end run (real driver, sandbox repository, real tick, real model) that I start on demand, so that the seams are proven to agree without making every test depend on the whole.
Evidence: [mike.md §12.1, the tiers](../mike.md#121-the-tiers), end-to-end tier.
Acceptance: the run is not in default CI; it writes its result, duration and cost to the issue that asked for it; no unit, component, contract or integration test imports from it.
Verdict: NEW.

#### MS-191 Dashboard tested at every tier
As a human, I want the dashboard client tested at the same tiers as the rest of Mike, with the seat card and every tab rendered alone from fixtures in a headless browser at 1180 px and 375 px, so that a layout or responsiveness break is caught before I open it on my phone.
Evidence: [mike.md §12.4, the dashboard](../mike.md#124-the-dashboard); [the dashboard spec §3, the Seats tab and the seat card](../mike-dashboard.md#3-the-seats-tab-and-the-seat-card).
Acceptance: each component has a render test at both widths asserting no horizontal overflow and a kept screenshot baseline; the client's command bodies equal the API fixtures byte for byte; an integration test against the in-process API shows a pushed frame updating one card while typed text survives; none of these needs a live control plane, vendor or GitHub.
Verdict: NEW.
