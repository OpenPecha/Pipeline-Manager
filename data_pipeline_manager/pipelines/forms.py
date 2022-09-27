from django import forms

OCR_ENGINE_CHOICES = (
    ("GV", "Google Vision"),
    ("GB", "Google Books"),
    ("NS", "Namsel"),
)


class OCRTaskForm(forms.Form):
    name = forms.CharField(max_length=255)
    inputs = forms.CharField(widget=forms.Textarea, required=True)
    ocr_engine = forms.ChoiceField(choices=OCR_ENGINE_CHOICES)
    model_name = forms.CharField(max_length=255, required=False)
    credentials = forms.JSONField()
