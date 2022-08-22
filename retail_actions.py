"""import cv2
import numpy as np
from PIL import Image
import os, time
import logging
import json
from datetime import datetime"""
import logging
import queue

from numpy import array
from speech_errors import SpeechResult as enums
from speech_errors import SpeechProcessError, SpeechInvalidArgumentError
import user_database
import user_input
# from decorators import status_check
"""elif self.check_registered_retailer(is_android_action) is not None:
    retailer = is_android_action
    query_type = "order"
    return True"""

query_type = ""
business_name = ""
item_list = []
add_ons = []
description = []
action_type = ""
location = "hillsboro"

g_db_obj = user_database.ProcessDataBaseRequests()

class RetailActions:
    def __init__(self, text_input: array):
        """stores parameter text_input into self.data, creates an empty list with name self.words,
        initiates self.user_input_data_obj() with variable name self.g_ui_obj, and creates an object of user_database.creates_connection()

        Args:
            text_input (array): array from function convert_strings_to_num_array(strings)
        """
        self.data = text_input
        self.words = []
        self.g_ui_obj = self.user_input_data_obj()
        g_db_obj.create_connection()

    def __del__(self):
        pass

    @staticmethod
    def user_input_data_obj():
        """creates an object of ProcessUserInput() class from user_input module

        Returns:
            object: object of user_input.ProcessUserInput() class
        """
        logging.info("Success")
        return user_input.ProcessUserInput()

    @staticmethod
    def compare_input_string(string_input: str, compare_string: str):
        """compare the user input string with the one fetched from databse

        Args:
            string_input (str): string fetched from database.
            compare_string (str): string entered by user.

        Returns:
            Boolean: TRUE - if string_input is same as compare_string
                     FALSE - if string_input is not same as compare_string
        """
        for i in range(len(string_input)):
            if string_input[i] != compare_string[i]:
                logging.info("Success")
                return False
        logging.info("Success")
        return True

    
    def get_retail_db_words(self, table: str, index: int):
        """Fetch all the rows from given table with the given index then find the one that match the user input and stores 
        the string in self.words


        Args:
            table (str): table name to search and get data from.

            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            bytes: r[3] if there is only one word in user input, 4th item of row is fetched from database which is a string converted into bytes.
            NONE: if there is no matching data found in database or there are more than one words in user input.
        """
        try:
            if index == 1:
                rows = g_db_obj.fetch_db_data(table, self.data[0][0])
                if rows is not None:
                    for r in rows:
                        if r[1] == self.data[0][1]:
                            if self.compare_input_string(r[3], self.data[0][2]):
                                self.words.append(r[3])
                                return r[3]
                    logging.info("Success")
                    return None
                else:
                    logging.debug("This is of intention to " + query_type + " android application")
                    return None
            for i in range(index):
                rows = g_db_obj.fetch_db_data(table, self.data[i][0])
                if rows is not None:
                    for r in rows:
                        if r[1] == self.data[i][1]:
                            if self.compare_input_string(r[3], self.data[i][2]):
                                self.words.append(r[3])
            logging.info("Success")
            return None
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechProcessError(e)

    
    def validate_user_input(self, index: int):
        """check self.is_input_incomplete() and puts the item returned in a new list

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Returns:
            NONE: NONE
            word: a list
        """
        incomplete = self.is_input_incomplete(index)
        word = []
        if incomplete is not None:
            for item in incomplete:
                word.append(item)
            logging.info("Success")
            return word
        logging.info("Success")
        return None

    
    def is_input_incomplete(self, index: int):
        """fill in details like query_type, business_name, item_list if they are none

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Returns:
            NONE: if result list is empty
            result: if result is not empty
        """
        global query_type, business_name, item_list, add_ons, description
        result = []
        if not query_type:
            result.append("query_type")
        if not business_name:
            result.append("business_name")
        if not item_list:
            result.append("item_list")
        if item_list and not add_ons:
            if self.check_add_ons_need(index):
                result.append("add_ons")
            if self.check_description_need(index):
                result.append("description")
        if result:
            logging.info("Success")
            return result
        logging.info("Success")
        return None

    
    def check_add_ons_need(self, index: int):
        """check for add ons from supply_add_ons table

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            NONE: NONE
            bytes: byte string
            
        """
        try:
            addon_req = self.get_retail_db_words("Supply_Add_ons", index)
            if addon_req is not None:
                logging.info("Success")
                return addon_req
            logging.info("Success")
            return None
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechProcessError(e)

    
    def check_description_need(self, index: int):
        """check for description from supply_descriptions table

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            NONE: NONE
            bytes: byte string
            
        """
        try:
            desc_need = self.get_retail_db_words("Supply_Descriptions", index)
            if desc_need is not None:
                logging.info("Success")
                return desc_need
            logging.info("Success")
            return None
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechProcessError(e)

    @staticmethod
    def generate_retail_action_request():
        """creates a list of dictionaries with keys `query_type`, `item_list`, `description`, `business_name`, `add_ons` and its corresponding values 

        Returns:
            list: a list of dictionaries items with key value pairs
        """
        lis = [{"query_type": query_type}, {"item_list": item_list},
               {"description": description}, {"business_name": business_name},
               {"add_ons": add_ons}]
        logging.info("Success")
        return lis

    
    def ret_get_more_input(self, incomplete: list):
        """calls request_user_for_input() and update_user_input_to_cloud() from user_input module

        Args:
            incomplete (list): list with word and its descriptions

        Raises:
            SpeechInvalidArgumentError: _description_

        Returns:
            str: SUCCESS
            str: FAILURE
        """
        try:
            if self.g_ui_obj.request_user_for_input() == enums.FAILURE.name:
                logging.error("Insufficient input from user, could not process the request '{}'".format(incomplete))
                y=self.g_ui_obj.update_user_input_to_cloud(incomplete)
                return enums.FAILURE.name
            logging.info("Success")
            return enums.SUCCESS.name
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechInvalidArgumentError(e)

    
    def get_business_name(self, index: int):
        """search businesses table for matching row and return business name in bytes string or notify user and get confirmation

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            NONE: NONE
            bytes: name of business in bytes string
        """
        try:
            self.get_retail_db_words("Businesses", index)
            if not self.words:
                logging.debug("No business in user request")
                return None
            else:
                if len(self.words) == 1:
                    logging.info("Success")
                    return self.words[0]
                else:
                    logging.debug("Notify user and get confirmation")
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechProcessError(e)

    
    def get_business_action(self, index: int):
        """check and return the matching business action from business_Actions table

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            NONE: NONE
            bytes: name of business in bytes string
        """
        try:
            self.get_retail_db_words("Business_actions", index)
            if not self.words:
                logging.debug("No business in user request")
                return None
            else:
                logging.info("Success")
                return self.words[0]
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechProcessError(e)

    
    def get_business_supplies_list(self, index: int):
        """check given business's table for suuplies or available_supplies table for matching supplies

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            NONE: NONE
            bytes: name of business in bytes string
        """
        try:
            global business_name
            if business_name is not None:
                self.get_retail_db_words(business_name.decode("utf_8")+"_supplies", index)
            else:
                self.get_retail_db_words("Available_supplies", index)
            if not self.words:
                logging.debug("No business in user request")
                return None
            else:
                logging.info("Success")
                return self.words
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechProcessError(e)

    
    def check_retail_command_status(self, index: int):
        """calls get_business_name, get_business_supplies_list, get_business_action, check_description_need and check_add_ons
        then fill the variables bussiness_name, item_list, query_type, description and add_ons 

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)

        Raises:
            SpeechProcessError: _description_

        Returns:
            str: SUCCESS
            str: FAILURE
        """
        try:
            global business_name
            global item_list
            business_name = self.get_business_name(index)
            if business_name is not None:
                self.words.clear()
                item_list = self.get_business_supplies_list(index)
                if item_list is not None:
                    self.words.clear()
            else:
                item_list = self.get_business_supplies_list(index)
                if item_list is not None:
                    self.words.clear()
            global query_type
            query_type = self.get_business_action(index)
            if query_type is not None:
                self.words.clear()
            global description
            description = self.check_description_need(index)
            if description is not None:
                self.words.clear()
            global add_ons
            add_ons = self.check_add_ons_need(index)
            if add_ons is not None:
                self.words.clear()
            if business_name and item_list and query_type and description and add_ons:
                logging.info("Success")
                return enums.SUCCESS.name
            else:
                logging.info("Success")
                return enums.FAILURE.name
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechProcessError(e)

    
    def decode_user_input_for_retail_actions(self, index: int, q_t: queue):
        """Decode anp Process user input after getting an array and index from user_input.convert_strings_to_num_array(strings) and put results in queue q_t which can be either
        SUCCESS or FAILURE depending on conditions in the function.

        Args:
            index (int): length of the array created by convert_strings_to_num_array(strings)
            q_t (queue): object created from Queue.queue() class

        Raises:
            SpeechProcessError: _description_
        """
        try:
            if index == 1 and self.get_retail_actions(self.get_retail_db_words("Business_actions", index)):
                logging.warning("This is of intention to " + query_type + " business action and incomplete")
                """ Request for user input"""
                words = self.validate_user_input(index)
                if self.ret_get_more_input(words) == enums.SUCCESS.name:
                    if self.check_retail_command_status(index) == enums.SUCCESS.name:
                        if self.validate_user_input(index) is not None:
                            q_t.put(enums.SUCCESS.name)
                        else:
                            q_t.put(enums.FAILURE.name)
                    else:
                        q_t.put(enums.FAILURE.name)
                else:
                    q_t.put(enums.FAILURE.name)
            else:
                if self.check_retail_command_status(index) == enums.SUCCESS.name:
                    words = self.validate_user_input(index)
                    if self.ret_get_more_input(words) == enums.SUCCESS.name:
                        if self.check_retail_command_status(index) == enums.SUCCESS.name:
                            if self.validate_user_input(index) is not None:
                                q_t.put(enums.SUCCESS.name)
                            else:
                                q_t.put(enums.FAILURE.name)
                        else:
                            q_t.put(enums.FAILURE.name)
                    else:
                        q_t.put(enums.FAILURE.name)
                else:
                    q_t.put(enums.FAILURE.name)
            logging.info("Success")
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechProcessError(e)

    
    def get_retail_actions(self, words: bytes):
        """match words in argument with bytes string in self.data and fill query_type with word if matched

        Args:
            words (bytes): byte string from get_retail_db_words()

        Raises:
            SpeechProcessError: _description_

        Returns:
            NONE: NONE
            bytes: same as argument
        """
        try:
            if words == self.data[0][2]:
                global query_type
                query_type = words.decode("utf_8")
                logging.info("Success")
                return words
            logging.info("Success")
            return None
        except Exception as e:
            logging.error(f"{e}")
            raise SpeechProcessError(e)