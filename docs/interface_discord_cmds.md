callsign = `@c4`

## Discord Bot Commands

### Basic Commands

- clg / challenge
  - `'none'` -> dialog
  - `player [$id]` -> challenge player
    - `-t $int` / `--timer $int` 
  - `agent [%id]` -> challenge agent
    - `-d $int` / `--difficulty $int`
    - `-t $int` / `--timer $int` 
- lb / leaderboard
  - `'none'` -> total record
  - `player(s)` ->  players record
  - `agent(s)`  -> agents record
  - `record $id, [%id]`  -> record between two players or agents 
    - `-t $datetime` / `--time $datetime`

### Advanced Commands (Reach Goals)

- resume - resume game with session id, maybe require password
  - `none` - dialog
  - `$id`  - resume game with session id
- settings
  - `set` (default challenge settings)
    - `resume`         - true/false
    - `timer_allowed`  - true/false
    - `timer_default`  - true/false
    - `timer_duration` - seconds
    - `agents`         - agent dialog
    - `agent $id`      - true/false
  - `reset` (settings to default)
  - `player $id`
    - `none`           - list player status
    - `show_record`    - true/false
    - `ban`            - start/true/false
    - `reset`
    - `promote`    (user status)
    - `demote`     (user status)