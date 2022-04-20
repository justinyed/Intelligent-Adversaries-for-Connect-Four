# Connect Four Discord Bot with Intelligent Adversaries

## Introduction

### Description

Connect Four Discord Bot with Artificially Intelligent Opponents which vary in difficulty.

### Background:

My first semester at CNU I took CPSC 250 (Python). Towards the end of the semester we were sent home due to Covid-19. I got bored and wrote a simple command line connect four game. The Fall semester of my Senior year at CNU I took CPSC 471: Applied Artificial Intelligence and really enjoyed it. Thus, I decided to rewrite connect four in python and create artificial opponents to play against.

---

## Setup

### Install Requirements:

See dependencies in the `requirements.txt` file.

```shell
python -m pip install -r requirements.txt
```

[//]: # (Generated Requirements File with:)
[//]: # (```shell)
[//]: # (python -m pip freeze > requirements.txt)
[//]: # (```)


```bash
pip install -e .
```

### Run Setup File

Run the `setup.py` file to set up the `PYTHONPATH`.

```bash
python setup.py build && python setup.py install
```

---

## Details

### Components


| Component    | Directory         | Description                                                                                                                     |
|--------------|:------------------|---------------------------------------------------------------------------------------------------------------------------------|
| Interface    | `discord_bot`     | Discord Game Bot that will allow human players to play Connect Four against each other or Artificially Intelligent Adversaries. |
| Game         | `game_components` | Connect Four Game Mechanics and Board Representation.                                                                           |
| Intelligence | `intelligence`    | The Artificial Intelligence for the Adversarial Agents.                                                                         |

---

### Discord Bot Interface

**[Discord](https://discord.com/) Bot Interface:** Challenge Agents or Human Players, and Leader Board.  This project utilizes [discord.py](https://discordpy.readthedocs.io/en/stable/), which is a modern, easy to use, feature-rich, and idiomatic API wrapper for Discord.

#### Features:
- Challenge Handler
- Leaderboard System
- Help Dialog

#### Basic Bot Usage:


| Callsign        | Description                                                                                                       |
|-----------------|-------------------------------------------------------------------------------------------------------------------|
| `@c4 [command]` | In order to interact with the Connect Four Game Bot in a Discord Chat a command must be preceded by its callsign. |

| Command            | Alias | Description                                                                                                                           |
|--------------------|-------|---------------------------------------------------------------------------------------------------------------------------------------|
| `challenge [ID]`   | `clg` | Challenge a player or agent by providing the ID.  If no parameter is given, then a menu will assist.                                  |
| `leaderboard [ID]` | `lb`  | Display the record for a player or agent by providing the ID. If no parameter is given, then a default leaderboard will be displayed. |
- Help: `-h` or `--help` preceded by a command will show a help dialog with options.

---

### Intelligence

**Intelligent Agents:** Choose the action which leads to the greatest expected utility.

| Agents                 | Description                                                                                                        |
|------------------------|--------------------------------------------------------------------------------------------------------------------|
| Reflex                 | Choices a move based only on an evaluation function                                                                |
| Minimax                | Choices a move which maximizes its own utility and minimizes the utility of its opponent                           |
| Alpha-Beta Minimax     | Extension of Minimax which focuses on evaluating relevant states by pruning sub-trees with too few utility points. |
| Iterative Deepening    | Minimax with Anytime Iterative Deepening.                                                                          |

---

## Acknowledgements

- Learned a lot from the CNU Course CPSC 471: Intro to AI taught by Dr. Conner.
- Agents were inspired by **my solutions** to the [AI UC Berkley Problems](http://ai.berkeley.edu).
- The idea for the particular Static Evaluation Function I implemented is found in a paper by Martin Stenmark.
