import asyncio

topics = {}
class broker():

    async def gestisci_client(self, reader, writer):
        try:

            while True:
                dati = await reader.readline()
                if not dati:
                    break
                testo = dati.decode("ascii").strip()
                print("Testo ricevuto:", testo)
                if testo.startswith("sub:"):
                    topic = testo[4:]
                    if topic not in topics:
                        topics[topic] = []
                    if writer not in topics[topic]:
                        topics[topic].append(writer)

                    print("Nuova sottoscrizione:", topic)

                elif testo.startswith("pub:"):
                    parti = testo.split(":", 2)
                    if len(parti) == 3:

                        topic = parti[1]

                        messaggio = parti[2]

                        print("Pubblicazione sul topic:", topic)

                        subscribers = topics.get(topic, [])

                        for subscriber in subscribers:
                            subscriber.write(
                                f"{topic}:{messaggio}\n".encode("ascii")
                            )

                            await subscriber.drain()

        except (ConnectionError, UnicodeDecodeError):
            pass

        finally:
            for lista in topics.values():
                if writer in lista:
                    lista.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def main(self):
        server = await asyncio.start_server(
            self.gestisci_client, "localhost", 5000
        )
        print("Server in ascolto sulla porta 5000")
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(broker().main())

