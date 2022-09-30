# DuneDiscordBot

## Requirements

* Python 3.10 (Developed in Python 3.10 but other versions can work)
* Python Packages
    * discord
    * numpy
    * pandas
    * requests
    * matplotlib
* Discord
  Bot: [Tutorial: How to create a Discord bot with python](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)
    * Discord Bot Token
    * Discord Guild ID
* Dune Token: [How to get a Token](https://dune.com/docs/api/#obtaining-an-api-key)

## Installation

1. Install python requirements

```
pip install requirements.txt
```

2. Set Environment variables

   2.1 Set the DUNE_TOKEN with following command:

    ```
    export DUNE_TOKEN=123456789
    ```

   2.2 Set the DISCORD_BOT_TOKEN with following command:

    ```
    export DISCORD_BOT_TOKEN=123456789
    ```

   2.3 Set the GUILD_ID with following command:

    ```
    export GUILD_ID=123456789
    ```

3. Invite the Discord Bot to your Server
4. Execute python script

```
python DiscordController.py
```

## Using Discord

### Dune Command

#### Base Command

```
!dune {dune_query_id} {output_type} {x_column} {y_column}
```

#### Parameter description

| Parameter     | Description                                       | Required |
|---------------|---------------------------------------------------|----------|
| dune_query_id | ID of a Dune Query.                               | yes      |
| output_type   | Which result type the data should be given back.  | no       |
| x_column      | Name or index of the column to use for the x axis | no       |
| y_column      | Name or index of the column to use for the y axis | no       |

#### Output Type options

| Option       | Description              |
|--------------|--------------------------|
| bar          | Matplotlib Bar graph     |
| line         | Matplotlib Line graph    |
| scatter      | Matplotlib Scatter graph |
| table        | data as ".csv" table     |
| single_value | Single value as text     |
