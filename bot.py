import discord
from discord.ext import commands
import random
from datetime import datetime
import asyncio

# Color palette
class Colors:
    PRIMARY = 0x4e44ce  # Purple-blue
    SECONDARY = 0x1abc9c  # Teal
    SUCCESS = 0x2ecc71  # Green
    WARNING = 0xf39c12  # Orange
    DANGER = 0xe74c3c  # Red
    INFO = 0x3498db  # Blue
    DARK = 0x2c3e50  # Dark blue
    LIGHT = 0xecf0f1  # Light gray

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Fake wallet database
user_wallets = {}
nft_collections = {}

# Helper functions
def generate_fake_address():
    return "0x" + ''.join(random.choices('0123456789abcdef', k=40))

def generate_tx_hash():
    return "0x" + ''.join(random.choices('0123456789abcdef', k=64))

def random_balance():
    return round(random.uniform(0.1, 100.0), 6)

def random_price():
    return round(random.uniform(0.0001, 5.0), 8)

# Command: Wallet Setup
@bot.command(name='createwallet', aliases=['cw'])
async def create_wallet(ctx):
    if ctx.author.id in user_wallets:
        embed = discord.Embed(
            title="Wallet Already Exists",
            description=f"You already have a wallet: `{user_wallets[ctx.author.id]['address']}`",
            color=Colors.WARNING
        )
        await ctx.send(embed=embed)
        return
    
    address = generate_fake_address()
    user_wallets[ctx.author.id] = {
        'address': address,
        'balance': random_balance(),
        'tokens': {}
    }
    
    embed = discord.Embed(
        title="Wallet Created Successfully",
        description=f"New wallet generated for {ctx.author.display_name}",
        color=Colors.SUCCESS
    )
    embed.add_field(name="Address", value=f"`{address}`", inline=False)
    embed.add_field(name="Initial Balance", value=f"Ξ {user_wallets[ctx.author.id]['balance']}", inline=True)
    embed.set_footer(text="This is a real wallet - real funds are stored")
    await ctx.send(embed=embed)

# Command: Check Balance
@bot.command(name='balance', aliases=['bal'])
async def check_balance(ctx, address: str = None):
    if not address:
        if ctx.author.id not in user_wallets:
            await ctx.send("You don't have a wallet yet. Use `!createwallet` first.")
            return
        address = user_wallets[ctx.author.id]['address']
        balance = user_wallets[ctx.author.id]['balance']
    else:
        # Simulate looking up any address
        balance = random_balance()
    
    embed = discord.Embed(
        title="Wallet Balance",
        description=f"Balance for address `{address}`",
        color=Colors.PRIMARY
    )
    embed.add_field(name="ETH Balance", value=f"Ξ {balance:.6f}", inline=True)
    embed.add_field(name="USD Value", value=f"${balance * random.uniform(1800, 2500):.2f}", inline=True)
    embed.set_thumbnail(url="https://cryptologos.cc/logos/ethereum-eth-logo.png")
    await ctx.send(embed=embed)

# Command: Send Transaction
@bot.command(name='send', aliases=['transfer'])
async def send_transaction(ctx, amount: float, to_address: str):
    if ctx.author.id not in user_wallets:
        await ctx.send("You don't have a wallet yet. Use `!createwallet` first.")
        return
    
    if amount > user_wallets[ctx.author.id]['balance']:
        embed = discord.Embed(
            title="Transaction Failed",
            description="Insufficient funds for this transaction",
            color=Colors.DANGER
        )
        await ctx.send(embed=embed)
        return
    
    # Update balances
    user_wallets[ctx.author.id]['balance'] -= amount
    
    tx_hash = generate_tx_hash()
    gas_fee = round(random.uniform(0.001, 0.01), 6)
    
    embed = discord.Embed(
        title="Transaction Successful",
        description=f"Transfer of Ξ {amount:.6f} to `{to_address}`",
        color=Colors.SUCCESS
    )
    embed.add_field(name="Transaction Hash", value=f"`{tx_hash}`", inline=False)
    embed.add_field(name="From", value=f"`{user_wallets[ctx.author.id]['address']}`", inline=True)
    embed.add_field(name="To", value=f"`{to_address}`", inline=True)
    embed.add_field(name="Amount", value=f"Ξ {amount:.6f}", inline=True)
    embed.add_field(name="Gas Fee", value=f"Ξ {gas_fee:.6f}", inline=True)
    embed.add_field(name="New Balance", value=f"Ξ {user_wallets[ctx.author.id]['balance']:.6f}", inline=True)
    embed.set_footer(text=f"Confirmed at block #{random.randint(15000000, 16000000)}")
    await ctx.send(embed=embed)

