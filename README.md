# 💸 Expense Splitter Backend (Split App)

This is a FastAPI-based backend application that helps users track shared expenses and calculate who owes whom — similar to Splitwise or Google Pay's bill split feature.

## 🚀 Features

- Add, update, and delete expenses with amount, description, and payer
- Automatically tracks participants from expenses (no manual user creation)
- Calculates balances: how much each person owes or is owed
- Generates simplified settlement summary (minimal transactions)
- RESTful API with full documentation at `/docs`

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Storage:** In-memory (no DB required for this demo)
- **API Testing:** Postman

---

## 📦 API Endpoints

### ➤ Expense Management
- `POST /expenses` – Add an expense
- `GET /expenses` – List all expenses
- `PUT /expenses/{id}` – Update an expense
- `DELETE /expenses/{id}` – Delete an expense

### ➤ Calculations
- `GET /balances` – Net amount owed/received per person
- `GET /settlements` – Optimized settlement transactions
- `GET /people` – List all people involved in expenses

---



## 💻 Local Development Setup

### ✅ Prerequisites
- Python 3.10+
- pip (Python package installer)
- Git

### 🧰 Setup Instructions

#### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/ExpenseSplitter.git
cd ExpenseSplitter
```

#### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the FastAPI server
```bash
uvicorn main:app --reload
```

#### 5. Open your browser
```
http://localhost:8000/docs
```
Use the Swagger UI to test all endpoints.

---

## 🧪 Testing the API with Postman

You can use the provided Postman Collection:  
🔗 [Postman Collection Gist](https://gist.github.com/your-link-here)

Base URL for deployed version:  
```
https://your-app-name.onrender.com
```
