# Runtime and Reports

nexu 0.3 adds an intentionally simple static runtime for capsules.

The runtime is not a production frontend. It is a review surface that lets a human quickly inspect what the capsule currently contains:

- UI blueprint screens,
- API mock endpoints,
- Intract contracts,
- fixtures,
- iteration timeline.

Build it with:

```bash
nexu capsule runtime menu-icons
```

Open:

```text
.nexu/capsules/menu-icons/runtime/index.html
```

## Why static HTML?

The point is to keep the capsule cheap and portable. A static runtime can be opened without Docker, Vite, FastAPI or a database. Later versions can add richer React/FastAPI runners, but the first reliable layer should be easy to inspect and archive.

## Reports

Build a report with:

```bash
nexu capsule report menu-icons
```

Generated files:

```text
.nexu/capsules/menu-icons/reports/report.yaml
.nexu/capsules/menu-icons/reports/report.md
.nexu/capsules/menu-icons/reports/report.html
```

The report is the promotion checkpoint. It answers:

```text
what changed?
what did verification say?
did the source drift?
what events happened in this capsule?
```
