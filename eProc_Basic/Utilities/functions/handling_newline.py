
def handle_newline(self):
    """
    Replace the new line character with the normal space
    :return: String with removal of new line character if exists
    """
    if "\n" in self:
        self.replace("\n", " ")
