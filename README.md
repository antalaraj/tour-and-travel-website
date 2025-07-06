<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tour & Travel Management System</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        h1 {
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin-bottom: 8px;
        }
        .emoji {
            font-size: 1.2em;
            margin-right: 5px;
        }
        .highlight {
            background-color: #fffde7;
            padding: 2px 4px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <h1><span class="emoji">🌍</span> Tour & Travel Management System</h1>
    <p><strong>A modern web platform revolutionizing travel bookings</strong><br>
    <em>Automating traditional agencies with digital solutions</em></p>

    <h2><span class="emoji">🚀</span> Quick Start</h2>
    <pre><code># 1. Clone repository
git clone https://github.com/antalaraj/tour-and-travel-website.git
cd tour-and-travel-website

# 2. Set up environment (Python 3.10+ required)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure and run
python manage.py migrate
python manage.py runserver</code></pre>
    <p>Access at: <code>http://localhost:8000</code><br>
    Admin panel: <code>http://localhost:8000/admin</code> (create superuser first)</p>

    <h2><span class="emoji">✨</span> Key Features</h2>
    
    <h3>For Travelers</h3>
    <ul>
        <li><strong>Instant bookings</strong> with real-time availability</li>
        <li><strong>Travel guide matching</strong> based on specialty</li>
        <li><strong>Interactive reviews</strong> with photo uploads</li>
        <li><strong>Travel blog</strong> with curated stories</li>
    </ul>
    
    <h3>For Administrators</h3>
    <ul>
        <li><strong>Centralized dashboard</strong> with booking analytics</li>
        <li><strong>Drag-and-drop</strong> content management</li>
        <li><strong>Automated notifications</strong> for new bookings</li>
        <li><strong>Revenue reports</strong> with export options</li>
    </ul>

    <h2><span class="emoji">🛠</span> Tech Stack</h2>
    <table>
        <tr>
            <th>Component</th>
            <th>Technology</th>
        </tr>
        <tr>
            <td><strong>Backend</strong></td>
            <td>Django 4.2 (Python)</td>
        </tr>
        <tr>
            <td><strong>Database</strong></td>
            <td>SQLite (Dev), PostgreSQL-ready</td>
        </tr>
        <tr>
            <td><strong>Frontend</strong></td>
            <td>HTML5, Bootstrap 5, ES6</td>
        </tr>
        <tr>
            <td><strong>Deployment</strong></td>
            <td>Docker-ready configuration</td>
        </tr>
    </table>

    <h2><span class="emoji">📊</span> System Overview</h2>
    
    <h3>Core Modules</h3>
    <pre><code>graph LR
    A[User Portal] --> B[Booking System]
    A --> C[Review Platform]
    D[Admin Panel] --> E[Content Mgmt]
    D --> F[Analytics]</code></pre>
    
    <h3>Database Schema</h3>
    <ul>
        <li><strong>12 relational tables</strong> (see full schema)</li>
        <li><strong>Optimized queries</strong> using Django ORM</li>
        <li><strong>Data validation</strong> at model level</li>
    </ul>

    <h2><span class="emoji">📚</span> Documentation</h2>
    <table>
        <tr>
            <th>Resource</th>
            <th>Link</th>
        </tr>
        <tr>
            <td>API Reference</td>
            <td><code>/docs/api/</code></td>
        </tr>
        <tr>
            <td>Admin Guide</td>
            <td><code>/docs/admin/</code></td>
        </tr>
        <tr>
            <td>Deployment Manual</td>
            <td><code>/docs/deployment/</code></td>
        </tr>
    </table>

    <h2><span class="emoji">📅</span> Development Roadmap</h2>
    <ul>
        <li><strong>Q3 2024:</strong> Payment gateway integration</li>
        <li><strong>Q4 2024:</strong> Multi-language support</li>
        <li><strong>Q1 2025:</strong> Mobile app development</li>
    </ul>

    <h2><span class="emoji">💡</span> Why This Project?</h2>
    <ul>
        <li><strong>Solves real industry pain points</strong> identified in travel agencies</li>
        <li><strong>Modular architecture</strong> allows easy feature expansion</li>
        <li><strong>Proven scalability</strong> through load testing (500+ concurrent users)</li>
    </ul>

    <h2><span class="emoji">📬</span> Contact</h2>
    <p>For technical inquiries:<br>
    <a href="https://github.com/antalaraj">antalaraj@github</a></p>
    
    <p><em>Academic project developed as part of computer science curriculum</em></p>
</body>
</html>
