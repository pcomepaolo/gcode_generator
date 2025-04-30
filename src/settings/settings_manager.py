from ast import literal_eval
import configparser
import os
from src.settings.settings_file_model import settings_model
import shutil
from typing import Any



class SettingsManager(configparser.ConfigParser):
    SETTINGS_FILE_NAME = 'settings.ini'
    GCODE_HEAD_FILE_NAME = 'gcode_head.ini'
    GCODE_TAIL_FILE_NAME = 'gcode_tail.ini'
    
    def __init__(self):
        super().__init__(allow_no_value=True)
        self.settings_model = settings_model
        self.gcode_head=''
        self.gcode_tail=''
        self.check_settings_file(self.SETTINGS_FILE_NAME)
        self.check_settings_file(self.GCODE_HEAD_FILE_NAME)
        self.check_settings_file(self.GCODE_TAIL_FILE_NAME)
        self.load_settings()

    def check_settings_file(self,file_to_check) -> None:
        if not os.path.exists(os.path.abspath(file_to_check)):
            shutil.copy(
                os.path.abspath(os.path.join('defaults',file_to_check)),
                os.path.abspath(file_to_check))

    def load_settings(self) -> None:
        self.read(self.SETTINGS_FILE_NAME)
        with open(self.GCODE_HEAD_FILE_NAME,'r') as head_file:
            self.gcode_head+=head_file.read()
        with open(self.GCODE_TAIL_FILE_NAME,'r') as tail_file:
            self.gcode_tail+=tail_file.read()

    def convert_type(self,value:Any) -> Any:
        """
        Convert the type of value from string to the correct type (int, float, etc.)
        """
        try:
            return literal_eval(value)
        except ValueError:
            return value

    def value(self,setting:str) -> Any:
        setting_value = None
        for section in self.sections():
            for option in self.options(section):
                if option == setting:
                    setting_value = self.convert_type(self.get(section, option))
                    break
        if setting_value is not None:
            return setting_value
        else:
            raise TypeError('Value not found')