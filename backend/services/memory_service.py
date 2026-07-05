from sqlalchemy.orm import Session

from database import SessionLocal
from models_db import Run, Message, MemorySummary


def create_run(run_id: str):
    db: Session = SessionLocal()

    try:
        run = Run(run_id=run_id)
        db.add(run)
        db.commit()
    finally:
        db.close()


def get_run(run_id: str):
    db: Session = SessionLocal()

    try:
        return db.query(Run).filter(Run.run_id == run_id).first()
    finally:
        db.close()


def save_message(run_id: str, role: str, content: str):
    db: Session = SessionLocal()

    try:
        message = Message(
            run_id=run_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()

    finally:
        db.close()


def get_messages(run_id: str):
    db: Session = SessionLocal()

    try:
        messages = (
            db.query(Message)
            .filter(Message.run_id == run_id)
            .order_by(Message.id)
            .all()
        )

        return [
            {
                "role": m.role,
                "content": m.content,
            }
            for m in messages
        ]

    finally:
        db.close()


def save_summary(run_id: str, summary: str):
    db: Session = SessionLocal()

    try:
        existing = (
            db.query(MemorySummary)
            .filter(MemorySummary.run_id == run_id)
            .first()
        )

        if existing:
            existing.summary = summary
        else:
            db.add(
                MemorySummary(
                    run_id=run_id,
                    summary=summary,
                )
            )

        db.commit()

    finally:
        db.close()


def get_summary(run_id: str):
    db: Session = SessionLocal()

    try:
        memory = (
            db.query(MemorySummary)
            .filter(MemorySummary.run_id == run_id)
            .first()
        )

        if memory:
            return memory.summary

        return ""

    finally:
        db.close()

def get_all_runs():
    db = SessionLocal()

    try:
        runs = db.query(Run).order_by(Run.created_at.desc()).all()

        return [
            {
                "run_id": run.run_id,
                "created_at": run.created_at,
            }
            for run in runs
        ]

    finally:
        db.close()