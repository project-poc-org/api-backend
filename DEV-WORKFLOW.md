# Developer Workflow Best Practices

## Overview

This document defines **production-grade development practices** used at companies like Google, Netflix, Spotify, and Datadog. Following these practices ensures code quality, security, and scalability.

---

## 1. Branch Strategy

### Branch Types & Lifespan

| Branch | Purpose | Lifespan | Merges To |
|--------|---------|----------|-----------|
| `main` | Production code | Permanent | N/A (protected) |
| `develop` | Integration/staging | Permanent | `main` (via release) |
| `feature/*` | New features | 1-7 days | `develop` |
| `bugfix/*` | Bug fixes | 1-3 days | `develop` |
| `hotfix/*` | Emergency prod fixes | Hours | `main` + `develop` |
| `release/*` | Release preparation | 1-3 days | `main` + `develop` |

### Branch Naming Conventions

```bash
# Features
feature/oauth-support
feature/user-dashboard
feature/JIRA-123-add-payment-method

# Bug Fixes
bugfix/null-pointer-login
bugfix/JIRA-456-fix-timeout
bugfix/memory-leak-worker

# Hotfixes
hotfix/security-patch
hotfix/critical-data-loss
hotfix/JIRA-789-prod-outage

# Releases
release/1.1.0
release/2.0.0
```

**Rules:**
- Use lowercase with hyphens
- Include ticket number if applicable
- Be descriptive but concise
- Delete after merge

---

## 2. Commit Message Standards (Conventional Commits)

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description | Version Bump | Example |
|------|-------------|--------------|---------|
| `feat` | New feature | MINOR (1.0.0 → 1.1.0) | `feat(auth): add OAuth2 support` |
| `fix` | Bug fix | PATCH (1.0.0 → 1.0.1) | `fix(api): handle null pointer` |
| `feat!` | Breaking change | MAJOR (1.0.0 → 2.0.0) | `feat(api)!: change response format` |
| `docs` | Documentation | None | `docs: update API guide` |
| `style` | Code style (formatting) | None | `style: fix indentation` |
| `refactor` | Code restructuring | None | `refactor(auth): simplify token validation` |
| `perf` | Performance improvement | PATCH | `perf(db): add query caching` |
| `test` | Add/update tests | None | `test(auth): add OAuth2 unit tests` |
| `chore` | Maintenance | None | `chore: update dependencies` |
| `ci` | CI/CD changes | None | `ci: add Docker build caching` |

### Good Commit Examples

```bash
# Feature with context
feat(auth): add OAuth2 Google provider

Implemented OAuth2 authentication flow for Google.
Includes token refresh and revocation endpoints.

Closes #123

# Bug fix with impact
fix(api): prevent race condition in user creation

Added mutex lock around user creation to prevent
duplicate user records when concurrent requests occur.

Impact: Affects 0.1% of signup requests
Closes #456

# Breaking change
feat(api)!: migrate to JSON:API specification

BREAKING CHANGE: All API responses now follow JSON:API
format. Clients must update response parsing.

Migration guide: docs/v2-migration.md
Closes #789

# Security fix
fix(auth): patch SQL injection vulnerability

SECURITY: Critical SQL injection in login endpoint.
Added parameterized queries and input validation.

CVSS Score: 9.8 (Critical)
CVE: CVE-2026-12345
Closes #999
```

### Bad Commit Examples (Don't Do This)

```bash
# Too vague
git commit -m "fix bug"
git commit -m "updates"
git commit -m "WIP"

# Not following format
git commit -m "Added OAuth support and fixed some bugs and updated docs"

# Multiple concerns in one commit
git commit -m "feat: add OAuth + fix typos + update CI"
```

### Commit Hygiene

**✅ DO:**
- One logical change per commit
- Write descriptive commit messages
- Reference issue/ticket numbers
- Sign commits (`git commit -S`)
- Test before committing

**❌ DON'T:**
- Commit commented-out code
- Commit secrets/credentials
- Make huge commits (>500 lines)
- Use `git commit -m "fixup"` in shared branches

---

## 3. Pull Request (PR) Workflow

### Creating a PR

#### Step 1: Create Feature Branch

```bash
# Update develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/oauth-support

# Work on feature
git add app/auth.py
git commit -m "feat(auth): add OAuth2 configuration"

git add app/routes/auth.py
git commit -m "feat(auth): implement OAuth2 flow"

git add tests/test_auth.py
git commit -m "test(auth): add OAuth2 integration tests"

# Push to remote
git push origin feature/oauth-support
```

#### Step 2: Open PR on GitHub

**PR Title:** Follow conventional commits format
```
feat(auth): add OAuth2 support
```

