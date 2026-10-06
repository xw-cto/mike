# Mike user stories: configure

The stories for configuration: settings and priorities, the config store applying on change, and many projects on one instance. Rules, verdicts and the other files: [the user stories index](README.md).

## Configure

#### MS-035 One Running or Paused switch
As a human (Tig today), I want one Running/Paused switch for the loop that acts on click, so that I can stop all automated action at once.
Evidence: [factory dashboard app.js line 956, the Running/Paused switch](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L956); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: while Paused a tick records 0 seat actions; a repeat click's job is applied with why `already Paused`.
Verdict: CHANGE: Running or Paused is a setting key written by `POST settings`, its answer a job ([Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands)).
Urgency: high · Running or Paused is one of the two human switches

#### MS-036 Live or dry-run loop mode
As a human (Tig today), I want loop mode live or dry-run, with a confirm only when going live, so that dry-run is safe and live is deliberate.
Evidence: [factory dashboard rules.mjs line 1543, the loop mode confirm](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1543); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: switching to live opens a confirm, to dry-run does not; in dry-run every verb writes a record and sends 0 bytes to any vendor or GitHub.
Verdict: KEEP.
Urgency: high · live or dry-run is an MLP Settings switch with its confirm

#### MS-037 Loop cadence from 1 to 60 minutes
As a human (Tig today), I want the loop cadence settable from 1 to 60 minutes, so that I trade responsiveness for cost.
Evidence: [factory harness settings.py line 409, the cadence setting](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L409); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: 0 and 61 are refused by the server; a non-integer is refused on the page.
Verdict: KEEP.
Urgency: high · cadence is in the minimal Settings tab

#### MS-038 Settings show unit, actor and version
As a human (Tig today), I want every setting shown with its value in its unit, who changed it last and when, and the store version that wrote it, so that I can trust and audit settings without a column that says nothing.
Evidence: [factory dashboard app.js line 1141, the settings table](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1141); [Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes).
Acceptance: each setting shows its label, its control with the unit as part of it (5 min, 24 h, 75 %), one line of help, and "changed by <login>, <ago> · v<version>"; there is no From or source column; a secret shows its name and set or not set.
Verdict: CHANGE: factory's From column is dropped, every setting lives in the config store; `settingRow` carries `type`, `unit`, `range`, `help`, `changed_by` as a login and `changed_at` ([Mike dashboard API §7, payload shapes](../mike-dashboard-api.md#7-payload-shapes)).
Urgency: high · the minimal Settings tab shows each value with unit, actor and version

