Influencer Engagement and Sponsorship Coordination Platform (IESCP)
Overview
The Influencer Engagement and Sponsorship Coordination Platform (IESCP) is a web application designed to connect sponsors and influencers. Sponsors can advertise products/services via influencer campaigns, and influencers benefit monetarily by participating in ad campaigns. This project has three roles: Admin, Sponsor, and Influencer, each with specific dashboards and workflows.

Project built with Flask (Python)

Uses Jinja2 templates and Bootstrap for responsive frontend

Data stored in SQLite database

All features run locally and do not require external hosting.

Features
User Roles
Admin: Oversees platform activity, can flag users/campaigns, view statistics

Sponsor: Creates and manages campaigns, sends/accepts ad requests, tracks budgets

Influencer: Receives/negotiates ad requests, manages their public profile, searches for campaigns

Core Functionality
Login and user registration for all roles

Admin dashboard showing user, campaign, ad request statistics

Campaign management (create, edit, delete, public/private)

Ad request lifecycle management (create, edit, accept, reject, negotiate)

Search influencers/campaigns by niche, reach, budget

Influencers can update their own profiles

Data Model
Users: Role-based (Admin, Sponsor, Influencer)

Campaigns: Budget, description, goals, visibility, time window

AdRequests: Linked to campaigns & influencers, tracks negotiation, status, payment

Influencer Profiles: Niche, category, reach/followers, public info

Frameworks and Libraries Used
Flask: Main application framework

Flask-Jinja2: HTML template rendering

Bootstrap: CSS styling and responsive design

SQLite: Relational data storage

(Optional) ChartJS for displaying stats visually

Running the App
Clone the repository and unzip in one folder.

Install requirements:

text
pip install flask
Start the application:

text
python app.py
Open http://localhost:5000 in your web browser to use the platform.

Demo logins are provided for each role.

Database Design (ER Diagram)
User Table: user_id, role, username, password, (plus profile fields for sponsors/influencers)

Campaign Table: campaign_id, sponsor_id, name, description, start_date, end_date, budget, visibility, goals

AdRequest Table: request_id, campaign_id, influencer_id, messages, requirements, payment_amount, status

Influencer Table: influencer_id, name, category, niche, reach

(Relationships: Sponsors create campaigns; Influencers receive ad requests; Admin can flag users/campaigns.)

API Resource Endpoints (if implemented)
/api/users (GET, POST)

/api/campaigns (GET, POST, PUT, DELETE)

/api/adrequests (GET, POST, PUT, DELETE)

Project Submission
Code is present in this zip file; report is inside as ProjectReport.pdf.

Please refer to the drive link in the report for the presentation video.

All demo and instructions follow the guidelines provided.

