#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-09-07 00:36:36
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-04-09 19:46:01
FilePath: /hotkey/hotkey_manager.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 
'''

import os
from hi_basic import *


class HotKeyVars(object):
    """For dynamic change the hotkey command."""

    PATH = "@PATH"
    DIR = "@DIR"
    pass


class Hotkey(object):
    """For provide hotkey."""
    NAME_KEY = "hotkey"
    COMMAND_KEY = "command"
    PATH_KEY = "path"

    def __init__(self, hotkey: str, command: str, path: str = "") -> None:
        """Init a hotkey.

        Args:
            hotkey (str): the hotkey for call.
            command (str): the command in hotkey.
            path (str, optional): the path where to call. Defaults to "".
        """
        self._hotkey = hotkey
        self._command = command
        self._path = path
        pass

    @classmethod
    def from_dict(cls, info: dict) -> "Hotkey":
        """Create hotkey from dict."""
        info.get(cls.NAME_KEY)

        return Hotkey(
            hotkey=info.get(cls.NAME_KEY),
            command=info.get(cls.COMMAND_KEY),
            path=info.get(cls.PATH_KEY)
        )

    def to_dict(self) -> dict:
        """Trans hotkey to dict."""
        return {
            self.NAME_KEY: self._hotkey,
            self.COMMAND_KEY: self._command,
            self.PATH_KEY: self._path
        }

    def to_cmd(self) -> str:
        """Get the actual command."""
        cmd = self._command.replace(
                HotKeyVars.PATH, os.getcwd()
            ).replace(
                HotKeyVars.DIR, os.path.dirname(os.getcwd())
            )
        return cmd

    @property
    def hotkey(self) -> str:
        """Get the hotkey."""
        return self._hotkey

    @property
    def raw_command(self) -> str:
        """Get the command."""
        return self._command

    @property
    def path(self) -> str:
        """Get the path will run."""
        return self._path

    pass


class HotkeyManager(object):
    """For Hotkey manager."""

    HOTKEY_CONFIG = HiPath.userpath("hotkey.json")
    HOTKEY_TABLE_KEY = "hotkey_list"

    @classmethod
    def set_hotkey(cls, hotkey: Hotkey) -> None:
        """Set a hotkey."""
        config = HiConfig(cls.HOTKEY_CONFIG)
        config.writer[hotkey.hotkey] = hotkey.to_dict()
        pass

    @classmethod
    def del_hotkey(cls, hotkey: str) -> bool:
        """Del a hotkey."""
        config = HiConfig(cls.HOTKEY_CONFIG)
        if config[hotkey] is None:
            return False
        del config.writer[hotkey]
        return True

    @classmethod
    def del_all(cls) -> None:
        """Del all hotkey."""
        config = HiConfig(cls.HOTKEY_CONFIG)
        config.set_items({})
        pass

    @classmethod
    def get_hotkey_list(cls) -> list:
        """Get hotkey list. Return type is list[Hotkey]."""
        config = HiConfig(cls.HOTKEY_CONFIG)

        hotkey_list = []
        for key in config.items:
            hotkey_list.append(Hotkey.from_dict(config[key]))
        return hotkey_list

    @classmethod
    def get_hotkey(cls, hotkey: str) -> Hotkey:
        """Use to get hotkey."""
        hotkey_dict = HiConfig(cls.HOTKEY_CONFIG)[hotkey]
        if hotkey_dict is None:
            return None
        return Hotkey.from_dict(hotkey_dict)

    @classmethod
    def fixed_hotkey(cls, hotkey: str) -> bool:
        """Use to fixed hotkey."""
        hotkey_info = cls.get_hotkey(hotkey=hotkey)
        if hotkey_info is None:
            return False

        cls.set_hotkey(Hotkey(
            hotkey=hotkey,
            command=hotkey_info.raw_command,
            path=os.getcwd()
        ))
        return True

    @classmethod
    def unfixed_hotkey(cls, hotkey: str) -> bool:
        """Use to unfixed hotkey."""
        hotkey_info = cls.get_hotkey(hotkey=hotkey)
        if hotkey_info is None:
            return False

        cls.set_hotkey(Hotkey(
            hotkey=hotkey,
            command=hotkey_info.raw_command,
            path=""
        ))
        return True

    @classmethod
    def run_hotkey(cls, hotkey: str) -> bool:
        """Run hotkey."""
        config = HiConfig(cls.HOTKEY_CONFIG)
        if config[hotkey] is None:
            return False
        hotkey: Hotkey = Hotkey.from_dict(config[hotkey])
        if hotkey.path:
            os.chdir(hotkey.path)
            HiLog.debug("Change dir to:" + hotkey.path)
        os.system(hotkey.to_cmd())
        return True

    pass
