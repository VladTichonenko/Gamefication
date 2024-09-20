from telethon.sync import TelegramClient
from telethon import functions, types

api_id = "21451938"
api_hash = "02e804da78ecfda445b8ce657e9020bc"
phone = "+88802424137"

client = TelegramClient(phone, api_id, api_hash)

async def reaction(index):
    async with client:
        try:
            messages = await client.get_messages('https://t.me/mvp1test', limit=5)

            if messages:
                # Используем второе сообщение в списке
                msg_id = messages[index].id
                print(f"Используемый msg_id: {msg_id}")
                '''
                # Отправка реакции
                await client(functions.messages.SendReactionRequest(
                    peer='@luxcrypto123',
                    msg_id=msg_id,
                    big=True,
                    add_to_recent=True,
                    reaction=[types.ReactionEmoji(emoticon='👍')]
                ))
                '''
                # Получение списка реакций
                result = await client(functions.messages.GetMessagesReactionsRequest(
                    peer='https://t.me/mvp1test',
                    id=[msg_id]
                ))

                # Подсчет общего количества реакций
                total_reactions = 0
                for update in result.updates:
                    if isinstance(update, types.UpdateMessageReactions):
                        total_reactions += sum(reaction.count for reaction in update.reactions.results)
                print(f"Общее количество реакций: {total_reactions}")

                return total_reactions
            else:
                print("Сообщения не найдены.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

with client:
    client.loop.run_until_complete(reaction(0))
