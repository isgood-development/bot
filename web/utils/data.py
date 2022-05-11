async def _inform_to_bot(data, ipc):
    for setting, value in data.items():
        await ipc.inform((setting, value,), destinations=['ig-bot'])