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
            'waifu': 'Случайная вайфу',
            'buyPremium': 'Купить премиум',
            'admin': 'Ты админ',
        },
        'en': {
            'randomFoto': 'Random foto',
            'randomVideo': 'Random video',
            'loadFoto': 'Load foto',
            'loadVideo': 'Load Video',
            'buy': 'Buy',
            'cancel': 'Cancel',
            'pay': 'Teleram Stars',
            'waifu': 'Random waifu',
            'buyPremium': 'Buy premium',
            'admin': 'U are admin',
        }
    }

    def getMainMarkup(self, lang):
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(self.langs[lang]['randomFoto']),
            types.KeyboardButton(self.langs[lang]['loadFoto']),
            types.KeyboardButton(self.langs[lang]['buyPremium'])
        )

    def getAdminMarkup(self, lang):
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(self.langs[lang]['randomFoto']),
            types.KeyboardButton(self.langs[lang]['loadFoto']),
            types.KeyboardButton(self.langs[lang]['randomVideo']),
            types.KeyboardButton(self.langs[lang]['loadVideo']),
            types.KeyboardButton(self.langs[lang]['waifu']),
            types.KeyboardButton(self.langs[lang]['admin'])
        )
    
    def getPremiumMarkup(self, lang):
        return types.ReplyKeyboardMarkup(resize_keyboard=True).add(
            types.KeyboardButton(self.langs[lang]['randomFoto']),
            types.KeyboardButton(self.langs[lang]['loadFoto']),
            types.KeyboardButton(self.langs[lang]['randomVideo']),
            types.KeyboardButton(self.langs[lang]['loadVideo']),
            types.KeyboardButton(self.langs[lang]['waifu']),
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

