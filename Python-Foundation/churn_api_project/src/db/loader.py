# src/db/loader.py
import csv
from pathlib import Path

from src.db.database import Base, SessionLocal, get_engine
from src.db.models import User, Subscription


def load_csv_to_db(filepath):
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal(bind=engine)
    try:
        with Path(filepath).open(mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 1. Check if user already exists to avoid duplicates
                existing_user = (
                    db.query(User).filter(User.customer_id == row["customerID"]).first()
                )
                if existing_user:
                    continue

                # 2. Create and insert the User
                new_user = User(
                    customer_id=row["customerID"],
                    gender=row["gender"],
                    senior_citizen=row["SeniorCitizen"] == "1",
                )
                db.add(new_user)
                db.flush()  # Flushes to database to generate the new_user.user_id

                # 3. Handle potential empty strings in TotalCharges
                total_charges = row["TotalCharges"]
                total_charges_val = (
                    float(total_charges)
                    if total_charges.replace(".", "", 1).isdigit()
                    else 0.0
                )

                # 4. Create and insert the linked Subscription
                new_sub = Subscription(
                    user_id=new_user.user_id,
                    tenure_months=int(row["tenure"]),
                    monthly_charges=float(row["MonthlyCharges"]),
                    total_charges=total_charges_val,
                    churn=row["Churn"] == "Yes",
                )
                db.add(new_sub)

            # 5. Commit all changes as a single transaction
            db.commit()
            print("Data successfully loaded into the database.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_csv_to_db("data/churn_data.csv")
