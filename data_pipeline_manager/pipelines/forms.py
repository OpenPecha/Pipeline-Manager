import json

from django import forms
from ocr_pipelines.engines import GoogleVisionEngine

OCR_ENGINE_CHOICES = (("GV", "Google Vision"),)

OCR_ENGINES = {
    "GV": GoogleVisionEngine.__name__,
}

OCR_MODELS = {
    "Google Vision[bo-t-i0-handwrit]": ["bo-t-i0-handwrit"],
    "Google Vision[bo, und-t-i0-handwrit]": ["bo", "und-t-i0-handwrit"],
    "Google Vision[und-t-i0-handwrit]": ["und-t-i0-handwrit"],
}
OCR_MODEL_CHOICES = [(model_name, model_name) for model_name in OCR_MODELS.keys()]

OCR_LANGUAGES = {
    "---Select Language---": "",
    "Tibetan": "bo",
    "Chinese": "zh",
    "Devanagari": "hi",
}
OCR_LANGUAGES_CHOICES = [(lang, lang) for lang in OCR_LANGUAGES.keys()]


class OCRTaskForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Name for the batch"}),
        max_length=255,
    )
    inputs = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "One work id per line, for eg:\nW30305\nMW14081\nMW30303"
            }
        ),
        required=True,
    )
    ocr_engine = forms.ChoiceField(label="OCR Engine", choices=OCR_ENGINE_CHOICES)
    model_type = forms.ChoiceField(
        label="Model Type", choices=OCR_MODEL_CHOICES, required=False
    )
    language_hint = forms.ChoiceField(
        label="Language Hint", choices=OCR_LANGUAGES_CHOICES, required=False
    )
    google_vision_api_key = forms.CharField(
        label="Google Vision API Key",
        widget=forms.TextInput(
            attrs={"placeholder": "Paste your API key here", "type": "password"}
        ),
        required=False,
    )

    def clean_google_vision_api_key(self):
        ocr_engine = self.cleaned_data.get("ocr_engine")
        api_key_str = self.cleaned_data.get("google_vision_api_key")
        if ocr_engine == "GV":
            if not api_key_str:
                raise forms.ValidationError(
                    "Google Vision API Key is required for Google Vision OCR Engine",
                )

        try:
            api_key_dict = json.loads(api_key_str)
        except Exception:
            raise forms.ValidationError("Google Vision API Key is not valid JSON")
        return api_key_dict
