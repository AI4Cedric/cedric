def restore_text(
    text: str,
    mapping: dict
):

    for placeholder, original in mapping.items():

        text = text.replace(
            placeholder,
            original
        )

    return text
