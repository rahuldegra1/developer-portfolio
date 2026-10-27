import os
import unittest
from unittest.mock import patch

import pandas as pd
from fastapi import HTTPException

os.environ.setdefault("JWT_SECRET_KEY", "test-only-secret-value-at-least-32-characters")

from src.api import main


class StubModel:
    def predict(self, features):
        return [1]


class ApiTests(unittest.TestCase):
    def test_prediction_uses_bound_customer_id(self):
        customer_id = "x' OR '1'='1"
        captured = {}

        def fake_read_sql_query(query, engine, params):
            captured["query"] = query.text
            captured["params"] = params
            return pd.DataFrame(
                [
                    {
                        "gender": "Female",
                        "senior_citizen": False,
                        "tenure_months": 1,
                        "monthly_charges": 29.85,
                        "total_charges": 29.85,
                    }
                ]
            )

        with (
            patch.object(main, "get_engine", return_value=object()),
            patch.object(main.pd, "read_sql_query", side_effect=fake_read_sql_query),
            patch.object(main, "model", StubModel()),
            patch.dict(
                os.environ,
                {"JWT_SECRET_KEY": "test-only-secret-value-at-least-32-characters"},
            ),
        ):
            result = main.predict_churn(customer_id, _username="test")

        self.assertEqual(result["customer_id"], customer_id)
        self.assertTrue(result["will_churn"])
        self.assertIn(":customer_id", captured["query"])
        self.assertNotIn(customer_id, captured["query"])
        self.assertEqual(captured["params"], {"customer_id": customer_id})

    def test_login_rejects_empty_username(self):
        with self.assertRaises(HTTPException) as error:
            main.login(" ")

        self.assertEqual(error.exception.status_code, 400)

    def test_login_requires_configured_secret(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(HTTPException) as error:
                main.login("demo")

        self.assertEqual(error.exception.status_code, 503)

    def test_prediction_reports_missing_model(self):
        with (
            patch.object(main, "model", None),
            patch.object(
                main, "MODEL_PATH", main.MODEL_PATH.with_name("missing-model.pkl")
            ),
        ):
            with self.assertRaises(HTTPException) as error:
                main.get_model()

        self.assertEqual(error.exception.status_code, 503)


if __name__ == "__main__":
    unittest.main()
