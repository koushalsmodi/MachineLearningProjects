# Data Layer

## Overview
The data layer contains all business configuration for the Travel-GPT agent. 
Policy rules, traveler profiles, and team budgets are stored as JSON files 
separate from application code — meaning travel policies and budgets can be 
updated without touching any agent logic. In a real enterprise environment, 
each file would be owned by a different business team and updated independently.

---

## File Relationships
The three files are connected through the traveler profile:

- `travelers.json` → `policy.json`: each traveler has a `tier` field (entry/manager/senior) 
  that maps directly to a policy block in `policy.json`. The agent uses this to 
  determine which rules apply for every policy check.
- `travelers.json` → `budgets.json`: each traveler has an `assigned_budget_pool` 
  field (Finance/Engineering/Commercial) that maps to a team budget in `budgets.json`. 
  The agent checks `remaining_budget` against `max_trip_budget` before approving any booking.
- `policy.json` → agent decisions: every flight option returned by the search is 
  run through the policy rules for that traveler's tier before being surfaced.

---

## policy.json
**Real-world owner:** Corporate travel team

Defines the rules for each employee tier. The agent references this file 
on every policy check.

| Key | Description |
|---|---|
| `cabin_class` | Maximum permitted cabin class for this tier |
| `approved_airlines` | List of airlines the traveler is permitted to book |
| `upgrade_eligibility` | Whether the traveler can request an upgrade |
| `max_upgrade_cost` | Maximum additional cost permitted for an upgrade (manager/senior only) |
| `lounge_access` | Whether the traveler is entitled to airport lounge access |
| `advance_booking_days` | Minimum days in advance a trip must be booked |
| `max_trip_budget` | Maximum cost permitted for a single trip |

**Tiers:**
- `entry` — economy, strictest booking window, no upgrades or lounge access
- `manager` — premium economy, upgrade eligible up to $200, 10 day booking window
- `senior` — business class, broader airline access, lounge access, 7 day booking window

---

## travelers.json
**Real-world owner:** HR / People team

Contains mock traveler profiles for three employees, one per tier. 
The agent looks up the traveler by employee ID at the start of every request.

| Key | Description |
|---|---|
| `employee_id` | Unique identifier for the traveler |
| `tier` | Maps to a policy block in `policy.json` |
| `team` | The traveler's team — used for budget pool lookup |
| `firstName` / `lastName` | Traveler name for response output |
| `email` | Corporate email address |
| `home_airport` | Default departure airport (IATA code) |
| `loyalty_programs` | Airline loyalty numbers used in upgrade decisions |
| `assigned_budget_pool` | Maps to a team budget in `budgets.json` |

---

## budgets.json
**Real-world owner:** Finance team

Contains travel budget pools for each team. The agent checks 
`remaining_budget` against the traveler's `max_trip_budget` before 
approving a booking.

| Key | Description |
|---|---|
| `project_budget` | Total annual travel budget allocated to the team |
| `remaining_budget` | Budget remaining after all trips booked to date |

---

## Key Distinctions

**`max_trip_budget` vs `remaining_budget`** — these are easy to confuse:

- `max_trip_budget` lives in `policy.json` and is a **per trip ceiling by tier** — 
  no single booking can exceed this amount regardless of how much budget remains
- `remaining_budget` lives in `budgets.json` and is the **cumulative team pool** — 
  the total amount left across all trips for that team this period

Both checks must pass for a booking to be approved. A trip can be within 
the per-trip cap but still fail if the team pool is exhausted.

---

## Updating This Data

**Adding a new tier:** add a new block to `policy.json` with all required keys, 
then assign travelers to it via the `tier` field in `travelers.json`

**Adding a new traveler:** add a new employee block to `travelers.json` with a 
unique employee ID, ensuring `tier` matches an existing policy block and 
`assigned_budget_pool` matches an existing team in `budgets.json`

**Adding a new team budget:** add a new team block to `budgets.json` and 
update the relevant travelers' `assigned_budget_pool` field in `travelers.json`

---

## Test Scenarios
Five test scenarios referencing this data layer are provided in `tests/scenarios/`. 
Each scenario file contains a trip request and expected agent output, covering 
the happy path, policy violations, last minute bookings, and upgrade approvals.