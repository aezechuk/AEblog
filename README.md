![CI/CD](https://github.com/aezechuk/AEblog/actions/workflows/deploy.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-black.svg?logo=flask)
![AWS Elastic Beanstalk](https://img.shields.io/badge/AWS-Elastic_Beanstalk-orange.svg?logo=amazonaws)

# Arielle’s Blog & Security Writing Platform

This repository contains the source code for my personal blog and security writing platform, built with **Flask** and deployed on **AWS Elastic Beanstalk**. The site serves as a public archive of real-world security writeups, vulnerability analysis, and lessons learned, alongside reflections from my career in technology.

The project began as a way to deepen my understanding of Flask and backend systems, and evolved into a production-deployed application supporting long-form technical writing.

🌐 **Live site:** https://arielleezechukwu.com

---

## Project Focus

This project emphasizes:

- Realistic backend application structure  
- Secure configuration and deployment practices  
- Clean separation between presentation, business logic, and data  
- Practical features that support writing and publishing workflows  

It is intentionally scoped as a **single-author platform**, rather than a multi-user CMS.

---

## Key Features

- Public blog with post archives and individual post pages  
- Markdown-based content rendering with HTML sanitization  
- Post summaries for previews on the home and blog pages  
- Slug-based URLs for clean, readable links  
- Admin-only authentication for content creation  
- Secure deployment using AWS Elastic Beanstalk  
- HTTPS and DNS management via Cloudflare  

---

## Technology Overview

### Backend
- Python / Flask  
- SQLAlchemy ORM  
- Flask-Login  
- Flask-Migrate  
- Flask-Mail  
- Markdown + Bleach (sanitization)

### Frontend
- Jinja templates  
- Bootstrap  
- Moment.js for date handling  

### Infrastructure
- AWS Elastic Beanstalk (Python platform)  
- SQLite (local development)  
- PostgreSQL (production)  
- Environment-based configuration (secrets not committed)

---

## Architecture Notes

- Content is stored in a relational database with explicit `published` and `summary` fields to support archival writing.  
- Markdown is converted and sanitized on write to prevent XSS.  
- The application is designed to minimize attack surface by limiting authentication and authoring capabilities.  
- Followers and social features exist in the underlying model but are intentionally unused.

---

## Current Status & Roadmap

### Completed
- Production deployment on AWS  
- Content rendering and archival structure  
- Home and blog UX refinements  
- Secure configuration and logging
- - CI-based deployment validation 

### Planned
- Unit and integration testing  
- Post editing and deletion  
- Draft/unpublished content workflow  
 

## Testing

This project includes a foundational automated test suite built with pytest and Flask’s test client.
The purpose is to validate core application behavior—authentication, post creation, routing, and slug generation—while maintaining stability as the project grows.

Tests run against an in-memory SQLite database, with application contexts created and cleaned up automatically. This ensures fast, isolated execution without touching local or production data.

### What’s Covered
- Route accessibility and basic page loads
- Login and logout workflows
- Handling of invalid and valid authentication attempts
- Blog post creation (authenticated-only behavior)
- Automatic slug generation
- Unique slug handling when titles collide

These tests were intentionally scoped to reinforce understanding of Flask internals, request flow, and database interactions. They also form the foundation for continuous integration and eventual continuous deployment.

### Continuous Integration
All tests run automatically in GitHub Actions on each push and pull request.
The CI workflow installs dependencies, executes the test suite, and ensures the application remains stable before any deployment step.

---

## About the Author

I’m a systems thinker who likes to tinker. I write about real-world security incidents, vulnerabilities, and lessons learned, drawing from experience across cybersecurity operations, delivery management, technology leadership, and community-based work.

This project represents how I think about systems: practical, secure, and designed around real-world usage.

---

## Notes

This repository is a **personal project and portfolio artifact**. It is not intended to be a reusable template or drop-in application.

<!-- CI/CD test: README change should NOT deploy -->
