from django import forms


class BootstrapFormMixin:
    """
    Automatically applies Bootstrap 5 classes
    to every visible field.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():

            css = field.field.widget.attrs.get("class", "")

            field.field.widget.attrs["class"] = (
                f"{css} form-control"
            ).strip()

            field.field.widget.attrs.setdefault(
                "autocomplete",
                "off",
            )