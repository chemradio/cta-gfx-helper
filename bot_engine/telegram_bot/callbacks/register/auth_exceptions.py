class UnregisteredUser(Exception):
    def __init__(self, user_first_name, user_telegram_id):
        self.first_name = user_first_name
        self.telegram_id = user_telegram_id
        super().__init__()

    def __str__(self):
        return f"Unregistered user accessed the bot. First name: {self.first_name}, Telegram ID: {self.telegram_id}"


class BlockedUser(Exception):
    def __init__(self, user_first_name, user_telegram_id):
        self.first_name = user_first_name
        self.telegram_id = user_telegram_id
        super().__init__()

    def __str__(self):
        return f"Blocked user accessed the bot. First name: {self.first_name}, Telegram ID: {self.telegram_id}"


class PendingUser(Exception):
    def __init__(self, user_first_name, user_telegram_id):
        self.first_name = user_first_name
        self.telegram_id = user_telegram_id
        super().__init__()

    def __str__(self):
        return f"Pending user accessed the bot. First name: {self.first_name}, Telegram ID: {self.telegram_id}"
