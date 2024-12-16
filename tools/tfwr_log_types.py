""" This module houses the different log type classes for tfwr_watcher. """

import os
import time

C_INFO = "\033[33m"  # Color text yellow
C_GOOD = "\033[32m"  # Color text green
C_BAD = "\033[31m"  # Color text red
C_END = "\033[0m"  # Reset


class TheFarmerWasReplacedLog():
    """ Base class for log types """

    def __init__(self, content: list[str], timestamp: float, base_log_dir) -> None:
        # self._content should not be overwritten. It should == output.txt
        self._content = content
        self._timestamp = timestamp
        self.id = str(int(self._timestamp))[2:]  # This is free to change.
        self.save_to = f"{base_log_dir}{self.__class__.__name__}/{self.id}"
        self.save_to_latest = f"{base_log_dir}latest_{self.__class__.__name__}"
        print(f"{C_INFO}Initializing log id#{self.id}. {type(self)=}{C_END}")

    # You can call save manually for the base class if you really want to

    def __call__(self):
        """
        This should execute default behaviors from child classes,
        such as saving them as .log """
        raise NotImplementedError

    def save_log(self, what: list[str], extension=".log", write_latest=True) -> None:
        """ Saves the log, potentially overwriting it."""

        if isinstance(self, TheFarmerWasReplacedLog):
            raise NotImplementedError("Should never save the base class")

        log_dir = os.path.dirname(f"{self.save_to}{extension}")
        if not os.path.exists(log_dir):
            print(f"{C_BAD} Making log directory, since it wasn't found.{C_END}")
            os.makedirs(log_dir)

        with open(f"{self.save_to}{extension}", "w", encoding="utf-8") as file:
            for line in what:
                file.write(line + "\n")

        print(f"Successfully saved {self.save_to}{extension}")

        if write_latest:
            print(
                f"{C_GOOD}Writing latest_{self.__class__.__name__}"
                f"{extension}{C_END}")
            with open(f"{self.save_to_latest}{extension}", "w", encoding="utf-8") as file:
                for line in what:
                    file.write(line + "\n")

    @classmethod
    def all_behaviors(cls) -> list[callable]:
        return [method for method in dir(cls)
                if callable(method) and not method.startswith("__")]


class Unknown(TheFarmerWasReplacedLog):
    """ The default log type if we couldn't figure out the log type. """

    def __init__(self, content: list[str], timestamp: float, base_log_dir):
        super().__init__(content, timestamp, base_log_dir)
        print(f"{C_BAD}Was unable to classify log {self.id}{C_END}")

    def __call__(self):
        self.save_log(self._content)