#### MS-039 Schema check before save
As a human (Tig today), I want a value checked against the store's schema before it saves, so that a typo fails on the page and not in the loop.
Evidence: [factory dashboard rules.mjs line 1517, the schema check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/rules.mjs#L1517); [Mike dashboard API §6, commands](../mike-dashboard-api.md#6-commands).
Acceptance: invalid input shows "<label> must be <type>" and writes no version; the page and the server use one schema file.
Verdict: KEEP.
Urgency: high · a bad `gh_user`, cadence or seat type fails before save

#### MS-040 Copyable View Settings dump
As a human (Tig today), I want a View all as JSON dump of every effective value with its type, unit and version that I can copy, so that I can paste the config into an issue.
Evidence: [factory dashboard app.js line 892, View Settings](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L892); [Mike dashboard API §5, reads](../mike-dashboard-api.md#5-reads).
Acceptance: pretty-printed JSON with `{value, type, unit, version}` per key; a secret appears by name only; Copy says "Copied."
Verdict: KEEP.
Urgency: normal · View all as JSON belongs to the full Settings tab

#### MS-041 Typing survives live frames
As a human (Tig today), I want what I am typing kept when a frame arrives, so that live updates do not eat my edit.
Evidence: [factory dashboard app.js line 1202, the per-frame redraw](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1202).
Acceptance: a field with unsaved text keeps its text and focus across 10 consecutive frames.
Verdict: CHANGE: the page patches changed rows instead of rebuilding the tab per frame ([mike.md §10 item 21, dashboard patches](../mike.md#10-what-mike-does-not-re-create)).
Urgency: high · a stream frame must not eat an edit on the Settings tab

#### MS-042 Unreadable config store said
As a human (Tig today), I want the page to say when the config store cannot be read, so that I know nothing is steered.
Evidence: [factory dashboard app.js line 1170, the store unreadable banner](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1170).
Acceptance: the lead line reads "The config store is unmeasured: <reason>. Nothing is steered until it reads." and the loop records 0 steers.
Verdict: KEEP.
Urgency: high · the config store is MLP and an unreadable one must say so

#### MS-043 Every tunable read each tick
As the loop, I want every tunable read from the config store each tick, so that a tune needs no pull request.
Evidence: [factory harness settings.py line 445, the tunable settings](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L445).
Acceptance: a save writes one version and one log line; the next tick's records cite the new version.
Verdict: CHANGE: the key set shrinks to Mike's (loop window, read reserve, fill-missing cap, shares, mint thresholds); paste, pe-retarget, main-restart lists and redelivery keys go.
Urgency: high · reload-on-change of the config store is MLP

#### MS-104 Seat host files from config
As a lane-PE, I want a seat host's runtime files rendered from instance config with a report of what differs, and an apply that fixes only that, so that a host is config-as-code.
Evidence: [factory agent-harness README.md line 179, the host render](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/README.md#L179).
Acceptance: report-only by default; apply writes nothing outside the configured root; a launch script without the generated-by marker is refused without `--force`.
Verdict: CHANGE: rendered from instance config, not `seats.yaml`; no ladder step check.
Urgency: normal · seat hosts are v1

#### MS-193 JSON settings open in a real editor
As a human (Tig today), I want any setting whose value is JSON to open in a real editor, pretty-printed, with line numbers, syntax coloring, a Format button and validation that names the line and column, so that I never edit a one-line blob in a text box.
Evidence: [the dashboard spec, the Settings tab](../mike-dashboard.md); factory's Settings tab took JSON in a plain input ([factory dashboard app.js line 1141, the settings table](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/dashboard/app.js#L1141)).
Acceptance: a `json` setting opens the editor beside the list on desktop and full-screen on a phone; Format pretty-prints; an invalid document shows the error with line and column and Save is disabled until it validates against the setting's schema; a valid save posts one settings command based on the shown store version.
Verdict: NEW.
Urgency: normal · the MLP's seat types live in the config file; the JSON editor comes with the full Settings groups in v1

## Config store apply-on-change

#### MS-155 Settings applied live
As a human (Tig today), I want a setting change applied live by the smallest action (reload, remint the affected seats, or swap a key), recorded, so that a change takes effect without a reboot.
Evidence: [factory#1524, config applied live](https://github.com/excaliwire/factory/issues/1524); [factory harness settings.py line 1258, settings apply](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/settings.py#L1258); [mike.md §5, the control plane](../mike.md#5-the-control-plane).
Acceptance: each save writes one record naming the action taken; a cadence change remints 0 seats; a role model change remints only that role's seats.
Verdict: NEW.
Urgency: high · reload-on-change is MLP; a seat-type change remints the affected seat

#### MS-156 One source for each fact
As a human (Tig today), I want desired state (roles, roster, projects, lanes, hosts, vendors, briefs) as instance config changed by pull request, shipped defaults in a separate file, and live state never in git, so that one source holds each fact.
Evidence: [factory harness store.py line 3, the file store](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/store.py#L3); [mike.md §5, the control plane](../mike.md#5-the-control-plane), [mike.md §10 item 16, settings seeded from four places](../mike.md#10-what-mike-does-not-re-create).
Acceptance: the instance config repository holds 0 live-state files; each setting has exactly one source (shipped default, instance config, or config store).
Verdict: NEW.
Urgency: high · install is one config file, shipped defaults and a store outside git

#### MS-157 One locked store owner
As the loop, I want the store owned by one locked process, append-only where it is a log, so that two writers never race and no row is silently replaced.
Evidence: [factory harness store.py line 3, the unlocked file store](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/store.py#L3); [mike.md §5, the control plane](../mike.md#5-the-control-plane), [mike.md §10 item 15, an unlocked file store](../mike.md#10-what-mike-does-not-re-create).
Acceptance: a second process opening the store is refused and named on Health; a log row once written is never rewritten (test).
Verdict: NEW.
Urgency: high · the store is MLP and has one owner

#### MS-158 Failed reads are unmeasured
As the loop, I want a GitHub read that fails to read `unmeasured`, never empty, so that an outage does not look like "no work".
Evidence: [factory harness gh.py line 100, the GitHub read module](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/gh.py#L100); [mike.md §5, the control plane](../mike.md#5-the-control-plane).
Acceptance: with GitHub returning 502, the tick records `unmeasured` for each read and 0 steers or mints.
Verdict: NEW.
Urgency: high · the tick must not read a GitHub outage as no work

## Multi-project, single instance

#### MS-141 One instance, several projects
As a human (Tig today), I want one Mike instance to manage several projects with one loop, one store, one dashboard and one priorities list, so that I do not deploy Mike per repository.
Evidence: [tig/mike#2, the master plan](https://github.com/tig/mike/issues/2); [mike.md §1.2, multi-repository, one instance](../mike.md#12-multi-repository-one-instance), [decision 6, one list per instance](../mike.md#11-decisions); [Mike dashboard API §9, where this is tested](../mike-dashboard-api.md#9-where-this-is-tested).
Acceptance: an install with no factory checkout manages two projects from one instance and passes the contract tests in [Mike dashboard API §9, where this is tested](../mike-dashboard-api.md#9-where-this-is-tested).
Verdict: NEW.
Urgency: normal · several projects per instance are v1

#### MS-142 Unlisted repositories refused
As a human (Tig today), I want a verb on a repository not on the instance's project list refused before any call runs, for every caller, so that no seat works outside the program.
Evidence: [factory harness __main__.py line 1425, `cmd_steer` does not check](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L1425); [gate 2, the project gate](../mike.md#33-gates-mike-enforces-for-every-caller).
Acceptance: a steer, mint or GitHub write naming an unlisted repository makes 0 GitHub or vendor calls and writes one refused record.
Verdict: NEW.
Urgency: high · the project gate is an MLP gate

#### MS-143 Every GitHub verb names project
As a seat (any), I want every verb that touches GitHub to take the project explicitly, so that `#N` is never ambiguous across projects.
Evidence: [factory harness __main__.py line 748, `cmd_steer`](https://github.com/excaliwire/factory/blob/bb2bf4c6ecabf1df53054519c899b77ea9ef65e8/agent-harness/agent_harness/__main__.py#L748); [mike.md §1.2, multi-repository, one instance](../mike.md#12-multi-repository-one-instance).
Acceptance: a GitHub verb called without a project is refused; every record and log line of such a verb has a `project` field.
Verdict: NEW.
Urgency: normal · with one project `#N` is unambiguous; several projects are v1

#### MS-192 Two instances on one repository stay harmless
As a human running two Mike instances that both manage one repository, I want each instance to act only on its own `gh_user` and its own seat names and to treat every other `seat:` label, `[Name]` prefix and `To:` address as another owner's work, so that the overlap costs load, not a wrong action.
Evidence: [mike.md §1.3, overlapping instances](../mike.md#13-overlapping-instances).
Acceptance: with two instances on one fixture repository with distinct `gh_user` and disjoint seat names, a tick in each produces 0 steers onto the other's assigned issues, 0 Health findings about the other's labels, and 0 steers from a `To:` naming the other's seat; with a shared `gh_user` the same fixture produces two `seat:` labels on one issue, which the spec names as the undetected case.
Verdict: NEW.
Urgency: normal · overlapping instances are v1
