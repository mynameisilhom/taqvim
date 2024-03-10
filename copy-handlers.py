# from aiogram import F, Router
# from aiogram.filters import CommandStart
# from aiogram.types import CallbackQuery, Message
# import app.keyboards as kb
# from db import User, session
#
# router = Router()
#
#
# @router.message(CommandStart())
# async def start(message: Message):
#     await message.answer("Assalomu alaykum!",
#                          reply_markup=await kb.inline_regions())
#
#
# @router.callback_query(lambda callback: F.data == callback.data)
# async def choosen_region(callback: CallbackQuery):
#     user_id = callback.from_user.id
#     first_name = callback.from_user.first_name
#     region = callback.data
#
#     existing_user = session.query(User).filter_by(user_id=user_id).first()
#
#     if existing_user:
#         existing_user.region = region
#         session.commit()
#         await callback.message.answer(f'Hududingizni {callback.data}ga o\'zgartirildi')
#     else:
#         user = User(user_id=user_id, first_name=first_name, region=region)
#         session.add(user)
#         session.commit()
#         await callback.message.answer(f'Hududingiz belgilandi - {callback.data}')
#
#
# #
#
# # @router.message(F.text('/taqvim'))
# # async def taqvim(message: Message):
# #     await message.answer_photo("")
#
