# Azure Flask Media Storage Application

## 📌 Overview
The **Azure Flask Media Storage Application** is a secure web-based solution to upload, store, view, and manage media files (photos, videos, documents) using **Azure App Service** and **Azure Blob Storage**.  
It includes **Microsoft Entra ID (Azure AD)** authentication via **MSAL** to ensure only authorized users can access the application.

---

## ✨ Features
- 🔐 **Azure AD Authentication** using MSAL
- 📤 Upload media files to Azure Blob Storage
- 📄 Auto-renaming of files to avoid name conflicts
- 📋 List uploaded files with metadata
- 📥 Download stored files
- ❌ Delete files from storage
- 🛠 Basic, clean UI for quick access

---

## 🏗 Architecture
**Frontend:** HTML + Jinja2 templates  
**Backend:** Flask (Python)  
**Authentication:** Microsoft Entra ID (Azure AD) via MSAL  
**Storage:** Azure Blob Storage  
**Hosting:** Azure App Service

---

## 📂 Project Structure
Azure-media-storage-container/
│
├── auth/ # Authentication Blueprint
│ ├── init.py
│ └── routes.py
│
├── templates/ # HTML templates
│ ├── index.html
│ ├── upload.html
│ └── ...
│
├── static/ # CSS, JS, and image files
│
├── requirements.txt # Python dependencies
├── run.py # Main Flask application entry point
├── config.py # Configuration (environment variables, Azure setup)
└── README.md # Project documentation


---

## ⚙️ Prerequisites
- **Python 3.8+**
- **Azure Subscription**
- **Azure Blob Storage account**
- **Azure App Registration** (Microsoft Entra ID)
- **Azure App Service** for deployment

---

## 🚀 Local Setup

1️⃣ **Clone the repository**  
```bash
git clone https://github.com/<your-username>/Azure-media-storage-container.git
cd Azure-media-storage-container

2️⃣ **Clone the repository**

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Set environment variables (replace with your values)
Mac/Linux

export CLIENT_ID="your-azure-client-id"
export CLIENT_SECRET="your-azure-client-secret"
export AUTHORITY="https://login.microsoftonline.com/<your-tenant-id>"
export REDIRECT_PATH="/getAToken"
export SCOPE="User.Read"
export SESSION_TYPE="filesystem"

export AZURE_STORAGE_CONNECTION_STRING="your-storage-connection-string"
export AZURE_STORAGE_CONTAINER_NAME="your-container-name"


Windows PowerShell

set CLIENT_ID=your-azure-client-id
set CLIENT_SECRET=your-azure-client-secret
set AUTHORITY=https://login.microsoftonline.com/<your-tenant-id>
set REDIRECT_PATH=/getAToken
set SCOPE=User.Read
set SESSION_TYPE=filesystem

set AZURE_STORAGE_CONNECTION_STRING=your-storage-connection-string
set AZURE_STORAGE_CONTAINER_NAME=your-container-name


5️⃣ Run locally

python run.py


🌐 Deployment to Azure App Service

Push code to your GitHub repository

Create an Azure App Service and connect to your repo

Configure environment variables in Azure App Service → Configuration

Deploy using VS Code Azure extension or GitHub Actions

Access your app via the Azure-provided URL

🔮 Future Improvements

📑 In-browser document preview

📊 File usage analytics

📱 Mobile-friendly responsive UI

🗄 Multi-container support for different media types

📝 License

This project is licensed under the MIT License.
