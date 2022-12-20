import json

from data_pipeline_manager.pipelines.forms import OCRTaskForm


class TestOCRTaskForm:
    def test_form_valid(self):
        data = {
            "name": "Test OCR Task",
            "inputs": "01\n02\n03",
            "ocr_engine": "GV",
            "model_type": "builtin/stable",
            "language_hint": "bo",
            "google_vision_api_key": '{"api-key": "fake-api-key"}',
            "sponsor_name": "Test Sponsor",
            "sponsor_concent": True,
        }

        form = OCRTaskForm(data=data)

        assert form.is_valid()

        data["google_vision_api_key"] = json.loads(data["google_vision_api_key"])
        assert form.cleaned_data == data
