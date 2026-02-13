# 🚀 FastAPI Todo Application (Full-Stack)

A robust, production-ready Todo management system built with **FastAPI**, featuring a secure backend, cloud database integration, and automated deployment.

## 🌟 Key Features
* **User Management:** Full Authentication & Authorization system (Register/Login).
* **Role-Based Access Control (RBAC):** Distinct permissions for `Users` and `Admins`.
* **Cloud Database:** Fully integrated with **Supabase (PostgreSQL)** via SQLAlchemy ORM.
* **Security:** Password hashing with `Bcrypt` and secure token generation using `JWT`.
* **Live Deployment:** Successfully deployed and hosted on **Railway.app**.
* **Interactive API Docs:** Built-in support for Swagger UI and ReDoc.

## 🛠️ Tech Stack
* **Language:** Python 3.13
* **Framework:** FastAPI
* **Database:** PostgreSQL (Supabase)
* **ORM:** SQLAlchemy
* **Authentication:** JWT (JSON Web Tokens)
* **Infrastructure:** Railway (CI/CD)
* **Testing:** Pytest

## 🛣️ API Endpoints

### Authentication & Users
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/users/register` | Create a new user account |
| POST | `/users/login` | Login and receive JWT access token |
| GET | `/users/login-page` | Render login frontend page |

### Todos Management
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/todos/` | Get all todos for current user |
| POST | `/todos/todo` | Create a new todo task |
| PUT | `/todos/todo/{todo_id}` | Update an existing task |
| DELETE | `/todos/todo/{todo_id}` | Remove a task |

### Admin Panel
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/admin/todo` | Access all users' todos (Admin Only) |
| DELETE | `/admin/todo/{todo_id}` | Delete any todo (Admin Only) |

## 🚀 Installation & Local Setup

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd TodoApp
