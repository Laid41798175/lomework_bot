from dotenv import load_dotenv
load_dotenv()

import os
import discord
import boto3
from discord.ext import commands
from discord.utils import get

from expedition import EXPEDITIONS
from content import CONTENTS
from alias import get_class
from owner import get_id, get_owner

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('expedition')

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)
BOT_TOKEN = os.getenv('BOT_TOKEN')
RESET_STATE = 'aaaaaaa'

@bot.event
async def on_ready():
    activity = discord.Activity(name="!도움", type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity)

def get_item(owner, nickname):
    response = table.get_item(
        Key = {
            'owner': owner,
            'nickname': nickname
        }
    )
    item = response.get('Item')
    if item:
        return item
    else:
        raise KeyError

def get_item_state(owner, nickname):
    item = get_item(owner, nickname)
    state = item.get('state')
    if state:
        return state
    else:
        raise KeyError
    
def get_item_class(owner, nickname):
    item = get_item(owner, nickname)
    _class = item.get('class')
    if _class:
        return _class
    else:
        raise KeyError

def check_clearable(state: str, content: int, abrelshud4 = False) -> bool:
    if content == 3 and abrelshud4:
        return state[content] == 'd'
    
    count = 0
    for i in range(len(state)):
        if state[i] in ['b', 'd', 'e']:
            if i == content:
                return False
            count += 1
            
    return count < 3

def replace_index(state, index, new_char) -> str:
    return state[:index] + new_char + state[index + 1:]

def get_new_state(state: str, content: str, abrelshud4 = False) -> str:
    if content == 3:
        if abrelshud4:
            return replace_index(state, content, 'b')
        else:
            if state[content] == 'a': # 진행 가능
                return replace_index(state, content, 'd') # 3관문 클리어
            elif state[content] == 'c': # 진행 가능 (지난 주 클리어)
                return replace_index(state, content, 'e') # 3관문 클리어
            else:
                raise KeyError
    else:
        return replace_index(state, content, 'b')

def update_state(owner, nickname, new_state) -> bool:
    try:
        response = table.update_item(
            Key={
                'owner': owner,
                'nickname': nickname
            },
            UpdateExpression='SET #attr = :val',
            ExpressionAttributeNames={
                '#attr': 'state',
            },
            ExpressionAttributeValues={
                ':val': new_state,
            },
            ReturnValues="NONE"
        )
    
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            print("Update failed")
            return False
    except Exception as e:
        print(f"Error updating item: {e}")
        return False

def expedition_state(owner) -> str:
    result = f"{owner}'s expedition\n"
    expedition = EXPEDITIONS[owner]
    for key, nickname in expedition.items():
        result += f"{nickname} ({get_item_class(owner, nickname)})\n"
        state = get_item_state(owner, nickname)
        contents = []
        for i, char in enumerate(state):
            if char == 'a':
                pass
            elif char == 'b':
                contents.append('아브4' if i == 3 else CONTENTS[i])
            elif char == 'c':
                pass
            elif char == 'd':
                contents.append('아브13' if i == 3 else CONTENTS[i])
            elif char == 'e':
                contents.append('아브13' if i == 3 else CONTENTS[i])
            else:
                raise KeyError
        while len(contents) < 3:
            contents.append(None)
        result += f"1. {contents[0]} / 2. {contents[1]} / 3. {contents[2]}\n"
    return result

@bot.command(name='깃헙', aliases=['깃허브', 'github'])
async def github(ctx):
    await ctx.send("https://github.com/Laid41798175/lomework")
    await ctx.send("https://github.com/Laid41798175/lomework_bot")

@bot.command(name='도움', aliases=['헬프'])
async def help(ctx):
    await ctx.send("!숙제, !리셋 (직업), !올리셋, !깃헙")
    await ctx.send("!발탄/비아/쿠크/... (직업)")

@bot.command(name='숙제')
async def print_state(ctx):
    try:
        id = get_id(ctx)
        owner = get_owner(id)
        result = expedition_state(owner)
        await ctx.send(result)
        await ctx.message.add_reaction('⭕')
    except KeyError:
        await ctx.send("Who are you? (please contact Amanna)")
        await ctx.message.add_reaction('❓')

@bot.command(name='리셋')
async def reset(ctx, alias=None):
    if alias is None:
        await ctx.send('Please try !올리셋')
        await ctx.message.add_reaction('❌')
        return
    await reset_character(ctx, alias)

async def reset_character(ctx, alias):
    id = get_id(ctx)
    try:
        owner = get_owner(id)
    except KeyError:
        await ctx.send("Who are you? (please contact Amanna)")
        await ctx.message.add_reaction('❓')
        return
    
    expedition = EXPEDITIONS[owner]
    try:
        character_class = get_class(alias)
    except KeyError:
        await ctx.send("There is no such alias. (If you intended a class, please contact Amanna)")
        await ctx.message.add_reaction('❓')
        return

    nickname = expedition.get(character_class, None)
    if nickname is None:
        await ctx.send("Hmm.. It seems you don't have a character of that.")
        await ctx.message.add_reaction('❓')
        return
    
    update = update_state(owner, nickname, RESET_STATE)
    await ctx.message.add_reaction('⭕' if update else '❌')
    
