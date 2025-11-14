from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

PRIORITIES = ['Low', 'Medium', 'High', 'Critical']
TYPES = ['Inquiry', 'Incident', 'Jira', 'Bug', 'Feature Request']
PRODUCTS = [
    'Cloud Platform', 'Analytics Dashboard', 'Mobile App',
    'API Gateway', 'Data Warehouse', 'CRM System',
    'E-commerce Platform', 'Payment Gateway', 'Messaging Service'
]
STATUSES = ['Open', 'In Progress', 'Resolved', 'Closed']
GEOGRAPHIES = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East', 'Africa']

VERB = [
    "login", "checkout", "submit", "update", "delete", "create", "view", "export", "import", "sync", "connect"
]

ISSUE_TEMPLATES = [
    "Unable to login to the system. Getting error message: {error}",
    "Payment processing failed for transaction {id}. Customer is unable to complete checkout.",
    "API endpoint {endpoint} returning 500 error intermittently.",
    "Dashboard not loading data correctly. Shows {error} instead of charts.",
    "Request for new feature: {feature}",
    "Database query performance is very slow for {operation}",
    "Mobile app crashes when {action}",
    "Security vulnerability found in {component}",
    "Customer reporting incorrect billing amount of ${amount}",
    "How do I configure {feature} in the system?",
    "Integration with {service} not working as expected",
    "Need documentation on how to use {feature}",
    "System experiencing high latency during {time}",
    "Data export functionality is broken for {format} format",
    "User interface has display issues on {device}",
]

def generate_case_id(index: int) -> str:
    return f"CASE-{index:05d}"

def generate_fake_case(index: int) -> dict:
    priority = random.choices(
        PRIORITIES,
        weights=[30, 40, 20, 10],
        k=1
    )[0]

    case_type = random.choice(TYPES)
    product = random.choice(PRODUCTS)
    status = random.choices(
        STATUSES,
        weights=[40, 30, 20, 10],
        k=1
    )[0]

    template = random.choice(ISSUE_TEMPLATES)
    description = template.format(
        error=fake.catch_phrase(),
        id=fake.uuid4()[:8],
        endpoint=f"/api/v1/{fake.word()}",
        feature=fake.bs(),
        operation=fake.word(),
        action=random.choice(VERB),
        component=fake.word(),
        amount=random.randint(10, 1000),
        service=fake.company(),
        time=fake.time(),
        format=random.choice(['CSV', 'JSON', 'XML', 'PDF']),
        device=random.choice(['mobile', 'tablet', 'desktop'])
    )

    days_ago = random.randint(0, 30)
    created_date = datetime.now() - timedelta(days=days_ago)

    return {
        'case_id': generate_case_id(index),
        'customer_name': fake.company(),
        'description': description,
        'priority': priority,
        'type': case_type,
        'product': product,
        'status': status,
        'geography': random.choice(GEOGRAPHIES),
        'created_date': created_date.isoformat()
    }

def generate_batch_cases(start_index: int, count: int) -> list:
    return [generate_fake_case(start_index + i) for i in range(count)]
