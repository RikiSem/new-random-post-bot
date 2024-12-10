from aiogram import types


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
            'adminSendMessage': 'Разослать всем юзерам',
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
            'adminSendMessage': 'Send message to all users',
        }
    }

    def getMainMarkup(self, lang):
        btnList = [
            [
                types.KeyboardButton(text=self.langs[lang]['randomFoto']),
                types.KeyboardButton(text=self.langs[lang]['loadFoto']),
                types.KeyboardButton(text=self.langs[lang]['buyPremium'])
            ],
        ]
        return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btnList)

    def getAdminMarkup(self, lang):
        btnList = [
            [
                types.KeyboardButton(text=self.langs[lang]['randomFoto']),
                types.KeyboardButton(text=self.langs[lang]['loadFoto']),
                types.KeyboardButton(text=self.langs[lang]['randomVideo'])
            ],
            [
                types.KeyboardButton(text=self.langs[lang]['loadVideo']),
                types.KeyboardButton(text=self.langs[lang]['waifu']),
                types.KeyboardButton(text=self.langs[lang]['admin'])
            ]
        ]
        return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btnList)
    
    def getPremiumMarkup(self, lang):
        btnList = [
            [
                types.KeyboardButton(text=self.langs[lang]['randomFoto']),
                types.KeyboardButton(text=self.langs[lang]['loadFoto']),
                types.KeyboardButton(text=self.langs[lang]['randomVideo'])
            ],
            [
                types.KeyboardButton(text=self.langs[lang]['loadVideo']),
                types.KeyboardButton(text=self.langs[lang]['waifu']),
            ]
        ]
        return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btnList)

    def getSubMarkup(self, lang):
        btnList = [
            [
                types.KeyboardButton(text=self.langs[lang]['buy']),
                types.KeyboardButton(text=self.langs[lang]['cancel'])
            ],
        ]
        return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btnList)

    def getPayMarkup(self, lang):
        btnList = [
            [
                types.KeyboardButton(text=self.langs[lang]['pay']),
                types.KeyboardButton(text=self.langs[lang]['cancel'])
            ],
        ]
        return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btnList)

