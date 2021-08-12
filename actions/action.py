from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker, Action
from rasa_sdk.events import UserUtteranceReverted, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from markdownify import markdownify as md

from requests import (
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    Timeout
)

from chat.actions import ChatApis
from chat.actions.WeatherApis import get_weather_by_day


###打招呼
class ActionFirst(Action):
    def name(self) -> Text:
        return "action_first"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        dispatcher.utter_message(md("您好，我是小瑞，您的AI智能助理，我会闲聊、查天气预报，请问有什么可以帮您？您可以这样向我提问: <br/>你今年多少岁了<br/>\
                                     可以讲一个幽默的笑话吗<br/>\
                                     中国面积有多大<br/>\
                                     长沙天气怎么样<br/>\
                                     周杰伦是谁<br/>\
                                     上海后天天气怎么样"))
        return []




# #### (查询手机号码业务)
# class NumberForm(FormAction):
#     """Example of a custom form action"""
#
#     def name(self) -> Text:
#         """Unique identifier of the form"""
#
#         return "number_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         return ["type", "number", "business"]
#
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""
#
#         return {
#             "type": self.from_entity(entity="type", not_intent="chitchat"),
#             "number": self.from_entity(entity="number", not_intent="chitchat"),
#             "business": [
#                 self.from_entity(
#                     entity="business", intent=["inform", "request_number"]
#                 ),
#                 self.from_entity(entity="business"),
#             ],
#         }
#
#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""
#         number_type = tracker.get_slot('type')
#         number = tracker.get_slot('number')
#         business = tracker.get_slot('business')
#         if not business:
#             dispatcher.utter_message(text="您要查询的{}{}所属人为张三，湖南长沙人，现在就职于地球村物业管理有限公司。".format(number_type, number))
#             return []
#
#         dispatcher.utter_message(text="你要查询{}为{}的{}为：balabalabalabalabala。".format(number_type, number, business))
#         return [SlotSet("business", None)]



#### 调用心知天气的API(天气问答)
class WeatherForm(FormAction):

    def name(self) -> Text:
        return "weather_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["date_time", "address"]

    def submit(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict]:
        address = tracker.get_slot('address')
        date_time = tracker.get_slot('date_time')

        date_time_number = text_date_to_number_date(date_time)

        if isinstance(date_time_number, str):  # parse date_time failed
            dispatcher.utter_message("暂不支持查询 {} 的天气".format([address, date_time_number]))
        else:
            weather_data = get_text_weather_date(address, date_time, date_time_number)
            dispatcher.utter_message(weather_data)
        return []

def get_text_weather_date(address, date_time, date_time_number):
    try:
        result = get_weather_by_day(address, date_time_number)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = """
            {} {} ({}) 的天气情况为：白天：{}；夜晚：{}；气温：{}-{} °C
        """
        text_message = text_message_tpl.format(
            result['location']['name'],
            date_time,
            result['result']['date'],
            result['result']['text_day'],
            result['result']['text_night'],
            result['result']["high"],
            result['result']["low"],
        )

    return text_message

def text_date_to_number_date(text_date):
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "后天":
        return 2

    # Not supported by weather API provider freely
    if text_date == "大后天":
        # return 3
        return text_date

    if text_date.startswith("星期"):
        # TODO: using calender to compute relative date
        return text_date

    if text_date.startswith("下星期"):
        # TODO: using calender to compute relative date
        return text_date

    # follow APIs are not supported by weather API provider freely
    if text_date == "昨天":
        return text_date
    if text_date == "前天":
        return text_date
    if text_date == "大前天":
        return text_date



#### 调用百度unit的API(闲聊)
class ActionDefaultFallback(Action):

    def name(self):
        return 'action_default_fallback'

    def run(self, dispatcher, tracker, domain):

        text = tracker.latest_message.get('text')
        message = ChatApis.unit_chat(text)
        if message is not None:
            dispatcher.utter_message(message)
        else:
            dispatcher.utter_template('utter_default', tracker, silent_fail=True)
        return [UserUtteranceReverted()]
