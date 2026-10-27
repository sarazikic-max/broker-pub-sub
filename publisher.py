#Pubblica un messaggio su un topic

import asyncio,sys

async def main():

    host = sys.argv[1]
    topic = sys.argv[2]
    messaggio = sys.argv[3]
    reader, writer = await asyncio.open_connection(host, 5000)
    testo = f"pub:{topic}:{messaggio}\n"
    writer.write(testo.encode("ascii"))
    await writer.drain()
    writer.close()
    await writer.wait_closed()

asyncio.run(main())
