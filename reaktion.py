from telethon.sync import TelegramClient
from telethon import functions, types

api_id = "20211195"
api_hash = "900a88063d66744450d23f6ddd52af6e"
phone = "+375295332073"

client = TelegramClient(phone, api_id, api_hash)

async def reaction(index):
    async with client:
        messages = await client.get_messages('@mvp1test', limit=5)

        if messages:
            msg_id = messages[index].id
            print(f"Используемый msg_id: {msg_id}")

            # Отправка реакции
            await client(functions.messages.SendReactionRequest(
                peer='@mvp1test',
                msg_id=msg_id,
                big=True,
                add_to_recent=True,
                reaction=[types.ReactionEmoji(emoticon='👍')]
            ))

            # Получение списка реакций
            result = await client(functions.messages.GetMessagesReactionsRequest(
                peer='@mvp1test',
                id=[msg_id]
            ))

            # Подсчет общего количества реакций
            total_reactions = 0
            for update in result.updates:
                if isinstance(update, types.UpdateMessageReactions):
                    total_reactions += sum(reaction.count for reaction in update.reactions.results)
            print(f"Общее количество реакций: {total_reactions}")

            return total_reactions

with client:
    client.loop.run_until_complete(reaction(0))
