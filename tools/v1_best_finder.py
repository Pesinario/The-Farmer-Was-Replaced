import os


def find_logs_dir(start_from="/") -> str:
    """
    Returns the path to the logs/TimedRunV1 directory.
    By default it will start from root, which will take very long.
    """

    def is_recycle_bin(root) -> bool:
        if os.name == 'nt':  # Windows
            if '$Recycle.Bin' in root:
                return True
        else:  # Unix-like systems (Linux/Mac)
            recycle_paths = [
                os.path.expanduser('~/.local/share/Trash'),  # Linux Trash
                os.path.expanduser('~/.Trash')              # macOS Trash
            ]
            if any(recycle_path in root for recycle_path in recycle_paths):
                return True
        return False

    print("\033[31m",
          "Finding your logs directory, may take a while.",
          "\033[0m")

    for root, _, _ in os.walk(start_from):  # Start from root
        if is_recycle_bin(root):  # Don't return deleted log folders
            continue
        if os.path.basename(root) == 'TimedRunV1':
            if 'logs' in os.path.basename(os.path.dirname(root)):
                return root  # Return the path to the 'logs/TimedRunV1' directory
    raise FileNotFoundError("Was unable to find your logs directory.")


def find_timed_runs(logs_dir) -> list[str]:
    """ Returns a list of paths to timed run v1 files """
    log_files = []
    for curr_dir, _, files in os.walk(logs_dir):
        for file in files:
            if file.endswith(".log"):
                log_files.append(os.path.join(curr_dir, file))

    if len(log_files) < 1:
        raise FileNotFoundError("Was unable to find any log files.")
    else:
        return log_files


def find_best_time(paths_to_logs) -> tuple[float, str]:
    """ Returns the best time as a float, and the path to the file"""
    curr_best = 999_999_999  # about 270,000 hours
    curr_best_at = None

    for path in paths_to_logs:
        with open(path, "r", encoding="utf-8") as log:
            lines = log.readlines()

        # We assume the end time will be in the last 5 lines of the log:
        check_from = len(lines) - 5
        for line in lines[check_from:]:
            if line.startswith("~ End time is"):
                this_time = float(line[14:])
                if this_time < curr_best:
                    curr_best = this_time
                    curr_best_at = path
    return (curr_best, curr_best_at)


# You should place your own logs directory instead of find_logs_dir()
# if you want to make this script run a LOT faster. otherwise the script
# will search the entire tree of your OS
paths_to_runs = find_timed_runs(find_logs_dir())

best_time, best_time_path = find_best_time(paths_to_runs)

hours, remainder = divmod(best_time, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Best time was: {int(hours)}:{int(minutes)}:{seconds:.3f}")
print(best_time_path)
