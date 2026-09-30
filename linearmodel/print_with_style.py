"""
print_with_style.py

A utility module for printing text with various styles such as color, bold, italic.
"""
from colorama import Style, init

# Initialise colorama for Windows
init()

class PrintWithStyle:
    """
    A utility class for printing text with various styles such as color, bold, italic.
    """

    @staticmethod
    def colored_text(text, color):
        """
        Apply color to the text.

        Parameters:
        - text (str): The text to apply color to.
        - color (colorama.Fore): The color to apply (e.g., Fore.RED, Fore.GREEN).

        Returns:
        - str: The text with applied color.
        """
        return f"{color}{text}{Style.RESET_ALL}"

    @staticmethod
    def bold_text(text):
        """
        Apply bold style to the text.

        Parameters:
        - text (str): The text to apply bold style to.

        Returns:
        - str: The text with applied bold style.
        """
        return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def italic_text(text):
        """
        Apply italic style to the text.

        Parameters:
        - text (str): The text to apply italic style to.

        Returns:
        - str: The text with applied italic style.
        """
        return f"{Style.DIM}{text}{Style.RESET_ALL}"


    @staticmethod
    def print_with_style(text, color=None, bold=False, italic=False):
        """
        Print the text with specified styles.
        Parameters:
        - text (str): The text to print.
        - color (colorama.Fore, optional): The color to apply (e.g., Fore.RED, Fore.GREEN). Defaults to None.
        - bold (bool, optional): Whether to apply bold style. Defaults to False.
        - italic (bool, optional): Whether to apply italic style. Defaults to False.
        """
        styled_text = text

        if color:
            styled_text = PrintWithStyle.colored_text(styled_text, color)

        if bold:
            styled_text = PrintWithStyle.bold_text(styled_text)

        if italic:
            styled_text = PrintWithStyle.italic_text(styled_text)
        print(styled_text)
