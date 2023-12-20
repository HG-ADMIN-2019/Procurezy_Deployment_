
def handle_tab(str):
    """
    Replace the tab space with the normal space
    :return: String with removal of tabs if exists
    """
    if "\t" in str:
        str.replace("\t", " ")
        print(str)
    return str
