import edge_tts, asyncio, json

async def main():
    voices = await edge_tts.list_voices()
    for v in voices:
        name = v["ShortName"]
        if "tr-" in name.lower() or "Multilingual" in name:
            print(f"{name} | {v['Gender']} | {v.get('Locale','')}")

asyncio.run(main())
