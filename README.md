# ForumAPP

Project Description

The Forum System API is a RESTful API designed for a forum platform, enabling users to interact through topics, replies, messages, and categories, with administrative controls for managing content and access. The API supports a range of functionalities, from user authentication and topic creation to private category management and voting on replies. It is built to be consumed by various clients, ensuring flexibility and scalability.

Key Features:

Users: Register, log in, create topics/replies, send messages, and vote on replies.

Administrators: Manage users, categories, topics, and access permissions.

Core Resources: Users, Topics, Categories, Replies, and Messages.

Authentication: Token-based access for secure endpoints.

Flexibility: Supports search, sort, pagination, and private category controls.

## Database ![image](https://github.com/user-attachments/assets/de596e70-d3fe-4684-87f9-cd78d6611418)

## Database ![Database Schema Diagram](/static/images/Database_schema.png)

## Web Interface (Jinja2 Templates)

   The application includes a responsive web interface using Jinja2:
   
| Page                    | URL                         | Purpose                                  |
|-------------------------|-----------------------------|-------------------------------------------|
| Home                    | `/`                         | Welcome page and entry to the forum       |
| Register                | `/users/register`           | User registration                         |
| Login                   | `/users/login`              | Login + access token display              |
| Dashboard               | `/users/dashboard`          | User panel + admin panel access           |
| Topics                  | `/topics/`                  | View, filter, and create topics           |
| Topic Details           | `/topics/{id}`              | View topic with replies and vote          |
| Categories              | `/categories/`              | View and create categories                |
| Admin Panel             | `/admin`                    | Manage category access (admins only)      |
| Messages                | `/messages/`                | Private chat system with search           |

------
## Templates Included
| Template File           | Description                                        |
|-------------------------|----------------------------------------------------|
| `base.html`             | Layout and navigation bar                          |
| `home.html`             | Landing page with CTA buttons                      |
| `dashboard.html`        | User dashboard                                     |
| `topics.html`           | All topics + search/filter                         |
| `topic.html`            | Topic details, replies, voting, best reply         |
| `create_topic.html`     | Create new topic                                   |
| `categories.html`       | All categories with search/sort                    |
| `create_category.html`  | Create new category (with privacy option)          |
| `category_detail.html`  | View category and its topics                       |
| `messages.html`         | Chat interface, real-time-like                     |
| `admin_panel.html`      | Manage access to categories                        |
| `manage_access.html`    | Grant/revoke user access to private categories     |
| `login.html` / `register.html` | Authentication forms                       |
| `error.html`            | Reusable error page with GIF                       |

---

## Techologies
- **FastAPI** - RESTful backend
- **Jinja2** - Web template rendering
- **MariaDB** - Database
- **JWT** - Auth token
- **bcrypt** - Password hashing
- **CSS** - Custom styling

## Run Locally
   
1. Run the server:
     ```bash
     uvicorn main:app --reload
2. Open in browser:
   ```bash
   http://localhost:8000/
3. Access API Docs:
   ```bash
   http://localhost:8000/docs

## Project structure
```
Forum-app/
  ├── common/             # Auth logic
  ├── routers/            # API and web routes
  ├── templates/          # Jinja2 templates (HTML)
  ├── static/             # CSS / images
  ├── services/           # Business logic
  ├── data/               # Models and DB layer
  ├── main.py             # FastAPI entry point
  └── README.md
```
---
## Database schema location

FORUM-APP/data/Forum_App_schema.sql


## Authors:
Created by Uasim Halak, Dimitur Boychew, Ivan Pustovit


