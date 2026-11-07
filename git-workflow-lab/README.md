# 🌿 Git & GitHub Version Control & Branching Workflow Lab

## 📌 Overview
This lab documents practical experience with version control, feature branching strategies, remote repository synchronization, and collaborative Pull Request (PR) lifecycles using Git and GitHub. Built as part of the Google IT Automation / Introduction to Git and GitHub coursework.

## 🛠️ Key Concepts & Workflows Mastered

### 1. Local Repository Management
- Initialized and configured local repositories, tracking line-by-line file changes across commit histories.
- Managed staging environments (`git add`) and executed descriptive, atomic commits (`git commit`).

### 2. Branching & Isolation Strategies
- Created isolated feature branches (`git checkout -b feature-name`) to develop updates and security patches safely without impacting production (`main`).
- Merged completed feature branches back into the primary codebase (`git merge`).

### 3. Conflict Resolution & Remediation
- Identified and resolved manual merge conflicts by inspecting conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
- Validated code integrity post-resolution prior to finalizing merges.

### 4. Remote Collaboration & GitHub Workflows
- Managed remote connections (`git remote`), synchronized upstream changes (`git fetch` / `git pull`), and deployed local updates (`git push`).
- Managed end-to-end Pull Request (PR) lifecycles, code reviews, and remote branch merges on GitHub.

## ⚙️ Essential Command Toolkit
```bash
# Branching & Operations
git checkout -b feature/security-patch
git status
git add .
git commit -m "Fix: Update access log parsing parameters"

# Remote Synchronization
git push origin feature/security-patch
git pull origin main
