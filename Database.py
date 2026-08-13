import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def check_slot(job, date, time):

    with engine.connect() as db:

        result = db.execute(
            text("""
                SELECT *
                FROM interview_bookings
                WHERE job = :job
                AND date = :date
                AND time = :time
            """),
            {
                "job": job,
                "date": date,
                "time": time
            }
        )

        return result.fetchone()


def book_interview(name, email, job, date, time):

    check = check_slot(job, date, time)

    if check:
        return False

    with engine.begin() as db:

        db.execute(
            text("""
                INSERT INTO interview_bookings
                (name, email, job,date,time)
                VALUES
                (:name, :email, :job, :date, :time)
            """),
            {
                "name": name,
                "email": email,
                "job": job,
                "date": date,
                "time": time
            }
        )

    return True

#TESTING
# result = book_interview(
#     "John Doe",
#     "qg2Zp@example.com",
#     "Software Engineer",
#     "2026-07-01",
#     "10:00:00"
# )

# print(result)
# result = check_slot(
#     "Software Engineer",
#     "2026-07-01",
#     "10:00:00")
# if result : print(False)