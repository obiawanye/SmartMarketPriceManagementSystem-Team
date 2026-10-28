# Smart Market Delivery Platform
## System Documentation

**Course:** CSC 303  
**Project:** Smart Market Delivery Platform (SMDP)  
**Requirements source:** [`Smart_Market_Delivery_Platform_MySQL.pdf`](./Smart_Market_Delivery_Platform_MySQL.pdf)  
**Database design:** [`DATABASE_SCHEMA.md`](./DATABASE_SCHEMA.md)

## 1. Project Overview

The Smart Market Delivery Platform is a proposed system for helping customers
plan meals, estimate ingredient costs, and arrange the purchase and delivery of
groceries from selected markets. It connects customers, market-shopping
workers, and operations staff through a workflow that begins with recipe and
pantry planning and continues through shopping, payment verification, and
delivery.

The platform's database is designed to preserve both current operational
information and historical transaction details. In particular, order records
are intended to retain snapshots of recipe outputs, delivery addresses, item
quantities, and purchase information so later catalog changes do not rewrite
the history of an order.

This document describes the SMDP requirements and proposed system design. It
distinguishes documented workflows and implemented database code from
functionality that remains planned. It does not claim that the application is
fully implemented or deployed.

## 2. Problem Statement

Planning a meal and sourcing its ingredients involves several connected
decisions: identifying ingredients and quantities, accounting for items a
customer already has, selecting a suitable market, estimating prices from
dated observations, and coordinating shopping and delivery. Substitutions or
price changes may require customer approval. Payment confirmation and
fulfilment records must also be kept distinct and traceable.

SMDP addresses this coordination problem by organizing recipe and ingredient
information, market and price data, customer orders, worker activity, payment
references, delivery records, and audit history in one platform design.
Generated recipe suggestions or estimated prices are not treated as verified
market facts or authoritative order totals.

## 3. Purpose and Scope

### Purpose

The project aims to define and begin implementing a relational foundation for
a market-delivery platform that can:

- support recipe-based shopping lists and pantry subtraction;
- associate ingredients, units, markets, and dated price observations;
- coordinate worker assignment, shopping progress, and substitutions;
- record payment verification, delivery, receipts, and support activity; and
- preserve enough history to explain how an order was planned and fulfilled.

### Scope

The documented target includes identity and roles, worker profiles, markets
and service zones, ingredient and recipe catalogs, price observations, orders
and their line items, worker assignments, substitution decisions, delivery,
payment and refund records, evidence references, support cases, and order
events.

The initial implementation scope is narrower: nine new catalog and worker
profile SQLAlchemy models have been written, along with one forward Alembic
migration. Other database entities and application workflows are documented
as planned. The migration has not been applied to a database.

## 4. System Actors and Responsibilities

The actors below represent the roles supported or anticipated by the design.
The database design does not itself establish that corresponding user
interfaces or services are implemented.

| Actor | Responsibilities |
|---|---|
| Customer | Provides meal or recipe preferences, reviews the ingredient list and estimates, supplies pantry information and a delivery address, approves or rejects material substitutions or price changes, and receives the delivery and itemized receipt. |
| Market-shopping worker | Accepts or declines an assignment, shops for the order, reports item availability and actual purchase details, proposes substitutions when required, and records fulfilment progress. |
| Operations staff | Oversees markets, delivery coverage, worker onboarding and assignments, resolves fulfilment or support issues, and monitors order and payment status. |
| Payment provider | Processes payment externally and supplies a transaction reference or event that the platform must verify before treating payment as confirmed. It is an external system, not an SMDP user role. |
| Recipe-generation service (if used) | May produce recipe suggestions or structured output. Its results are treated as editable suggestions and are not authoritative for live prices, payment state, or final totals. |

The existing role system associates users with roles. A worker-specific profile
is modeled separately so worker-only information does not need to be stored
on every user.

## 5. Functional Requirements and Main Workflow

The following requirements are grounded in the supplied SMDP brief and the
corresponding workflow documented in the schema. Database structures that
support these behaviors are not, by themselves, proof that the application
features are complete.

