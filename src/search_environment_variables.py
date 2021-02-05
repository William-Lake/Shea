from argparse import ArgumentParser
import os


def determine_match_type(name, value, search_string):

    match_type_determiners = {
        "BOTH": lambda: search_string.upper() in name.upper()
        and search_string.upper() in value.upper(),
        "NAME": lambda: search_string.upper() in name.upper(),
        "VALUE": lambda: search_string.upper() in value.upper(),
    }

    match_type = None

    for mt, determiner in match_type_determiners.items():

        if determiner():

            match_type = mt

            break

    return match_type


def gather_args():

    arg_parser = ArgumentParser()

    arg_parser.add_argument("search_string")

    return arg_parser.parse_args().search_string


if __name__ == "__main__":

    print(
        "### NOTE THAT IF YOU WANT TO SEARCH ALL ENVIROMENT VARIABLES YOU NEED TO RUN THIS PROMPT AS AN ADMIN. ###"
    )

    search_string = gather_args()

    for name, value in os.environ.items():

        if (
            search_string.upper() in name.upper()
            or search_string.upper() in value.upper()
        ):

            match_type = determine_match_type(name, value, search_string)

            print(
                f"""
### MATCH FOUND ###

MATCH TYPE: {match_type}

Environment Variable Name:  {name}
Environment Variable Value: {value}
"""
            )

    input("Press any key to exit.")
