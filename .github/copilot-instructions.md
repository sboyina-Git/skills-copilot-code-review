# Repository Guidelines

This repository contains a small FastAPI application with a static front-end and a guided exercise workflow.

## Purpose
- Keep the implementation simple and focused on the exercise requirements.
- Ensure the GitHub Actions workflows align with the current branch and review process.

## Branching
- Use feature branches for changes, typically named for the task or step.
- The main branch is the default branch and should remain stable.
- Workflow-specific branches may be required for step-based exercise evaluation.

## Pull Requests
- Open pull requests against `main`.
- Use descriptive titles and bodies.
- If a workflow expects a review request or step-specific trigger, ensure the correct event is generated.

## Coding Guidelines
- Keep frontend and backend concerns separated.
- Prefer explicit, readable code over compact but hard-to-follow implementations.
- Keep API contracts consistent between the client and server.

## Workflow Notes
- Workflow step files live under `.github/workflows/`.
- Step content and guidance are stored under `.github/steps/`.
- If a workflow does not trigger, check the `on:` event filters and branch names first.

## Review and Testing
- Verify changes locally before pushing whenever possible.
- For frontend changes, ensure the relevant HTML/CSS/JS files are updated together.
- For backend changes, confirm the API route behavior matches the client requests.

## Security

- Validate input sanitization practices.
- Search for risks that might expose user data.
- Prefer loading configuration and content from the database instead of hard coded content. If absolutely necessary, load it from environment variables or a non-committed config file.

## Code Quality

- Use consistent naming conventions.
- Try to reduce code duplication.
- Prefer maintainability and readability over optimization.
- If a method is used a lot, try to optimize it for performance.
- Prefer explicit error handling over silent failures.