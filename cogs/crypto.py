import discord
import cryptocompare
from discord.ext import commands
from discord.commands.commands import slash_command

class CryptoRoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role):
        super().__init__(label=role.name,
                         style=discord.enums.ButtonStyle.primary, custom_id=str(role.id))

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        role = interaction.guild.get_role(int(self.custom_id))
        if role is None:
            return
        if role not in user.roles:
            await user.add_roles(role)
            await interaction.response.send_message(f"🎉 You have been given the role {role.mention}", ephemeral=True)
        else:
            await user.remove_roles(role)
            await interaction.response.send_message(f"❌ The {role.mention} role has been taken from you", ephemeral=True)

class Crypto(commands.Cog, name="Crypto Commands"):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="cprice", usage=f"(crypto) (number)", description="Sends an embed with the chosen crypto to USD or the cryptos chosen by Loveless#2020")
    async def cprice(self, ctx, crypto=None, number=None):
        await ctx.message.delete()
        c = cryptocompare.get_coin_list(format=False)
        if crypto and not number:
            try:
                em = discord.Embed(color=0xF39C12, title=":scales: Crypto Price(s)", description=f"Fetched USD price for {crypto.upper()}")
                price = cryptocompare.get_price(coin=crypto.upper(), currency="USD")
                em.add_field(name=f"{c[crypto.upper()]['FullName']}", value=f"${price[crypto.upper()]['USD']}", inline=False)
                em.set_thumbnail(url=f"https://www.cryptocompare.com/{c[crypto.upper()]['ImageUrl']}")
            except Exception as e:
                print(e)
                em = discord.Embed(color=0xFF0000, title=":x: Crypto Not Found", description=f"The crypto you selected `{crypto.upper()}` could not be found!")
            await ctx.send(embed=em)
            return
        if crypto and number:
            try:
                em = discord.Embed(color=0xF39C12, title=":scales: Crypto Price(s)", description=f"Converted {number} {crypto.upper()} to USD")
                price = cryptocompare.get_price(coin=crypto.upper(), currency="USD")
                em.add_field(name=f"{c[crypto.upper()]['FullName']}", value=f"{number} {crypto.upper()} => ${round(price[crypto.upper()]['USD']*int(number), 2)}", inline=False)
                em.set_thumbnail(url=f"https://www.cryptocompare.com/{c[crypto.upper()]['ImageUrl']}")
            except Exception as e:
                print(e)
                em = discord.Embed(color=0xFF0000, title=":x: Crypto Not Found", description=f"The crypto you selected `{crypto}` could not be found!")
            await ctx.send(embed=em)
            return
        pop_c = ["BTC", "ETH", "DOGE", "XMR", "XRP", "ZOO"]
        em = discord.Embed(color=0xF39C12, title=":scales: Crypto Price(s)", description=f"Fetched the {len(pop_c)} hottest cryptocurrencies")
        prices = cryptocompare.get_price(pop_c, "USD")
        for crypto in pop_c:
            em.add_field(name=f"{c[crypto.upper()]['FullName']}", value=f"${prices[crypto.upper()]['USD']}", inline=False)
        await ctx.send(embed=em)
        return

    @commands.has_permissions(manage_guild=True)
    @commands.command(pass_context=True, name="cbutton", usage=f"[#channel] [@role] \"(title)\" \"(description)\"", description="Publishes an embed in the selected channel with a button that gives a role")
    async def cbutton(self, ctx, channel: discord.TextChannel, role: discord.Role, title=None, desc=None):
        await ctx.message.delete()
        if title is None:
            title = "Crypto Role Giver"
        if desc is None:
            desc = "Click the button to receive the Crypto role!"
        view = discord.ui.View(timeout=None)
        view.add_item(CryptoRoleButton(role))
        em = discord.Embed(color=0xF39C12, title=title, description=desc)
        await channel.send(embed=em, view=view)
        self.bot.add_view(view)

def setup(bot):
    bot.add_cog(Crypto(bot))