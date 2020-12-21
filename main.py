#!/usr/local/bin/python
#
# -*- coding: latin-1 -*-s
import discord, re
from discord.ext import commands, tasks
from discord.ext.commands import bot, has_permissions, MissingPermissions, guild_only
import asyncio
from discord import Activity, ActivityType
import datetime
import random
import json
import nekos
from discord.voice_client import VoiceClient
import youtube_dl
from random import choice
import aiohttp
import os, sys

bot = commands.Bot(command_prefix=">")
bot.remove_command('help')
songs = asyncio.Queue()
play_next_song = asyncio.Event()

@bot.group(invoke_without_command=True)
async def help(ctx):
	embed = discord.Embed(title='Коротко о командах бота',description='MagBot | 2021',color=0xd42222)
	embed.add_field(name=':sparkles: Весёлости',value='`>help fun`',inline=False)
	embed.add_field(name=':wrench: Утилиты',value='`>help utils`',inline=False)
	embed.add_field(name=':tools: Модерация',value='`>help mod`',inline=False)
	await ctx.send(embed=embed)
@help.command()
async def fun(ctx):
	embed = discord.Embed(title='Весёлости:',description='```Ниже описаны команды созданные для разнообразия```', color=0xd42222)
	embed.add_field(name=':green_circle: |>hug @ник',value='`Обнять участника`',inline=False)
	embed.add_field(name=':green_circle: |>kiss @ник',value='`Поцеловать участника`',inline=False)
	embed.add_field(name=':green_circle: |>tickle @ник',value='`Пощекотать участника :>`',inline=False)
	embed.add_field(name=':green_circle: |>slap @ник',value='`Ударить участника`',inline=False)
	embed.add_field(name=':green_circle: |>pat @ник',value='`Погладить участника`',inline=False)
	embed.add_field(name=':green_circle: |>блинчик',value='`Рецепт блинчиков😂`')
	embed.add_field(name=':green_circle: |>kill @ник Нож/Дробовик',value='`Убить участника :D`',inline=False)
	embed.add_field(name=':green_circle: |>bite @ник',value='`Укусить участника`',inline=False)
	embed.add_field(name=':green_circle: |>ship @ник',value='`:)`')
	embed.add_field(name=':green_circle: |>nom @ник',value='`Дать вкусняшку другу/подруге`',inline=False)
	await ctx.send(embed=embed)
@help.command()
async def utils(ctx):
	embed = discord.Embed(title='Утилиты',description='```Утилиты которомы можно пользоваться в некоторых случаях```',color=0xd42222)
	embed.add_field(name=':green_circle: |>ping',value='`Узнать задержку Discord`',inline=False)
	embed.add_field(name=':green_circle: |>say',value='`Написать сообщение от имени бота`',inline=False)
	embed.add_field(name=':green_circle: |>uinfo @ник',value='`Узнать информацию об участнике`',inline=False)
	embed.add_field(name=':green_circle: |>contact',value='`Контакты разработчика`',inline=False)
	embed.add_field(name=':green_circle: |>nickc',value='`Сменить ник через бота`',inline=False)
	embed.add_field(name=':green_circle: |>stats',value='`Статистика бота`',inline=False)
	embed.add_field(name=':green_circle: |>avatar',value='`Показывает ваш аватар`',inline=False)
	await ctx.send(embed=embed)
@help.command()
async def mod(ctx):
	embed = discord.Embed(title='Модерация',description='```Команды для модераторов```', color=0xd42222)
	embed.add_field(name=':green_circle: |>ban',value='`Забанить участника`',inline=False)
	embed.add_field(name=':green_circle: |>clear число',value='`Очистка сообщений в чате`',inline=False)
	embed.add_field(name=':green_circle: |>unban ник+тег (пример: >unban MagMigo#6666)',value='`Разбанить участника`',inline=False)
	embed.add_field(name=':green_circle: |>kick @ник',value='`Кикнуть участника`',inline=False)
	await ctx.send(embed=embed)
@bot.command()
async def ping(ctx):
  embed = discord.Embed(title=f":ping_pong: Задержка: {round(bot.latency*1000)}ms")
  await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    emb = discord.Embed(title='📌Cообщение', description=message, color=discord.Color.green())
    emb.set_author(name=ctx.author.name, icon_url = ctx.author.avatar_url)

    await ctx.send(embed=emb)

