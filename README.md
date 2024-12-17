# Welcome to my repository for "The Farmer Was Replaced"!
## What is ["The Farmer Was Replaced"](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/)?

It is a programming game where you use a **subset** of Python to automate farming with a drone
### Limitations coding for "The Farmer Was Replaced":
#### Missing Python features in the game, and what I would've used them for:
- fStrings – Missing, which makes debugging and performance optimization harder.
- Classes – Could have helped manage grind orders, logs, and maze-solving.
- __Many__ built-in type methods, some notable mentions:
  - Almost everything string related.
  - `list.reverse`, `list.sort`, `list.index` and `list.count`
#### The game will refuse to execute any code that contains:
- Docstrings
- Type hinting
- Inlined statements (e.g., `else: return False`)

## About my repository (and its branches)
- The `jul-2024` branch has pretty much **all** of the code I made that is in use (and some older, unused code) for the game in legacy version `jul-2024`, accessible through the steam beta feature.
- The `legacy` branch represents the state of the code slightly after successfully completing my first timed run, and only exists to watch how far the project has come.
- The `dev` branch is where the more cutting edge features live, but they _may_ not be very stable, and no guarantees are given, it gets merged into `stable` every now and then.

The repository also has some of the tools I made to make my life easier when trying to get a better time and debugging **(Check out tfwr_watcher!)**

### Please keep in mind:
- The quite limiting nature of what the game will let you execute inside of it.
- Some readability and best practices were sacrificed to optimize for the game’s unique performance criteria (which might differ from conventional expectations).
- Effort was put into conforming with *most* of PEP8, line length *should* be 80 characters or under, for some lines, this rule was broken.
- At the point of starting this project, I was quite inexperienced with git, so please excuse the mistakes that took place here.
- The goal of this project is **not** to get a *great* time on the leaderboard.
- The goals of this project **are:**
  - To learn how to use git properly.
  - To write (pseudo) Python code that is readable and modular.
  - To hopefully be useful to someone, someday.
  - To get a *decent* time (somewhere around 30 minutes has always been the target).

If you have any suggestions on how I could improve towards my goals, please contact me, or make a pull request!
### Please interact with this repository! You could:
- Clone it
  - And use any of the code as you wish!
- Open an issue
  - And I'll try to fix it!
- Fork it (and then)
  - Make a pull request with some improvements.
- Show appreciation by
  - Watching it
  - Giving it a star

## Instructions for using the code
### Setting up the code:
1. Get the files in one of two ways
    - Clone the repository using git (recommended: directly into your save directory).
    - Download individual files and their dependencies (import statements at the top).
2. Place the ".py" files inside a save directory, along with a save file. By default on windows it will be located in:

(C:\Users\ **YourUser** \AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\ **Yoursave** )
### Executing the code from inside the game
- Run "timed_run.py" from inside the game if you want to do a run with my code
- Run "method_tester.py" to play around with the different farming methods I've made over the past few weeks (there's quite a few, many obsolete.)
### Using the (external) tools I made
Anything located in the "tools" subdirectory will require you have Python installed and configured, you should be able to just run them without any dependencies unless specified otherwise, consult the local README for instructions.

## History of the best time for each version of the code

| Version | Best Time   |
|---------|-------------|
| v1      | 2:48:37.230 |
| v1.1    | 1:48:08.733 |
| v1.2    | 1:22:58.444 |
| v1.21   | 1:14:01.313 |
| v1.22   | 1:10:51.399 |
| v1.3    | 0:40:28.440 | < First time that got under top 100
| v1.31   | 0:39:42.503 |
| v1.32   | 0:39:27.286 |
| v1.4    | 0:37:17.038 |
| v1.5    | 0:34:10.629 |
| v1.6    | 0:30:59.302 |
| v1.61   | 0:30:43.208 |
| v1.62   | 0:30:00.776 |

Latest version (1.62) Changed all of the remaining print() statements to quick_print() statements (And apparently saved over 42 seconds with it, that pumpkin bug was killing the times)

## Known issues and future plans
- The maze method is not 100% stable, it *sometimes* crashes a timed run attempt.
- The (pre-fertilizer?) pumpkin farming has a bug I can’t seem to diagnose. I’d appreciate any help, as I’ve tried various approaches without success.
- Logs are usually quite verbose, especially on the `dev` branch.
