class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def colorize(text: str, color: str) -> str:
        return f"{color}{text}{Colors.ENDC}"

    @staticmethod
    def header(text: str) -> str:
        return Colors.colorize(text, Colors.HEADER)

    @staticmethod
    def info(text: str) -> str:
        return Colors.colorize(text, Colors.BLUE)

    @staticmethod
    def success(text: str) -> str:
        return Colors.colorize(text, Colors.GREEN)

    @staticmethod
    def warning(text: str) -> str:
        return Colors.colorize(text, Colors.WARNING)

    @staticmethod
    def error(text: str) -> str:
        return Colors.colorize(text, Colors.FAIL)

    @staticmethod
    def bold(text: str) -> str:
        return Colors.colorize(text, Colors.BOLD)

    @staticmethod
    def underline(text: str) -> str:
        return Colors.colorize(text, Colors.UNDERLINE) 