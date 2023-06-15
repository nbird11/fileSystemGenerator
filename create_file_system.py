import os
import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        """Creates the gui for the create_file_system application with its functionalities."""
        super().__init__()

        # configure window
        self.title("Create File System")
        self.geometry(f"{720}x{480}")

        self.label_root_dir = ctk.CTkLabel(
            self, text="Full path of root directory to create folder system in:"
        )
        self.label_root_dir.grid(
            column=0, row=0, columnspan=3, padx=10, pady=10, sticky=ctk.W
        )
        self.entry_root_dir = ctk.CTkEntry(
            self, placeholder_text=os.path.abspath("..\\"), width=500
        )
        self.entry_root_dir.grid(column=0, row=1, columnspan=3, padx=10, sticky=ctk.W)
        self.button_browse_local_dirs = ctk.CTkButton(
            self, text="Browse", command=self._browse_local
        )
        self.button_browse_local_dirs.grid(column=4, row=1, padx=10, sticky=ctk.E)

        self.label_root_name = ctk.CTkLabel(
            self, text="Name of the Root Folder for file structure:"
        )
        self.label_root_name.grid(column=0, row=2, padx=10, pady=10, sticky=ctk.W)
        self.entry_root_name = ctk.CTkEntry(self, placeholder_text="Root", width=150)
        self.entry_root_name.grid(column=0, row=3, padx=10, sticky=ctk.W)

        self.label_num_units = ctk.CTkLabel(self, text="Number of units:")
        self.label_num_units.grid(column=0, row=4, padx=10, pady=10, sticky=ctk.W)
        self.entry_num_units = ctk.CTkEntry(self, width=30)
        self.entry_num_units.grid(column=0, row=5, padx=10, sticky=ctk.W)

        self.label_num_subunits = ctk.CTkLabel(self, text="Number of subunits:")
        self.label_num_subunits.grid(column=1, row=4, padx=10, pady=10, sticky=ctk.W)
        self.entry_num_subunits = ctk.CTkEntry(self, width=30)
        self.entry_num_subunits.grid(column=1, row=5, padx=10, sticky=ctk.W)

        self.label_unit_format = ctk.CTkLabel(self, text="Format for unit names:")
        self.label_unit_format.grid(column=0, row=6, padx=10, pady=10, sticky=ctk.W)
        self.entry_unit_format = ctk.CTkEntry(
            self, placeholder_text="Unit ?", width=150
        )
        self.entry_unit_format.grid(column=0, row=7, padx=10, sticky=ctk.W)
        self.label_unit_format_tip = ctk.CTkLabel(self, text="(? is the unit number)")
        self.label_unit_format_tip.grid(column=0, row=8, padx=10, sticky=ctk.W)

        self.label_subunit_format = ctk.CTkLabel(self, text="Format for subunit names:")
        self.label_subunit_format.grid(column=1, row=6, padx=10, pady=10, sticky=ctk.W)
        self.entry_subunit_format = ctk.CTkEntry(
            self, placeholder_text="Unit ?.??", width=150
        )
        self.entry_subunit_format.grid(column=1, row=7, padx=10, sticky=ctk.W)
        self.label_subunit_format_tip = ctk.CTkLabel(
            self, text="(? is the unit number;\n?? is the subunit number)"
        )
        self.label_subunit_format_tip.grid(column=1, row=8, padx=10, sticky=ctk.W)

        self.button_generate_dirs = ctk.CTkButton(
            self, text="Generate File System", command=self._generate_dirs
        )
        self.button_generate_dirs.grid(
            column=4, row=10, padx=10, pady=100, sticky=ctk.E
        )

    def _browse_local(self):
        """Creates a new window with directory browsing capabilities."""
        dir_name = filedialog.askdirectory(initialdir=os.path.abspath("."))
        self.entry_root_dir.configure(placeholder_text=os.path.abspath(dir_name))

    def _generate_dirs(self):
        """Gets all the current settings from the gui entries then generates the
        directories using those settings.
        """
        initialdir = os.path.abspath(".")

        root_dir = (
            self.entry_root_dir.get()
            if (self.entry_root_dir.get() != "")
            else self.entry_root_dir.cget("placeholder_text")
        )
        root_name = (
            self.entry_root_name.get()
            if (self.entry_root_name.get() != "")
            else self.entry_root_name.cget("placeholder_text")
        )

        if self.entry_num_units.get() != "":
            num_units = int(self.entry_num_units.get())
        else:
            self._pop_up(
                message_type="warning", message="Number of Units entry unfilled."
            )
            return

        if self.entry_num_subunits.get() != "":
            num_subunits = int(self.entry_num_subunits.get())
        else:
            self._pop_up(
                message_type="warning", message="Number of Subunits entry unfilled."
            )
            return

        unit_format = (
            self.entry_unit_format.get()
            if (self.entry_unit_format.get() != "")
            else self.entry_unit_format.cget("placeholder_text")
        )
        subunit_format = (
            self.entry_subunit_format.get()
            if (self.entry_subunit_format.get() != "")
            else self.entry_subunit_format.cget("placeholder_text")
        )

        unit_format = unit_format.replace("?", "{0}")
        subunit_format = subunit_format.replace("??", "{1}").replace("?", "{0}")

        os.chdir(root_dir)

        try:
            os.mkdir(root_name)
        except:
            msg = f"Root directory '{root_name}' already exists in this context.\n"
            msg += "Either change the name in the Root Folder Name entry, or delete the existing directory."
            self._pop_up(message_type="error", message=msg)
            return

        os.chdir(root_name)

        for i in range(num_units):
            dir_name = unit_format.format(i + 1)
            os.mkdir(dir_name)
            os.chdir(dir_name)
            for j in range(num_subunits):
                sub_dir_name = subunit_format.format(i + 1, j + 1)
                os.mkdir(sub_dir_name)
            os.chdir("..")

        os.chdir(initialdir)

        self._pop_up(
            message_type="info",
            message=f"File System generated successfully in: {root_dir}",
        )

    def _pop_up(self, message_type: str, message: str):
        """Creates a new popup window.

        :param message_type - The type of popup (can be ['info', 'error', 'warning'])
        :param message - The message to display in the popup
        """
        if message_type == "info":
            messagebox.showinfo(title="INFO", message=message)
        elif message_type == "warning":
            messagebox.showwarning(title="WARNING", message=message)
        elif message_type == "error":
            messagebox.showerror(title="ERROR", message=message)
        else:
            assert (
                False
            ), "You typed a wrong message_type somewhere when calling this function"


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
