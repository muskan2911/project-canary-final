# Project Canary - AI-Powered Case Management Dashboard

A full-stack application that uses AI/ML to detect customer issues, sentiment shifts, and anomalies across customers, products, and geographies.

## Features

- **AI-Powered Classification**: Automatically classifies cases into types (Inquiry, Incident, Bug, Jira, Feature Request)
- **Smart Similarity Detection**: Finds related cases using TF-IDF and cosine similarity
- **Real-time Updates**: Live dashboard updates as new cases arrive
- **Responsive Design**: Fully responsive UI with sliding tabs and panels
- **Advanced Filtering**: Search and filter by customer, case ID, product, priority, type, and status
- **Auto-Grouping**: New cases automatically categorized into modules and sub-modules
- **Cron Job**: Generates 5 new fake cases every 10 minutes

## Architecture

### Frontend (React + TypeScript + Tailwind CSS)
- Real-time dashboard with Supabase subscriptions
- Responsive sliding tabs for case categories
- Advanced filtering and search
- Related cases panel with similarity scores
- Modern, clean UI design

### Backend (FastAPI + Python)
- ML-based case classification
- TF-IDF + cosine similarity for finding related cases
- APScheduler for generating cases every 10 minutes
- RESTful API with full CORS support

### Database (Supabase PostgreSQL)
- Stores cases and case similarity relationships
- Row Level Security (RLS) enabled
- Real-time subscriptions for live updates

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Supabase account (already configured)

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. The environment variables are already configured in `.env`

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5173

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a `.env` file with your Supabase credentials:
```bash
cp .env.example .env
```

3. Edit `.env` and add:
```
SUPABASE_URL=https://bjkcbevvldicikwuzzar.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<your_service_role_key>
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Start the FastAPI server:
```bash
python main.py
```

Or use the start script:
```bash
./start.sh
```

The backend will be available at http://localhost:8000

## Database

The database schema includes:

### Cases Table
- Stores all customer support cases
- Auto-classified by type, module, and category
- Includes priority, status, and product information

### Case Similarity Table
- Pre-computed similarity relationships
- Updated automatically when new cases arrive
- Top 3 similar cases per case

## API Endpoints

- `GET /api/stats` - Dashboard statistics
- `GET /api/cases` - All cases with optional filters
- `GET /api/cases/high-priority` - High priority cases
- `GET /api/cases/incidents` - Incident cases
- `GET /api/cases/open` - Open cases
- `GET /api/cases/{case_id}` - Get specific case
- `GET /api/cases/{case_id}/similar` - Get similar cases
- `POST /api/cases` - Create new case

## How It Works

1. **Initial Data Load**: On first run, backend generates 500 fake cases
2. **ML Classification**: Each case is classified by:
   - Type (Inquiry, Incident, Bug, Jira, Feature Request)
   - Module (Authentication, Payment, API, Database, etc.)
   - Category (P0-P3 priority levels)
3. **Similarity Detection**: TF-IDF vectorization + cosine similarity finds related cases
4. **Auto-Grouping**: New cases automatically subdivided into appropriate categories
5. **Cron Job**: Every 10 minutes, 5 new cases are generated and processed
6. **Real-time UI**: Frontend subscribes to database changes and updates live

## Key Technologies

- **Frontend**: React, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: FastAPI, scikit-learn, Faker, APScheduler
- **Database**: Supabase (PostgreSQL)
- **ML**: TF-IDF Vectorization, Cosine Similarity

## Production Deployment

### Frontend
```bash
npm run build
```
Deploy the `dist` folder to any static hosting service.

### Backend
Deploy to any Python hosting service that supports FastAPI:
- Railway
- Render
- Heroku
- AWS/GCP/Azure

Make sure to set environment variables for Supabase credentials.

## Notes

- The backend automatically initializes with 500 cases on first run
- New cases are generated every 10 minutes
- Similar cases are computed automatically for each new case
- The UI updates in real-time using Supabase subscriptions
- All case data is stored in Supabase PostgreSQL
