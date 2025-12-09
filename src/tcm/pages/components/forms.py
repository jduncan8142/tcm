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


def SelectField(
    name: str,
    label: str,
    options: list[tuple[str, str]],
    required: bool = False,
    selected_value: str = "",
    placeholder: str = "Select an option",
    allow_custom: bool = False,
):
    """
    Reusable select/dropdown field component with label.

    Args:
        name: Select field name attribute
        label: Label text for the select
        options: List of (value, display_text) tuples
        required: Whether the field is required
        selected_value: Pre-selected value
        placeholder: Placeholder option text
        allow_custom: If True, renders as datalist for custom input

    Returns:
        FastHTML div containing label and select/input
    """
    if allow_custom:
        # Use datalist for autocomplete with custom input
        list_id = f"{name}_list"
        input_attrs = {
            "type": "text",
            "id": name,
            "name": name,
            "value": selected_value,
            "list": list_id,
            "placeholder": placeholder,
            "cls": "form-input",
        }
        if required:
            input_attrs["required"] = True

        return Div(
            Label(label, fr=name, cls="form-label"),
            Input(**input_attrs),
            Datalist(
                *[Option(display, value=value) for value, display in options],
                id=list_id,
            ),
            cls="form-group",
        )
    else:
        # Standard select dropdown
        select_attrs = {
            "id": name,
            "name": name,
            "cls": "form-input form-select",
        }
        if required:
            select_attrs["required"] = True

        option_elements = [Option(placeholder, value="", disabled=True, selected=not selected_value)]
        for value, display in options:
            opt_attrs = {"value": value}
            if value == selected_value:
                opt_attrs["selected"] = True
            option_elements.append(Option(display, **opt_attrs))

        return Div(
            Label(label, fr=name, cls="form-label"),
            Select(*option_elements, **select_attrs),
            cls="form-group",
        )


def TextAreaField(
    name: str,
    label: str,
    required: bool = False,
    placeholder: str = "",
    value: str = "",
    rows: int = 4,
):
    """
    Reusable textarea field component with label.

    Args:
        name: Textarea field name attribute
        label: Label text for the textarea
        required: Whether the field is required
        placeholder: Placeholder text
        value: Pre-filled value
        rows: Number of visible text lines

    Returns:
        FastHTML div containing label and textarea
    """
    textarea_attrs = {
        "id": name,
        "name": name,
        "placeholder": placeholder,
        "rows": rows,
        "cls": "form-input form-textarea",
    }

    if required:
        textarea_attrs["required"] = True

    return Div(
        Label(label, fr=name, cls="form-label"),
        Textarea(value, **textarea_attrs),
        cls="form-group",
    )


def CheckboxField(
    name: str,
    label: str,
    checked: bool = False,
):
    """
    Reusable checkbox field component with label.

    Args:
        name: Checkbox field name attribute
        label: Label text for the checkbox
        checked: Whether the checkbox is checked

    Returns:
        FastHTML div containing checkbox and label
    """
    checkbox_attrs = {
        "type": "checkbox",
        "id": name,
        "name": name,
        "cls": "form-checkbox",
    }

    if checked:
        checkbox_attrs["checked"] = True

    return Div(
        Label(
            Input(**checkbox_attrs),
            Span(label, cls="checkbox-label-text"),
            fr=name,
            cls="form-label checkbox-label",
        ),
        cls="form-group form-group-checkbox",
    )


def TagBadge(
    value: str,
    category: str = "",
    is_predefined: bool = False,
    show_category: bool = False,
):
    """
    Tag badge/chip component for displaying tags.

    Args:
        value: Tag value text
        category: Tag category
        is_predefined: Whether tag is predefined
        show_category: Whether to show category prefix

    Returns:
        FastHTML span element styled as a badge
    """
    badge_cls = "tag-badge"
    if is_predefined:
        badge_cls += " tag-badge-predefined"

    content = f"{category}: {value}" if show_category and category else value

    return Span(
        content,
        cls=badge_cls,
        data_category=category,
    )


def ActionButton(
    text: str,
    href: str = "",
    onclick: str = "",
    btn_type: str = "secondary",
    size: str = "normal",
):
    """
    Action button component for edit, delete, etc.

    Args:
        text: Button text
        href: Link destination (if link button)
        onclick: JavaScript onclick handler
        btn_type: Button type (primary, secondary, danger)
        size: Button size (small, normal)

    Returns:
        FastHTML button or anchor element
    """
    cls = f"btn btn-{btn_type}"
    if size == "small":
        cls += " btn-small"

    if href:
        return A(text, href=href, cls=cls)
    else:
        return Button(text, type="button", onclick=onclick, cls=cls)


