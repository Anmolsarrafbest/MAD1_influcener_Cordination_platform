Influencer Engagement and Sponsorship Coordination Platform (IESCP)
📌 Overview

The Influencer Engagement and Sponsorship Coordination Platform (IESCP) is a web-based application built using Flask, Jinja2 + Bootstrap, and SQLite. It acts as a bridge between Sponsors and Influencers while providing oversight to Admins. Sponsors can create and manage campaigns, send ad requests, and monitor campaign performance. Influencers can search campaigns, accept/decline/renegotiate ad requests, and maintain a public profile. Admins have complete monitoring capabilities and can flag inappropriate activities.

The project has been designed to demonstrate full-stack web development concepts, role-based access, CRUD operations, and relational data handling.

🚀 Features
👨‍💻 Admin Role

Monitor all users, campaigns, and ad requests.

View application statistics (active campaigns, flagged users, public vs private campaigns, etc.).

Flag inappropriate campaigns and users.

💼 Sponsor Role

Create, update, and delete campaigns.

Send and manage ad requests for specific campaigns.

Search influencers by category, niche, or reach.

Track budget and campaign performance.

🎥 Influencer Role

Search public campaigns based on niche, relevance, and budget.

Accept, reject, or renegotiate ad requests.

Maintain and update a publicly visible profile.

Track collaborations and payment agreements.

🗂️ Database Schema (SQLite)

The core entities are:

Users Table (stores Admin, Sponsor, Influencer accounts with role-based field separation)

Campaigns Table (sponsor_id, name, description, goals, start_date, end_date, budget, visibility)

Ad Requests Table (campaign_id, influencer_id, requirements, payment_amount, status, messages)

Profiles Table (specific influencer details like niche, reach, followers)

🛠️ Tech Stack

Backend: Flask

Frontend: Jinja2, Bootstrap, HTML5, CSS3

Database: SQLite

Optional Libraries: Chart.js (for statistics visualization), flask_login (for authentication)

📊 Core Functionalities

User authentication and role-based login.

Campaign and ad request management (CRUD).

Search functionality (influencers, campaigns).

Negotiation and contract handling between sponsors and influencers.

Admin dashboard with statistics.