@bot.command()
async def uinfo(ctx,member:discord.Member):
	emb = discord.Embed(title='Информация о аккаунте',color=0xff0000)
	emb.add_field(name='Когда присоединился',value=member.joined_at,inline=False)
	emb.add_field(name='Когда создан аккаунт',value=member.created_at.strftime("%a,%#d %B %Y, %I:%M %p UTC"),inline=False)
	emb.add_field(name='Отображаемое имя',value=member.display_name,inline=False)
	emb.set_thumbnail(url=member.avatar_url)
	emb.set_footer(text=f"Вызвал:{ctx.message.author}",icon_url=ctx.message.author.avatar_url)
	await ctx.send(embed = emb)	
@bot.command()
@commands.has_permissions(view_audit_log=True)
async def clear(ctx,amount=5):
	deleted = await ctx.message.channel.purge(limit=amount + 1)
	embed = discord.Embed(title='Очистка',color=0xd42222)
	embed.add_field(name=f'Очистил: {ctx.message.author} `{amount}` сообщений',value=bot.user.name)
	embed.set_footer(text='© MagM1go')
	await ctx.send(embed=embed)
@bot.command()
async def contact(ctx):
	emb = discord.Embed(title='Контакты создателя:',color=0xff0000)
	emb.add_field(name='Создатель бота',value="MagMigo#6666\n https//vk.com/magmigo/",inline=False)
	await ctx.send(embed = emb)
@bot.event
async def on_member_join(member):
  channel = bot.get_channel(789454068665155594)
  role = discord.utils.get(member.guild.roles, id=786147045819940894)
  await member.add_roles(role)
  await channel.send(f"{member.mention} Приветствую тебя, новичок!")

@bot.event
async def on_member_remove(member):
  channel = bot.get_channel(789454068665155594)
  await channel.send(f"{member.mention} Прощай...")
@bot.event
async def on_ready():
	print('Бот успешно запущен.')
	Game = discord.Game("with the API")
	await bot.change_presence(status=discord.Status.online,activity=discord.Game('MagBot-Beta | UP 2021'))
async def audio_player_task():
    while True:
        play_next_song.clear()
        current = await songs.get()
        current.start()
        await play_next_song.wait()
def toggle_next():
    bot.loop.call_soon_threadsafe(play_next_song.set)


@bot.command(pass_context=True)
async def play(ctx, url):
    if not voice.is_voice_connected(ctx.message.server):
        voice = await voice.join_voice_channel(ctx.message.author.voice_channel)
    else:
        voice = voice.voice_client_in(ctx.message.server)

    player = await voice.create_ytdl_player(url, after=toggle_next)
    await songs.put(player)

bot.loop.create_task(audio_player_task())

@bot.event
async def on_raw_reaction_add(payload):
	if payload.message_id == 789693741194936340 and payload.emoji.name == '👍':
		for guild in bot.guilds:
			role = discord.utils.get(guild.roles, id = 786147045819940894)
			await payload.member.add_roles(role)
@bot.event
async def on_voice_state_update(member,before,after):
	if after.channel.id == 789782496358957080:
		print(f'{member} Зашёл в канал')
		for guild in bot.guilds:
			main = discord.utils.get(guild.categories, id=677857623516643334)
			channel2 = await guild.create_voice_channel(name=f'Канал {member.display_name}',category = main)
			await channel2.set_permissions(member,connect=True,kick_members=True)
			await member.move_to(channel2)
			def check(x,y,z):
				return len(channel2.members) == 0
			await bot.wait_for('voice_state_update',check=check)
			await channel2.delete()
@bot.command()
async def kiss(ctx,member:discord.Member):
	emb = discord.Embed(color=0xebebeb)
	emb.add_field(name=f'Поцеловал(-а) {member}',value='\uFEFF')
	emb.set_image(url=nekos.img('kiss'))
	await ctx.send(embed=emb)
@bot.command()
async def slap(ctx,member:discord.Member):
	emb = discord.Embed(color=0xebebeb)
	emb.add_field(name=f'Ударил(-а) {member}',value='\uFEFF')
	emb.set_image(url=nekos.img('slap'))
	await ctx.send(embed=emb)
