import discord
from discord.ext import commands
import json
import asyncio

TOKEN = "VOTRE_TOKEN"  # Remplace par ton token Discord

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)  # Pas de préfixe

# Chargement des niveaux depuis un fichier JSON
try:
    with open("levels.json", "r") as f:
        levels = json.load(f)
except FileNotFoundError:
    levels = {}

RANKS = {
    10: "Débutant",
    50: "Intermédiaire",
    100: "Avancé",
    200: "Expert",
    500: "Légende"
}

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    await bot.tree.sync()

# Système de messages et de rôles
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    levels[user_id] = levels.get(user_id, 0) + 1

    for level, role_name in sorted(RANKS.items(), reverse=True):
        role = discord.utils.get(message.guild.roles, name=role_name)
        if levels[user_id] >= level and role and role not in message.author.roles:
            await message.author.add_roles(role)
            embed = discord.Embed(
                title="🎉 Nouveau Rang !",
                description=f"{message.author.mention} a obtenu le rôle **{role_name}** !",
                color=discord.Color.gold(),
            )
            await message.channel.send(embed=embed)

    with open("levels.json", "w") as f:
        json.dump(levels, f)

    await bot.process_commands(message)

@bot.command(name="rank")
async def rank(ctx):
    user_id = str(ctx.author.id)
    user_level = levels.get(user_id, 0)

    embed = discord.Embed(title="📊 Votre Rang", color=discord.Color.blue())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
    embed.add_field(name="🔢 Messages envoyés", value=str(user_level), inline=False)

    current_role = "Aucun"
    for level, role_name in sorted(RANKS.items(), reverse=True):
        if user_level >= level:
            current_role = role_name
            break

    embed.add_field(name="🏆 Rôle actuel", value=current_role, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="birthday")
async def birthday(ctx, date: str):
    embed = discord.Embed(
        title="🎂 Anniversaire Enregistré !",
        description=f"{ctx.author.mention}, votre date d'anniversaire a été enregistrée : **{date}** 🎉",
        color=discord.Color.purple(),
    )
    await ctx.send(embed=embed)

@bot.command(name="check")
async def check(ctx):
    embed = discord.Embed(
        title="🔍 Informations Utilisateur",
        description=f"👤 **Pseudo :** {ctx.author.name}\n🆔 **ID :** {ctx.author.id}\n📅 **Compte créé le :** {ctx.author.created_at.strftime('%d/%m/%Y')}",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)

@bot.command(name="claim")
async def claim(ctx, code: str):
    embed = discord.Embed(
        title="🎁 Récompense Récupérée !",
        description=f"{ctx.author.mention} a utilisé le code **{code}** et reçu une récompense !",
        color=discord.Color.gold(),
    )
    await ctx.send(embed=embed)

@bot.command(name="event")
async def event(ctx):
    embed = discord.Embed(
        title="📅 Événements à venir",
        description="🎉 **Tournoi du serveur** - 15 février\n🎮 **Soirée Gaming** - 22 février\n📢 **Annonce spéciale** - 1er mars",
        color=discord.Color.orange(),
    )
    await ctx.send(embed=embed)

@bot.command(name="guide")
async def guide(ctx):
    embed = discord.Embed(
        title="📖 Guide du Serveur",
        description="Bienvenue ! Voici quelques commandes utiles :\n\n"
                    "🔹 `/rank` - Voir votre niveau\n"
                    "🔹 `/event` - Voir les événements\n"
                    "🔹 `/leaderboard` - Voir le classement\n"
                    "🔹 `/support` - Contacter l'équipe\n",
        color=discord.Color.blue(),
    )
    await ctx.send(embed=embed)

@bot.command(name="leaderboard")
async def leaderboard(ctx):
    sorted_users = sorted(levels.items(), key=lambda x: x[1], reverse=True)[:10]
    ranking = "\n".join([f"🏅 **{i+1}.** <@{user}> - {score} messages" for i, (user, score) in enumerate(sorted_users)])

    embed = discord.Embed(
        title="🏆 Classement des Utilisateurs",
        description=ranking if ranking else "Aucun utilisateur classé.",
        color=discord.Color.gold(),
    )
    await ctx.send(embed=embed)

@bot.command(name="report")
async def report(ctx, *, bug: str):
    embed = discord.Embed(
        title="🚨 Bug Signalé",
        description=f"📝 **Description du bug** : {bug}\n📢 Signalé par : {ctx.author.mention}",
        color=discord.Color.red(),
    )
    await ctx.send(embed=embed)

@bot.command(name="season")
async def season(ctx):
    embed = discord.Embed(
        title="🍂 Saison Actuelle",
        description="🏆 **Saison 3 - Hiver 2025**\n🎯 **Objectif :** 1000 messages pour atteindre le niveau Légende !",
        color=discord.Color.teal(),
    )
    await ctx.send(embed=embed)

@bot.command(name="support")
async def support(ctx):
    embed = discord.Embed(
        title="📞 Support du Bot",
        description="Besoin d'aide ? Rejoins le serveur support : [Clique ici](https://discord.gg/exemple)",
        color=discord.Color.blue(),
    )
    await ctx.send(embed=embed)

# Réduction des niveaux chaque jour
async def decrease_levels():
    while True:
        await asyncio.sleep(86400)  # 86400 secondes = 1 jour
        for user_id in list(levels.keys()):
            levels[user_id] = max(0, levels[user_id] - 5)
        with open("levels.json", "w") as f:
            json.dump(levels, f)


bot.run(TOKEN)