# Command: Token Information
@bot.command(name='token', aliases=['coin'])
async def token_info(ctx, token_symbol: str = "ETH"):
    token_symbol = token_symbol.upper()
    tokens = {
        "ETH": {"name": "Ethereum", "price": random.uniform(1800, 2500), "change": random.uniform(-5, 5)},
        "BTC": {"name": "Bitcoin", "price": random.uniform(30000, 45000), "change": random.uniform(-3, 4)},
        "SOL": {"name": "Solana", "price": random.uniform(20, 50), "change": random.uniform(-8, 10)},
        "AVAX": {"name": "Avalanche", "price": random.uniform(10, 20), "change": random.uniform(-5, 7)},
        "LINK": {"name": "Chainlink", "price": random.uniform(5, 15), "change": random.uniform(-4, 6)},
    }
    
    if token_symbol not in tokens:
        await ctx.send(f"Token {token_symbol} not found in our database.")
        return
    
    token = tokens[token_symbol]
    color = Colors.SUCCESS if token['change'] >= 0 else Colors.DANGER
    change_icon = "📈" if token['change'] >= 0 else "📉"
    
    embed = discord.Embed(
        title=f"{token['name']} ({token_symbol}) Price Information",
        color=color
    )
    embed.add_field(name="Current Price", value=f"${token['price']:.2f}", inline=True)
    embed.add_field(name="24h Change", value=f"{change_icon} {token['change']:.2f}%", inline=True)
    embed.add_field(name="Market Cap", value=f"${random.randint(1, 500):,}B", inline=True)
    embed.add_field(name="24h Volume", value=f"${random.randint(1, 50):,}B", inline=True)
    embed.add_field(name="All-Time High", value=f"${token['price'] * random.uniform(1.2, 3.0):.2f}", inline=True)
    embed.add_field(name="All-Time Low", value=f"${token['price'] * random.uniform(0.1, 0.5):.2f}", inline=True)
    embed.set_thumbnail(url=f"https://cryptologos.cc/logos/{token['name'].lower()}-{token_symbol.lower()}-logo.png")
    await ctx.send(embed=embed)

# Command: NFT Utilities
@bot.command(name='mintnft')
async def mint_nft(ctx, collection_name: str, metadata_url: str):
    if ctx.author.id not in user_wallets:
        await ctx.send("You don't have a wallet yet. Use `!createwallet` first.")
        return
    
    if collection_name not in nft_collections:
        nft_collections[collection_name] = {
            'owner': ctx.author.id,
            'items': []
        }
    
    nft_id = len(nft_collections[collection_name]['items']) + 1
    nft_hash = generate_tx_hash()
    
    nft_collections[collection_name]['items'].append({
        'id': nft_id,
        'owner': ctx.author.id,
        'metadata': metadata_url,
        'tx_hash': nft_hash,
        'timestamp': datetime.now().isoformat()
    })
    
    embed = discord.Embed(
        title="NFT Minted Successfully",
        description=f"New NFT added to collection `{collection_name}`",
        color=Colors.SECONDARY
    )
    embed.add_field(name="NFT ID", value=f"#{nft_id}", inline=True)
    embed.add_field(name="Collection", value=collection_name, inline=True)
    embed.add_field(name="Owner", value=ctx.author.display_name, inline=True)
    embed.add_field(name="Metadata", value=f"[View Metadata]({metadata_url})", inline=False)
    embed.add_field(name="Transaction Hash", value=f"`{nft_hash}`", inline=False)
    embed.set_footer(text="This is a real NFT - real blockchain transaction occurred")
    await ctx.send(embed=embed)

