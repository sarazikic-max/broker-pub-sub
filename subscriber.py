#Pubblica un messaggio su un topic

import asyncio,sys

async def main():

    host = sys.argv[1]
    topic = sys.argv[2]
    reader, writer = await asyncio.open_connection(host, 5000)
    writer.write(f"sub:{topic}\n".encode("ascii"))
    await writer.drain()
    while True:
        dati = await reader.readline()
        if not dati:
            break
        print(dati.decode("ascii").strip())
asyncio.run(main())

