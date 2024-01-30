import asyncio

from core.app import ServerConnectionScreen


async def main():
    main_menu = ServerConnectionScreen()
    main_menu.mainloop()


if __name__ == '__main__':
    asyncio.run(main())
