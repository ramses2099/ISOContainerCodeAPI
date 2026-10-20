"""Provision a login account: python create_user.py USERNAME."""
import argparse
from getpass import getpass

from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError

from db import Base, SessionLocal, engine
from models import User


def main():
    parser = argparse.ArgumentParser(description="Create an API login account")
    parser.add_argument("username")
    args = parser.parse_args()
    username = args.username.strip()
    if not username:
        parser.error("Username cannot be empty")
    password = getpass("Password (at least 12 characters): ")
    if len(password) < 12:
        parser.error("Password must contain at least 12 characters")
    if password != getpass("Confirm password: "):
        parser.error("Passwords do not match")

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.add(User(username=username,
                    hashed_password=PasswordHash.recommended().hash(password)))
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            parser.exit(1, "Username already exists\n")
    print(f"Created user: {username}")


if __name__ == "__main__":
    main()
