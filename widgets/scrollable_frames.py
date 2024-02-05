import customtkinter


class ScrollableCheckBoxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = customtkinter.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]


class ScrollableRadiobuttonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = customtkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()


class PlayerScrollableButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command_1=None, command_2=None, **kwargs):
        super().__init__(master, **kwargs)
        self.command_1 = command_1
        self.command_2 = command_2
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):

        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button_1 = customtkinter.CTkButton(self, text="Command", width=75, height=24)
        button_2 = customtkinter.CTkButton(self, text="Command", width=75, height=24)

        if self.command_1 is not None:
            button_1.configure(command=lambda: self.command_1(item))
        if self.command_2 is not None:
            button_1.configure(command=lambda: self.command_2(item))


        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button_1.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        button_2.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)

        # label.pack(side="top", pady=(2, 2), anchor="w")
        # button_1.pack(in_=label, side="top", pady=(0, 0), padx=5)
        # button_2.pack(in_=label, side="top", pady=(0, 0), padx=5)
        button_1.place(x=10, y=25 * len(self.button_list) + 24)
        button_2.place(x=90, y=25 * len(self.button_list) + 24)

        self.label_list.append(label)
        self.button_list.append(button_1)
        self.button_list.append(button_2)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return
