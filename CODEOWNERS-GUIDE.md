# Code Ownership & Review Requirements

## What is CODEOWNERS?

CODEOWNERS is a GitHub feature that **automatically assigns reviewers** to pull requests based on which files are changed. It enforces accountability and ensures the right people review critical code.

### How It Works

When a PR touches specific files/directories, GitHub automatically:
1. Requests review from designated owners
2. Marks the PR as "Changes requested" until owners approve
3. Blocks merging if required reviews are missing (with branch protection)

## CODEOWNERS File

Location: `.github/CODEOWNERS` (root of repository)

```
# Default owners for everything (fallback)
* @project-poc-org/platform-team

# DevOps & Infrastructure
/.github/ @project-poc-org/devops-team @jonathangarciaes
/Dockerfile @project-poc-org/devops-team
/docker-compose.yml @project-poc-org/devops-team
/.dockerignore @project-poc-org/devops-team
/scripts/ @project-poc-org/devops-team

# CI/CD Pipelines (CRITICAL - requires senior approval)
/.github/workflows/ @project-poc-org/sre-team @jonathangarciaes
/VERSION @project-poc-org/release-managers
/CHANGELOG.md @project-poc-org/release-managers

# Application Code
/app/ @project-poc-org/backend-team
/app/auth.py @project-poc-org/security-team @project-poc-org/backend-team
/app/routes/ @project-poc-org/backend-team

# Database & Migrations
/app/models.py @project-poc-org/database-team @project-poc-org/backend-team
/migrations/ @project-poc-org/database-team

# Security-Critical Files
/app/auth.py @project-poc-org/security-team
/app/settings.py @project-poc-org/security-team @jonathangarciaes

# Documentation (anyone can approve)
*.md @project-poc-org/tech-writers
/docs/ @project-poc-org/tech-writers

# Dependencies (security review required)
requirements.txt @project-poc-org/security-team @project-poc-org/backend-team
package.json @project-poc-org/security-team @project-poc-org/frontend-team
package-lock.json @project-poc-org/security-team

# Configuration
*.yml @project-poc-org/devops-team
*.yaml @project-poc-org/devops-team
*.toml @project-poc-org/devops-team
*.ini @project-poc-org/devops-team
```

## Syntax

```
# Pattern                          # Owner(s)
path/to/file.py                    @username
/directory/**                      @org/team-name
*.js                               @frontend-team @security-team
```

- **@username**: Individual GitHub user
- **@org/team-name**: GitHub team within organization
- **Multiple owners**: All must approve (if required)
- **Order matters**: Last matching pattern wins

## Real-World Examples

### Example 1: Small Team (Startup)

```
# Default: CTO reviews everything
* @cto

# Backend code
/app/ @backend-lead @cto
/app/auth.py @cto  # Security-critical

# CI/CD (CTO + DevOps)
/.github/workflows/ @cto @devops-lead

# Docs (anyone)
*.md @team
```

### Example 2: Enterprise (Big Tech Style)

```
# Default owners
* @project-poc-org/engineering

# Critical Infrastructure (2 senior SREs required)
/.github/workflows/ @project-poc-org/sre-leads @project-poc-org/platform-architects
/Dockerfile @project-poc-org/container-experts
/scripts/deploy.sh @project-poc-org/sre-leads

# Security (must have security team approval)
/app/auth.py @project-poc-org/appsec @project-poc-org/backend-leads
/app/crypto.py @project-poc-org/crypto-team
requirements.txt @project-poc-org/supply-chain-security

# Database (DBA approval required)
/migrations/ @project-poc-org/dba-team @project-poc-org/data-platform
/app/models.py @project-poc-org/dba-team

# Frontend
/src/ @project-poc-org/frontend-team
/src/components/Payment* @project-poc-org/payments-team @project-poc-org/security

# Compliance & Legal
/LICENSE @project-poc-org/legal
/PRIVACY.md @project-poc-org/legal @project-poc-org/compliance
```

### Example 3: Monorepo (Multiple Services)

```
# API Backend
/services/api-backend/ @backend-team
/services/api-backend/app/auth.py @security-team @backend-team

# Worker Service
/services/worker-service/ @data-team

# Frontend
/services/website-frontend/ @frontend-team

# Shared Libraries
/libs/auth/ @security-team @platform-team
/libs/database/ @dba-team @platform-team

# Infrastructure (applies to all services)
**/Dockerfile @devops-team
**/.github/workflows/ @sre-team
```

## Branch Protection Integration

Combine CODEOWNERS with branch protection rules for enforcement:

### GitHub Settings → Branches → Branch Protection Rules

**For `main` branch:**
```yaml
✅ Require pull request reviews before merging
   └─ Required approving reviews: 2
   └─ Dismiss stale reviews when new commits are pushed
   └─ Require review from Code Owners ← KEY SETTING
   └─ Require approval of most recent reviewable push

✅ Require status checks to pass before merging
   └─ Require branches to be up to date
   └─ Status checks: CI, Security Scan, SonarQube

✅ Require conversation resolution before merging

✅ Require signed commits

❌ Allow force pushes

❌ Allow deletions
```

