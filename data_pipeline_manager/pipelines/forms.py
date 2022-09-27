from secrets import choice

from django import forms

OCR_ENGINE_CHOICES = (
    ("GV", "Google Vision"),
    ("GB", "Google Books"),
    ("NS", "Namsel"),
)

OCR_ENGINES = dict(OCR_ENGINE_CHOICES)

OCR_MODELS = {
    "google[bo-t-i0-handwrit]": ["bo-t-i0-handwrit"],
    "google[bo, und-t-i0-handwrit]": ["bo", "und-t-i0-handwrit"],
    "google[und-t-i0-handwrit]": ["und-t-i0-handwrit"],
}

OCR_MODEL_CHOICES = [(model_name, model_name) for model_name in OCR_MODELS.keys()]


class OCRTaskForm(forms.Form):
    name = forms.CharField(max_length=255)
    inputs = forms.CharField(widget=forms.Textarea, required=True)
    ocr_engine = forms.ChoiceField(choices=OCR_ENGINE_CHOICES)
    model_name = forms.ChoiceField(choices=OCR_MODEL_CHOICES)
