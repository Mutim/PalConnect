from core.login import ServerConnectionScreen
import asyncio


def main():
    print("Starting Main Program Loop")

    loop = asyncio.get_event_loop()
    main_menu = ServerConnectionScreen(loop)
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()
