from quart import Blueprint, render_template, redirect, request, url_for, current_app as app

dash = Blueprint("dashboard", __name__)


@dash.route("/dashboard")
async def dashboard_no_guild():
    return redirect(url_for("server_selection"))

@dash.route("/dashboard/<int:guild_id>", methods=["POST", "GET"])
async def dashboard(guild_id):
    if not await app.discord.authorized:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        form = await request.form
        print(form)

    guild = await app.ipc.request("get_guild_data", source="ig-bot", guild_id=guild_id)

    if guild is None:
        return redirect(f"https://discord.com/api/oauth2/authorize?client_id={app.config['DISCORD_CLIENT_ID']}&permissions=8&scope=bot%20applications.commands")

    user = await app.discord.fetch_user()

    uname = user.name
    uavatar = user.avatar_url

    return await render_template(
        "dashboard.html",
        name=guild["name"],
        icon_url=guild["icon_url"],
        created_at=guild["created_at"],
        owner=guild["owner"],
        channels=guild["channels"],
        roles=guild["roles"],
        prefix=guild["prefix"],
        modrole=guild["modrole"],
        member_count=guild["member_count"],
        member_count_no_bot=guild["member_count_no_bot"],
        bots=int(guild["member_count"]) - int(guild["member_count_no_bot"]),
        username=uname,
        avatar=uavatar,

    )