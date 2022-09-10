from discord import Intents, utils, Status, Embed, Color, Activity, ActivityType
from discord.ext import commands
import os
import asyncio

discord_info = {'log_channel_id': 955177936519041054,
                'token': os.getenv('JabronyBot_TOKEN', None),
                'help_command_list': [[
                    ["__Музыкальные команды__ :musical_note:", 'Дайте Жаброне разбомбить ваши кабаньи ушки', False],
                    ["`join` или `j`", '**Добавить** *бота* в голосовой канал', True],
                    ["`leave` или `l`", 'Выгнать *бота* из голосового канала', True],
                    ["`play` или `p` ", "Добавить трек в очередь и начать воспроизведение\n"
                                        "Максимальное количество треков в очереди **10**\n"
                                        "Треки можно добавлять по их **названию**, либо по **yt-ссылке** на них",
                     False],
                    ["`find` или `f` ", "**Найти** треки по названию", True],
                    ["`queue` или `q` ", "Посмотреть **список** треков", True],
                    ["`skip` или `s`", "**Пропустить** трек", True],
                    ["`pause`", "**Приостановить** трек на время", True],
                    ["`resume`", "**Продолжить** трек", True]],

                    [["__Dota2 команды__ :video_game:", 'Хрюкни', False],
                     ["`cp` или counter_pick", 'Посмотреть контрпики для героя', False]]]
                }
intents = Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    # --- Функция для отслеживания активации бота ---
    utils.setup_logging()

    await bot.change_presence(status=Status.online, activity=(Activity(type=ActivityType.listening, name="!help 🐗")))
    print("готов")
    log_channel = bot.get_channel(discord_info["log_channel_id"])
    await log_channel.send("Жаброня на месте")


@bot.command(aliases=['h', 'he', 'hel'])
async def help(ctx, *, msg=None):
    if msg is None:
        embed = Embed(title="КОМАНДЫ",
                      color=Color.brand_green(),
                      description="Преффикс команд - :exclamation:\n Каждая из команд должна начинаться с восклицательного знака.")
        music_command = "!help `music` или `m` — все команды\n`join`⠀⠀или `j` — войти\n`leave`⠀ или `l` — покинуть\n`play`⠀⠀или `p` — играть\n"
        dota_command = "!help `dota` или `d` — все команды\n`cp` — контрпики героя"

        embed.add_field(name="__Музыкальные команды__ :musical_note:", value=music_command, inline=True)
        embed.add_field(name="__Dota2 команды__ :video_game:", value=dota_command, inline=True)

        return await ctx.send(embed=embed)

    elif msg.startswith('m'):
        embed = Embed(title="КОМАНДЫ Music",
                      color=Color.brand_green(),
                      description="Преффикс команд - :exclamation:")
        for field in discord_info['help_command_list'][0]:
            embed.add_field(name=field[0], value=field[1], inline=field[2])
        return await ctx.send(embed=embed)

    elif msg.startswith('d'):
        embed = Embed(title="КОМАНДЫ Dota2",
                      color=Color.brand_green(),
                      description="Преффикс команд - :exclamation:")
        for field in discord_info['help_command_list'][1]:
            embed.add_field(name=field[0], value=field[1], inline=field[2])
        return await ctx.send(embed=embed)


async def main():
    async with bot:
        await load_extensions()
        await bot.start(discord_info['token'])


if __name__ == '__main__':
    asyncio.run(main())
    bot.run(discord_info['token'], reconnect=False)
