'''
-------------------------------------------------------------------
* Discord_Bot_TRPG
*
* COPYRIGHT ⓒ 2024 BaPeveloper
*
-------------------------------------------------------------------
'''
# Module Import

import logging
import os

from dotenv import load_dotenv
import discord
from discord.ext import commands

'''
-------------------------------------------------------------------
[Main Bot Class]
'''
load_dotenv()
# Cogs List
extension_list = ["dice"]        

class DiscordBot(commands.Bot):
    def __init__(self, logger):
        super().__init__(
            command_prefix="!",             
            intents=discord.Intents.all()
        )
        self.logger = logger

    # Command Setup
    async def setup_hook(self):
        for ext in extension_list:
            await self.load_extension(f"Cogs.{ext}")    # Command Load
        await bot.tree.sync()                           # CommandTree Load (@app_commands.command)

    # Bot is Ready
    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user}")
    
    # Error Handler
    async def on_error(self, event, *args, **kwargs):
        self.logger.exception("")

    
'''
-------------------------------------------------------------------
[Main]
'''

# Main
if __name__ == "__main__":
    bot = DiscordBot(logger=logging.getLogger("bot"))

    @bot.tree.command(name="reload", description="CoC 기능치 재입력 시 사용")
    async def reload (interaction: discord.Interaction) :
        await interaction.response.defer()
        try : 
            for ext in extension_list:
                await bot.unload_extension(f"Cogs.{ext}")
                await bot.load_extension(f"Cogs.{ext}")
            await bot.tree.sync()   
            await interaction.followup.send(f"> 설정을 다시 로드합니다.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed! Could not reload this cog class. See error below\n```{e}```")

    # TOKEN needs to be changed
    bot.run(os.getenv('DISCORD_TOKEN'))                    
     
