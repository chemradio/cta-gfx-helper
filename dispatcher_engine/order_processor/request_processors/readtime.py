from custom_types_enums import ContainerOutputFile, FileType


async def process_readtime(order: dict) -> list[ContainerOutputFile]:
    words = order["readtime_text"].split()
    numbers = [word for word in order["readtime_text"] if word.isdigit()]
    total_words = len(words) + len(numbers)
    readtime_secs = total_words / order["readtime_speed"] * 60

    return [
        ContainerOutputFile(
            file_type=FileType.TEXT,
            text=f"Вы прочтете этот текст за {readtime_secs} секунд",
        ),
    ]
