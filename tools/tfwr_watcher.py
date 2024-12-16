import os
import json
import signal
import time

import tfwr_log_types  # pylint:disable=E0401

# DISCLAIMER: As far as I know the game is only meant to run on windows.
# This should work on any platform but you may need to hardcode the location
# of the the "output.txt" file that TFWR generates after executing scripts.


# This HAS to be hardcoded. If you want to change it to a different directory,
# don't forget to create said directory yourself, it deals with log
# directories automatically, though.
WATCHER_MEM = "watcher.json"

# Some colors used on watcher itself for slightly less dim console output
C_INFO = "\033[34m"  # Color text blue
C_S_INFO = "\033[36m"  # Color text cyan, Super info
C_GOOD = "\033[32m"  # Color text green
C_BAD = "\033[31m"  # Color text Red
C_END = "\033[0m"  # Reset


if not os.path.exists(os.getcwd() + "/tfwr_watcher.py"):
    print(f"{C_BAD}Current working directory does not contain the script.")
    print(os.getcwd(), C_END)
    raise SystemExit


def find_output_dot_txt() -> str:
    """ Should return the path to TFWR's "output.txt" file """

    if os.name == "nt":
        # The reason why I don't just go straight to output.txt is that
        # I want to make sure that the file exists, with the for loop below.
        user_user_dir = (
            os.path.expanduser("~") +
            "\\AppData\\LocalLow\\TheFarmerWasReplaced\\TheFarmerWasReplaced"
        )
    else:
        # I'm sorry non-windows users, but the game is windows only afaik
        # and i don't have a clue how proton works
        user_user_dir = os.path.expanduser("~")

    for curr_dir, _, files in os.walk(user_user_dir):
        if os.path.basename(curr_dir) == "TheFarmerWasReplaced":
            if "output.txt" in files:
                return os.path.join(curr_dir, "output.txt")

    raise FileNotFoundError("Was unable to find TheFarmerWasReplaced's"
                            "output.txt file.")


def yes_no_prompt(prompt) -> bool:
    """Returns True if the user said yes, False if he said no"""

    while True:
        user_input: str = input(prompt).strip().lower()
        if user_input in ["y", "yes"]:
            return True
        elif user_input in ["n", "no"]:
            return False
        else:
            print(f"{C_BAD}Unknown response,",
                  "please type yes or no to continue.\n{C_END}")


def prompt_user_portable() -> bool:
    """Returns False if the user wants to make a config file."""

    wants_portable = yes_no_prompt(
        "Do you want to run watcher in portable mode?\n"
    )

    if wants_portable:
        print(f"{C_GOOD}Okay, won't save your settings.{C_END}")
        return True
    else:
        print(f"{C_GOOD}Okay, will save your settings.{C_END}")
        return False


def prompt_user_defaults() -> bool:
    """Returns True if the user wants to use default settings."""

    wants_defaults = yes_no_prompt(
        "Do you want to run watcher with default settings?\n"
    )

    if wants_defaults:
        print(f"{C_GOOD}Okay, will use default settings.{C_END}")
        return True
    else:
        return False


def prompt_user_settings() -> tuple[str, float, bool]:
    rel_log_path = input(
        "Specify your desired log output path (relative), no quotes.\n"
        "Default value: \"../logs/\".\n"
        "Hit enter without typing anything to use default\n"
    )
    if rel_log_path == "":
        rel_log_path = "logs/"

    rf_rate = input(
        "Specify your desired refresh rate for watcher\n"
        "Default value is 2 seconds."
        "Hit enter without typing anything to use default\n"
    )
    if rf_rate == "":
        rf_rate = 2
    else:
        rf_rate = float(rf_rate)

    auto_behavior = yes_no_prompt(
        "Do you want to enable the default behavior of each type of log?\n"
    )

    return rel_log_path, rf_rate, auto_behavior


def watcher_init(rerun=False) -> tuple[float, str, str, float, bool, bool]:
    if os.path.exists(WATCHER_MEM) and not rerun:
        with open(WATCHER_MEM, "r", encoding="utf-8") as memory:
            saved_data = json.loads(memory.read())
            try:
                last_timestamp: float = saved_data["last_timestamp"]
                path_to_output: str = saved_data["abs_path_to_tfwr_output"]
                log_path: str = saved_data["rel_path_to_logs"]
                rf_rate: float = saved_data["refresh_rate"]
                auto_behavior: bool = saved_data["auto_behaviors"]
                path_to_latest_log: str = saved_data["abs_path_to_last_save"]
            except KeyError:
                return watcher_init(True)
            is_portable = False

    else:
        print(f"{C_BAD}Was unable to find a proper configuration file.{C_END}")
        last_timestamp = 0  # Save whatever is in output.txt
        path_to_output = find_output_dot_txt()
        is_portable = prompt_user_portable()
        path_to_latest_log = None
        use_defaults = prompt_user_defaults()
        if use_defaults:
            log_path = "../logs/"
            rf_rate = 2
            auto_behavior = True
        else:
            log_path, rf_rate, auto_behavior = prompt_user_settings()

    watcher_settings = {
        "last_timestamp": last_timestamp,
        "abs_path_to_tfwr_output": path_to_output,
        "rel_path_to_logs": log_path,
        "refresh_rate": rf_rate,
        "watcher_portable": is_portable,
        "auto_behaviors": auto_behavior,
        "abs_path_to_last_save": path_to_latest_log
    }
    return watcher_settings