**PR Description Template:**

```markdown
## Description
Add OAuth2 authentication support with Google provider.

## Type of Change
- [x] New feature (feat)
- [ ] Bug fix (fix)
- [ ] Breaking change (BREAKING CHANGE)
- [ ] Documentation update (docs)

## Changes Made
- Added OAuth2 configuration in settings.py
- Implemented Google OAuth2 flow in routes/auth.py
- Added token refresh and revocation endpoints
- Created integration tests for OAuth2 flow

## Testing
- [x] Unit tests pass locally
- [x] Integration tests pass locally
- [x] Manual testing completed
- [x] Security scan passed (Semgrep, Trivy)

## Checklist
- [x] Code follows project style guide
- [x] Self-reviewed code
- [x] Commented complex logic
- [x] Updated documentation
- [x] Added tests for new functionality
- [x] All tests passing
- [x] No new security vulnerabilities
- [x] Branch is up-to-date with develop

## Related Issues
Closes #123
Related to #100

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Deployment Notes
- Requires new environment variable: `OAUTH_CLIENT_SECRET`
- Database migration required: `alembic upgrade head`
- Update .env.example with new OAuth config

## Reviewer Notes
Please pay special attention to:
- Token validation logic in `app/auth.py:validate_oauth_token()`
- Error handling in OAuth callback endpoint
```

#### Step 3: Request Reviews

- **Auto-assigned:** Via CODEOWNERS file
- **Manual:** Tag specific reviewers
- **Draft PR:** Use if work-in-progress

```
Draft PR → Ready for Review
```

### Reviewing PRs

#### As a Reviewer

**✅ Check for:**

1. **Code Quality**
   - Follows style guide
   - No code smells
   - Well-structured
   - Proper error handling

2. **Security**
   - No hardcoded secrets
   - Input validation
   - SQL injection prevention
   - XSS protection

3. **Testing**
   - Tests cover new code
   - Edge cases tested
   - Tests actually pass

4. **Documentation**
   - Code is self-documenting
   - Complex logic has comments
   - README updated if needed

5. **Performance**
   - No obvious performance issues
   - Database queries optimized
   - No N+1 queries

6. **Breaking Changes**
   - API contracts maintained
   - Backward compatibility
   - Migration path documented

**Review Types:**

```
✅ Approve: Code is good to merge
💬 Comment: Suggestions, non-blocking feedback
❌ Request Changes: Must fix before merging
```

**Good Review Comments:**

```markdown
# Constructive
"Consider using a database transaction here to ensure data consistency. Example: `with db.session.begin():`"

# Specific
"Line 45: This query could cause an N+1 problem. Suggest using `joinedload()` to eager-load relationships."

# Educational
"Great work on the OAuth implementation! One suggestion: consider adding rate limiting to prevent brute force attacks."
```

**Bad Review Comments:**

```markdown
# Too vague
"This doesn't look right"

# Not actionable
"Bad code"

# Bikeshedding
"I prefer spaces over tabs" (when project already has a standard)
```

#### As a PR Author

**Responding to Reviews:**

1. **Be Receptive**
   - Don't take feedback personally
   - Ask clarifying questions
   - Explain decisions if needed

2. **Make Changes**
   ```bash
   # Make requested changes
   git add app/auth.py
   git commit -m "fix(auth): add rate limiting per reviewer feedback"
   git push origin feature/oauth-support
   ```

3. **Reply to Comments**
   - Mark resolved when fixed
   - Explain if you disagree (politely)
   - Thank reviewers

4. **Request Re-review**
   - After addressing all feedback
   - Tag reviewers again

### Merging Strategy

#### Merge Types

| Strategy | When to Use | Result |
|----------|-------------|--------|
| **Merge Commit** | Release branches, important features | Preserves full history |
| **Squash & Merge** | Feature branches with many commits | Clean, single commit |
| **Rebase & Merge** | Small features, keeping linear history | Linear history |

**Our Standard:**

- `feature/*` → `develop`: **Squash & Merge** (clean history)
- `develop` → `main`: **Merge Commit** (preserve context)
- `hotfix/*` → `main`: **Merge Commit** (traceability)

#### Before Merging Checklist

```
✅ All CI checks passing
✅ Required approvals received (per CODEOWNERS)
✅ All conversations resolved
✅ Branch is up-to-date with target branch
✅ No merge conflicts
✅ Version bumped (if applicable)
✅ Documentation updated
✅ Tests passing
```

#### Merge Button

```
GitHub Settings → Merge Button Options

✅ Allow squash merging (for features)
✅ Allow merge commits (for releases)
❌ Allow rebase merging (can be confusing)
✅ Automatically delete head branches
```

