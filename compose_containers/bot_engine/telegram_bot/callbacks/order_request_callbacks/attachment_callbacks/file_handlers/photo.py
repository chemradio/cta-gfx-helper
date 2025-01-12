from telegram import File, Message


async def photo_handler(message: Message) -> tuple[File, str]:
    # find the best quality photo
    photo_file_size = 0
    best_quality_photo_index = 0
    for index, photo in enumerate(message.photo):
        if photo["file_size"] > photo_file_size:
            photo_file_size = photo["file_size"]
            best_quality_photo_index = index

    return await message.photo[best_quality_photo_index].get_file(), "image/jpeg"
