# 11. Integration Tools & Customization

This document outlines the standard "Tools" (functions) that the Core Logic Engine (specifically the specialized industry agents) utilizes to interact with external systems. 

**Important Note on Current Implementation:**
Currently, all functions within the `app/services/integrations.py` file are **Mock/Static implementations**. They simulate database queries and CRM integration by returning hardcoded values (e.g., returning fixed available times or a fake booking ID). 

Before deploying to production, these static functions must be replaced with actual API calls or SQLAlchemy database queries to the respective services (e.g., Google Calendar API, Mindbody, Epic, Twilio).

---

## Expected Production Tool Calls

A robust Multi-Agent Voice System relies on the following categories of tool calls to be fully functional:

### 1. Scheduling & Calendar Tools
These tools manage appointments and resource availability.
* **`check_availability(business_id, date, service_type)`**: Queries the underlying database or external calendar (like Google Calendar API or Acuity) to find open time slots for a specific date and service.
* **`create_booking(business_id, caller_number, date, time, service)`**: Commits a new appointment to the database or CRM, effectively reserving the slot.
* **`cancel_booking(booking_id, caller_number)`**: Cancels an existing appointment, freeing up the resource.
* **`reschedule_booking(booking_id, new_date, new_time)`**: Modifies the time/date of an existing appointment.

### 2. Information Retrieval Tools
These tools fetch dynamic data to provide accurate answers to the caller.
* **`get_service_menu(business_id)`**: Fetches the list of offered services and their current prices (e.g., pulling the cost of a haircut, or pulling the current night's rate for a hotel room).
* **`lookup_customer_profile(caller_number)`**: Checks if the caller is a returning customer (based on phone number) to pull up their history and preferences. This enables personalized greetings (e.g., "Welcome back John, do you want your usual haircut?"). 
* **`get_faqs(query)`**: Dynamically fetches answers to common questions from a knowledge base or vector database (e.g., QA retreival for "What are your visiting hours?").

### 3. Action & Handoff Tools
These tools perform actions that affect the call flow or trigger external communications.
* **`send_sms_link(caller_number, link_type)`**: Triggers a text message to the caller during or immediately after the call. Examples include texting a secure Stripe payment link to reserve a hotel room, or texting a Google Maps link for a Real Estate site visit.
* **`escalate_to_human(call_id, reason)`**: A critical tool the AI can call if the user is angry, frustrated, or asks a highly complex question that the agent is not programmed to answer (e.g., complex medical advice). This tool signals the PBX (Twilio/Asterisk) to immediately transfer the active call stream to a live receptionist.

## Replacing Static Mocks

To implement a real integration, simply rewrite the body of the function in `integrations.py`.

**Example: Replacing Static Availability with Google Calendar:**

*Current Static Implementation:*
```python
def check_calendar_availability(business_id: str, date: str, service_type: str, industry: str = "general") -> List[str]:
    # ... mock logic ...
    return ["10:00 AM", "1:30 PM", "3:00 PM"]
```

*Future Implementation (Conceptual):*
```python
def check_calendar_availability(business_id: str, date: str, service_type: str, industry: str = "general") -> List[str]:
    # 1. Look up the Google Calendar ID for the business_id
    # 2. Authenticate with Google Calendar API
    # 3. Query freeBusy endpoint for the given date
    # 4. Calculate available slots based on service duration rules
    # 5. Return list of available times strings
    pass
```