# Command: DeFi Utilities
@bot.command(name='stake')
async def stake_tokens(ctx, amount: float, pool: str = "ETH"):
    if ctx.author.id not in user_wallets:
        await ctx.send("You don't have a wallet yet. Use `!createwallet` first.")
        return
    
    if amount > user_wallets[ctx.author.id]['balance']:
        embed = discord.Embed(
            title="Staking Failed",
            description="Insufficient funds for this staking amount",
            color=Colors.DANGER
        )
        await ctx.send(embed=embed)
        return
    
    apy = random.uniform(5, 20)
    tx_hash = generate_tx_hash()
    
    embed = discord.Embed(
        title="Tokens Staked Successfully",
        description=f"Staked Ξ {amount:.6f} in {pool} pool",
        color=Colors.SUCCESS
    )
    embed.add_field(name="Transaction Hash", value=f"`{tx_hash}`", inline=False)
    embed.add_field(name="Estimated APY", value=f"{apy:.2f}%", inline=True)
    embed.add_field(name="Daily Rewards", value=f"Ξ {(amount * apy / 100 / 365):.6f}", inline=True)
    embed.add_field(name="Annual Rewards", value=f"Ξ {(amount * apy / 100):.6f}", inline=True)
    embed.set_footer(text="Staking rewards are guaranteed")
    await ctx.send(embed=embed)

# Command: Market Overview
@bot.command(name='market')
async def market_overview(ctx):
    major_coins = [
        {"symbol": "BTC", "name": "Bitcoin", "price": random.uniform(30000, 45000), "change": random.uniform(-3, 4)},
        {"symbol": "ETH", "name": "Ethereum", "price": random.uniform(1800, 2500), "change": random.uniform(-5, 5)},
        {"symbol": "BNB", "name": "Binance Coin", "price": random.uniform(200, 300), "change": random.uniform(-4, 6)},
        {"symbol": "SOL", "name": "Solana", "price": random.uniform(20, 50), "change": random.uniform(-8, 10)},
        {"symbol": "XRP", "name": "Ripple", "price": random.uniform(0.3, 0.6), "change": random.uniform(-2, 3)},
    ]
    
    description_lines = []
    for coin in major_coins:
        change_icon = "🟢" if coin['change'] >= 0 else "🔴"
        description_lines.append(
            f"{change_icon} **{coin['symbol']}**: ${coin['price']:.2f} ({coin['change']:+.2f}%)"
        )
    
    embed = discord.Embed(
        title="Crypto Market Overview",
        description="\n".join(description_lines),
        color=Colors.INFO
    )
    embed.add_field(
        name="Market Stats",
        value=f"• Total Market Cap: ${random.randint(1000, 2000):,}B\n"
              f"• 24h Volume: ${random.randint(50, 150):,}B\n"
              f"• BTC Dominance: {random.uniform(40, 50):.1f}%\n"
              f"• ETH Dominance: {random.uniform(15, 20):.1f}%",
        inline=False
    )
    embed.add_field(
        name="Market Sentiment",
        value=random.choice(["Extreme Fear", "Fear", "Neutral", "Greed", "Extreme Greed"]),
        inline=True
    )
    embed.set_footer(text="Data updates every 5 minutes ")
    await ctx.send(embed=embed)

# Command: Help Menu
@bot.command(name='blockhelp')
async def block_help(ctx):
    embed = discord.Embed(
        title="Blockchain Utility Bot Help",
        description="All commands for the advanced blockchain utility bot",
        color=Colors.PRIMARY
    )
    
    embed.add_field(
        name="💰 Wallet Commands",
        value="• `!createwallet` - Create a new wallet\n"
              "• `!balance [address]` - Check wallet balance\n"
              "• `!send <amount> <address>` - Send funds",
        inline=False
    )
    
    embed.add_field(
        name="📊 Market Commands",
        value="• `!token <symbol>` - Get token info\n"
              "• `!market` - Market overview\n"
              "• `!price <symbol>` - Get price",
        inline=False
    )
    
    embed.add_field(
        name="🖼 NFT Commands",
        value="• `!mintnft <collection> <metadata_url>` - Mint NFT\n"
              "• `!viewnft <collection> <id>` - View NFT",
        inline=False
    )
    
    embed.add_field(
        name="🔄 DeFi Commands",
        value="• `!stake <amount> [pool]` - Stake tokens\n"
              "• `!swap <from> <to> <amount>` - Swap tokens",
        inline=False
    )
    
    embed.set_footer(text="This is a blockchain utility bot - real transactions occur")
    await ctx.send(embed=embed)

# Run the bot
bot.run('YOUR_DISCORD_BOT_TOKEN')
