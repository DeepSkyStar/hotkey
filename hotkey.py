#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-09-07 00:36:36
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 19:46:18
FilePath: /hotkey/hotkey.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

from hotkey_manager import *
from hi_basic import *
import os
import argparse
import textwrap

def __hotkey(args):
    is_del = args["del"]
    is_del_all = args["del_all"]
    is_list = args["list"]
    is_fixed = args["fixed"]
    is_not_fixed = args["not_fixed"]

    if is_del is not None and len(is_del) == 1:
        if is_del[0]:
            hotkey = is_del[0]
            if HotkeyManager.del_hotkey(hotkey=hotkey):
                HiLog.info(HiText("menu_hotkey_del_successed", "Successfully del hotkey: ") + hotkey)
            else:
                HiLog.warning(HiText("menu_hotkey_not_find", "Cannot find ") + hotkey)
        else:
            HiLog.info(HiText("menu_hotkey_input_error", "Error input!"))
    elif is_fixed is not None and len(is_fixed) == 1:
        if is_fixed[0]:
            hotkey = is_fixed[0]
            if HotkeyManager.fixed_hotkey(hotkey=hotkey):
                HiLog.info(HiText("menu_hotkey_fixed_successed", "Successfully fixed hotkey: ") + hotkey)
            else:
                HiLog.warning(HiText("menu_hotkey_not_find", "Cannot find ") + hotkey)
        else:
            HiLog.info(HiText("menu_hotkey_input_error", "Error input!"))
    elif is_not_fixed is not None and len(is_not_fixed) == 1:
        if is_not_fixed[0]:
            hotkey = is_not_fixed[0]
            if HotkeyManager.unfixed_hotkey(hotkey=hotkey):
                HiLog.info(HiText("menu_hotkey_unfixed_successed", "Successfully unfixed hotkey: ") + hotkey)
            else:
                HiLog.warning(HiText("menu_hotkey_not_find", "Cannot find ") + hotkey)
        else:
            HiLog.info(HiText("menu_hotkey_input_error", "Error input!"))
    elif is_del_all:
        HotkeyManager.del_all()
        HiLog.info(HiText("menu_hotkey_del_all", "All hotkey is deleted."))
    elif is_list:
        display = ""
        for hotkey in HotkeyManager.get_hotkey_list():
            display += "{:10} ".format(hotkey.hotkey) + " "
            display += "{:10} ".format("cmd:" + hotkey.raw_command) + " "
            display += "{:10} ".format("path:" + hotkey.path) + "\n"

        if not display:
            display = "No hotkey.\n"
        print(display + "\n")
    else:
        HiLog.info(HiText("menu_hotkey_nothing_happen", "Nothing happened."))
    pass


def __set_hotkey(hotkey: str, command: str) -> None:
    HotkeyManager.set_hotkey(Hotkey(
                hotkey=hotkey,
                command=command
            ))
    HiLog.info(HiText("menu_hotkey_set_successed", "Successfully set hotkey: ") + hotkey)
    pass


def __setup_parser():
    # Define the menu.
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(HiText("menu_hotkey_desc", """
        For define hotkey,
        hotkey --set [hotkey] [command] can make a hotkey.
        hotkey --del [hotkey] can del a hotkey.
        hotkey --fixed [hotkey] can set the hotkey fixed running in the cur path.
        hotkey --not-fixed [hotkey] can set the hotkey not fixed running.
        Used @PATH get running path, Used @DIR get running dirname.
        """))
        )

    parser_hotkey_group = parser.add_mutually_exclusive_group()

    parser_hotkey_group.add_argument(
        "-l",
        "--list",
        help=HiText("menu_hotkey_list_desc", "List all hotkey."),
        action="store_true"
    )

    parser_hotkey_group.add_argument(
        "-s",
        "--set",
        nargs=2,
        help=HiText("menu_hotkey_set_desc", "Set a hotkey."),
    )

    parser_hotkey_group.add_argument(
        "-d",
        "--del",
        nargs=1,
        help=HiText("menu_hotkey_del_desc", "Del the hotkey."),
    )

    parser_hotkey_group.add_argument(
        "--del-all",
        help=HiText("menu_hotkey_del_all_desc", "Del all the hotkey."),
        action="store_true"
    )

    parser_hotkey_group.add_argument(
        "-f",
        "--fixed",
        nargs=1,
        help=HiText("menu_hotkey_fixed_desc", "Make hotkey become fixed running."),
    )

    parser_hotkey_group.add_argument(
        "-n",
        "--not-fixed",
        nargs=1,
        help=HiText("menu_hotkey_not_fixed_desc", "Make hotkey become not fixed."),
    )

    parser.set_defaults(func=__hotkey)

    # Check hotkey.
    if len(sys.argv) >= 2:
        if sys.argv[1] == "-s" or sys.argv[1] == "--set":
            if len(sys.argv) < 4:
                HiLog.warning(HiText("menu_hotkey_set_warning", "Params number is invalid!"))
            else:
                second_param = ""
                for i in range(3, len(sys.argv)):
                    if i != 3:
                        second_param += " "
                    second_param += sys.argv[i]
                __set_hotkey(sys.argv[2], second_param)
            return None
        elif HotkeyManager.get_hotkey(sys.argv[1]) is not None:
            HotkeyManager.run_hotkey(sys.argv[1])
            return None
    elif len(sys.argv) == 1:
        parser.print_help()
        return None

    # parse the input.
    args = parser.parse_args()

    if len(vars(args)) == 0:
        # if no input print help.
        parser.print_help()
    else:
        # select the function
        args.func(vars(args))
    pass


def main():
    """Entry."""
    __setup_parser()
    pass


if __name__ == "__main__":
    main()
    pass
