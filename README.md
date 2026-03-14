# 🚀 Building in Six Months: AI Automation & Micro-SaaS Sprint

## 🎯 The Mission
This repository documents a high-intensity, 6-month sprint focused exclusively on building production-ready AI automation systems, data extraction tools, and Micro-SaaS backends. 

The core philosophy of this project is **Execution over Theory**. Every script and application built here is designed to solve real-world business problems, automate tedious workflows, and operate reliably in production environments.

## 🛠️ Tech Stack & Focus Areas
* **Language:** Python 3.10+
* **Data Extraction:** BeautifulSoup, Playwright, HTTP Sessions
* **Backend & APIs:** FastAPI, RESTful architecture
* **Database:** SQLite (Local), PostgreSQL (Production)
* **AI Integration:** OpenAI/Anthropic APIs, LangChain, RAG Systems
* **Deployment:** Docker, GitHub Actions, Cloud VPS

## 📅 Architecture & Progress

The repository is structured chronologically to demonstrate daily execution and progressive system complexity.

### Month 1: The Automation & Extraction Engine
* **Week 1: Advanced OOP Python and core scraping architecture.**
    * *Status:* 🟢 Completed
    * *Key Build:* Resilient, class-based `LeadExtractor` using custom sessions and headers to bypass basic bot-detection.
* **Week 2: Web Scraping Mastery.** * *Status:* 🟢 Completed
    * *Key Build:* Dynamic data extraction utilizing Playwright. Bypassing basic anti-bot systems, handling asynchronous loading, and traversing pagination across catalog sites.

### Month 2: Bots, Alerts, and Interfaces
*(Scheduled: Telegram/Discord integrations and scheduled Cron jobs with APScheduler and Logging)*

### Month 3: Building the Micro-SaaS Backend
*(Scheduled: FastAPI endpoints, Authentication, and Stripe payment integration)*

### Month 4: Agentic AI & Smart Systems
*(Scheduled: Connecting extraction engines to LLMs for autonomous decision-making)*

### Month 5: Deployment & MLOps
*(Scheduled: Dockerization and live server deployment)*

## 📂 Active Modules Built
1.  **Hacker News Lead Extractor:** Target acquisition and HTML parsing.
2.  **Authenticated Ghost Browser:** Injects credentials, captures session cookies (`auth.json`), and traverses gated servers.
3.  **Remote Job Vault:** Scrapes live job boards and enforces unique data constraints within an SQLite database.
4.  **Book Catalog Crawler:** Recursively handles pagination to extract complete product datasets including pricing and availability.

## ⚙️ Development Environment Setup
To run these systems locally:
1.  Clone the repository.
2.  Create a virtual environment: `python -m venv .venv`
3.  Activate the environment.
4.  Install dependencies: `pip install -r requirements.txt`
5.  *Code quality enforced by Ruff (line-length = 100)*