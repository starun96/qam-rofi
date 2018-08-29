import os
import sys
import json
import subprocess
import argparse
import glob

home_path = os.environ['HOME']

""" # preferences
secondary_color = "lightblue",
secondary_font = "DroidSansMono Nerd Font Mono 9"
root_search_path = f"{home_path}/main"
rofi_path = f"{home_path}/main/configs/rofi"
rofi_options = "-dmenu -sep @ -markup-rows -p Search -normal-window -format i -i" """

# load configuration options
with open('config.json', 'r') as conf_file:
    config = json.load(conf_file)


def get_formatted_filepath(path):
    basename = os.path.basename(path)
    parent_dir = os.path.dirname(path).replace(f"{home_path}/", str())
    return f"<b>{basename}</b>   <span color='{config['secondary_color']}' font='{config['secondary_font']}'>{parent_dir}</span>"


def get_formatted_application(title, command):
    return f"<b>{title}</b>   <span color='{config['secondary_color']}' font='{config['secondary_font']}'>{command}</span>"


def get_formatted_secondary_option(option):
    return f"<b>{option}</b>"


if __name__ == '__main__':

    formatted_options = []

    # produce all applications
    application_commands = []
    for application in config['applications']:
        app_title = application['title']
        app_command = application['command']
        application_commands.append(app_command)
        formatted_options.append(
            get_formatted_application(app_title, app_command))

    # produce all filepaths as options to the option selector and accumulate formatted filepaths
    filepaths = []
    for dir_path, subdirs, filenames in os.walk(config['root_search_path']):
        filepaths.append(dir_path)
        formatted_options.append(get_formatted_filepath(dir_path))
        subdirs[:] = [
            dir for dir in subdirs if dir not in config['ignored_dirs']]
        filepaths += [os.path.join(dir_path, filename)
                      for filename in filenames]

    # produce one long '@' separated string of properly formatted options
    all_formatted_options = '@'.join(formatted_options)

    # run rofi with the formatted list as options
    feed_options_cmd = f'echo "{all_formatted_options}"'
    show_rofi_cmd = f"rofi -config {config['rofi_config_path']} {config['rofi_options']}"

    # get the index of the selected option
    index = int(subprocess.check_output(
        f"{feed_options_cmd} | {show_rofi_cmd}", shell=True).decode())

    # decide the type of option and the according selection menu to be shown
    app_options_len = len(application_commands)

    if index < app_options_len:
        selected_command = application_commands[index]
        subprocess.run(selected_command, Shell=True)
    elif index >= app_options_len:
        index -= app_options_len
        selected_file = filepaths[index]

        # load manip options

        manip_options = config['manip_options']
        second_options = []
        formatted_second_options = []
        # run options on the selected option

        if os.path.isdir(selected_file):
            for option in manip_options['dirs']:
                second_options.append(option)
                formatted_second_options.append(get_formatted_secondary_option(list(option.values()[0])))

        if selected_file.endswith(('.py', '.sh')):
            for option in manip_options['scripts']:
                second_options.append(option)
                formatted_second_options.append(get_formatted_secondary_option(list(option.values()[0])))

        for option in manip_options['files']:
            second_options.append(option)
            formatted_second_options.append(get_formatted_secondary_option(list(option.values()[0])))

        formatted_second_options = '@'.join(formatted_second_options)

        cmd_echo_second_options = f'echo "{formatted_second_options}"'

        cmd_index = int(subprocess.check_output(
            f"{cmd_echo_second_options} | {cmd_show_options}", shell=True).decode())

        selected_action = second_options[cmd_index].split(' # ')[1]


""" parser = argparse.ArgumentParser(description='Process some integers')

parser.add_argument('integers', metavar='N', type=int,
                    nargs='+', help='an integer for the accumulator')

parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max, help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers)) """
