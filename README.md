# 🚀 Telegram Authentication Project

A **full-stack web application** that enables users to authenticate with their **Telegram account via phone number**.
It supports the complete Telegram login flow, including **two-factor authentication (2FA)**.

---

## ✨ Features

* **📱 Phone Number Login** — users enter their phone number and receive a verification code directly in Telegram.
* **🔐 2FA Support** — handles accounts protected by Telegram password-based two-factor authentication.
* **🧠 Secure Session Storage** — Telegram session strings are **encrypted using Fernet (symmetric encryption)** before saving to the database.
* **🚫 Rate Limiting** — protects the API from brute-force attacks.
* **⚡ Asynchronous Backend** — built with **FastAPI** and **async SQLAlchemy** for high performance.

---

## 🛠️ Tech Stack

| Layer                     | Technology                                         |
| ------------------------- | -------------------------------------------------- |
| **Backend**               | FastAPI, Telethon, SQLAlchemy (async), Pydantic    |
| **Frontend**              | React + Vite                                       |
| **Database**              | PostgreSQL                                         |
| **Cache**                 | Redis                                              |
| **Containerization**      | Docker & Docker Compose                            |

---

## 🧩 Project Structure

```
telegram-auth-project/
├── backend/          # FastAPI application
├── frontend/         # React + Vite client
├── .dockerignore
├── docker-compose.yml
├── .gitignore
├── .env.example
└── README.md
```

---

## ⚙️ Getting Started

### Step 1. Prerequisites

* Install **Docker** and **Docker Compose**
  → [Get Docker](https://www.docker.com/get-started)
* Obtain **Telegram API credentials**:

  1. Go to [my.telegram.org](https://my.telegram.org)
  2. Log in to your account
  3. Open **API development tools**
  4. Create a new app — you’ll get `api_id` and `api_hash`

---

### Step 2. Setup

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/VoranReygetov/telegram-auth-project.git
cd telegram-auth-project
```

#### 2️⃣ Create the Environment File

Duplicate `.env.example` and rename it to `.env`:

```bash
cp .env.example .env
```

#### 3️⃣ Fill in the Values

* `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`: your Telegram credentials
* `SECRET_KEY`: generate a secure JWT key

  ```bash
  openssl rand -hex 32
  ```
* `ENCRYPTION_KEY`: generate a Fernet key

  ```bash
  python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
  ```

---

### Step 3. Run the Application with Docker

Build and start all services:

```bash
docker-compose up --build
```

Once running:

* 🖥️ **Frontend:** [http://localhost:5173](http://localhost:5173)

---

### Step 4. Stopping the Application

To stop all running containers:

```bash
docker-compose down
```

---

## 📡 API Endpoints

| Method | Endpoint                | Description                                          |
| ------ | ----------------------- | ---------------------------------------------------- |
| `POST` | `/api/auth/send-code`   | Sends a verification code to a Telegram phone number |
| `POST` | `/api/auth/verify-code` | Verifies the code and logs in the user               |
| `POST` | `/api/auth/verify-2fa`  | Completes login for accounts with 2FA enabled        |

---

## 🧱 Additional Notes

* All sensitive data (like session strings) are **encrypted** before saving.
* Default frontend address (for local development):
  👉 **[http://localhost:5173](http://localhost:5173)**

