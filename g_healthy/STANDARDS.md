# Contributing to Grow Healthy

Welcome to the Grow Healthy project!
We're thrilled to have you here. This project is built on the **Frappe framework** and leverages a **React SDK** for its frontend. Whether you're here to squash bugs, build features, optimize APIs, or improve documentation — this guide will walk you through everything you need to contribute effectively.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Development Setup](#development-setup)
3. [Code Style Guidelines](#code-style-guidelines)
4. [Frappe Development Guidelines](#frappe-development-guidelines)
5. [React SDK Guidelines](#react-sdk-guidelines)
6. [API Development Guidelines](#api-development-guidelines)
7. [Authentication & Authorization](#authentication--authorization)
8. [Testing Guidelines](#testing-guidelines)
9. [Documentation Guidelines](#documentation-guidelines)
10. [Workflow and Git Guidelines](#workflow-and-git-guidelines)
11. [Security Guidelines](#security-guidelines)
12. [Performance Guidelines](#performance-guidelines)
13. [Frappe Coding Standards](#frappe-coding-standards)
14. [Pre-commit Hooks](#pre-commit-hooks)

---

## Project Overview

Grow Healthy is a modular health and wellness ERP platform built using Frappe. It consists of:

- A centralized backend with modular Doctypes.
- A React SDK-based frontend for user apps.
- Role-based access with domain-specific logic (e.g., admin, coach, user).
- API-first design to support mobile and cross-platform extensions.

Goals:

- Provide a seamless user experience for health tracking and coaching.
- Modular, scalable, and secure codebase.
- Developer-friendly contributions via React SDK + Frappe synergy.

---

## Development Setup

### Requirements

- Ubuntu 22.04+ recommended
- Node.js (v18+), Yarn
- Python 3.10+, Frappe Bench
- Redis, MariaDB, Node-Sass

### Setup

1. Clone the repo and install backend:

   ```bash
   bench init growhealthy-bench --frappe-branch version-15
   cd growhealthy-bench
   bench get-app growhealthy
   bench new-site growhealthy.local
   bench --site growhealthy.local install-app growhealthy
   ```

2. Setup frontend:

   ```bash
   cd apps/g_healthy
   yarn
   yarn dev
   ```

3. Access local apps via:

   - `admin.growhealthy.local`
   - `g-healthy.growhealthy.local`
   - `bumpcoach.growhealthy.local`

---

## Code Style Guidelines

- Use 4 spaces (no tabs).
- Follow Frappe's linting rules (`black`, `flake8` for Python).
- For React, use Prettier + ESLint.
- Use meaningful variable names and avoid abbreviations.

---

## Frappe Development Guidelines

- Use standard Doctype structures.
- Avoid hardcoding values; use DocField options.
- All custom scripts must be under `hooks.py`.
- Avoid using private methods in overrides.

---

## React SDK Guidelines

- Components live in `components/` and must follow atomic design.
- Use `frappe-react-sdk` for API interactions.
- Avoid direct axios/fetch calls.
- Use context providers for auth/session handling.

---

## API Development Guidelines

- Use Frappe's `whitelisted` methods for secure API endpoints.
- Always validate inputs server-side.
- Use `frappe.response` format consistently.
- API versioning to be handled via route prefixes (e.g., `/api/v1/...`).

---

## Authentication & Authorization

- Use Frappe's built-in login and session manager.
- Each subdomain handles its own auth context.
- Role-based permission is mandatory in both frontend and backend.

---

## Testing Guidelines

- Use `pytest` for backend.
- Use `jest` and `react-testing-library` for frontend.
- Aim for 80%+ coverage on critical modules.
- Write tests alongside new features.

---

## Documentation Guidelines

- All modules must have a README.md.
- Functions and classes require docstrings.
- Use Frappe's in-app help wherever applicable.
- Markdown files should be in `/docs`.

---

## Workflow and Git Guidelines

- Use feature branches: `feature/xyz`, `fix/issue-123`, etc.
- Write clear commit messages: `feat: add health summary page`
- Pull Requests must include:

  - Description of the change
  - Screenshot or video (if UI-related)
  - Checklist for testing and review

---

## Security Guidelines

- Never commit `.env`, credentials, or private keys.
- Validate every user input server-side.
- Rate-limit sensitive endpoints.
- Use `frappe.get_doc().run_method()` cautiously.

---

## Performance Guidelines

- Use `frappe.db.sql` only when necessary; prefer ORM.
- Avoid N+1 queries.
- For frontend, lazy-load non-critical components.
- Monitor browser performance using React Dev Tools.

---

## Frappe Coding Standards

- Follow [Frappe's official coding guide](https://frappeframework.com/docs).
- Avoid unnecessary custom fields — prefer Doctype design.
- Use background jobs for long-running tasks.

---
