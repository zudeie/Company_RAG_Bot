from tools import check_interview_slot ,book_interview_slot
from tools import company_policy_tool

print(
    check_interview_slot.invoke({
        "job":"Software Engineer",
        "date":"2026-07-01",
        "time":"10:00:00"}
    ))

print(
    company_policy_tool.invoke("What is the company policy on remote work?")
)