from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
from database import Database
from ml_model import CaseClassifier, SimilarityDetector
from fake_data_generator import generate_batch_cases
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Project Canary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()
classifier = CaseClassifier()
similarity_detector = SimilarityDetector()

class CaseCreate(BaseModel):
    customer_name: str
    description: str
    product: str
    priority: Optional[str] = "Medium"
    status: Optional[str] = "Open"
    geography: Optional[str] = "North America"

class DashboardStats(BaseModel):
    total_cases: int
    high_priority: int
    incidents: int
    open_cases: int

def classify_and_process_case(case_data: dict) -> dict:
    case_type = classifier.classify_type(case_data['description'])
    module, sub_module = classifier.classify_module(case_data['description'])
    category = classifier.assign_category(case_type, case_data['priority'])

    case_data['type'] = case_type
    case_data['module'] = module
    case_data['sub_module'] = sub_module
    case_data['category'] = category

    return case_data

def compute_similarities_for_case(case_id: str, case_description: str):
    try:
        all_cases = db.get_all_cases()
        if len(all_cases) > 1:
            similarity_detector.fit(all_cases)
            similar_cases = similarity_detector.find_similar(case_description, case_id, top_k=3)

            db.delete_similarities_for_case(case_id)

            for related_id, score in similar_cases:
                if score > 0.1:
                    db.insert_similarity(case_id, related_id, score)
    except Exception as e:
        logger.error(f"Error computing similarities: {e}")

def generate_and_insert_cases():
    try:
        logger.info("Generating new fake cases...")
        current_count = db.get_case_count()
        new_cases = generate_batch_cases(current_count + 1, 5)

        processed_cases = []
        for case in new_cases:
            processed_case = classify_and_process_case(case)
            processed_cases.append(processed_case)

        inserted_cases = db.insert_cases_batch(processed_cases)
        logger.info(f"Inserted {len(inserted_cases)} new cases")

        for case in inserted_cases:
            compute_similarities_for_case(case['id'], case['description'])

    except Exception as e:
        logger.error(f"Error generating cases: {e}")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Project Canary API...")

    try:
        case_count = db.get_case_count()
        if case_count == 0:
            logger.info("Initializing database with 500 fake cases...")
            initial_cases = generate_batch_cases(1, 500)

            processed_cases = []
            for case in initial_cases:
                processed_case = classify_and_process_case(case)
                processed_cases.append(processed_case)

            batch_size = 100
            for i in range(0, len(processed_cases), batch_size):
                batch = processed_cases[i:i+batch_size]
                db.insert_cases_batch(batch)
                logger.info(f"Inserted batch {i//batch_size + 1}")

            logger.info("Computing similarities...")
            all_cases = db.get_all_cases()
            if all_cases:
                similarity_detector.fit(all_cases)
                for case in all_cases[:100]:
                    similar_cases = similarity_detector.find_similar(case['description'], case['id'], top_k=3)
                    for related_id, score in similar_cases:
                        if score > 0.1:
                            db.insert_similarity(case['id'], related_id, score)

            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")

    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_and_insert_cases, 'interval', minutes=10)
    scheduler.start()
    logger.info("Scheduled job for generating cases every 10 minutes")

@app.get("/")
async def root():
    return {"message": "Project Canary API", "status": "running"}

@app.get("/api/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    try:
        stats = db.get_dashboard_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cases")
async def get_cases(
    customer_name: Optional[str] = Query(None),
    case_id: Optional[str] = Query(None),
    product: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    try:
        if status:
            cases = db.get_cases_by_status(status)
        elif any([customer_name, case_id, product, priority, type]):
            cases = db.search_cases(customer_name, case_id, product, priority, type)
        else:
            cases = db.get_all_cases()

        return {"cases": cases, "count": len(cases)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cases/high-priority")
async def get_high_priority_cases():
    try:
        high = db.get_cases_by_priority('High')
        critical = db.get_cases_by_priority('Critical')
        cases = critical + high
        return {"cases": cases, "count": len(cases)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cases/incidents")
async def get_incidents():
    try:
        cases = db.get_cases_by_type('Incident')
        return {"cases": cases, "count": len(cases)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cases/open")
async def get_open_cases():
    try:
        cases = db.get_cases_by_status('Open')
        return {"cases": cases, "count": len(cases)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cases/{case_id}")
async def get_case(case_id: str):
    try:
        case = db.get_case_by_id(case_id)
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        return case
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cases/{case_id}/similar")
async def get_similar_cases(case_id: str):
    try:
        similar = db.get_similar_cases(case_id, limit=3)
        return {"similar_cases": similar, "count": len(similar)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cases")
async def create_case(case: CaseCreate):
    try:
        case_dict = case.dict()
        processed_case = classify_and_process_case(case_dict)

        current_count = db.get_case_count()
        processed_case['case_id'] = f"CASE-{current_count + 1:05d}"

        inserted_case = db.insert_case(processed_case)

        compute_similarities_for_case(inserted_case['id'], inserted_case['description'])

        return inserted_case
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products")
async def get_products():
    try:
        all_cases = db.get_all_cases()
        products = list(set(case['product'] for case in all_cases))
        return {"products": sorted(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/types")
async def get_types():
    return {"types": ["Inquiry", "Incident", "Jira", "Bug", "Feature Request"]}

@app.get("/api/priorities")
async def get_priorities():
    return {"priorities": ["Low", "Medium", "High", "Critical"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
