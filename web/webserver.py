from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from decouple import config
from logging import getLogger
import logging
import winerp

app = Quart(__name__)

getLogger("winerp").setLevel(logging.DEBUG)
ipc = winerp.Client("ig-web", port=5464)


app.config["SECRET_KEY"] = "."
app.config["DISCORD_CLIENT_ID"] = config("CLIENT_ID")
app.config["DISCORD_CLIENT_SECRET"] = config("CLIENT_SECRET")
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:3050/callback"   

discord = DiscordOAuth2Session(app)

@app.before_first_request
async def start_ipc_client():
    print('starting IPC client')
    try:
        await ipc.start()
    except Exception as e:
        print(f'failed to connect to IPC client:\n\n {e}')
    finally:
        print('connected to IPC client')

@app.route("/")
async def home():
    return await render_template("index.html")

@app.route("/login")
async def login():
    return await discord.create_session()

@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except:
        pass

    return redirect("server-selection")

@app.route("/server-selection")
async def server_selection():
    if not await discord.authorized:
        return redirect(url_for("login"))
    
    guild_ids = await ipc.request("get_guild_ids", source="ig-bot")
    user_guilds = await discord.fetch_guilds()
    
    all_guilds = []

    print(1)
    for guild in user_guilds:
        if guild.permissions.administrator:
            guild.cls_colour = "green-border" if guild.id in all_guilds else "red-border"
            all_guilds.append(guild)
    
    all_guilds.sort(key=lambda x: x.cls_colour == "red-border")
    
    print(2)

    uname = await discord.fetch_user()
    uname = uname.name
    
    print(3)

    print(guild_ids)

    return await render_template(
        "server_select.html",
        all_guilds=all_guilds,
        username=uname
    )

@app.route("/dashboard/<int:guild_id>")
async def dashboard(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))
    
    guild = await ipc.request("get_guild_data", source="ig-bot", guild_id=guild_id)

    if guild is None:
        return redirect(f"https://discord.com/api/oauth2/authorize?client_id={app.config['DISCORD_CLIENT_ID']}&permissions=8&scope=bot%20applications.commands")

    return await render_template(
        "dashboard.html",
        name=guild["name"],
        icon_url=guild["icon_url"],
        created_at=guild["created_at"],
        owner=guild["owner"],
        channels=guild["channels"],
        roles=guild["roles"],
        prefix=guild["prefix"],
        modrole=guild["modrole"]
    )

if __name__ == "__main__":
    app.run(port=3050, debug=True)
