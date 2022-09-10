from my_difflib import get_close_matches_indexes
from table2ascii import table2ascii as t2a, Alignment
from parsing_hero_info import parse, get_html, get_list_of_hero_name, get_img_links, get_img
from discord.ext import commands
from discord import Embed, Color, File
from PIL import Image
from io import BytesIO


class Dota2(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cp', 'co', 'cou', 'coun'])
    async def counter_pick(self, ctx, *, msg: str):
        """Позволяет узнать контрпики героя *ПРИМЕР: !cp legion *"""
        if ctx.author.bot:

            return
        else:
            url = 'https://ru.dotabuff.com'

            # Список с именами всех героев
            list_of_name = get_list_of_hero_name(get_html(url + "/heroes"))
            # Укорачивание каждого из значений имён относительно длинны запроса пользователя
            shorted_names = list(map(lambda list_: list_[:len(msg)], list_of_name))
            # Получение индекса имени героя, имя которого максимально совпадает с запросом пользователя
            index = get_close_matches_indexes(msg.lower().strip(), shorted_names, cutoff=.6)[0]

            # Парсинг данных героя и составление ASCII таблицы
            hero_url = f'{url}/heroes/{list_of_name[index]}/counters'
            head, data, avatar_src = parse(hero_url)

            table = t2a(
                header=["Name", "Winrate"],
                body=data,
                column_widths=[20] * 1 + [10] * 1,
                alignments=[Alignment.LEFT] * 2
            )

            img_links = get_img_links(get_html(hero_url))
            hoho = list(map(lambda h: get_img(h), img_links))
            haha = list(map(lambda i: Image.open(BytesIO(i.content)), hoho))
            new_image = Image.new('RGB', (640, 72), (250, 250, 250))

            k = 0
            for j in haha:
                new_image.paste(j, (k, 0))
                k += 128

            with BytesIO() as image_binary:
                new_image.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=File(fp=image_binary, filename='image.png'))

            embed = Embed(title="Винрейты", colour=Color.dark_gold())

            embed.set_thumbnail(url=f'https://ru.dotabuff.com{avatar_src}')
            embed.add_field(name=f"{head}:", value=f"```\n{table}\n```")
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dota2(bot))
