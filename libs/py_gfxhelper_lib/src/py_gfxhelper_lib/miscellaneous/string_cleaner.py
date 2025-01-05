def cleanup_string(string: str) -> str:
    substitutions = (
        ("\n\n", "\n"),
        ("\t\t", "\t"),
        ("\n\t", "\n"),
        ("\t", "\n"),
        (" <...> <...> ", " <...> "),
        ("Ë", "Е"),
        ("ё", "е"),
        ("«", '"'),
        ("»", '"'),
        (" - ", " – "),
        ("  ", " "),
    )

    for sub in substitutions:
        while sub[0] in string:
            string = string.replace(sub[0], sub[1])
    return string.strip()