### Functional requirements

1. **Recipe and ingredient planning:** represent recipes as structured
   ingredients, quantities, units, and preparation details. Recipe output may
   be edited before it becomes an order list.
2. **Pantry subtraction:** allow the planning process to account for
   ingredients already available to the customer and determine what remains to
   be purchased. Persistent household pantry storage is not confirmed; the
   current MVP assumption is to record pantry quantities on the order.
3. **Market selection and price estimation:** associate markets with delivery
   coverage and store timestamped price observations with their units and
   provenance. Old observations remain historical; generated estimates are
   not presented as verified observations.
4. **Order creation:** record the customer, selected market, requested items,
   quantities, delivery details, and estimates. Snapshot data should preserve
   the order as it was agreed.
5. **Worker fulfilment:** assign a worker and retain progress and assignment
   attempts. Record purchased quantities and prices for an itemized receipt.
6. **Substitutions and price changes:** capture proposed changes and require
   customer approval before purchasing a material substitution or accepting a
   material price change.
7. **Payment verification:** maintain payment references and status separately
   from the order. Treat payment as confirmed only after provider verification.
8. **Delivery and receipt:** record delivery status and provide an itemized
   view of requested and purchased goods, subject to the final reconciliation
   policy.
9. **Audit and support:** maintain an order event history and support records
   so operational decisions and issues can be traced.

### End-to-end workflow

1. The customer selects or reviews a recipe and specifies servings.
2. The system presents an ingredient list with quantities and units. The
   customer reviews it and identifies pantry quantities.
3. The system subtracts pantry amounts, subject to supported unit conversions,
   and produces the list of items to buy.
4. The customer chooses a serviceable market. The platform uses available,
   dated price observations to create an estimate and communicates uncertainty
   where price data may be stale or incomplete.
5. The customer confirms the order and delivery details. The order stores the
   agreed item, recipe-output, address, and estimate snapshots as appropriate.
6. The platform records a worker assignment. The worker reports availability
   and purchase details and raises a substitution request when needed.
7. The customer approves or rejects material changes before the worker
   proceeds with them.
8. The platform verifies payment with the provider and records the verification
   result and provider reference. It does not rely on an unverified client
   claim.
9. The worker completes fulfilment; delivery status and evidence references
   may be recorded. The customer receives an itemized receipt.
10. Order events and support records preserve a trace of relevant actions and
    exceptions.

The exact fee formula, price-change threshold, payment adjustment/refund
process, response timeouts, and delivery split policy remain open decisions
documented in [`DATABASE_SCHEMA.md`](./DATABASE_SCHEMA.md).

## 6. System Architecture and Technologies

The repository uses a Python web application stack:

- **FastAPI** is the web framework identified by the project.
- **SQLAlchemy** defines the relational ORM models and metadata.
- **Alembic** manages versioned schema changes.
- **MySQL** is the target relational database.
- **PyMySQL** is declared as the MySQL Python driver.

At a logical level, clients and operational users interact with application
services through the web layer. The application layer is responsible for
validating requests, enforcing workflow rules, calculating estimates, and
communicating with external payment or recipe services where those integrations
are implemented. SQLAlchemy models represent persisted entities; Alembic
revisions describe schema changes; MySQL stores operational and historical
records.

This is an architectural description of the project and target design, not a
claim that every API endpoint or external integration is implemented. The
application startup path has previously been identified as invoking Alembic
upgrade behavior; therefore startup is intentionally not used as a validation
method in this assignment preparation.

## 7. Database Design

The complete proposed inventory, detailed column notes, constraints, and
Mermaid ER diagram are maintained in [`DATABASE_SCHEMA.md`](./DATABASE_SCHEMA.md).
The following summary explains the relational design.

### Primary keys

A primary key (PK) uniquely identifies a row in a table. Entity tables
generally use an integer `id` PK. The `workers` table uses `user_id` as both
its PK and FK because a worker profile belongs to one existing user. The
`user_role` and `market_coverage` association tables use composite PKs made
from their two relationship columns; this prevents duplicate associations.

