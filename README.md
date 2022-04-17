# Intelligent Adversaries for Connect Four with a Discord Bot Interface

## Introduction

### Description

Python implementation of Connect Four with adversarial agents to play against. The Discord Game Bot interface allows the selection of agents or human players and will provide a leaderboard.

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

### Intelligence

**Intelligent Agents:** Choose the action which leads to the greatest expected utility.

| Agents                 | Description                                                                                                        |
|------------------------|--------------------------------------------------------------------------------------------------------------------|
| Reflex                 | Choices a move based only on an evaluation function                                                                |
| Minimax                | Choices a move which maximizes its own utility and minimizes the utility of its opponent                           |
| Alpha-Beta Minimax     | Extension of Minimax which focuses on evaluating relevant states by pruning sub-trees with too few utility points. |
| Iterative Deepening    | Minimax with Anytime Iterative Deepening.                                                                          |
| Reinforcement Learning | Utilizes Reinforcement Learning (specifically Q-Learning) to Develop Policies.                                     |

### Command Line Interface

**Command Line Interface:** Challenge Agents or Human Players.
- Mainly For Testing or Debugging
- Displays Turn, Current Status, and Last Move Made 
- Colored Board

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


## Project Structure

### Logical Structure

| Component    | Description                                                                                                                     |
|--------------|---------------------------------------------------------------------------------------------------------------------------------|
| Interface    | Discord Game Bot that will allow human players to play Connect Four against each other or Artificially Intelligent Adversaries. |
| Game         | Connect Four Game Mechanics and Board Representation.                                                                           |
| Intelligence | The Artificial Intelligence for the Adversarial Agents.                                                                         |
| Analysis     | Analyze the performance and behavior of these techniques generally & when challenging each other during Connect Four battles.   |

### Directory Structure
| Directory         | Description                                       |
|-------------------|---------------------------------------------------|
| `discord_bot`     | Discord Bot Interface                             |
| `game_components` | Connect Four Game Engine & Command Line Interface |
| `intelligence`    | Various Agents/Opponents for Connect Four         |
| `analysis`        | Notebooks & scripts for analysis.                 |

---


## Acknowledgements


- Learned a lot from the CNU Course CPSC 471: Intro to AI taught by Dr. Conner.

- Agents were inspired by **my solutions** to the [AI UC Berkley Problems](http://ai.berkeley.edu).