---

## 4. Code Review Best Practices

### Timing

- **Within 1 business day**: First review response
- **Within 1 hour**: High-priority/hotfix reviews
- **Within 2 days**: Full review cycle complete

### Review Size

**Ideal PR Size:** 200-400 lines of code

| Lines Changed | Review Quality | Time Required |
|---------------|----------------|---------------|
| < 50 | Easy, thorough | 10 minutes |
| 50-200 | Good | 30 minutes |
| 200-400 | Acceptable | 1 hour |
| 400-1000 | Difficult | 2+ hours |
| > 1000 | Poor quality | Impossible to review well |

**If PR is too large:**
```
Option 1: Split into multiple PRs
Option 2: Review in person/pair programming
Option 3: Incremental reviews (mark sections as reviewed)
```

### Reviewer Rotation

**Round-robin reviews:** Distribute review load evenly

```
Monday: Alice reviews Bob's PRs
Tuesday: Bob reviews Charlie's PRs
Wednesday: Charlie reviews Alice's PRs
```

### Automated Checks (Before Human Review)

```yaml
1. ✅ Linting (Black, ESLint, Prettier)
2. ✅ Tests (Pytest, Jest)
3. ✅ Security (Semgrep, Trivy, TruffleHog)
4. ✅ Code Quality (SonarQube)
5. ✅ Build (Docker image builds successfully)

If any fail → Fix before requesting review
```

---

## 5. Development Lifecycle

### Complete Feature Workflow

```bash
# Day 1: Start Feature
git checkout develop
git pull origin develop
git checkout -b feature/oauth-support

# Day 1-3: Development
git commit -m "feat(auth): add OAuth2 config"
git commit -m "feat(auth): implement OAuth2 flow"
git commit -m "test(auth): add unit tests"
git push origin feature/oauth-support

# Day 3: Open PR
# GitHub → Create Pull Request
# CI runs automatically
# Request reviews from team

# Day 4: Address Review Feedback
git commit -m "fix(auth): add rate limiting per review"
git push origin feature/oauth-support
# Request re-review

# Day 5: PR Approved
# Squash & Merge to develop
# Delete feature branch automatically

# Day 6: Testing on Staging
# CI deploys to staging automatically
# QA team tests

# Day 10: Release
git checkout develop
git pull origin develop
git checkout -b release/1.1.0
# Final testing

# Day 11: Deploy to Production
git checkout main
git merge --no-ff release/1.1.0
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main --tags
# CI deploys to production

# Cleanup
git checkout develop
git merge release/1.1.0
git branch -d release/1.1.0
git push origin --delete release/1.1.0
```

### Emergency Hotfix Workflow

```bash
# Production issue discovered
git checkout main
git pull origin main
git checkout -b hotfix/security-patch

# Fix issue immediately
git commit -m "fix(auth)!: patch SQL injection

SECURITY: Critical SQL injection vulnerability.
CVSS: 9.8
Closes #999"

# Open PR (expedited review)
git push origin hotfix/security-patch
# Tag: @jonathangarciaes (urgent)

# After approval (same day)
git checkout main
git merge --no-ff hotfix/security-patch
git tag -a v1.1.1 -m "Hotfix: Security patch"
git push origin main --tags

# Merge back to develop
git checkout develop
git merge hotfix/security-patch
git push origin develop

# CI deploys to production immediately
# Post-incident review scheduled
```

---

## 6. Permission Levels & RBAC

### GitHub Repository Roles

| Role | Permissions | Who Gets This |
|------|-------------|---------------|
| **Admin** | Full access, settings, delete repo | DevOps Lead, CTO |
| **Maintain** | Manage issues, PRs, some settings | Tech Leads |
| **Write** | Push to branches, merge PRs | Developers |
| **Triage** | Manage issues and PRs | Junior Devs, QA |
| **Read** | Read-only access | Contractors, Auditors |

### Branch Protection Rules

#### `main` Branch

```yaml
✅ Require pull request reviews before merging
   └─ Required approving reviews: 2
   └─ Dismiss stale reviews: Yes
   └─ Require review from Code Owners: Yes
   
✅ Require status checks to pass
   └─ Build & Test
   └─ Security Scan
   └─ Code Quality (SonarQube)
   
✅ Require conversation resolution

✅ Require signed commits

✅ Include administrators: Yes

❌ Allow force pushes: No
❌ Allow deletions: No
```

#### `develop` Branch

```yaml
✅ Require pull request reviews: 1
✅ Require status checks to pass
✅ Require conversation resolution
❌ Allow force pushes: No
```