@bot.command(name='올리셋')
async def all_reset(ctx):
    id = get_id(ctx)
    try:
        owner = get_owner(id)
    except KeyError:
        await ctx.send("Who are you? (please contact Amanna)")
        await ctx.message.add_reaction('❓')
    expedition = EXPEDITIONS[owner]
    for key, nickname in expedition.items():
        update = update_state(owner, nickname, RESET_STATE)
        if not update:
            await ctx.message.add_reaction('❌')
            return
    await ctx.message.add_reaction('⭕')
        
@bot.command(name='발탄', aliases=['발하'])
async def valtan(ctx, alias=None):
    if alias is None:
        await ctx.send('Please specify your character by its class!')
        await ctx.message.add_reaction('❌')
        return
    await select_content(ctx, 0, alias)

@bot.command(name='비아키스', aliases=['비하', '비아'])
async def biackiss(ctx, alias=None):
    if alias is None:
        await ctx.send('Please specify your character by its class!')
        await ctx.message.add_reaction('❌')
        return
    await select_content(ctx, 1, alias)

@bot.command(name='쿠크세이튼', aliases=['쿠크'])
async def kouku_saton(ctx, alias=None):
    if alias is None:
        await ctx.send('Please specify your character by its class!')
        await ctx.message.add_reaction('❌')
        return
    await select_content(ctx, 2, alias)
    
@bot.command(name='아브렐슈드13', aliases=['아브13', '노브13', '하브13', '하12노3', '아브3', '노브3', '하브3'])
async def abrelshud3(ctx, alias=None):
    if alias is None:
        await ctx.send('Please specify your character by its class!')
        await ctx.message.add_reaction('❌')
        return
    await select_content(ctx, 3, alias) 

@bot.command(name='아브렐슈드4', aliases=['아브4', '노브4', '하브4'])
async def abrelshud4(ctx, alias=None):
    if alias is None:
        await ctx.send('Please specify your character by its class!')
        await ctx.message.add_reaction('❌')
        return
    await select_content(ctx, 3, alias, True)

@bot.command(name='카양겔', aliases=['노양겔', '하양겔', '양겔', '카양', '노양', '하양'])
async def kayangel(ctx, alias=None):
    if alias is None:
        await ctx.send('Please specify your character by its class!')
        await ctx.message.add_reaction('❌')
        return
    await select_content(ctx, 4, alias)

@bot.command(name='일리아칸', aliases=['일리', '아칸', '노칸', '하칸'])
async def illiakan(ctx, alias=None):
    if alias is None:
        await ctx.send('Please specify your character by its class!')
        await ctx.message.add_reaction('❌')
        return
    await select_content(ctx, 5, alias)
    
@bot.command(name='상아탑', aliases=['상노탑', '상하탑', '아탑', '노탑', '하탑'])
async def voldis(ctx, alias=None):
    if alias is None:
        await ctx.send('Please specify your character by its class!')
        await ctx.message.add_reaction('❌')
        return
    await select_content(ctx, 6, alias) 

@bot.command(name='아브렐슈드', aliases=['아브', '노브', '하브'])
async def abrelshud(ctx, alias=None):
    await ctx.send('Please try !아브13 or !아브4')
    await ctx.message.add_reaction('❌')
    return

async def select_content(ctx, content: int, alias: str, abrelshud4 = False):
    id = get_id(ctx)
    try:
        owner = get_owner(id)
    except KeyError:
        await ctx.send("Who are you? (please contact Amanna)")
        await ctx.message.add_reaction('❓')
    expedition = EXPEDITIONS[owner]
    try:
        character_class = get_class(alias)
    except KeyError:
        await ctx.send("There is no such alias. (If you intended a class, please contact Amanna)")
        await ctx.message.add_reaction('❓')
        return
    
    nickname = expedition.get(character_class, None)
    if nickname is None:
        await ctx.send("Hmm.. It seems you don't have a character of that.")
        await ctx.message.add_reaction('❓')
        return
    
    state = get_item_state(owner, nickname)
    if not check_clearable(state, content, abrelshud4):
        await ctx.send(f"{nickname} cannot clear the content!")
        await ctx.message.add_reaction('❌')
        return
    
    new_state = get_new_state(state, content, abrelshud4)
    update = update_state(owner, nickname, new_state)
    await ctx.message.add_reaction('⭕' if update else '❌')

if __name__ == '__main__':
    bot.run(BOT_TOKEN)