def save_watcher(config) -> None:
    """
    This expects the same tuple that watcher_init produces, for convenience.
    """

    with open(WATCHER_MEM, "w", encoding="utf-8") as memory:
        json.dump(config, memory)
    print(f"{C_INFO}Saved watcher configuration successfully{C_END}")


CONFIG_VARS = watcher_init()
last_processed_log = CONFIG_VARS["last_timestamp"]
PATH_TO_OUTPUT = CONFIG_VARS["abs_path_to_tfwr_output"]
LOG_SAVE_PATH = CONFIG_VARS["rel_path_to_logs"]
REFRESH_RATE = CONFIG_VARS["refresh_rate"]
WATCHER_PORTABLE = CONFIG_VARS["watcher_portable"]
DEFAULT_BEHAVIORS_ENABLED = CONFIG_VARS["auto_behaviors"]
path_to_latest_saved = CONFIG_VARS["abs_path_to_last_save"]


def exit_watcher(*args) -> None:
    """This is called when we get 'SIGINT'"""
    print(f"{C_S_INFO}Stopped @: {args}")
    print(f"Stopped listening, will exit when done.{C_END}")
    global keep_going  # pylint:disable=W0603
    keep_going = False


try:
    with open(path_to_latest_saved, "r", encoding="utf-8") as file:
        past_content = [line.strip() for line in file]  # IMPORTANT, STRIPPED.

except (TypeError, FileNotFoundError):
    print(f"{C_BAD}Couldn't find latest saved log, "
          f"it must have been deleted.{C_END}")
    with open(PATH_TO_OUTPUT, "r", encoding="utf-8") as file:
        past_content = [line.strip() for line in file]  # IMPORTANT, STRIPPED.
    # This makes sure that we save the starting output.txt write, when we get a
    # new write, assuming the value of output.txt at startup has never been
    # logged by watcher.


print(f"{C_S_INFO}Finished setting up the script.{C_END}")
print(f"{C_GOOD}Current settings:")
for setting, value in CONFIG_VARS.items():
    print(setting, value)
print(C_END, end="")

if not WATCHER_PORTABLE:
    save_watcher(CONFIG_VARS)  # Save the settings, just in case.


def make_log(content, ts):
    my_log = tfwr_log_types.get_log(
        ts, content, LOG_SAVE_PATH)

    if DEFAULT_BEHAVIORS_ENABLED:
        my_log()  # the __call__ method executes default behaviors.
    else:
        # This is a good spot to implement custom behaviors based on log type.
        # For example:
        if isinstance(my_log, tfwr_log_types.TimedRunV1):
            my_log.output_to_console()


# From this point onwards, we care about exiting gracefully:
keep_going = True  # should be switched to false after the user wants to exit
signal.signal(signal.SIGINT, exit_watcher)

last_skip = None
# Main script loop:
while keep_going:
    time.sleep(REFRESH_RATE)
    latest_update = os.path.getmtime(PATH_TO_OUTPUT)
    if latest_update == last_processed_log:
        continue  # guard clause

    # in case a script is running inside the game but hasn't printed anything.
    if os.path.getsize(PATH_TO_OUTPUT) < 2:
        continue  # guard clause

    with open(PATH_TO_OUTPUT, "r", encoding="utf-8") as file:
        latest_content = [line.strip() for line in file]  # IMPORTANT, STRIPPED.

    # We effectively only save logs when the next output.txt write doesn't
    # contain the last output.txt write in it's entirety.
    # This means only the first and last writes of a log should be saved.
    # Maybe only the last write, if your next run of the script completely
    # contains the last run of your script (in terms of output).

    if set(past_content).issubset(set(latest_content)):
        if latest_update != last_skip:
            print(f"Skipped making log{latest_update}, it's a superset")

        last_skip = latest_update
        past_content = latest_content
        continue
    else:
        # Save previous superset:
        if last_skip is not None:
            make_log(past_content, ts=last_skip)
        past_content = latest_content  # Clear memory of saved log

        # Save current new log (probably 1 line):
        make_log(latest_content, ts=latest_update)
        last_processed_log = latest_update


# The following is the behavior after the user hit CTRL+C to end the script
if latest_update != last_processed_log:  # Save last write to output.txt
    make_log(latest_content, ts=latest_update)
    last_processed_log = latest_update
else:
    print(f"{C_INFO}Not saving because we already saved last output.txt write{C_END}")

if not WATCHER_PORTABLE:
    def find_path_to_log(timestamp: float):
        last_log_id = str(int(timestamp))[2:]
        for curr_dir, _, files in os.walk(
                os.path.join(os.getcwd(), LOG_SAVE_PATH)):
            if f"{last_log_id}.log" in files:
                return os.path.join(curr_dir, f"{last_log_id}.log")
        raise FileNotFoundError("Was unable to find the latest saved log.")

    path_to_latest_saved = find_path_to_log(last_processed_log)
    CONFIG_VARS.update({"last_timestamp": last_processed_log})
    CONFIG_VARS.update({"abs_path_to_last_save": path_to_latest_saved})
    save_watcher(CONFIG_VARS)


exit(f"{C_GOOD}We're done.{C_END}")
