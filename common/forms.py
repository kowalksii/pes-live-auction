from django import forms


class BootstrapFormMixin:
    """
    Automatically apply Bootstrap classes to form fields.
    """

    default_class = "form-control"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            widget = field.widget

            css = widget.attrs.get("class", "")

            if isinstance(widget, (forms.CheckboxInput,)):
                widget.attrs["class"] = "form-check-input"

            else:
                widget.attrs["class"] = f"{css} {self.default_class}".strip()