#### `feature/*` Branches

```
No restrictions (developers can force-push during WIP)
```

### Team Permissions

```
Organization Settings → Teams

@sre-team:
- Repository access: Admin
- Can create repos: Yes
- Can delete repos: Yes

@backend-team:
- Repository access: Write
- Can create repos: No
- Can delete repos: No

@contractors:
- Repository access: Read
- Can create repos: No
- Can fork: No
```

---

## 7. Best Practices Summary

### Developer Dos & Don'ts

**✅ DO:**

1. Write conventional commits
2. Keep PRs small (< 400 lines)
3. Request reviews within 4 hours of PR creation
4. Review PRs within 1 business day
5. Run tests locally before pushing
6. Update documentation with code changes
7. Delete branches after merge
8. Sign commits with GPG
9. Rebase on target branch before merging
10. Add ticket numbers to commits

**❌ DON'T:**

1. Commit directly to `main`
2. Force-push to shared branches
3. Merge your own PRs without approval
4. Push untested code
5. Commit secrets/credentials
6. Leave commented-out code
7. Create PRs with > 1000 lines
8. Ignore review feedback
9. Merge failing PRs
10. Skip CI checks

### DevOps Segregation of Duties

**As DevOps Engineer, You Control:**

1. **CI/CD Pipelines** (/.github/workflows/)
2. **Infrastructure** (Dockerfiles, docker-compose.yml)
3. **Deployment Scripts** (/scripts/)
4. **Branch Protection Rules**
5. **Secrets Management** (GitHub Secrets, Vault)
6. **Monitoring & Alerting** (Prometheus, Grafana)

**Developers Control:**

1. **Application Code** (/app/, /src/)
2. **Tests** (/tests/)
3. **Documentation** (*.md)

**Shared Ownership:**

1. **Dependencies** (requirements.txt - security team approves)
2. **Database Migrations** (DBAs review)
3. **Security Code** (/app/auth.py - security team reviews)

**Access Control Matrix:**

| Resource | Developers | DevOps | Security | Managers |
|----------|-----------|---------|----------|----------|
| Application Code | Write | Read | Read | Read |
| CI/CD Pipelines | Read | Write | Read | Read |
| Production Servers | None | Admin | Read | Read |
| Secrets | None | Admin | Admin | None |
| AWS Console | None | Admin | Read | Billing |
| Kubernetes Cluster | None | Admin | Read | None |

---

## 8. Tooling & Automation

### Required Tools

```bash
# Commit message validation
npm install -g commitlint @commitlint/cli

# Pre-commit hooks
pip install pre-commit
pre-commit install

# Code formatting
pip install black isort
npm install -g prettier

# Linting
pip install flake8 pylint
npm install -g eslint

# Security scanning
brew install truffleHog trivy semgrep
```

### Pre-commit Hooks

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: commitlint
        name: Validate commit message
        entry: scripts/commit-msg.sh
        language: script
        stages: [commit-msg]
      
      - id: black
        name: Format Python code
        entry: black
        language: python
        types: [python]
      
      - id: truffleHog
        name: Scan for secrets
        entry: trufflehog filesystem .
        language: system
        pass_filenames: false
```

---

## 9. Metrics & KPIs

Track these metrics to improve workflow:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| PR Review Time | < 1 day | GitHub Insights |
| PR Size | < 400 lines | GitHub Insights |
| Build Success Rate | > 95% | GitHub Actions |
| Code Coverage | > 80% | SonarQube |
| Security Vulns | 0 critical | Trivy, Semgrep |
| Deployment Frequency | Daily | GitHub Actions |
| Mean Time to Recovery | < 1 hour | Incident logs |

---

## 10. Escalation & Support

### When You're Stuck

1. **Can't resolve merge conflict?**
   - Ask for help in #dev-help Slack channel
   - Tag the person who made conflicting changes

2. **PR stuck in review for > 2 days?**
   - Ping reviewers in Slack
   - Escalate to tech lead

3. **CI failing with unclear error?**
   - Check #ci-failures Slack channel
   - Tag @devops-team

4. **Need urgent review (hotfix)?**
   - Tag `urgent-review` label
   - Ping in #urgent-reviews Slack channel
   - Tag on-call engineer

### Resources

- **CONTRIBUTING.md**: Conventional commits guide
- **BRANCHING.md**: Git workflow
- **CODEOWNERS-GUIDE.md**: Code ownership rules
- **Slack #dev-help**: Ask questions
- **Weekly Dev Sync**: Thursdays 2pm

---

**Remember:** These practices exist to help us ship high-quality, secure code faster. When in doubt, ask!
