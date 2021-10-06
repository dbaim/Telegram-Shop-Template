from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnMain = KeyboardButton('⬅️ Main Menu')
btnKorz = KeyboardButton('Cart')
btnKat = KeyboardButton('Catalogue')

# Main Menu
btnKat = KeyboardButton('Catalog')
btnKorzina = KeyboardButton('Cart')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnKat, btnKorzina)

# Catalogue
Type1 = KeyboardButton('Shop Item Type 1')
Type2 = KeyboardButton('Shop Item Type 2')
CatMenu = ReplyKeyboardMarkup(row_width=1).add(Type1, Type2, btnMain)

# Properties of some shop item
MainPBt = KeyboardButton('Shop Item Properties')
MainPropMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(MainPBt, btnKat)


Color1 = InlineKeyboardButton('Red', callback_data='button1')
Color2 = InlineKeyboardButton('Blue', callback_data='button2')
Color3 = InlineKeyboardButton('Green', callback_data='button3')
ColMenu = InlineKeyboardMarkup(resize_keyboard=True, row_width=2).add(Color1, Color2, Color3)

# Shopping
ProdBtn = KeyboardButton('Continue Shopping')
AddBtn = KeyboardButton('Add to Cart')
DecMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(ProdBtn, AddBtn)

# Yes / No
YesBtn = KeyboardButton('Yes')
NoBtn = KeyboardButton('No')
DecMenu1 = ReplyKeyboardMarkup(resize_keyboard=True).add(YesBtn, NoBtn)

# Quantity Selection
MainQbt = KeyboardButton('Choose a quantity')
MainQMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(MainQbt, btnKat)

# Cart
btnClear = KeyboardButton('Clear cart')
btnOform = KeyboardButton('Form an order')
KorzMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnClear, btnOform, btnKat)