class TimedRunV1(TheFarmerWasReplacedLog):
    """
    Supports the same symbols as my GitHub repo, and offers direct to console
    parsed output and writing to markdown, where you keep open the preview of
    the "latest.md" file to look at your run's results in between runs.
    """

    __ANSI_COLORS: dict[str, int] = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
        "default": 39,
        "reset": 0
    }

    __SYMBOLS = {  # Customizable from here
        "°": {
            "4char": "ERR:",
            "terminal_format": f"[{__ANSI_COLORS['red']}m",
            "markdown_color": "color:#eb0000"
        },
        "$": {
            "4char": "BUD:",
            "terminal_format": f"[{__ANSI_COLORS['green']}m",
            "markdown_color": "color:#5bc0de"
        },
        "+": {
            "4char": "GND:",
            "terminal_format": f"[{__ANSI_COLORS['yellow']}m",
            "markdown_color": "color:#f0ad4e"
        },
        "-": {
            "4char": "INF:",
            "terminal_format": f"[{__ANSI_COLORS['blue']}m",
            "markdown_color": "color:#0275d8"
        },
        "~": {
            "4char": "MLS:",
            "terminal_format": f"[{__ANSI_COLORS['magenta']}m",
            "markdown_color": "color:#8e44ad"
        }
    }

    def __init__(self, content, timestamp, base_log_dir) -> None:
        super().__init__(content, timestamp, base_log_dir)
        self.console_parsed = None
        self.markdown_parsed = None

    def __call__(self) -> None:
        """ Default behavior here is to output to console after parsing. """
        # self.output_to_console() # No longer default behavior.
        self.save_log(self._content)
        self.save_markdown()

    def prepare_console_output(self) -> None:
        if self.console_parsed is not None:
            print(f"About to overwrite the console_parsed of {self.id}")
        else:
            print(f"We're about to define {self.id}'s terminal output.")

        console_output = []
        for line in self._content:
            if line == "":
                continue
            line_symbol = line[0]

            if line_symbol in TimedRunV1.__SYMBOLS:
                # We use octal codes here.
                start_code = "\033"
                color_code = TimedRunV1.__SYMBOLS[line_symbol]["terminal_format"]
                prefix = TimedRunV1.__SYMBOLS[line_symbol]["4char"]
                # This resets the console to default color
                end_code = "\033[0m"

                parsed_line = line.replace(
                    line_symbol,  # replace what
                    start_code + color_code + prefix + end_code,  # replace with
                    count=1)  # replace only the first time

                parsed_line += end_code
            else:
                parsed_line = "UNK: " + line

            console_output.append(parsed_line)

        self.console_parsed = console_output

    def output_to_console(self) -> None:
        """
        This method prints all of the logs to console, but lacks filtering.
        You may try your luck using timed_run_v1_parser.py instead.
        """

        if self.console_parsed is None:
            self.prepare_console_output()

        print(f"{C_INFO} About to clear the terminal and start printing...")
        print("This means that you are entering log reading mode.")
        time.sleep(5)  # Just giving a little heads up.
        print("\033[H\033[J")
        print(f"{C_INFO}If you're reading this, the"
              f"terminal is showing all of the logs.{C_END}")

        for line in self.console_parsed:
            print(line)
        print(f"Total line count: {len(self.console_parsed)}")

    def parse_into_markdown(self):
        # A note: there is no (feasible) way that i know of to display
        # colored text on github's markdown display, so this is meant for
        # use in vscode by looking at the preview of "latest.md"
        if self.markdown_parsed is not None:
            print(f"{C_BAD}About to overwrite the markdown_parsed"
                  f"of {self.id}{C_END}")
        else:
            print(f"We're about to define {self.id}'s markdown.")
        ls = "<span style="
        markdown_lines = [f"# Timed run log with id#: {self.id}\n"]
        for line in self._content:
            if line == "":
                continue
            if line[0] not in TimedRunV1.__SYMBOLS:
                # We don't want detailed, small picture output in the markdown.
                continue
            parsed_line = line
            parsed_line = line.replace(
                line[0],
                ls + TimedRunV1.__SYMBOLS[line[0]]["markdown_color"] + ">"
                + TimedRunV1.__SYMBOLS[line[0]]["4char"],
                count=1)
            parsed_line += "</span><br>\n"
            markdown_lines.append(parsed_line)

        markdown_lines.append("# End of log")
        self.markdown_parsed = markdown_lines

    def save_markdown(self) -> None:
        if self.markdown_parsed is None:
            self.parse_into_markdown()
        self.save_log(self.markdown_parsed, extension=".md")


class MazePathTaken(TheFarmerWasReplacedLog):
    """ This class is for detailed logs of maze runs """

    def __init__(self, content: list[str], timestamp: float, base_log_dir):
        super().__init__(content, timestamp, base_log_dir)
        self.save_to = f"{base_log_dir}Maze path taken/{self.id}"

    def __call__(self):
        self.save_log(self._content)


def get_log(unix_timestamp, file_content, path_to_log_directory):
    """ This function returns an object of the corresponding log type. """

    SIGNATURES = {
        "~ Start time is": TimedRunV1,
        "[(0,0)": MazePathTaken
    }
    for signature in SIGNATURES:  # pylint:disable=C0206
        if file_content[0].startswith(signature):
            return SIGNATURES[signature](
                file_content, unix_timestamp, path_to_log_directory)

    return Unknown(file_content, unix_timestamp, path_to_log_directory)
