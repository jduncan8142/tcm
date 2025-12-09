"""
Reusable form components for FastHTML pages.
"""

from fasthtml.common import *


def InputField(
    name: str,
    label: str,
    input_type: str = "text",
    required: bool = False,
    placeholder: str = "",
    value: str = "",
    autocomplete: str = "",
):
    """
    Reusable input field component with label.

    Args:
        name: Input field name attribute
        label: Label text for the input
        input_type: Type of input (text, password, email, etc.)
        required: Whether the field is required
        placeholder: Placeholder text
        value: Pre-filled value
        autocomplete: Autocomplete attribute value

    Returns:
        FastHTML div containing label and input
    """
    input_attrs = {
        "type": input_type,
        "id": name,
        "name": name,
        "placeholder": placeholder,
        "value": value,
        "cls": "form-input",
    }

    if required:
        input_attrs["required"] = True

    if autocomplete:
        input_attrs["autocomplete"] = autocomplete

    return Div(
        Label(label, fr=name, cls="form-label"),
        Input(**input_attrs),
        cls="form-group",
    )


def SubmitButton(
    text: str = "Submit",
    loading_text: str = "Loading...",
    disabled: bool = False,
):
    """
    Primary submit button component.

    Args:
        text: Button text
        loading_text: Text to show when loading
        disabled: Whether button is disabled

    Returns:
        FastHTML button element
    """
    button_attrs = {
        "type": "submit",
        "cls": "btn btn-primary",
    }

    if disabled:
        button_attrs["disabled"] = True

    return Button(text, **button_attrs)


def ErrorMessage(message: str):
    """
    Error alert message component.

    Args:
        message: Error message text

    Returns:
        FastHTML div with error styling
    """
    if not message:
        return None

    return Div(
        P(message),
        cls="alert alert-error",
        role="alert",
    )


def SuccessMessage(message: str):
    """
    Success alert message component.

    Args:
        message: Success message text

    Returns:
        FastHTML div with success styling
    """
    if not message:
        return None

    return Div(
        P(message),
        cls="alert alert-success",
        role="alert",
    )
