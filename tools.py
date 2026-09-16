from langchain_core.tools import tool
from Database import book_interview, check_slot
from RAG import Use_RAG

@tool
def check_interview_slot(job:str, date:str, time:str)->str: 
    """Check if an interview slot is available for a given job, date, and time. Use this tool when the user asks about availability of a specific interview slot. Example: Is there an interview slot available for a Software Engineer on 2026-07-01 at 10:00:00? """
    result = check_slot(job, date, time)
    if result:
        return f"An interview slot is already taken for {job} on {date} at {time},please choose a new slot."
    else:
        return f"Yes interview slot is available for {job} on {date} at {time}."

@tool
def book_interview_slot(name:str,email:str,job:str,date:str,time:str)->str:
    """Book an interview slot for the user. Use this tool when the user has provided all required booking information"""
    result = book_interview(name, email, job, date, time)
    if result:
        return f"Your interview is sucessfully booked {job} on {date} at {time},Thankyou for Applying."
    else:
        return f"Sorry The interview slot is already bookede for {job} on {date} at {time}."

@tool
def company_policy_tool(query:str)->str:
    """Usw this tool to retrieve relevant information about the company form the company handbook for any question related to the company.Use this tool when the user asks any question related to the company fr company information, company policies, rules, benefits, working conditions,leave, remote work, working hours, or other information contained in the company handbook.Example: "What is the company policy on remote work?" or "What are the benefits offered by the company?"
    """
    return Use_RAG(query)
