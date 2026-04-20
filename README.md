# 🔐 Team Password Manager

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Cryptography](https://img.shields.io/badge/Cryptography-AES--256-red.svg)](https://cryptography.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Enterprise-grade shared credential management system for teams**  
> *Stop sharing passwords via Telegram, Slack, or sticky notes*

---

---

## 📋 **Table of Contents**
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Security Architecture](#-security-architecture)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 **Overview**

**Team Password Manager** is a secure, enterprise-ready web application that solves the critical problem of shared credential management in organizations. Instead of passing passwords through insecure channels like email or chat, teams can centrally store, organize, and control access to all their credentials.

### **Problem We Solve**
- ❌ Passwords shared via Telegram/Slack/Email
- ❌ Password reuse across multiple services
- ❌ No visibility into who has access to what
- ❌ Security breaches due to poor password hygiene
- ❌ No audit trail or backup mechanism

### **Our Solution**
- ✅ **AES-256 encrypted** vault with master password
- ✅ **Real-time password reuse detection**
- ✅ **Tag-based organization** (by department/project)
- ✅ **Built-in password generator** with strength analysis
- ✅ **One-click copy** without exposing passwords
- ✅ **JSON export** for disaster recovery

---

## ✨ **Key Features**

### **Core Security**
| Feature | Description |
|---------|-------------|
| 🔒 **AES-256 Encryption** | All credentials encrypted before storage |
| 🗝️ **Master Password** | Single password unlocks entire vault |
| 🔐 **Auto-lock** | Session expires on browser close |
| 🛡️ **Password Reuse Detection** | Alerts if same password used elsewhere |

### **User Experience**
| Feature | Description |
|---------|-------------|
| 🎨 **Modern UI** | Gradient design with smooth animations |
| 🔍 **Search & Filter** | Instant search across all fields |
| 🏷️ **Tag System** | Organize by department (Marketing, Engineering, etc.) |
| 📋 **One-Click Copy** | Copy username/password without displaying |
| 📊 **Password Strength** | Visual indicator (Weak/Fair/Strong) |

### **Enterprise Features**
| Feature | Description |
|---------|-------------|
| 📤 **Export Backup** | Download encrypted JSON backup |
| 🔄 **CRUD Operations** | Full create/read/update/delete functionality |
| 🎯 **Empty State Guides** | First-time user onboarding |
| 🚀 **Password Generator** | Configurable length & character types |

### **Bonus Feature** ⭐
> **Password Reuse Detection & Alert System**  
> When saving a password, the system checks all existing credentials and warns if the same password is used elsewhere. Critical for preventing credential stuffing attacks.

---

## 🛠️ **Technology Stack**

### **Backend**
-🐍 Python 3.8+ - Core language
-🌶️ Flask 2.3.3 - Web framework
-🔐 Cryptography - AES-256 encryption
-🗄️ SQLite3 - Lightweight database

### **Frontend**
-🎨 HTML5/CSS3 - Responsive design
-✨ Vanilla JavaScript - No frameworks (pure JS)
-🎭 Flexbox/Grid - Modern layouts


---

## 💻 **Installation**

### **Prerequisites**
- Python 3.8 or higher
- pip package manager
- Git (optional)

# 🧭 To‘liq Ketma-ketlik (Detailed Setup)

### 1️⃣ Repositoryni klon qiling

```bash
git clone https://github.com/maqsud571/Password-Manager.git
cd Password-Manager
```
### 1️⃣ Muhitni yaratib olish
```
pip install -r requirements.txt
```
### 2️⃣ Loyihani ishga tushirish
```
python app.py
```
### 3️⃣ Mahalliy URL'lar
```
http://localhost:5000
```
