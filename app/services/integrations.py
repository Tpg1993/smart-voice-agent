from typing import List

def check_calendar_availability(business_id: str, date: str, service_type: str) -> List[str]:
    """
    Queries the local Postgres Database or an external CRM API
    to find open time slots for a business.
    """
    # TO-DO: Implement actual DB query using SQLAlchemy
    # session = SessionLocal()
    # slots = session.query(Slots).filter_by(business_id=business_id, date=date, status="AVAILABLE").all()
    # return [s.time for s in slots]
    
    print(f"Checking availability for {business_id} on {date} for {service_type}...")
    # Mock Response
    return ["10:00 AM", "1:30 PM", "3:00 PM"]

def create_booking(business_id: str, caller_number: str, date: str, time: str, service: str) -> str:
    """
    Commits a booking to the database or external CRM.
    """
    # TO-DO: Implement real DB commit
    print(f"Creating booking for {caller_number} at {business_id} on {date} @ {time} ({service})")
    return "BK_TEST_12345"
