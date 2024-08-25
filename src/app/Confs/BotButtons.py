from telebot import types


class BotButtons:
    langs = {
        'ru': {
            'randomFoto': 'Случайное фото',
            'randomVideo': 'Случайное видео',
            'loadFoto': 'Загрузить фото',
            'loadVideo': 'Загрузить видео',
            'buy': 'Купить',
            'cancel': 'Отмена',
            'pay': 'Оплата звездами ТГ',
            'admin_transactions': 'Cписки транзакций',
        },
        'en': {
            'randomFoto': 'Random foto',
            'randomVideo': 'Random video',
            'loadFoto': 'Load foto',
            'loadVideo': 'Load Video',
            'buy': 'Buy',
            'cancel': 'Cancel',
            'pay': 'Teleram Stars',
            'admin_transactions': 'List transactions',
        }
    }

    def getMainMarkup(self, lang):
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(self.langs[lang]['randomFoto']),
            types.KeyboardButton(self.langs[lang]['loadFoto']),
            types.KeyboardButton(self.langs[lang]['randomVideo']),
            types.KeyboardButton(self.langs[lang]['loadVideo']),
        )

    def getAdminMarkup(self, lang):
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(self.langs[lang]['randomFoto']),
            types.KeyboardButton(self.langs[lang]['loadFoto']),
            types.KeyboardButton(self.langs[lang]['randomVideo']),
            types.KeyboardButton(self.langs[lang]['loadVideo']),
            types.KeyboardButton(self.langs[lang]['admin_transactions'])
        )

    def getSubMarkup(self, lang):
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(self.langs[lang]['buy']),
            types.KeyboardButton(self.langs[lang]['cancel'])
        )

    def getPayMarkup(self, lang):
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(self.langs[lang]['pay']),
            types.KeyboardButton(self.langs[lang]['cancel'])
        )

    def getMarkups(self, lang):
        return self.getMainMarkup(lang), \
               self.getAdminMarkup(lang), \
               self.getSubMarkup(lang), \
               self.getPayMarkup(lang)