### Foreign keys

A foreign key (FK) references a key in another table and ensures that a
relationship points to an existing record. Examples in the implemented
batch include:

- `workers.user_id` → `users.id`;
- `market_coverage.market_id` → `markets.id`;
- `market_coverage.zone_id` → `delivery_zones.id`;
- `ingredient_aliases.ingredient_id` → `ingredients.id`; and
- `recipe_ingredients.recipe_id`, `ingredient_id`, and `unit_id` → their
  respective recipe, ingredient, and unit tables.

The planned design adds relationships such as orders to customers and markets,
assignments to orders and workers, and payment transactions to orders. The
ERD in the schema document shows the declared foreign-key relationships and
their cardinalities.

### Relationships and the ER diagram

The identity tables use a many-to-many relationship between users and roles
through `user_role`. Markets and delivery zones are many-to-many through
`market_coverage`. Recipes and ingredients are many-to-many through
`recipe_ingredients`; the association also records a quantity and unit.
The planned transaction model connects customers, orders, items, workers,
payments, deliveries, evidence, and events.

An Entity-Relationship Diagram (ERD) is a visual summary of entities, keys,
and relationship cardinalities. The schema document uses Mermaid `erDiagram`
syntax, which is text-based, versionable, and suitable for rendering in
compatible Markdown tools. It helps readers check the relationship structure
alongside the written table inventory.

### Existing and proposed table status

At the last documented read-only database inspection, the existing
application tables were `users`, `roles`, and `user_role`. Their existing
models and migration history are retained. The nine new models listed below
exist in the codebase and are described by revision `a6b93c1e7f42`, whose
parent is `d4dbb44eb27c`. That migration is generated but **unapplied**; the
nine tables must not be described as present in the live database based only
on the existence of model and migration code.

The remaining tables in the proposed 27-table application design—including
`password_reset_tokens`, addresses, worker-market membership, price
observations, orders, order items, assignments, substitutions, deliveries,
events, evidence, payment records, refunds, and support cases—are documented
as planned, not implemented in the current batch.

An existing authentication compatibility issue is also documented: the
current `User` ORM model and previously inspected live `users` table differ
in password-column name, email length, and the presence of `is_active` and
`created_at`. Existing password values were not examined, and no password
format is assumed. The existing migration files must remain preserved.

## 8. Security, Payment, Privacy, and Audit

- **Credentials:** do not expose environment variables, database credentials,
  or provider secrets. The existing user schema/model mismatch requires a
  separately reviewed compatibility plan; password contents and format are
  unknown. This document does not claim a completed password migration or
  authentication implementation.
- **Payment:** store provider references, amounts, currency, and status
  needed for reconciliation. Do not store raw card details. Verify payment
  through the provider before marking it confirmed, and keep order,
  transaction, and refund status distinct.
- **AI and estimates:** treat generated recipes as suggestions that users may
  edit. Do not treat generated prices as verified market observations or
  generated totals as authoritative payment amounts.
- **Privacy:** keep evidence files outside MySQL where appropriate, storing
  only private object-storage references. Restrict access to evidence by
  relevant order and fulfilment permissions. Avoid exposing personal
  addresses or contact information beyond operational need.
- **Integrity:** use PKs, FKs, uniqueness, required fields, and quantity checks
  to protect relational consistency. Prefer restricting deletion or
  deactivating records referenced by business history.
- **Auditability:** keep order events append-oriented and retain payment and
  fulfilment history according to a policy that remains to be confirmed.
  Event idempotency, evidence retention, and broader data-retention periods
  are provisional design matters, not confirmed policy.

## 9. Implementation Status

### Existing application tables and models

The project already contains models for:

1. `users` — [`app/model/user.py`](./app/model/user.py)
2. `roles` — [`app/model/role.py`](./app/model/role.py)
3. `user_role` — [`app/model/user_role.py`](./app/model/user_role.py)

