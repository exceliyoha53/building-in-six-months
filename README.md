# Building in Six Months: AI Automation & Micro-SaaS Architecture

## The Mission
This repository documents a 6-month engineering sprint focused on building production-ready AI automation systems, data extraction pipelines, and Micro-SaaS backends. 

The core philosophy of this project is execution over theory. Every system built here is designed to solve real-world business problems, automate manual workflows, and operate autonomously in production environments.

## Tech Stack & Focus Areas
* Language: Python 3.10+
* Data Extraction: BeautifulSoup, Playwright, HTTP Sessions
* Backend & APIs: FastAPI, RESTful architecture
* Database: SQLite (Local), PostgreSQL (Production)
* AI Integration: OpenAI/Anthropic APIs, LangChain, RAG Systems
* Deployment: Docker, GitHub Actions, Cloud VPS

## Architecture & Progress
The repository is structured chronologically to demonstrate progressive system complexity.

### Month 1: The Automation & Extraction Engine (Completed)
* Week 1: Advanced OOP Python and core scraping architecture.
* Week 2: Dynamic data extraction utilizing Playwright to bypass anti-bot systems and traverse pagination.
* Week 3: Task orchestration using APScheduler and professional logging for unattended execution.
* Week 4: Database architecture implementing live-sync UPSERT logic to maintain fresh data states.
* Master Project: Built an autonomous B2B Lead Generation Engine that scrapes, verifies, and reports data on a scheduled cron job.

### Month 2: Bots, Alerts, and Interfaces
(Scheduled: Integrating extraction engines with Telegram/Discord APIs for real-time mobile alerts and command execution.)

### Month 3: Building the Micro-SaaS Backend
(Scheduled: FastAPI endpoints, JWT Authentication, and Stripe payment integration.)

### Month 4: Agentic AI & Smart Systems
(Scheduled: Connecting pipelines to LLMs for autonomous decision-making and data synthesis.)

### Month 5: Deployment & MLOps
(Scheduled: Dockerization, CI/CD pipelines, and live cloud server deployment.)

## Active Modules Built
1. Autonomous B2B Lead Engine: Object-oriented Playwright scraper synced to an SQLite vault, orchestrated by APScheduler to generate daily CSV client deliverables.
2. Authenticated Ghost Browser: Injects credentials, captures session cookies (auth.json), and traverses gated servers.
3. Remote Job Vault: Scrapes live job boards and enforces unique data constraints with live timestamp syncing.
4. Book Catalog Crawler: Recursively handles pagination to extract complete product datasets including pricing and availability.

## Development Environment Setup
To run these systems locally:
1. Clone the repository.
2. Create a virtual environment: python -m venv .venv
3. Activate the environment.
4. Install dependencies: pip install -r requirements.txt
5. Note: Code quality is strictly enforced by Ruff.