**Result**: PRs touching `/app/auth.py` require:
1. Security team approval (from CODEOWNERS)
2. Backend team approval (from CODEOWNERS)
3. All CI checks passing
4. Signed commits

## Team Structure (GitHub Organizations)

Create teams in GitHub to match CODEOWNERS:

```
project-poc-org/
├── @platform-team
│   ├── jonathangarciaes (DevOps Engineer)
│   ├── sreleadandrew (SRE Lead)
│   └── infrastructurejane (Infrastructure Architect)
│
├── @backend-team
│   ├── backenddev1
│   ├── backenddev2
│   └── backendsara (Tech Lead)
│
├── @security-team
│   ├── securitymark (Security Engineer)
│   ├── appsecalice (AppSec Lead)
│   └── compliancebob (Compliance)
│
├── @sre-team
│   ├── sreandrew (SRE Lead)
│   ├── srekevin (SRE)
│   └── sreemily (SRE)
│
└── @release-managers
    ├── jonathangarciaes
    └── releasemanagertom
```

### Create Teams

**GitHub Organization Settings → Teams → New team**

```
Team Name: sre-team
Description: Site Reliability Engineers
Members: sreandrew, srekevin, sreemily
Repositories: All repositories (Read access by default)
```

## Granular Ownership Examples

### By File Type

```
# All Python files
**.py @backend-team

# All TypeScript/JS files
**.ts @frontend-team
**.tsx @frontend-team
**.js @frontend-team

# All Dockerfiles
Dockerfile @devops-team
**/*Dockerfile* @devops-team
```

### By Feature

```
# Authentication feature
/app/auth.py @security-team @backend-auth-squad
/app/routes/auth.py @security-team @backend-auth-squad
/tests/test_auth.py @backend-auth-squad

# Payment feature
/app/payments/ @payments-team @compliance-team @security-team
```

### Critical Paths (Multiple Required Approvals)

```
# Production deployment scripts (3 approvals required)
/scripts/deploy-prod.sh @cto @sre-lead @release-manager

# Database migrations (2 approvals required)
/migrations/ @dba-lead @backend-lead

# Security-critical (2 from security team required)
/app/auth.py @security-alice @security-bob @security-charlie
```

## Best Practices

### ✅ DO

1. **Start Broad, Get Specific**
   ```
   * @engineering
   /app/ @backend-team
   /app/auth.py @security-team @backend-team
   ```

2. **Require Multiple Approvals for Critical Code**
   ```
   /.github/workflows/ @sre-lead @devops-lead @cto
   ```

3. **Use Teams, Not Individuals** (scalability)
   ```
   # Good
   /app/ @backend-team
   
   # Bad (doesn't scale)
   /app/ @john @sarah @mike
   ```

4. **Document Ownership** (add comments)
   ```
   # Authentication (Security team mandatory for compliance)
   /app/auth.py @security-team @backend-team
   ```

### ❌ DON'T

1. **Don't Over-Specify** (review fatigue)
   ```
   # Bad: Every file has different owner
   /app/file1.py @person1
   /app/file2.py @person2
   /app/file3.py @person3
   ```

2. **Don't Create Single Points of Failure**
   ```
   # Bad: Only one person can approve
   /.github/workflows/ @only-devops-guy
   
   # Good: Team of people
   /.github/workflows/ @devops-team
   ```

3. **Don't Ignore Documentation**
   ```
   # Docs shouldn't block PRs
   *.md @engineering  # Anyone on team can approve
   ```

## Testing CODEOWNERS

Use GitHub's CODEOWNERS validator:

```bash
# Install tool
npm install -g codeowners

# Validate syntax
codeowners validate .github/CODEOWNERS

# See who owns a file
codeowners show app/auth.py
# Output: @security-team @backend-team
```

## Integration with CI/CD

### Automatic Assignment

When PR is created:
```
1. GitHub reads .github/CODEOWNERS
2. Matches changed files to patterns
3. Auto-requests review from matched owners
4. PR shows "Review required from @security-team"
```

### Enforcement

With branch protection enabled:
```
1. Developer creates PR changing app/auth.py
2. GitHub requires review from @security-team (CODEOWNERS)
3. GitHub requires review from @backend-team (CODEOWNERS)
4. Both must approve before merge button activates
5. CI must also pass (separate requirement)
```

## Notifications

Owners get notified via:
- GitHub notifications
- Email
- Slack (via GitHub app)
- Mobile app

Configure in: **GitHub Settings → Notifications**

## For Your Project

For `api-backend`, `worker-service`, `website-frontend`, `desktop-app`:

```
# .github/CODEOWNERS

# Default owner
* @jonathangarciaes

# CI/CD pipelines (critical infrastructure)
/.github/workflows/ @jonathangarciaes
/Dockerfile @jonathangarciaes
/VERSION @jonathangarciaes
/scripts/ @jonathangarciaes

# Security-critical files
/app/auth.py @jonathangarciaes
/app/settings.py @jonathangarciaes
requirements.txt @jonathangarciaes

# Application code (can be delegated later)
/app/ @project-poc-org/backend-team
/src/ @project-poc-org/frontend-team

# Documentation (flexible)
*.md
```

Start simple, add granularity as team grows!
