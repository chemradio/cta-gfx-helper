def preprocess_string(string: str) -> str:
    string = (
        string.strip()
        .replace("\t", " ")
        .replace("\n", " <...> ")
        .replace("Ë", "Е")
        .replace("ё", "е")
        .replace("«", '"')
        .replace("»", '"')
        .replace(" - ", " – ")
    )

    if "  " in string:
        while "  " in string:
            string = string.replace("  ", " ")

    return string
