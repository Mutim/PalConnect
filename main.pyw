from core.login import ServerConnectionScreen
import asyncio


def main():
    print("Starting Main Program Loop")
    # main_menu = ServerConnectionScreen()
    ServerConnectionScreen().mainloop()


if __name__ == '__main__':
    main()
