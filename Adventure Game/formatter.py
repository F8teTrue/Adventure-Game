from colorama import Fore, Style, init

init(autoreset=True)

class Formatter:
    """
    Handles formatting of text output for the game.
    """

    @staticmethod
    def location_name(name):
        """
        Format location name.
        Appearance: Bright cyan text.
        """
        return f"{Style.BRIGHT}{Fore.YELLOW}-- {name} --{Style.RESET_ALL}"
    
    @staticmethod
    def cyan_bold(text):
        """
        Format general titles or sections.
        Appearance: Bright cyan text.
        """
        return f"{Style.BRIGHT}{Fore.CYAN}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def yellow_bold(text):
        """
        Format yellow bold text.
        Appearance: Bright yellow text.
        """
        return f"{Style.BRIGHT}{Fore.YELLOW}{text}{Style.RESET_ALL}"

    @staticmethod
    def blue(text):
        """
        Format blue text.
        Appearance: Blue text.
        """
        return f"{Fore.BLUE}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def blue_bold(text):
        """
        Format blue bold text.
        Appearance: Bright blue text.
        """
        return f"{Style.BRIGHT}{Fore.BLUE}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def green_bold(text):
        """
        Format bright green bold text.
        Appearance: Bright green text.
        """
        return f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def red_bold(text):
        """
        Format bright red bold text.
        Appearance: Bright red text.
        """
        return f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def red_dim(text):
        """
        Format red dim text.
        Appearance: Red text.
        """
        return f"{Fore.RED}{Style.DIM}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def magenta_bold(text):
        """
        Format bright magenta bold text.
        Appearance: Bright magenta text.
        """
        return f"{Style.BRIGHT}{Fore.MAGENTA}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def yellow_stat(name, value):
        """
        Format yellow stat name with white value.
        Appearance: Bright yellow stat name followed by white value.
        """
        return f"{Style.BRIGHT}{Fore.YELLOW}{name}: {Fore.WHITE}{value}{Style.RESET_ALL}"
    
    @staticmethod
    def magenta(text):
        """
        Format magenta text.
        Appearance: Magenta text.
        """
        return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"

    @staticmethod
    def light_blue(text):
        """
        Format light blue text.
        Appearance: Light blue text.
        """
        return f"{Fore.LIGHTBLUE_EX}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def light_magenta(text):
        """
        Format light magenta text.
        Appearance: Light magenta text.
        """
        return f"{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def light_yellow(text):
        """
        Format light yellow text.
        Appearance: Light yellow text.
        """
        return f"{Fore.LIGHTYELLOW_EX}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def white_cyan_stat(name, value):
        """
        Format white stat name with light cyan value.
        Appearance: Bright white stat name followed by light cyan value.
        """
        return f"{Style.BRIGHT}{Fore.LIGHTWHITE_EX}{name}: {Fore.LIGHTCYAN_EX}{value}{Style.RESET_ALL}"
    
    @staticmethod
    def grey(text):
        """
        Format grey text.
        Appearance: Grey text.
        """
        return f"{Fore.LIGHTBLACK_EX}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def white_bold(text):
        """
        Format white text.
        Appearance: Bright white text.
        """
        return f"{Fore.WHITE}{Style.BRIGHT}{text}{Style.RESET_ALL}"