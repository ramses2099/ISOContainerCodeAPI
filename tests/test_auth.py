import os
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

os.environ["JWT_SECRET_KEY"] = "test-only-secret-" * 4

import jwt
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import db

# Import the application against an isolated database, never the project database.
engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                       poolclass=StaticPool)
with patch.object(db, "engine", engine):
    from app import app

from auth import ALGORITHM, SECRET_KEY, password_hash
from models import Base, ISOContainerType, User

Session = sessionmaker(bind=engine)


def tearDownModule():
    engine.dispose()


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        with Session() as session:
            session.add(User(username="tester",
                             hashed_password=password_hash.hash("test-password")))
            session.add(ISOContainerType(gkey=1, code="22G1", description="Container",
                                         length=20, height=8.5, group="G"))
            session.commit()

        def override_db():
            with Session() as session:
                yield session

        app.dependency_overrides[db.get_db] = override_db
        self.client = TestClient(app)
        self.addCleanup(app.dependency_overrides.clear)
        self.addCleanup(self.client.close)

    def login(self, username="tester", password="test-password"):
        return self.client.post("/token", data={"username": username, "password": password})

    def headers(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["token_type"], "bearer")
        return {"Authorization": "Bearer " + response.json()["access_token"]}

    def test_login_and_both_lookups(self):
        headers = self.headers()
        for path in ("/isocontainertypesbygkey/1", "/isocontainertypesbycode/22G1"):
            response = self.client.get(path, headers=headers)
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(response.json()["code"], "22G1")

    def test_missing_token(self):
        for path in ("/isocontainertypesbygkey/1", "/isocontainertypesbycode/22G1"):
            self.assertEqual(self.client.get(path).status_code, 401)

    def test_wrong_credentials(self):
        for username, password in (("tester", "wrong"), ("unknown", "test-password")):
            response = self.login(username, password)
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.headers["www-authenticate"], "Bearer")

    def test_invalid_tokens(self):
        now = datetime.now(timezone.utc)
        payload = {"sub": "1", "iat": now, "exp": now + timedelta(minutes=5)}
        cases = ["malformed", jwt.encode(payload, "different-secret-" * 4, algorithm=ALGORITHM)]
        cases.append(jwt.encode({**payload, "exp": now - timedelta(seconds=1)},
                                SECRET_KEY, algorithm=ALGORITHM))
        cases.append(jwt.encode({"sub": "1", "iat": now}, SECRET_KEY, algorithm=ALGORITHM))
        cases.append(jwt.encode({**payload, "sub": "invalid"}, SECRET_KEY, algorithm=ALGORITHM))
        cases.append(jwt.encode({**payload, "sub": "999"}, SECRET_KEY, algorithm=ALGORITHM))
        for token in cases:
            with self.subTest(token=token[:15]):
                response = self.client.get("/isocontainertypesbygkey/1",
                                           headers={"Authorization": f"Bearer {token}"})
                self.assertEqual(response.status_code, 401)

    def test_disabled_user(self):
        headers = self.headers()
        with Session() as session:
            session.get(User, 1).is_active = False
            session.commit()
        self.assertEqual(self.login().status_code, 401)
        self.assertEqual(self.client.get("/isocontainertypesbygkey/1", headers=headers).status_code, 401)

    def test_authenticated_missing_container(self):
        self.assertEqual(self.client.get("/isocontainertypesbygkey/999",
                                         headers=self.headers()).status_code, 404)


if __name__ == "__main__":
    unittest.main()
