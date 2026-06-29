import io
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlparse

import main


class ImageHosterIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_upload_dir = main.UPLOAD_DIR

        main.UPLOAD_DIR = Path(self.temp_dir.name)
        main.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        main.app.config["TESTING"] = True
        self.client = main.app.test_client()

    def tearDown(self):
        main.UPLOAD_DIR = self.original_upload_dir
        self.temp_dir.cleanup()

    def test_health_upload_and_fetch(self):
        health_resp = self.client.get("/health")
        self.assertEqual(health_resp.status_code, 200)
        self.assertEqual(health_resp.get_json(), {"status": "ok"})
        health_resp.close()

        fake_png = b"\x89PNG\r\n\x1a\n" + b"test-image-bytes"
        data = {
            "image": (io.BytesIO(fake_png), "sample.png"),
        }
        upload_resp = self.client.post(
            "/upload",
            data=data,
            content_type="multipart/form-data",
        )

        self.assertEqual(upload_resp.status_code, 201)
        payload = upload_resp.get_json()
        self.assertIsNotNone(payload)
        self.assertIn("url", payload)
        self.assertIn("filename", payload)
        self.assertIn("markdown", payload)
        upload_resp.close()

        image_path = urlparse(payload["url"]).path
        image_resp = self.client.get(image_path)
        self.assertEqual(image_resp.status_code, 200)
        self.assertEqual(image_resp.data, fake_png)
        image_resp.close()


if __name__ == "__main__":
    unittest.main()