@bot.command()
async def pat(ctx,member:discord.Member):
	emb = discord.Embed(color=0xebebeb)
	emb.add_field(name=f'Погладил(-а) {member}',value='\uFEFF')
	emb.set_image(url=nekos.img('pat'))
	await ctx.send(embed=emb)

@bot.command()
async def hug(ctx,member:discord.Member):
	emb = discord.Embed(color=0xebebeb)
	emb.add_field(name=f'Обнял(-а) {member}',value='\uFEFF')
	emb.set_image(url=nekos.img('hug'))
	await ctx.send(embed=emb)
@bot.command()
async def tickle(ctx,member:discord.Member):
	emb = discord.Embed(color=0xebebeb)
	emb.add_field(name=f'Пощекотал(-а) {member}',value='\uFEFF')
	emb.set_image(url=nekos.img('tickle'))
	await ctx.send(embed=emb)
@bot.command()
async def ship(ctx,member:discord.Member):
	embed = discord.Embed(color=0xebebeb)
	embed.add_field(name=f'Появилась новая парочка {ctx.message.author} + {member}',value='\uFEFF')
	embed.set_image(url=nekos.img('kiss'))
	await ctx.send(embed=embed)
@bot.command()
async def bite(ctx,member:discord.Member):
	embed = discord.Embed(color=0xebebeb)
	embed.add_field(name=f'{ctx.message.author} укусил {member}',value='КУСЬ!!! КУСЬЬЬЬЬ!!!!!')
	await ctx.send(embed=embed)
@bot.command()
async def neko(ctx):
	embed = discord.Embed(color=0xebebeb)
	embed.add_field(name='Neko',value='\uFEFF')
	embed.set_image(url=nekos.img('neko'))
	await ctx.send(embed=embed)
@bot.command()
async def nom(ctx,member:discord.Member):
	emb = discord.Embed(color=0xebebeb)
	emb.add_field(name=f'{ctx.message.author} дал(-а) вкусняшку {member} :з',value='Ням')
	await ctx.send(embed=emb)
@bot.command()
async def nickc(ctx, new: str = None):
  if not new:
    await ctx.send('Ты не указал пользователя.')
  elif len(new) > 16:
    await ctx.send('Ты придумал слишком длинный никнейм.')
  else:
    await ctx.author.edit(nick=new)
    await ctx.send('Ты сменил никнейм!')
@nickc.error
async def nickc_error(ctx, error):
  if isinstance(error, commands.errors.CommandInvokeError):
    await ctx.send('Я не могу сменить никнейм тебе.')

@bot.command()
async def kill( ctx, member: discord.Member, arg ):
	if arg == 'Дробовик':
		embed = discord.Embed(title = 'Убийство', description = 'Вы сможете кого-то убить дробовиком', colour = discord.Color.red())
	elif arg == 'Нож':
		embed = discord.Embed(title = 'Убийство', description = 'Вы сможете кого-то убить ножом', colour = discord.Color.red())

	if arg == 'Дробовик':
		embed.add_field( name = '**Доставание дробовика**', value = f"{ctx.author.mention} достаёт дробовик...", inline = False )
	elif arg == 'Нож':
		embed.add_field( name = '**Доставание ножа**', value = f"{ctx.author.mention} достаёт нож...", inline = False )

	if arg == 'Дробовик':
		embed.add_field( name = '**Направление дробовика**', value = f"{ctx.author.mention} направляет дробовик на {member.mention}...", inline = False )
	elif arg == 'Нож':
		embed.add_field( name = '**Думание попадания**', value = f"{ctx.author.mention} думает, куда будет бить на {member.mention}...", inline = False )

	if arg == 'Дробовик':
		embed.add_field( name = '**Стрельба**', value = f"{ctx.author.mention} стреляет в {member.mention}...", inline = False )
	elif arg == 'Нож':
		embed.add_field( name = '**Попадание**', value = f"{ctx.author.mention} попадает ножом в {member.mention}...", inline = False )
	
	if arg == 'Дробовик':
		embed.set_image(url='https://media.discordapp.net/attachments/690222948283580435/701494203607416943/tenor_3.gif')
	elif arg == 'Нож':
		embed.set_image(url='https://cdn.discordapp.com/attachments/789452703084445727/790543128058396692/305253a407fa8da8.gif')

	embed.add_field( name = '**Кровь**', value = f"{member.mention} истекает кровью...", inline = False )


	embed.add_field( name = '**Погибание**', value = f"{member.mention} погиб...", inline = False )

	await ctx.send( embed = embed )
