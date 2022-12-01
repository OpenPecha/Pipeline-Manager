import json

from django import forms
from ocr_pipelines.engines import GoogleVisionEngine

OCR_ENGINE_CHOICES = (("GV", "Google Vision"),)

OCR_ENGINES = {
    "GV": GoogleVisionEngine.__name__,
}

OCR_MODEL_CHOICES = (
    ("builtin/stable", "builtin/stable"),
    ("builtin/latest", "builtin/latest"),
    ("builtin/weekly", "builtin/weekly"),
)

OCR_LANGUAGES_CHOICES = [
    ("bo", "Tibetan"),
    ("zh", "Chinese"),
    ("hi", "Devanagari"),
]


def add_handwiriting_options(language_choices: list[tuple[str, str]]):
    """
    Add handwriting options to the language choices.
    """
    handwriting_indentifier = "t-i0-handwrit"
    new_language_choices = []
    for lang_code, lang_name in language_choices:
        new_language_choices.append((lang_code, lang_name))
        new_language_choices.append(
            (f"{lang_code}-{handwriting_indentifier}", f"{lang_name}-Handwriting")
        )
    return new_language_choices


OCR_LANGUAGES_CHOICES = add_handwiriting_options(OCR_LANGUAGES_CHOICES)
OCR_LANGUAGES_CHOICES.insert(0, ("", "Auto")),


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
        label="Language Hint",
        choices=OCR_LANGUAGES_CHOICES,
        required=False,
        initial="Auto",
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
