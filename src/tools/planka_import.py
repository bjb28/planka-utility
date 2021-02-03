#!/usr/bin/env python3

# Standard Python Libraries
import argparse
import itertools
import json
import logging

# Third-Party Libraries
import psycopg2
from psycopg2 import OperationalError

# Project Libraries
from ._version import __version__
from models.models import Project

POSITION_GAP = 65535


def generate_template():
    """Output template for a json file to be imported to Planka."""
    logging.debug("Creating Template File")

    temp = {
        "boards": [
            {
                "name": "Board Name",
                "lists": [
                    {
                        "name": "List Name",
                        "cards": [
                            {
                                "name": "Card Name",
                                "tasks": ["Take 1", "Task 2"],
                            }
                        ],
                    }
                ],
            }
        ],
    }

    with open("planka_template.json", "w") as fp:
        json.dump(temp, fp)
        logging.info("Template Saves to planka_template.json")


def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Create connection to postgres database.

    Args:
        db_name (string): Database Name
        db_user (string): Database Username
        db_password (string): Database password
        db_host (string): Database Hostname
        db_port (string): Database Port Number

    Raises:
        e: Connection errors.

    Returns:
        Psycopg2 Connection: A connection to the postgres database.
    """

    logging.debug("Connecting to postgres")
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        logging.info("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        raise e

    return connection


def execute_read_query(connection, query):
    """Execute a read query on the postgres database.

    Args:
        connection (Psycopg2 Connection): The connection to the postgres database.
        query (string): The SQL query to be run.

    Returns:
        list(tuples): The results of the SQL query.
    """

    logging.debug(f"Executing Read Query: {query}")
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        logging.debug("Query was successful.")
        return result
    except OperationalError as e:
        logging.error(f"The error '{e}' occurred")


def execute_query(connection, query):
    """Execute a query to change the database.

    Args:
        connection (Psycopg2 Connection): The connection to the postgres database.
        query (string): The SQL query to be run.
    """

    logging.debug(f"Executing Action: {query}")
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.debug("Query executed successfully")
    except OperationalError as e:
        logging.error(f"The error '{e}' occurred")


def pull_project(connection, project):
    """Pull a project from Planka

    Args:
        connection (Psycopg2 Connection): The connection to the postgres database.
        project (Project): A Project object representing a Planka database.
    """
    # TODO Build this out.
    pass


def add_board(connection, board, project_id):
    """Add board to Planka.

    A method to add a board to planka if it does not exists.
    If it does exist then the board object with appropriate
    info is returned.

    Args:
        connection (Psycopg2 Connection): The connection to the postgres database.
        board (Board): A Board object representing a Planka board.
        project_id (int): The project ID for the board.

    Returns:
        Board: A fully populated Board object.
    """
    # Get the board ID or crate new board if not found.
    try:
        (board.id, board.position, board.project_id) = execute_read_query(
            connection, board.select_board()
        )[0]
    except IndexError:
        # TODO Add validation to check a new board is desired.
        logging.warning(f"{board.name} not found. Adding board.")

        # Find last board postion and adds postion gap to the value.
        prior_position = execute_read_query(connection, board.max_position())[0][0]
        if prior_position:
            board.position = prior_position + POSITION_GAP
        else:
            board.position = 0

        board.project_id = project_id

        # Insert the new board.
        execute_query(connection, board.insert())

        # Get the new board's ID
        board.id = execute_read_query(connection, board.select_id())[0][0]

    return board


def add_list(connection, _list, board_id):
    """Add list to Planka.

    A method to add a list to planka if it does not exists.
    If it does exist then the list object with appropriate
    info is returned.

    Args:
        connection (Psycopg2 Connection): The connection to the postgres database.
        list (List): A List object representing a Planka list.
        board_id (int): The board ID for the list.

    Returns:
        List: A fully populated List object.
    """
    # Get the list ID or crate new list if not found.
    try:
        (_list.id, _list.position, _list.board_id) = execute_read_query(
            connection, _list.select_list()
        )[0]
    except IndexError:
        # TODO Add validation to check a new board is desired.
        logging.warning(f"{_list.name} not found. Adding list.")

        # Find last list postion and adds postion gap to the value.
        prior_position = execute_read_query(connection, _list.max_position())[0][0]
        if prior_position:
            _list.position = prior_position + POSITION_GAP
        else:
            _list.position = 0

        _list.board_id = board_id

        # Insert the new board.
        execute_query(connection, _list.insert())

        # Get the new board's ID
        _list.id = execute_read_query(connection, _list.select_id())[0][0]

    return _list


def add_card(connection, card, board_id, list_id):
    """Add card to Planka.

    A method to add a card to planka if it does not exists.
    If it does exist then the card object with appropriate
    info is returned.

    Args:
        connection (Psycopg2 Connection): The connection to the postgres database.
        card (Card): A Card object representing a Planka card.
        board_id (int): The board ID for the card.
        list_id (int): The list ID for the card.

    Returns:
        Card: A fully populated Card object.
    """
    # Get the card ID or crate new card if not found.
    try:
        (card.id, card.position, card.board_id, card.list_id) = execute_read_query(
            connection, card.select_card()
        )[0]
    except IndexError:
        # TODO Add validation to check a new card is desired.
        logging.warning(f"{card.name} not found. Adding card.")

        # Find last card postion and adds postion gap to the value.
        prior_position = execute_read_query(connection, card.max_position())[0][0]
        if prior_position:
            card.position = prior_position + POSITION_GAP
        else:
            card.position = 0

        card.board_id = board_id
        card.list_id = list_id

        # Insert the new board.
        execute_query(connection, card.insert())

        # Get the new board's ID
        card.id = execute_read_query(connection, card.select_id())[0][0]

    return card


def add_task(connection, task, db_tasks, card_id):
    """Add a task to Planka card

    Checks if the task is in the system before adding it to the card.
    If the task is found, a warning is printed and process continues.

    Args:
        connection (Psycopg2 Connection): The connection to the postgres database.
        task (string): The string indicating the task.
        db_tasks (list[tuples]): A list of tuples that holds the tasks from the database is index 0.
        card_id (int): The card id for which the task is associated with.
    """

    if task not in itertools.chain(*db_tasks):
        logging.debug(f"Adding {task}.")
        query = f"""
            INSERT INTO
                task (card_id, name, is_completed)
            VALUES
                ({card_id},'{task}', false)
        """
        execute_query(connection, query)
    else:
        logging.warning(f"{task} is already on card.")


def load_cards(connection, project, file_name):
    """Load data into cards.

    Args:
        connection (Psycopg2 Connection): The connection to the postgres database.
        project_id (string): The project that boards should be added to.
    """
    logging.debug(f"Loading data structure from {file_name}")

    # Load project from JSON.
    with open(file_name, "r") as fp:
        project.load_json(json.load(fp))

    for board_index, board in enumerate(project.boards):
        # Pull the board info from planka.
        logging.info(f"Pulling {board.name} Board.")

        board = add_board(connection, board, project.id)

        logging.debug(f"{board.name} Board id: {board.id}")

        for list_index, _list in enumerate(board.lists):
            # Pull the list info from planka.
            logging.info(f"Pulling {_list.name} List.")

            _list = add_list(connection, _list, board.id)

            logging.debug(f"{_list.name}List id: {_list.id}")

            # TODO Check if cards exists.
            for card_index, card in enumerate(_list.cards):
                # Process the cards. ASSUMES NO CARDS IN LIST.

                card = add_card(connection, card, board.id, _list.id)

                logging.debug(f"Card id: {card.id}")

                db_tasks = execute_read_query(connection, card.get_tasks())

                for task in card.tasks:
                    add_task(connection, task, db_tasks, card.id)

                _list.cards[card_index] = card
            board.lists[list_index] = _list
        project.boards[board_index] = board


def build_new(connection, project, file_name):
    """Build out the project boards

    Args:
        connection (Psycopg2 Connection): The connection to the postgres database.
        project (Project): The project object that the boards will be added under.
    """

    # Hold the postion of each item.
    board_position = POSITION_GAP
    list_position = POSITION_GAP
    card_position = POSITION_GAP

    logging.debug(f"Loading data structure from {file_name}")

    with open(file_name, "r") as fp:
        project.load_json(json.load(fp))

    for board_index, board in enumerate(project.boards):
        logging.info(f"Building {board.name} Board.")

        # Calculate the next board postion.
        board_position = board_position + (board_index * POSITION_GAP)
        board.position = board_position
        board.project_id = project.id

        execute_query(connection, board.insert())

        # Get the new board's ID
        board.id = execute_read_query(connection, board.select_id())[0][0]
        logging.debug(f"Board id: {board.id}")

        for list_index, _list in enumerate(board.lists):
            logging.info(f"Building {_list.name} List.")

            # Calculate the next list position.
            list_position = list_position + (list_index * POSITION_GAP)

            _list.position = list_position
            _list.board_id = board.id

            execute_query(connection, _list.insert())

            # Get the new list's ID
            _list.id = execute_read_query(connection, _list.select_id())[0][0]
            logging.debug(f"List id: {_list.id}")

            for card_index, card in enumerate(_list.cards):
                # Calculate the next card postion.
                card_position = card_position + (card_index * POSITION_GAP)

                card.position = card_position
                card.board_id = board.id
                card.list_id = _list.id

                logging.info(f"Building {card.name} Card.")

                execute_query(connection, card.insert())

                # Get the new card's ID
                card.id = execute_read_query(connection, card.select_id())[0][0]
                logging.debug(f"Card id: {card.id}")

                for task in card.tasks:
                    logging.debug(f"Adding {task}.")
                    query = f"""
                        INSERT INTO
                            task (card_id, name, is_completed)
                        VALUES
                            ({card.id},'{task}', false)
                    """
                    execute_query(connection, query)

                _list.cards[card_index] = card
            board.lists[list_index] = _list
        project.boards[board_index] = board
        logging.info(f"{board.name} Board Complete!")


def main():
    """Set up logging, connect to Postgres, call requested function(s)."""
    parser = argparse.ArgumentParser(
        description="Import JSON into Planka.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "PROJECT_NAME",
        action="store",
        help="The project name.",
    )
    parser.add_argument(
        "FILE_NAME",
        action="store",
        help="The JSON file to load content from.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-l", "--load", action="store_true", dest="load", help="Load NMAP File."
    )
    group.add_argument(
        "-n",
        "--new",
        action="store_true",
        dest="new",
        help="Set up a new Project from the the file planka_build.json",
    )
    group.add_argument(
        "-t",
        "--template",
        action="store_true",
        dest="template",
        help="Generate a JSON template for import into Planka. A project name is required still.",
        # TODO Make so a project name is not required.
    )

    parser.add_argument(
        "--DB-host",
        action="store",
        dest="db_host",
        default="127.0.0.1",
        help="The host IP for the postgres server.",
    )
    parser.add_argument(
        "--DB-pwd",
        action="store",
        dest="db_pwd",
        default="postgres",
        help="Password for the postgres server.",
    )
    parser.add_argument(
        "--DB-port",
        action="store",
        dest="db_port",
        default="5432",
        help="Port fo the postgres server.",
    )
    parser.add_argument(
        "--DB-name",
        action="store",
        dest="db_name",
        default="planka",
        help="Postgres database name.",
    )
    parser.add_argument(
        "--DB-user",
        action="store",
        dest="db_user",
        default="postgres",
        help="Username for the postgres server.",
    )
    parser.add_argument(
        "--log-level",
        action="store",
        dest="log_level",
        default="info",
        help='If specified, then the log level will be set to the specified value.  Valid values are "debug", "info", "warning", "error", and "critical".',
    )
    parser.add_argument("--version", action="version", version=__version__)

    args = parser.parse_args()

    # Set up logging
    log_level = args.log_level
    try:
        logging.basicConfig(
            format="%(levelname)s: %(message)s", level=log_level.upper()
        )
    except ValueError:
        logging.critical(
            f'"{log_level}" is not a valid logging level. Possible values are debug, info, warning, error, and critical.'
        )
        return 1

    if args.template:
        generate_template()
        return 0

    # Set up database connection
    try:
        connection = create_connection(
            args.db_name,
            args.db_user,
            args.db_pwd,
            args.db_host,
            args.db_port,
        )
    except OperationalError as e:
        logging.error(f"The connection error '{e}' occurred")
        return 1

    if args.new:
        project = Project(name=args.PROJECT_NAME)

        # Create the new Project.
        execute_query(connection, project.insert())

        # Gets value from first item in list and tuple
        project.id = execute_read_query(connection, project.select_id())[0][0]

        # Adds demo user to project
        # TODO handle already exists error.
        query = """SELECT id FROM user_account WHERE username='demo'"""
        user_id = execute_read_query(connection, query)[0][0]

        query = f"""
            INSERT INTO
                project_membership(project_id, user_id)
            VALUES
                ({project.id}, {user_id})
        """
        execute_query(connection, query)

        build_new(connection, project, args.FILE_NAME)

    elif args.load:
        project = Project(name=args.PROJECT_NAME)

        # Gets value from first item in list and tuple
        try:
            project.id = execute_read_query(connection, project.select_id())[0][0]
        except IndexError:
            logging.error(f"Project {project.name} does not exist.")
            return 1

        load_cards(connection, project, args.FILE_NAME)


if __name__ == "__main__":
    main()
