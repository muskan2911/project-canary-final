# Project Canary Backend

FastAPI backend with ML-powered case classification and similarity detection.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and add your Supabase credentials

3. Run the server:
```bash
python main.py
```

The server will:
- Initialize the database with 500 fake cases (first run only)
- Start generating 5 new cases every 10 minutes
- Compute case similarities using ML

## API Endpoints

- `GET /api/stats` - Dashboard statistics
- `GET /api/cases` - All cases with optional filters
- `GET /api/cases/high-priority` - High priority cases
- `GET /api/cases/incidents` - Incident cases
- `GET /api/cases/open` - Open cases
- `GET /api/cases/{case_id}` - Get specific case
- `GET /api/cases/{case_id}/similar` - Get similar cases
- `POST /api/cases` - Create new case
- `GET /api/products` - List of products
- `GET /api/types` - List of case types
- `GET /api/priorities` - List of priorities
