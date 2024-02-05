from core.login import ServerConnectionScreen


def main():
    print("Starting Main Program Loop")
    main_menu = ServerConnectionScreen()
    main_menu.mainloop()


if __name__ == '__main__':
    main()
