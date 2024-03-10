from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

regions = ['Angren', 'Andijon', 'Arnasoy', 'Ashxabod', 'Bekobod', 'Bishkek', 'Boysun', 'Buloqboshi', 'Burchmulla',
           'Buxoro', 'Gazli', 'Guliston', 'Denov', 'Dehqonobod', 'Do\'stlik', 'Dushanbe', 'Jalolobod', 'Jambul',
           'Jizzax', 'Jomboy', 'Zarafshon', 'Zomin', 'Kattaqo\'rg\'on', 'Konibodom', 'Konimex', 'Koson', 'Kosonsoy',
           'Marg\'ilon', 'Mingbuloq', 'Muborak', 'Mo\'ynoq', 'Navoiy', 'Namangan', 'Nukus', 'Nurota', 'Olmaota',
           'Olot', 'Oltiariq', 'Oltinko\'l', 'Paxtaobod', 'Pop', 'Rishton', 'Sayram', 'Samarqand', 'Tallimarjon',
           'Taxtako\'pir', 'Termiz', 'Tomdi', 'Toshkent', 'Toshhovuz', 'Turkiston', 'Turkmanobod', 'To\'rtko\'l',
           'Uzunquduq', 'Urganch', 'Urgut', 'O\'smat', 'Uchtepa', 'Uchquduq', 'Uchqo\'rg\'on', 'O\'sh', 'O\'g\'iz',
           'Farg\'ona', 'Xazorasp', 'Xiva', 'Xonobod', 'Xonqa', 'Xo\'jand', 'Xo\'jaobod', 'Chimboy', 'Chimkent',
           'Chortoq', 'Chust', 'Shahrixon', 'Sherobod', 'Shovot', 'Shumanay', 'Yangibozor', 'G\'allaorol', 'G\'uzor',
           'Qarshi', 'Qiziltepa', 'Qorako\'l', 'Qorovulbozor', 'Quva', 'Qumqo\'rg\'on', 'Qo\'ng\'irot',
           'Qo\'rg\'ontepa', 'Qo\'qon']


async def inline_regions():
    keyboard = InlineKeyboardBuilder()
    for region in regions:
        keyboard.add(InlineKeyboardButton(text=region, callback_data=f'{region}'))
    return keyboard.adjust(2).as_markup()


change_region = [
    [types.KeyboardButton(text="Bugungi vaqtlarni olish")],
    [types.KeyboardButton(text="Xududni o\'zgartirish")],
    [types.KeyboardButton(text="Vaqtni tekshirish")]
]
keyboard = types.ReplyKeyboardMarkup(keyboard=change_region, resize_keyboard=True)
