import os
import sys
import json
import subprocess
import argparse
import glob

home_path = os.environ['HOME']

# preferences
secondary_color = "lightblue",
secondary_font = "DroidSansMono Nerd Font Mono 9"
qam_path = f"{home_path}/main/configs/qam"
root_search_path = f"{home_path}/main"
rofi_path = f"{home_path}/main/configs/rofi"
rofi_options = "-dmenu -sep @ -markup-rows -p Search -normal-window -format i -i"

def get_formatted_filepath(path):
    basename = os.path.basename(path)
    parent_dir = os.path.dirname(path).replace(f"{home_path}/", str())
    return f"<b>{basename}</b>   <span color='{secondary_color}' font='{secondary_font}'>{parent_dir}</span>"


if __name__ == '__main__':

    # all basenames of directories that are to be ignored in the searching of files
    ignored_dirs = [
        "android_sdk",
        "music",
        "cursors",
        "icons",
        "fonts",
        "gradle",
        "build",
        "node_modules",
        "themes",
        "autokey",
        "snap",
        "yay",
        "syncthing",
        "vscode_extensions",
        "downloads",
        "extensions",
        "photos",
        ".git",
        ".gradle",
        ".idea",
        "plugins",
        "__pycache__",
        "swap"
    ]

    # produce all filepaths as options to the option selector
    filepaths = []
    for dir_path, subdirs, filenames in os.walk(root_search_path):
        filepaths.append(dir_path)
        
            dir_path).replace(f"{home_dir}/", str())
        formatted_file_options.append()
        subdirs[:] = [
            dir for dir in subdirs if dir not in ignored_dirs]
        filepaths += [os.path.join(dir_path, filename)
                      for filename in filenames]

    # produce formatted options for files from filepaths
    formatted_file_options = []

    for option in filepaths:
        filename = os.path.basename(option)
        parent_dir_path = os.path.dirname(option).replace(
            os.environ['HOME'] + '/', str())
        formatted_option = f"<b>{filename}</b>   <span color='{parent_path_color}' font='{sub_font}'>{parent_dir_path}</span>"
        formatted_file_options.append(formatted_option)

    # produce application options map (each entry is a map of title: Title and command: Executed command)
    applications_map = json.load(os.path.join(qam_dir, "applications.json"))

    formatted_application_options = []

    for application in applications_map:
        app_title = application['title']
        app_command = application['command']
        formatted_option = f"<b>{app_title}</b>   <span color='{parent_path_color}' font='{sub_font}'>{app_command}</span>"
        formatted_application_options.append(formatted_option)

    # produce one long '@' separated string of properly formatted options
    all_formatted_options = '@'.join(
        ['@'.join(formatted_application_options), '@'.join(formatted_file_options)])

    # run rofi with the formatted list as options
    feed_options_cmd = f'echo "{all_formatted_options}"'
    show_rofi_cmd = f"rofi -config {rofi_config_path} {rofi_options}"

    # get the index of the selected option
    index = int(subprocess.check_output(
        f"{feed_options_cmd} | {show_rofi_cmd}", shell=True).decode)

    # decide the type of option and the according selection menu to be shown
    app_options_len = len(applications_map)

    if index < app_options_len:
        app = list(applications_map)[index]
        app_command = app['command']
        subprocess.run(app_command, shell=True)
    elif index >= app_options_len:
        index -= app_options_len
        selected_file = filepaths[index]

        # load manip options

        manip_options_map = json.load(f"{qam_dir}/manip_options.json")

        manip_options = []

        # run options on the selected option

        if os.path.isdir(selected_file):
            formatted_manip_options += list(manip_options['dirs'].values())
        if selected_file.endswith(('.py', '.sh')):
            formatted_manip_options += list(manip_options['scripts'].values())
        form += list(manip_options['files'].values())

        formatted_second_options = '@'.join(
            [f"<b>{option.split(' # ')[0]}</b>" for option in second_options])

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
