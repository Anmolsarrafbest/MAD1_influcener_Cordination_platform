# Influencer Engagement and Sponsorship Coordination Platform (IESCP)

## Overview
The Influencer Engagement and Sponsorship Coordination Platform (IESCP) is a web application that connects Sponsors with Influencers for advertising collaborations, while providing monitoring capabilities to an Admin.

- Sponsors can launch and manage campaigns, send ad requests, and track budgets.
- Influencers can search public campaigns, accept or reject ad requests, and negotiate terms.
- Admins oversee the entire platform, manage flagged content, and view statistics.

The platform is built using:
- Flask (Backend framework)
- Jinja2 + Bootstrap (Frontend templating and styling)
- SQLite (Database)

---

## User Roles

### Admin
- Root access to the platform
- View statistics (users, campaigns, ad requests)
- Flag inappropriate users/campaigns

### Sponsors
- Create, update, delete campaigns
- Set campaign budget, goals, and visibility (public/private)
- Search for influencers by category, reach, or niche
- Send, manage, and track ad requests

### Influencers
- Maintain a public profile (name, niche, reach, category)
- Search for ongoing public campaigns
- Accept, reject, or negotiate ad requests
- Collaborate with sponsors through contracts

---

## Database Schema

**Users**
- id, username, password, role (Admin/Sponsor/Influencer)

**Sponsors**
- sponsor_id, name, industry, budget

**Influencers**
- influencer_id, name, category, niche, reach

**Campaigns**
- campaign_id, sponsor_id, name, description, start_date, end_date, budget, visibility, goals

**Ad Requests**
- request_id, campaign_id, influencer_id, requirements, payment_amount, messages, status (Pending/Accepted/Rejected)

---

## Features
- Role-based login (Admin, Sponsor, Influencer)
- Campaign management (CRUD for sponsors)
- Ad request management (CRUD, negotiation support)
- Influencer and campaign search functionality
- Admin dashboard with statistics
- Flagging inappropriate content/users

---

## Tech Stack
- Backend: Flask  
- Frontend: Jinja2, Bootstrap, HTML5, CSS3  
- Database: SQLite  
- Optional Enhancements:
  - Chart.js for visual reports
  - flask_login for authentication

---

## Installation & Setup

1. Clone the repository
   ```bash
   git clone <repo_link>
   cd iescp
