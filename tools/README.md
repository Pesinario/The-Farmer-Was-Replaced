## This tools directory contains:
* An example log of the TimedRunV1 type parsed into markdown.

NOTE: GitHub won't show colors, so I suggest you use a different method to look at the example log.
### Tools for dealing with the "output.txt" file that "The Farmer Was Replaced" generates
- timed_run_v1_parser - Simple script that reads from "output.txt" and then outputs to console (possibly) filtered events following the v1 format of timed runs, you'll have to modify the code to choose what gets filtered or read from a saved log.

- tfwr_watcher - A script that monitors the contents of the "output.txt". It then makes a copy of its contents and sends it to tfwr_log_types for sorting, and (by default, customizable) executes default behaviors (like saving, or parsing into markdown)
- tfwr_log_types - Contains classes representing types of logs, and `get_log` a function that decides what type of log a given "output.txt" read should be and returns the corresponding object. This is where you can implement your own log types if you so desire. Otherwise, you can conform to one of the bundled formats or keep saving logs as the default `Unknown` type

### Tools for using said tools:
- v1_best_finder - This script will print the best time it found in your TimedRunV1 folder, along with the path to it (You can ctrl+click it from vscode to open it)

The Timed Run V1 format is as follows:
- `° means error`
- `$ means possible to cut corners, maybe`
- `~ means milestone`
- `+ means grinding something`
- `- means info`