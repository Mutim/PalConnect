def break_message(message, max_length=40, ret="\n"):
    result = []
    current_line = ""

    for word in message.split():
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += f"{word} "
        else:
            result.append(current_line.strip())
            current_line = f"{word} "

    if current_line:
        result.append(current_line.strip())
    current = ""
    for line in result:
        current = f"{current + line}{ret}"
    return current


def main():
    message = "This is a very long message that will be returned if the message length is much much longer than the predetermined length of 40 characters. But it can be specified to use any return method, or character length"
    print(break_message(message))


if __name__ == '__main__':
    main()