@bot.command()
async def stats(ctx):
    dpyVersion = discord.__version__
    serverCount = len(bot.guilds)
    memberCount = len(set(bot.get_all_members()))
    embed = discord.Embed(title='Статистика', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)
    embed.add_field(name='Версия бота:', value='1.0')
    embed.add_field(name='Discord.Py версия', value=dpyVersion)
    embed.add_field(name='Число гильдий:', value=serverCount)
    embed.add_field(name='Число всех участников:', value=memberCount)
    embed.add_field(name='Разработчик бота:', value="<@598387707311554570>")
    embed.set_footer(text=f"{ctx.message.author}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)
@bot.command()
async def report(self, ctx, member:discord.Member,reason):
    channel = self.bot.get_channel(789454068665155594)
    author = ctx.message.author
    rearray = ' '.join(reason[:])
    if not rearray:
        await channel.send(f"{ctx.message.author} подал жалобу на {member.mention}, Причина: Not provided")
        await ctx.message.delete()
    else:
        await channel.send(f"{ctx.message.author} подал жалобу на {member.mention}, Причина: {rearray}")
        await ctx.message.delete()
@bot.command()
async def блинчик(ctx):
	embed = discord.Embed(title='Рецепт блинчиков :D',color=0x169416)
	embed.add_field(name='**1.** Один стакан муки',value='\uFEFF',inline=False)
	embed.add_field(name='**2.** Два стакана воды',value='\uFEFF',inline=False)
	embed.add_field(name='**3.** 50 г. растительного масла',value='\uFEFF',inline=False)
	embed.add_field(name='**4.** Одна столовая ложка сахара',value='\uFEFF',inline=False)
	embed.add_field(name='**5.** Одна третья чайной ложки соды',value='\uFEFF',inline=False)
	await ctx.send(embed=embed)
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(embed = discord.Embed(description = f'**Команда введена неправильно или не существует!**', colour = discord.Color.red()))
@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)
#The below code bans player.
@bot.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_id, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_id, member_discriminator):
    await ctx.guild.unban(user)
    await ctx.send(f"{member} Был разбанен.\nМодератор: {ctx.message.author.mention}")
    return
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
	await member.ban(reason = reason)
	await ctx.send(f'{member} Был забанен. Модератор: {ctx.message.author.mention}')
@bot.command()
@commands.has_permissions(view_audit_log = True)
async def kick(ctx,member:discord.Member, *, reason = None):
	await member.kick(reason = reason)
	await ctx.send(f"{member} Был кикнут. Модератор: {ctx.message.author.mention}")
@bot.command()
async def sinfo(ctx):
    memberCount = len(set(bot.get_all_members()))
    embed = discord.Embed(title='Информация о сервере', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)
    embed.add_field(name='Число всех участников:', value=memberCount)
    embed.add_field(name='Создатель сервера:', value="<@598387707311554570>")
    embed.set_footer(text=f"{ctx.message.author}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)
@bot.command()
async def about(ctx):
	embed = discord.Embed(title='Информация о боте',color=ctx.author.colour)
	embed.add_field(name='MagBot',value='Бот, созданнный для этого сервера, MagHub и разработан для модерации/администрирования на сервере\n так же есть и команды для веселья и прочие, в общем, пользуйтесь.',inline=False)
	embed.add_field(name='Разработчик бота:',value='<@598387707311554570> ```Основатель``` **Бот основан:** ```19.12.2020```',inline=False)
	embed.set_footer(text=f"{ctx.message.author}")
	await ctx.send(embed=embed)
@bot.command()
@commands.has_permissions(view_audit_log=True)
async def mute(ctx,member:discord.Member,reason = None):
    await member.add_roles(id=786144342674112584)
    await ctx.send(f'{member} Был замьючен')
TOKEN = 'NzQyNzM4MTY3MDQzNzE5MTY4.XzKe0g.Ml35u8c-e4oa5Q-k2QR3hfYU4d0'
bot.run(TOKEN)