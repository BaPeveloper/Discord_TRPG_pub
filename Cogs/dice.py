'''
-------------------------------------------------------------------
* item.py
* 
* command : /test /tt
-------------------------------------------------------------------
'''
# Module Import

import random
import discord
from discord.ext import commands
from discord import app_commands

from sheet import sheet, init_Enum, sanc
import re

'''
-------------------------------------------------------------------
[Class]
'''

def roll_dice(roll_str):
    pattern = r'(\d+)?d(\d+)'
    match = re.findall(pattern, roll_str)

    if match:
        dice_results = []
        for m in match:
            num_dice = int(m[0]) if m[0] else 1
            dice_size = int(m[1])

            result = [random.randint(1, dice_size) for _ in range(num_dice)]
            dice_results.append(result)

            result_str = f"({'+'.join(map(str, result))})"
            roll_str = roll_str.replace(f"{m[0]}d{m[1]}", result_str, 1)

        return roll_str
    else:
        return None
        


class Dice(commands.Cog):
    Skill = init_Enum()

    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="판정", description="Call of Cthulhu Dice")
    async def dice(
        self, 
        interaction: discord.Interaction, 
        기능 : Skill) -> None:
        await interaction.response.defer()
        
        try:
            user = interaction.user.display_name
            # 다시 설정
            Skill_dict = sheet(user)
            dice_val = random.randrange(1,100)
            skill_point = Skill_dict[기능.value]
            
            point1 = int(skill_point/5)
            point2 = int(skill_point/2)
            result = '오류'
            color = 0
            if (dice_val == 1) :
                result = '대성공'
                color = 0x59ff00
            elif (dice_val > 1 and dice_val <= point1) :
                result = '극단적 성공'
                color = 0x04db00
            elif (dice_val > point1 and dice_val <= point2) :
                result = '어려운 성공'
                color = 0x06ba03
            elif (dice_val > point2 and dice_val <= skill_point) :
                result = '성공'
                color = 0x028f00
            elif (dice_val > skill_point) :
                if (skill_point < 50 and dice_val >= 96):
                    result = '대실패'
                    color = 0xff0000
                elif (skill_point >= 50 and dice_val == 100):
                    result = '대실패'
                    color = 0xff0000
                else :
                    result = '실패'
                    color = 0x9e0000
            embed = discord.Embed(title= ':game_die:  ' + str(기능.name),description="────────────────────────────", colour=discord.Colour(color))
            embed.add_field(name= ":white_small_square: 결과 :  "+ result, value = ' ',  inline=False)
            # embed.add_field(name= str(skill_point) + " / " + str(point2) + " / " + str(point1), value = '', inline=False)
            embed.set_footer(text=str(skill_point) + " / " + str(point2) + " / " + str(point1))
            embed.add_field(name=str(dice_val) , value= '', inline=False)
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"오류가 발생했습니다: {e}", ephemeral=True)

    @app_commands.command(name="sanc", description="[SanC] 숫자만 입력 or dice 형태로 입력 ex. 1d3+5")
    async def sancheck(
        self, 
        interaction: discord.Interaction, 
        성공 : str,
        실패 : str) -> None:
        await interaction.response.defer()
        try : 
            user = interaction.user.display_name
            
            success_str = roll_dice(성공)
            if (success_str) == None :
                success_str = 성공
                success = int(성공)
            else :
                success = eval(success_str)

            fail_str = roll_dice(실패)
            if (fail_str) == None :
                fail_str = 실패
                fail = int(실패)
            else :
                fail = eval(fail_str)
            
            result, dice_result = sanc(user, success, fail)
            
            minus_val = 0
            minus_str = ''
            color = 0
            if (result == '실패') :
                color = 0x9e0000
                minus_val = fail
                minus_str = fail_str

            elif (result == '성공') :
                color = 0x028f00
                minus_val = success
                minus_str = success_str
            
            embed = discord.Embed(title= ':game_die: SanC '+성공+ '/'+실패 ,description="────────────────────────────", colour=discord.Colour(color))
            embed.add_field(name= ":white_small_square: 결과 :  "+ str(result), value = ' ',  inline=False)
            if minus_val > 0 :
                embed.add_field(name= '이성 :  -'+str(minus_val), value= '', inline=False)
            else :
                embed.add_field(name= '이성 감소 없음', value= '', inline=False)
            if not minus_str.isdigit() :
                embed.set_footer(text=minus_str)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"다이스 형식이 올바르지 않습니다. 다이스 형식은 'NdM' 또는 'NdM+X'와 같은 형식이어야 합니다.", ephemeral=True)

    @app_commands.command(name="r", description="Nomal Dice")
    async def dice_nomal(
        self, 
        interaction: discord.Interaction, 
        다이스 : str) -> None:
        await interaction.response.defer()
        try : 
            modified_expr = roll_dice(다이스)
            result = eval(modified_expr)
            embed = discord.Embed(title= ':game_die:  ' + 다이스,description="────────────────────────────", colour=discord.Colour(0))
            embed.add_field(name= ":white_small_square: 결과 :  "+ str(result), value = ' ',  inline=False)
            embed.set_footer(text=modified_expr)
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"다이스 형식이 올바르지 않습니다. 다이스 형식은 'NdM' 또는 'NdM+X'와 같은 형식이어야 합니다.", ephemeral=True)
    

'''
-------------------------------------------------------------------
[Setting]
'''
async def setup(bot):
    await bot.add_cog(Dice(bot))
