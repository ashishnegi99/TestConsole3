import json as simplejson

class TestSuiteJson:

    def __init__(self):
        self.kit_details = {
            "RELEASE": "APR-4.1(Fortuna)",
            "BUILD_NUMBER": "08.12.4"
        }
        self.box_list= {}
        self.suite_list = {}

    def set_kit_details(self, kit_details):
        self.kit_details = kit_details

    def create_box_details(self, **kwargs):
        box_details = {}
        box_details["BOX_IP"] = kwargs.get("ip")
        box_details["UNIT_ADDRESS"] = kwargs.get("unit_address")
        box_details["TERMINAL_ID"] = kwargs.get("terminal_id")
        box_details["CLIENT_IP"] = kwargs.get("client_ip")
        box_details["BOX_TYPE"] = kwargs.get("type")
        return box_details

    def append_box_impl(self, box_name, box_details):
        self.box_list[box_name] = box_details

    def append_box(self, box_name, **details):
        box_details = self.create_box_details(**details)
        self.append_box_impl(box_name, box_details)

    def append_suite(self, suite_name, test_cases):
        self.suite_list[suite_name] = test_cases

    def get_json(self):
        retval = {}
        retval["KIT_DETAILS"] = self.kit_details
        retval["BOX"] = self.box_list
        retval["SUITE_NAME"] = self.suite_list
        return retval