The original revisions are
[`394d19a5ae59_create_users_roles_and_user_role_tables.py`](./alembic/versions/394d19a5ae59_create_users_roles_and_user_role_tables.py)
and
[`d4dbb44eb27c_add_password_to_users.py`](./alembic/versions/d4dbb44eb27c_add_password_to_users.py).
They remain in the history and are not replaced by the new revision.

### New implemented SQLAlchemy models

The first business-table batch contains these nine models:

1. `workers` — [`app/model/worker.py`](./app/model/worker.py)
2. `delivery_zones` — [`app/model/delivery_zone.py`](./app/model/delivery_zone.py)
3. `markets` — [`app/model/market.py`](./app/model/market.py)
4. `market_coverage` — [`app/model/market_coverage.py`](./app/model/market_coverage.py)
5. `ingredients` — [`app/model/ingredient.py`](./app/model/ingredient.py)
6. `ingredient_aliases` — [`app/model/ingredient_alias.py`](./app/model/ingredient_alias.py)
7. `units` — [`app/model/unit.py`](./app/model/unit.py)
8. `recipes` — [`app/model/recipe.py`](./app/model/recipe.py)
9. `recipe_ingredients` — [`app/model/recipe_ingredient.py`](./app/model/recipe_ingredient.py)

The model package registers these classes through
[`app/model/__init__.py`](./app/model/__init__.py). Revision
[`a6b93c1e7f42_add_market_recipe_catalog_tables.py`](./alembic/versions/a6b93c1e7f42_add_market_recipe_catalog_tables.py)
creates these nine tables and is a forward child of `d4dbb44eb27c`. It has
not been applied. Therefore, the model and migration code exist, but the
database tables are not confirmed to exist.

`workers.status` currently defaults to `pending` as a provisional onboarding
decision; the requirements do not prescribe a status vocabulary or default.
For implemented tables with `updated_at`, SQLAlchemy's application-side
`onupdate` convention is used. The migration does not install database
triggers or a MySQL `ON UPDATE` clause, so updates made outside that ORM
behavior will not automatically refresh the timestamp.

## 10. Testing and Validation

### Completed static checks

The following checks have been completed without connecting to MySQL:

- Python syntax checks passed for the new model files and the new migration.
- Using the project's `.venv/bin/python`, SQLAlchemy metadata was loaded in
  isolation by substituting an in-memory declarative `Base` before importing
  model registrations. This avoided importing the database configuration,
  loading `.env`, or creating an engine.
- The nine new models were confirmed in metadata, and the FK graph resolved.
- Model and migration constraint names, index names, and key relationship
  targets were statically checked for consistency.
- The documented ingredient uniqueness was checked against the model and
  migration: `ingredients.normalized_name` and
  `ingredient_aliases.normalized_alias` are unique.
- Static revision inspection confirmed the chain
  `394d19a5ae59` → `d4dbb44eb27c` → `a6b93c1e7f42`.

These are static/source and isolated metadata checks. They do not prove that
the migration executes successfully on a particular MySQL server.

### Not yet completed

- No MySQL migration test or rollback test has been performed.
- No live database schema or data preservation check has been repeated for
  this document.
- No application integration, API, payment-provider, or end-to-end workflow
  tests are claimed as completed.

### Recommended next validation

When authorized, use a separate disposable MySQL database and a restricted
test account. Verify its target name before running Alembic; apply the parent
revision and the new revision there; inspect table definitions, indexes,
foreign keys, and checks; confirm synthetic user/role/association rows remain;
then test downgrade only on that disposable database and confirm those
identity fixtures remain. Record the MySQL version, since enforcement of
`CHECK` constraints depends on server version. Do not use the existing
database for this test.

## 11. Conclusion

SMDP's proposed relational design supports the documented meal-planning,
market sourcing, worker fulfilment, payment-verification, delivery, and
audit workflows. The project has preserved its three existing identity
tables and added a first batch of nine SQLAlchemy models with an unapplied
forward migration. The remaining platform entities and application behavior
are still planned. Static checks provide useful early assurance, while
disposable-MySQL migration and rollback testing remains necessary before any
future live application.
