# Azure Flask Media Storage Application

## 📌 Overview
The **Azure Flask Media Storage Application** is a secure web-based solution for uploading, storing, viewing, and managing media files (photos, videos, documents) using **Azure App Service** and **Azure Blob Storage**.  
It includes **Microsoft Entra ID (Azure AD)** authentication via **MSAL** to ensure only authorized users can access the application.

---

## ✨ Features
- Azure AD Authentication using MSAL
- Upload media files to Azure Blob Storage
- Auto-renaming of files to avoid name conflicts
- List uploaded files with metadata
- Download stored files
- Delete files from storage
- Simple, clean UI for quick access

---

## 🏗 Architecture
**Frontend:** HTML + Jinja2 templates  
**Backend:** Flask (Python)  
**Authentication:** Microsoft Entra ID (Azure AD) via MSAL  
**Storage:** Azure Blob Storage  
**Hosting:** Azure App Service

---

## 📂 Project Structure

- `auth/`                  → Authentication Blueprint  
  - `__init__.py`  
  - `routes.py`  
- `templates/`             → HTML templates  
  - `index.html`  
  - `upload.html`  
  - `layout.html`  
- `static/`                → CSS, JS, and image files  
- `requirements.txt`       → Python dependencies  
- `run.py`                 → Main Flask application entry point  
- `config.py`              → Configuration (environment variables, Azure setup)  
- `README.md`              → Project documentation

---

## ⚙️ Prerequisites
Before running this project, make sure you have:

- Python 3.8+
- Azure Subscription
- Azure Blob Storage account
- Azure App Registration (Microsoft Entra ID)
- Azure App Service for deployment

---

## 🚀 Local Setup

### 1. Clone the repository

bash
git clone https://github.com/<your-username>/Azure-media-storage-container.git
cd Azure-media-storage-container

### 2. Create a virtual environment

bash
- python -m venv venv

#### Mac/Linux

- source venv/bin/activate

#### Windows

- venv\Scripts\activate


### 3. Install dependencies 

Bash
- pip install -r requirements.txt

### 4. Set environment variables

#### Mac/Linux

Bash
- export CLIENT_ID="your-azure-client-id"
- export CLIENT_SECRET="your-azure-client-secret"
- export AUTHORITY="https://login.microsoftonline.com/<your-tenant-id>"
- export REDIRECT_PATH="/getAToken"
- export SCOPE="User.Read"
- export SESSION_TYPE="filesystem"
- export AZURE_STORAGE_CONNECTION_STRING="your-storage-connection-string"
- export AZURE_STORAGE_CONTAINER_NAME="your-container-name"

#### Windows PowerShell

Bash
- set CLIENT_ID=your-azure-client-id
- set CLIENT_SECRET=your-azure-client-secret
- set AUTHORITY=https://login.microsoftonline.com/<your-tenant-id>
- set REDIRECT_PATH=/getAToken
- set SCOPE=User.Read
- set SESSION_TYPE=filesystem
- set AZURE_STORAGE_CONNECTION_STRING=your-storage-connection-string
- set AZURE_STORAGE_CONTAINER_NAME=your-container-name


### 5. Run the application locally

Bash
- python run.py

---

## 🌐 Deployment to Azure App Service

- Push your code to GitHub.
- Create an Azure App Service and connect it to your repository.
- Configure Environment Variables in Azure App Service → Configuration.
- Deploy the application via VS Code Azure extension or GitHub Actions.
- Access the application using the Azure-provided URL.

---

## 🔮 Future Improvements

- In-browser document preview
- File usage analytics
- Mobile-friendly responsive UI
- Multi-container support for different media types
  
📝 License

This project is licensed under the MIT License.