def CategoryGroup(
    category: str,
    children,
    count: int = 0,
    collapsed: bool = False,
):
    """
    Collapsible category group component for organizing tags.

    Args:
        category: Category name
        children: Content to display in the group
        count: Number of items in the group
        collapsed: Whether group starts collapsed

    Returns:
        FastHTML details element with summary
    """
    return Details(
        Summary(
            Span(category.replace("_", " ").title(), cls="category-name"),
            Span(f"({count})", cls="category-count"),
            cls="category-header",
        ),
        Div(children, cls="category-content"),
        cls="category-group",
        open=not collapsed,
    )


def TagPickerField(
    name: str,
    label: str,
    available_tags: list[dict],
    selected_tag_ids: list[int] = None,
):
    """
    Enhanced tag picker field with autocomplete, pills, and browse modal.

    Args:
        name: Field name attribute
        label: Label text for the field
        available_tags: List of available tag dictionaries
        selected_tag_ids: List of selected tag IDs

    Returns:
        FastHTML div containing enhanced tag picker
    """
    selected_tag_ids = selected_tag_ids or []

    # Get selected tags
    selected_tags = [tag for tag in available_tags if tag["id"] in selected_tag_ids]

    # Group tags by category for the browse modal
    tags_by_category = {}
    for tag in available_tags:
        cat = tag["category"]
        if cat not in tags_by_category:
            tags_by_category[cat] = []
        tags_by_category[cat].append(tag)

    # Create JSON data for JavaScript
    tags_json = str(available_tags).replace("'", '"')
    selected_ids_json = str(selected_tag_ids)

    return Div(
        Label(label, fr=name, cls="form-label"),

        # Container for tag pills and input
        Div(
            # Selected tag pills
            Div(
                *[
                    Span(
                        tag["value"],
                        Button(
                            "×",
                            type="button",
                            cls="tag-pill-remove",
                            onclick=f"removeTag('{name}', {tag['id']})",
                        ),
                        cls="tag-pill",
                        data_tag_id=str(tag["id"]),
                    )
                    for tag in selected_tags
                ],
                cls="tag-pills-container",
                id=f"{name}_pills",
            ),

            # Input with autocomplete
            Div(
                Input(
                    type="text",
                    id=f"{name}_input",
                    placeholder="Type to search tags...",
                    cls="tag-picker-input",
                    autocomplete="off",
                    onkeyup=f"filterTags('{name}')",
                ),
                Button(
                    "Browse",
                    type="button",
                    cls="btn btn-secondary btn-small tag-picker-browse",
                    onclick=f"openTagBrowser('{name}')",
                ),
                cls="tag-picker-input-container",
            ),

            # Autocomplete dropdown
            Div(
                cls="tag-autocomplete-dropdown",
                id=f"{name}_dropdown",
                style="display: none;",
            ),

            cls="tag-picker-container",
        ),

        # Hidden inputs for form submission
        *[
            Input(
                type="hidden",
                name=name,
                value=str(tag_id),
                data_tag_input=name,
            )
            for tag_id in selected_tag_ids
        ],

        # Browse modal
        Div(
            Div(
                Div(
                    H3("Select Tags", cls="modal-title"),
                    Button(
                        "×",
                        type="button",
                        cls="modal-close",
                        onclick=f"closeTagBrowser('{name}')",
                    ),
                    cls="modal-header",
                ),
                Div(
                    *[
                        Details(
                            Summary(
                                category.replace("_", " ").title(),
                                cls="category-summary",
                            ),
                            Div(
                                *[
                                    Label(
                                        Input(
                                            type="checkbox",
                                            value=str(tag["id"]),
                                            checked=tag["id"] in selected_tag_ids,
                                            onchange=f"toggleTagInModal('{name}', {tag['id']})",
                                        ),
                                        Span(tag["value"]),
                                        cls="tag-option-label",
                                    )
                                    for tag in tags_by_category[category]
                                ],
                                cls="category-tags",
                            ),
                            cls="category-group-modal",
                            open=True,
                        )
                        for category in sorted(tags_by_category.keys())
                    ],
                    cls="modal-body",
                ),
                Div(
                    Button(
                        "Done",
                        type="button",
                        cls="btn btn-primary",
                        onclick=f"closeTagBrowser('{name}')",
                    ),
                    cls="modal-footer",
                ),
                cls="modal-content",
            ),
            cls="tag-browser-modal",
            id=f"{name}_modal",
            style="display: none;",
            onclick=f"closeModalOnBackdrop(event, '{name}')",
        ),

        # JavaScript data
        Script(f"""
            window.tagPickerData = window.tagPickerData || {{}};
            window.tagPickerData['{name}'] = {tags_json};
        """),

        cls="form-group tag-picker-field",
    )
