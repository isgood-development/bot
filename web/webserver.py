from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from decouple import config, UndefinedValueError
from logging import getLogger
import logging
import winerp

from dashboard import dash

app = Quart(__name__, static_folder="./templates/static/")
app.register_blueprint(dash)

getLogger("winerp").setLevel(logging.DEBUG)

@app.errorhandler(404)

async def not_found(e):
    return await render_template("404.html")

app.config["SECRET_KEY"] = "."
try:
    app.config["DISCORD_CLIENT_ID"] = config("CLIENT_ID")
    app.config["DISCORD_CLIENT_SECRET"] = config("CLIENT_SECRET")
except UndefinedValueError:
    raise ValueError("You haven't provided a CLIENT_ID or CLIENT_SECRET in the '.env' file.")
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:3050/callback"   


app.discord = DiscordOAuth2Session(app)
app.ipc = winerp.Client("ig-web", port=5464)

@app.before_first_request
async def start_ipc_client():
    print('starting IPC client')
    try:
        await app.ipc.start()
    except Exception as e:
        print(f'failed to connect to IPC client:\n\n {e}')
    finally:
        print('connected to IPC client')

@app.route("/")
async def home():
    authorized = await app.discord.authorized

    if authorized:
        user = await app.discord.fetch_user()
        uname = user.name
        uavatar = user.avatar_url
        return await render_template(
                "index.html",
                authorized=authorized,
                avatar=uavatar,
                username=uname
            )
    else:
        return await render_template(
            "index.html",
            authorized=authorized
        )


@app.route("/login")
async def login():
    return await app.discord.create_session(
        scope=[
            "guilds",
            "identify"
        ]
    )

@app.route("/logout")
async def logout():
    app.discord.revoke()

    return redirect(url_for("home"))

@app.route("/invite")
async def invite():
    return "todo"

@app.route("/callback")
async def callback():
    try:
        await app.discord.callback()
    except:
        pass

    return redirect("server-selection")

@app.route("/server-selection")
async def server_selection():
    if not await app.discord.authorized:
        return redirect(url_for("login"))

    bot_guilds = await app.ipc.request("get_guild_ids", source="ig-bot")
    user_guilds = await app.discord.fetch_guilds()

    all_guilds = []

    for guild in user_guilds:
        if guild.permissions.administrator:
            guild.cls_colour = "green-border" if guild.id in bot_guilds else "red-border"
            all_guilds.append(guild)

    all_guilds.sort(key=lambda x: x.cls_colour == "red-border")

    user = await app.discord.fetch_user()

    uname = user.name
    uavatar = user.avatar_url

    return await render_template(
        "server_select.html",
        all_guilds=all_guilds,
        username=uname,
        avatar=uavatar
    )

if __name__ == "__main__":
    app.run(port=3050, debug=True)
