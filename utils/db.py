from discord.ext import commands

def execute(bot: commands.Bot, query: str, **values):
    bot.conn.execute(query, **values)

def fetch(bot: commands.Bot, query: str, **values):
    bot.conn.fetch(query, **values)

def create_tables():
    query = """CREATE TABLE public.prefixes
    (
        guild_id bigint NOT NULL,
        prefix character varying NOT NULL,
        PRIMARY KEY (guild_id)
    )
    WITH (
        OIDS = FALSE
    );

    CREATE TABLE public.prefixes
    (
        guild_id bigint NOT NULL,
        prefix character varying NOT NULL,
        PRIMARY KEY (guild_id)
    )
    WITH (
        OIDS = FALSE
    );

    ALTER TABLE IF EXISTS public.prefixes, public.botbans
    OWNER to postgres;
    """
