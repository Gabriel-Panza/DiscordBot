import datetime
import discord

intents = discord.Intents.all()
intents.reactions = True  # Enable reaction events

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is logged in")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1207894821054717995)
    embed = discord.Embed(
        description=f"Bem vindo ao barco, **{member.mention}**!",
        color= 0x8520f0,
        timestamp=datetime.datetime.now()
    )
    await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1207894821054717995)
    embed = discord.Embed(
        description=f"Parece que **{member.mention}** pulou do barco!",
        color= 0x8520f0,
        timestamp=datetime.datetime.now()
    )
    await channel.send(embed=embed)

async def verificar_cargo_dos_reagentes(message_id, guild, name_role):
    role = discord.utils.get(guild.roles, name=name_role)
    if not role:
        print(f"O cargo {name_role} não foi encontrado no servidor.")
        return

    channel_list = guild.text_channels
    for channel in channel_list:
        try:
            msg = await channel.fetch_message(message_id)
            for reaction in msg.reactions:
                async for user in reaction.users():
                    member = guild.get_member(user.id)
                    if member and role not in member.roles:
                        await member.add_roles(role)
                        print(f"Assigned role {role.name} to {member.display_name}")
            break  # Interrompe após encontrar e processar a mensagem
        except discord.NotFound:
            continue  # A mensagem não foi encontrada neste canal, tenta o próximo
        except discord.Forbidden:
            print(f"O bot não tem permissão para acessar as mensagens no canal {channel.name}.")
            continue
        except discord.HTTPException as e:
            print(f"Erro ao buscar mensagens no canal {channel.name}: {e}")
            continue

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 1208114165538103366:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        if guild is not None:
            await verificar_cargo_dos_reagentes(message_id, guild, payload.emoji.name)
        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print(f"Assigned role {role.name} to {member.display_name}")
            else:
                print("Member not found!")
        else:
            print("Role not found!")

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 1208114165538103366:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        
        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                print(f"Removed role {role.name} from {member.display_name}")
            else:
                print("Member not found!")
        else:
            print("Role not found!")

client.run("")