# Connect Four Discord Bot with Intelligent Adversaries

## Introduction

### Description

Connect Four Discord Bot with Artificially Intelligent Opponents which vary in difficulty.

### Background:

My first semester at CNU I took CPSC 250 (Python).  Towards the end of the semester we were sent home due to Covid-19.  I got bored and wrote a simple command line connect four game.  The Fall semester of my Senior year at CNU I took CPSC 471: Applied Artificial Intelligence and really enjoyed it!  Thus, I decided to rewrite connect four in python and create artificial opponents to play against.

---

## Setup

### Install Requirements:

See dependencies in the `requirements.txt` file.

```shell
python -m pip install -r requirements.txt
```

[//]: # "Generated Requirements File with:"
[//]: # "```shell"
[//]: # "python -m pip freeze > requirements.txt"
[//]: # "```"


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
- The configuration settings can be found in `./discord_bot/discord_config.py`.

#### Basic Bot Usage:


| Callsign        | Description                                                                                                       |
|-----------------|-------------------------------------------------------------------------------------------------------------------|
| `@c4 [command]` | In order to interact with the Connect Four Game Bot in a Discord Chat a command must be preceded by its callsign. |

| Command            | Alias | Description                                                                                                                           |
|--------------------|-------|---------------------------------------------------------------------------------------------------------------------------------------|
| `challenge [ID]`   | `clg` | Challenge a player or agent by providing the ID.  If no parameter is given, then a menu will assist.                                  |
| `leaderboard [ID]` | `lb`  | Display the record for a player or agent by providing the ID. If no parameter is given, then a default leaderboard will be displayed. |
---

### Intelligence

**Intelligent Agents:** Choose the action which leads to the greatest expected utility.

Each Artificially Intelligent Opponent is an Iterative Deepening Agent with Alpha-Beta Pruning, Cached Successor Generator, Decision Timer, and Better Move Ordering.  Each difficulty is currently, configured as follows:

| Opponent | Forward Thinking Level | Decision Time Limit [seconds] |
| -------- | ---------------------- | ----------------------------- |
| Simple   | 1                      | 3.0                           |
| Easy     | 2                      | 3.0                           |
| Medium   | 3                      | 4.0                           |
| Hard     | 4                      | 4.0                           |
| Elite    | 10                     | 5.0                           |

Note: The setting for these opponents can be found in `./discord_bot/discord_config.py`, `line 25`.

---

## Acknowledgements

- Learned a lot from the CNU Course CPSC 471: Intro to AI taught by Dr. Conner.
- Agents were inspired by **my solutions** to the [AI UC Berkley Problems](http://ai.berkeley.edu).
- The idea for the particular Static Evaluation Function I implemented is found in a paper by Martin Stenmark.
