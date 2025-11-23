import os
import sys
import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), './app')))

from app.db.base import Base
from app.db.session import engine
from app.models.transaction import Transaction
from app.models.category import Category # Import the new Category model
from app.models.tag import Tag
from app.core.config import settings

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

def seed_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    tags = ["Work", "Travel", "Reimbursable", "Personal", "Urgent", "Entertainment"]
    tag_objs = []

    for t_name in tags:
        # Check if tag already exists to avoid duplicates
        existing_tag = db.query(Tag).filter_by(name=t_name).first()
        if not existing_tag:
            db_tag = Tag(name=t_name)
            db.add(db_tag)
            tag_objs.append(db_tag)
        else:
            tag_objs.append(existing_tag)

    db.commit()

    # Attach random tags to all transactions
    all_transactions = db.query(Transaction).all()
    for transaction in all_transactions:
        # Pick 1 to 3 random tags for each transaction
        transaction_tags = random.sample(tag_objs, k=random.randint(1, 3))
        transaction.tags = transaction_tags

    db.commit()

    db.close()

    try:
        # Check if the tables are empty before seeding
        if db.query(Transaction).count() == 0 or db.query(Category).count() == 0:
            print("Seeding database with initial data...")

            # Create categories
            categories_data = ["Food", "Income", "Housing", "Education", "Utilities", "Social", "Travel", "Shopping", "Health", "Investments", "Entertainment", "Transport", "Work", "Hobbies"]
            category_objects = {}
            for cat_name in categories_data:
                category = Category(name=cat_name)
                db.add(category)
                category_objects[cat_name] = category
            db.commit()

            # Refresh category objects to get their IDs
            for cat_name, category_obj in category_objects.items():
                db.refresh(category_obj)
            
            # Map category names to their IDs
            category_name_to_id_map = {cat_name: category_obj.id for cat_name, category_obj in category_objects.items()}

            transactions_data = [
                {"description": "Groceries", "amount": 50.25, "type": "debit", "category": "Food", "user_id": 1, "date": datetime(2025, 10, 26, 10, 0, 0)},
                {"description": "Salary", "amount": 2500.00, "type": "credit", "category": "Income", "user_id": 1, "date": datetime(2025, 10, 25, 9, 30, 0)},
                {"description": "Rent", "amount": 1200.00, "type": "debit", "category": "Housing", "user_id": 1, "date": datetime(2025, 10, 24, 14, 0, 0)},
                {"description": "Coffee", "amount": 4.50, "type": "debit", "category": "Food", "user_id": 1, "date": datetime(2025, 10, 23, 11, 15, 0)},
                {"description": "Freelance Payment", "amount": 750.00, "type": "credit", "category": "Income", "user_id": 1, "date": datetime(2025, 10, 22, 16, 45, 0)},
                {"description": "Books", "amount": 30.00, "type": "debit", "category": "Education", "user_id": 1, "date": datetime(2025, 10, 21, 13, 0, 0)},
                {"description": "Electricity Bill", "amount": 85.70, "type": "debit", "category": "Utilities", "user_id": 1, "date": datetime(2025, 10, 20, 10, 0, 0)},
                {"description": "Dinner with Friends", "amount": 70.00, "type": "debit", "category": "Social", "user_id": 1, "date": datetime(2025, 10, 19, 19, 30, 0)},
                {"description": "Transportation", "amount": 20.00, "type": "debit", "category": "Travel", "user_id": 1, "date": datetime(2025, 10, 18, 8, 0, 0)},
                {"description": "Online Course", "amount": 150.00, "type": "debit", "category": "Education", "user_id": 1, "date": datetime(2025, 10, 17, 12, 0, 0)},
                {"description": "Shopping", "amount": 75.50, "type": "debit", "category": "Shopping", "user_id": 1, "date": datetime(2025, 10, 16, 15, 0, 0)},
                {"description": "Gym Membership", "amount": 40.00, "type": "debit", "category": "Health", "user_id": 1, "date": datetime(2025, 10, 15, 9, 0, 0)},
                {"description": "Dividend Income", "amount": 150.00, "type": "credit", "category": "Investments", "user_id": 1, "date": datetime(2025, 10, 14, 11, 0, 0)},
                {"description": "Concert Tickets", "amount": 100.00, "type": "debit", "category": "Entertainment", "user_id": 1, "date": datetime(2025, 10, 13, 20, 0, 0)},
                {"description": "Utility Bill", "amount": 60.00, "type": "debit", "category": "Utilities", "user_id": 1, "date": datetime(2025, 10, 12, 14, 30, 0)},
                {"description": "Refund", "amount": 25.00, "type": "credit", "category": "Shopping", "user_id": 1, "date": datetime(2025, 10, 11, 10, 0, 0)},
                {"description": "Lunch", "amount": 15.75, "type": "debit", "category": "Food", "user_id": 1, "date": datetime(2025, 10, 10, 12, 45, 0)},
                {"description": "Subscription", "amount": 12.99, "type": "debit", "category": "Entertainment", "user_id": 1, "date": datetime(2025, 10, 9, 9, 0, 0)},
                {"description": "Bonus", "amount": 500.00, "type": "credit", "category": "Income", "user_id": 1, "date": datetime(2025, 10, 8, 17, 0, 0)},
                {"description": "Gas", "amount": 45.00, "type": "debit", "category": "Transport", "user_id": 1, "date": datetime(2025, 10, 7, 8, 30, 0)},
                {"description": "Healthcare", "amount": 80.00, "type": "debit", "category": "Health", "user_id": 1, "date": datetime(2025, 10, 6, 10, 0, 0)},
                {"description": "Gift", "amount": 50.00, "type": "credit", "category": "Income", "user_id": 1, "date": datetime(2025, 10, 5, 14, 0, 0)},
                {"description": "Software License", "amount": 29.99, "type": "debit", "category": "Work", "user_id": 1, "date": datetime(2025, 10, 4, 11, 0, 0)},
                {"description": "Travel Expenses", "amount": 120.00, "type": "debit", "category": "Travel", "user_id": 1, "date": datetime(2025, 10, 3, 9, 0, 0)},
                {"description": "Hobby Supplies", "amount": 35.00, "type": "debit", "category": "Hobbies", "user_id": 1, "date": datetime(2025, 10, 2, 16, 0, 0)},
            ]
            
            # Convert category names to IDs
            for data in transactions_data:
                data["category_id"] = category_name_to_id_map[data.pop("category")]

            for data in transactions_data:
                transaction = Transaction(**data)
                db.add(transaction)
            db.commit()
            print("Database seeded successfully.")
        else:
            print("Database already contains data, skipping seeding.")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # This will ensure tables are created before attempting to seed
    init_db()
    seed_db()

