from django import forms

OCR_ENGINE_CHOICES = (
    ("GV", "Google Vision"),
    ("GB", "Google Books"),
    ("NS", "Namsel"),
)


class OCRTaskForm(forms.Form):
    inputs = forms.CharField(max_length=10000)
    name = forms.CharField(max_length=255)
    ocr_engine = forms.ChoiceField(choices=OCR_ENGINE_CHOICES)
    pipeline_config = forms.JSONField()
    pipeline_type = forms.CharField(max_length=1)
