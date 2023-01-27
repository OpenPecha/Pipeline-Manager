import json

from django import forms
from django.utils.safestring import mark_safe
from ocr_pipelines.engines import GoogleVisionEngine

OCR_ENGINE_CHOICES = (("GV", "Google Vision"),)

OCR_ENGINES = {
    "GV": GoogleVisionEngine.__name__,
}

OCR_MODEL_CHOICES = (
    ("builtin/weekly", "builtin/weekly"),
    ("builtin/latest", "builtin/latest"),
    ("builtin/stable", "builtin/stable"),
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
    label_suffix = ""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "example@address.com"}),
        max_length=255,
    )
    gcloud_service_account_key = forms.CharField(
        label=mark_safe(
            "Google Cloud Service JSON key file (<a href='https://openpecha.org/tools/cloud-vision-key/' target='_blank'>how to get one</a>)"  # noqa
        ),
        widget=forms.TextInput(
            attrs={
                "placeholder": "Open file and paste contents here",
                "type": "password",
            }
        ),
        required=False,
    )
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={"placeholder": "Name of the batch"}),
        max_length=255,
    )
    inputs = forms.CharField(
        label="Input",
        widget=forms.Textarea(
            attrs={
                "placeholder": "One BDRC Scan ID per line, for eg:\nW30305\nW8CZ61\nW14322"
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
    sponsor_name = forms.CharField(
        label="Sponsor Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Sponsor's name will be added to OCR metadata"}
        ),
        max_length=255,
    )
    sponsor_concent = forms.BooleanField(
        label="Allow BDRC and OpenPecha to use the results to improve this service.",
        initial=True,
        required=True,
    )

    def clean_gcloud_service_account_key(self):
        ocr_engine = self.cleaned_data.get("ocr_engine")
        api_key_str = self.cleaned_data.get("gcloud_service_account_key")
        if ocr_engine == "GV":
            if not api_key_str:
                raise forms.ValidationError(
                    "Gcloud Service Account key is required for Google Vision OCR Engine",
                )

        try:
            api_key_dict = json.loads(api_key_str)
        except Exception:
            raise forms.ValidationError("Gcloud Service Account Key is not valid JSON")
        return api_key_dict
