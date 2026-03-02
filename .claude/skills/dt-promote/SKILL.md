---
name: dt-promote
description: Use when ready to promote a DataTransformer from local development to UAT or production via git tags.
---

# Promote DataTransformer — Tag and Deploy

Workflow for promoting a tested DataTransformer through environments.

## Prerequisites

- All local tests pass (`pytest tests/ -v`)
- Code is committed and pushed to remote
- Ecosystem model references this repo with an `EnvRefReleaseSelector`

## Workflow

### Step 1: Verify Tests Pass

```bash
pytest tests/ -v
```

**Checkpoint:** All tests pass. Do NOT promote with failing tests.

### Step 2: Commit and Push

```bash
git add -A
git commit -m "feat: <describe your changes>"
git push origin main
```

### Step 3: Tag for UAT

```bash
git tag v<version>-uat
git push --tags
```

Example: `git tag v1.0.0-uat && git push --tags`

**What happens next:**
- The Airflow DAG for this DT picks up the new tag via `EnvRefReleaseSelector`
- The DT runs on the next scheduled trigger in the UAT environment
- Monitor execution in the Airflow UI

### Step 4: Verify in UAT

- Check the Airflow UI for the DT DAG — all tasks should be green
- Query the merge database to verify output data is correct
- Check for errors in task logs if any task fails

### Step 5: Tag for Production

Once UAT verification passes:

```bash
git tag v<version>-prod
git push --tags
```

Example: `git tag v1.0.0-prod && git push --tags`

**What happens next:**
- Production Airflow picks up the new tag
- DT runs on production schedule
- Monitor first few runs in Airflow UI

## Version Naming Convention

| Tag Pattern | Environment | Example |
|-------------|-------------|---------|
| `v*-uat` | UAT / Integration | `v1.0.0-uat` |
| `v*-prod` | Production | `v1.0.0-prod` |
| `v*-demo` | Demo environments | `v1.0.0-demo` |

The tag pattern must match the `VersionPatternReleaseSelector` or `EnvRefReleaseSelector` configured in your RuntimeEnvironment.

## Rollback

To roll back to a previous version:

```bash
git tag v<previous-version>-prod
git push --tags
```

Airflow picks up the latest matching tag. Tagging a previous commit with a new tag effectively rolls back.
