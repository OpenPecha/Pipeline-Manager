from data_pipeline_manager.pipelines.forms import OCRTaskForm


class TestOCRTaskForm:
    def test_form_valid(self):
        data = {
            "name": "Test OCR Task",
            "inputs": "01\n02\n03",
            "ocr_engine": "GV",
            "model_type": "Google Vision[bo-t-i0-handwrit]",
            "language_hint": "Tibetan",
            "google_vision_api_key": "fake-api-key",
        }

        form = OCRTaskForm(data=data)

        assert form.is_valid()
        assert form.cleaned_data == data
