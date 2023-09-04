def preprocess_string(string: str) -> str:
    string = (
        string.strip()
        .replace("\n\n", "\n")
        .replace("\t\t", "\t")
        .replace("\n\t", "\n")
        .replace("\t", "\n")
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
