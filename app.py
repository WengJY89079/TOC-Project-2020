import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message
from MajongToc import MagjongFSM

load_dotenv()


'''machine = TocMachine(
    states=["user", "state1", "state2"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": "is_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {"trigger": "go_back", "source": ["state1", "state2"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)'''

check_clear_state = ["dealer", "elseplayer"]
han_cal_state = ["dealerclear", "dealernotclear", "elseclear", "elsenotclear",
                "dealerclear1han", "dealernotclear1han", "elseclear1han", "elsenotclear1han",
                "dealerclear2han", "dealernotclear2han", "elseclear2han", "elsenotclear2han",
                "dealerclear3han", "dealernotclear3han", "elseclear3han", "elsenotclear3han",
                "dealerclear4han", "dealernotclear4han", "elseclear4han", "elsenotclear4han",
                "dealerclear5han", "dealernotclear5han", "elseclear5han", "elsenotclear5han",
                "dealerclear6han", "dealernotclear6han", "elseclear6han", "elsenotclear6han",
                "dealerclear7han", "dealernotclear7han", "elseclear7han", "elsenotclear7han",
                "dealerclear8han", "dealernotclear8han", "elseclear8han", "elsenotclear8han",
                "dealerclear9han", "dealernotclear9han", "elseclear9han", "elsenotclear9han",
                "dealerclear10han", "dealernotclear10han", "elseclear10han", "elsenotclear10han",
                "dealerclear11han", "dealernotclear11han", "elseclear11han", "elsenotclear11han",
                "dealerclear12han", "dealernotclear12han", "elseclear12han", "elsenotclear12han"]

result_state = ["dealerfullhan", "elsefullhan", "dealersanbai", "elsesanbai", "dealerbai", "elsebai", "dealerhane", "elsehane", "dealermangan", "elsemangan",
            "dealer4han", "else4han", "dealer3han", "else3han", "dealer2han", "else2han", "dealer1han", "else1han"]


machine = MagjongFSM(
    states=["init", "dealer", "elseplayer", "dealerclear", "dealernotclear", "elseclear", "elsenotclear",
            "dealerclear1han", "dealernotclear1han", "elseclear1han", "elsenotclear1han",
            "dealerclear2han", "dealernotclear2han", "elseclear2han", "elsenotclear2han",
            "dealerclear3han", "dealernotclear3han", "elseclear3han", "elsenotclear3han",
            "dealerclear4han", "dealernotclear4han", "elseclear4han", "elsenotclear4han",
            "dealerclear5han", "dealernotclear5han", "elseclear5han", "elsenotclear5han",
            "dealerclear6han", "dealernotclear6han", "elseclear6han", "elsenotclear6han",
            "dealerclear7han", "dealernotclear7han", "elseclear7han", "elsenotclear7han",
            "dealerclear8han", "dealernotclear8han", "elseclear8han", "elsenotclear8han",
            "dealerclear9han", "dealernotclear9han", "elseclear9han", "elsenotclear9han",
            "dealerclear10han", "dealernotclear10han", "elseclear10han", "elsenotclear10han",
            "dealerclear11han", "dealernotclear11han", "elseclear11han", "elsenotclear11han",
            "dealerclear12han", "dealernotclear12han", "elseclear12han", "elsenotclear12han",
            "dealerfullhan", "elsefullhan", "dealersanbai", "elsesanbai", "dealerbai", "elsebai", "dealerhane", "elsehane", "dealermangan", "elsemangan",
            "dealer4han", "else4han", "dealer3han", "else3han", "dealer2han", "else2han", "dealer1han", "else1han", "fart"
            ],
    transitions=[
        {"trigger": "go_back", "source": ["dealerfullhan", "elsefullhan", "dealersanbai", "elsesanbai", "dealerbai", "elsebai", "dealerhane", "elsehane", "dealermangan", "elsemangan",
            "dealer4han", "else4han", "dealer3han", "else3han", "dealer2han", "else2han", "dealer1han", "else1han", "fart"], "dest": "init"},
        {"trigger": "go_end", "source": ["dealerclear12han", "dealernotclear12han", "dealerclear11han", "dealernotclear11han"], "dest":"dealersanbai", 'conditions': "end"},
        {"trigger": "go_end", "source": ["elseclear12han", "elsenotclear12han", "elseclear11han", "elsenotclear11han"], "dest":"elsesanbai", 'conditions': "end"},
        {"trigger": "go_end", "source": ["dealerclear10han", "dealernotclear10han", "dealerclear9han", "dealernotclear9han", "dealerclear8han", "dealernotclear8han"], "dest":"dealerbai", 'conditions': "end"},
        {"trigger": "go_end", "source": ["elseclear10han", "elsenotclear10han", "elseclear9han", "elsenotclear9han", "elseclear8han", "elsenotclear8han"], "dest":"elsebai", 'conditions': "end"},
        {"trigger": "go_end", "source": ["dealerclear7han", "dealernotclear7han", "dealerclear6han", "dealernotclear6han"], "dest":"dealerhane", 'conditions': "end"},
        {"trigger": "go_end", "source": ["elseclear7han", "elsenotclear7han", "elseclear6han", "elsenotclear6han"], "dest":"elsehane", 'conditions': "end"},
        {"trigger": "go_end", "source": ["dealerclear5han", "dealernotclear5han"], "dest":"dealermangan", 'conditions': "end"},
        {"trigger": "go_end", "source": ["elseclear5han", "elsenotclear5han"], "dest":"elsemangan", 'conditions': "end"},
        {"trigger": "go_end", "source": ["dealerclear4han", "dealernotclear4han"], "dest":"dealer4han", 'conditions': "end"},
        {"trigger": "go_end", "source": ["dealerclear4han", "dealernotclear4han"], "dest":"else4han", 'conditions': "end"},
        {"trigger": "go_end", "source": ["dealerclear3han", "dealernotclear3han"], "dest":"dealer3han", 'conditions': "end"},
        {"trigger": "go_end", "source": ["elseclear3han", "elsenotclear3han"], "dest":"else3han", 'conditions': "end"},
        {"trigger": "go_end", "source": ["dealerclear2han", "dealernotclear2han"], "dest":"dealer2han", 'conditions': "end"},
        {"trigger": "go_end", "source": ["elseclear2han", "elsenotclear2han"], "dest":"else2han", 'conditions': "end"},
        {"trigger": "go_end", "source": ["dealerclear1han", "dealernotclear1han"], "dest":"dealer1han", 'conditions': "end"},
        {"trigger": "go_end", "source": ["elseclear1han", "elsenotclear1han"], "dest":"else1han", 'conditions': "end"},
        {"trigger": "go_end", "source": ["dealerclear", "dealernotclear", "elseclear", "elsenotclear"], "dest":"fart", 'conditions': "end"},
        {
            'trigger': 'go_next', 'source': 'init', 'dest': 'dealer', 'conditions': "is_going_to_dealer",
        },
        {
            'trigger': 'go_next', 'source': 'init', 'dest': 'elseplayer', 'conditions': "is_going_to_elseplayer",
        },
        {
            'trigger': 'check_clear', 'source': 'dealer', 'dest': 'dealerclear', 'conditions': "is_going_to_clear",
        },
        {
            'trigger': 'check_clear', 'source': 'dealer', 'dest': 'dealernotclear', 'conditions': "is_going_to_notclear",
        },
        {
            'trigger': 'check_clear', 'source': 'elseplayer', 'dest': 'elseclear', 'conditions': "is_going_to_clear",
        },
        {
            'trigger': 'check_clear', 'source': 'elseplayer', 'dest': 'elsenotclear', 'conditions': "is_going_to_notclear",
        },
        # dealer clear 1 han cal
        {
            'trigger': 'go_han', 'source': 'dealerclear', 'dest': 'dealerclear1han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear1han', 'dest': 'dealerclear2han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear2han', 'dest': 'dealerclear3han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear3han', 'dest': 'dealerclear4han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear4han', 'dest': 'dealerclear5han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear5han', 'dest': 'dealerclear6han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear6han', 'dest': 'dealerclear7han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear7han', 'dest': 'dealerclear8han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear8han', 'dest': 'dealerclear9han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear9han', 'dest': 'dealerclear10han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear10han', 'dest': 'dealerclear11han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear11han', 'dest': 'dealerclear12han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "clear_han1",
        },
        # dealer not clear 1 han cal
        {
            'trigger': 'go_han', 'source': 'dealernotclear', 'dest': 'dealernotclear1han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear1han', 'dest': 'dealernotclear2han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear2han', 'dest': 'dealernotclear3han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear3han', 'dest': 'dealernotclear4han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear4han', 'dest': 'dealernotclear5han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear5han', 'dest': 'dealernotclear6han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear6han', 'dest': 'dealernotclear7han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear7han', 'dest': 'dealernotclear8han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear8han', 'dest': 'dealernotclear9han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear9han', 'dest': 'dealernotclear10han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear10han', 'dest': 'dealernotclear11han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear11han', 'dest': 'dealernotclear12han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "notclear_han1",
        },
        ##########################
        # else player clear 1 han cal
        {
            'trigger': 'go_han', 'source': 'elseclear', 'dest': 'elseclear1han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear1han', 'dest': 'elseclear2han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear2han', 'dest': 'elseclear3han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear3han', 'dest': 'elseclear4han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear4han', 'dest': 'elseclear5han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear5han', 'dest': 'elseclear6han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear6han', 'dest': 'elseclear7han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear7han', 'dest': 'elseclear8han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear8han', 'dest': 'elseclear9han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear9han', 'dest': 'elseclear10han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear10han', 'dest': 'elseclear11han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear11han', 'dest': 'elseclear12han', 'conditions': "clear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "clear_han1",
        },
        # else player not clear 1 han cal
        {
            'trigger': 'go_han', 'source': 'elsenotclear', 'dest': 'elsenotclear1han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear1han', 'dest': 'elsenotclear2han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear2han', 'dest': 'elsenotclear3han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear3han', 'dest': 'elsenotclear4han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear4han', 'dest': 'elsenotclear5han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear5han', 'dest': 'elsenotclear6han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear6han', 'dest': 'elsenotclear7han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear7han', 'dest': 'elsenotclear8han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear8han', 'dest': 'elsenotclear9han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear9han', 'dest': 'elsenotclear10han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear10han', 'dest': 'elsenotclear11han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear11han', 'dest': 'elsenotclear12han', 'conditions': "notclear_han1",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "notclear_han1",
        },
        ##########################

        # dealer clear 2 han
        {
            'trigger': 'go_han', 'source': 'dealerclear', 'dest': 'dealerclear2han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear1han', 'dest': 'dealerclear3han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear2han', 'dest': 'dealerclear4han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear3han', 'dest': 'dealerclear5han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear4han', 'dest': 'dealerclear6han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear5han', 'dest': 'dealerclear7han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear6han', 'dest': 'dealerclear8han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear7han', 'dest': 'dealerclear9han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear8han', 'dest': 'dealerclear10han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear9han', 'dest': 'dealerclear11han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear10han', 'dest': 'dealerclear12han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "clear_han2",
        },
        # dealer not clear 2 han cal
        {
            'trigger': 'go_han', 'source': 'dealernotclear', 'dest': 'dealernotclear2han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear1han', 'dest': 'dealernotclear3han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear2han', 'dest': 'dealernotclear4han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear3han', 'dest': 'dealernotclear5han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear4han', 'dest': 'dealernotclear6han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear5han', 'dest': 'dealernotclear7han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear6han', 'dest': 'dealernotclear8han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear7han', 'dest': 'dealernotclear9han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear8han', 'dest': 'dealernotclear10han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear9han', 'dest': 'dealernotclear11han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear10han', 'dest': 'dealernotclear12han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "notclear_han2",
        },
        ##########################
        # else clear 2 han
        {
            'trigger': 'go_han', 'source': 'elseclear', 'dest': 'elseclear2han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear1han', 'dest': 'elseclear3han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear2han', 'dest': 'elseclear4han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear3han', 'dest': 'elseclear5han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear4han', 'dest': 'elseclear6han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear5han', 'dest': 'elseclear7han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear6han', 'dest': 'elseclear8han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear7han', 'dest': 'elseclear9han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear8han', 'dest': 'elseclear10han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear9han', 'dest': 'elseclear11han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear10han', 'dest': 'elseclear12han', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "clear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "clear_han2",
        },
        # else not clear 2 han cal
        {
            'trigger': 'go_han', 'source': 'elsenotclear', 'dest': 'elsenotclear2han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear1han', 'dest': 'elsenotclear3han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear2han', 'dest': 'elsenotclear4han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear3han', 'dest': 'elsenotclear5han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear4han', 'dest': 'elsenotclear6han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear5han', 'dest': 'elsenotclear7han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear6han', 'dest': 'elsenotclear8han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear7han', 'dest': 'elsenotclear9han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear8han', 'dest': 'elsenotclear10han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear9han', 'dest': 'elsenotclear11han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear10han', 'dest': 'elsenotclear12han', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "notclear_han2",
        },
        {
            'trigger': 'go_han', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "notclear_han2",
        },

        ######################

        # dealer clear 3 han
        {
            'trigger': 'go_han', 'source': 'dealerclear', 'dest': 'dealerclear3han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear1han', 'dest': 'dealerclear4han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear2han', 'dest': 'dealerclear5han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear3han', 'dest': 'dealerclear6han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear4han', 'dest': 'dealerclear7han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear5han', 'dest': 'dealerclear8han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear6han', 'dest': 'dealerclear9han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear7han', 'dest': 'dealerclear10han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear8han', 'dest': 'dealerclear11han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear9han', 'dest': 'dealerclear12han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "clear_han3",
        },
        ##########################
        # else clear 3 han
        {
            'trigger': 'go_han', 'source': 'elseclear', 'dest': 'elseclear3han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear1han', 'dest': 'elseclear4han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear2han', 'dest': 'elseclear5han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear3han', 'dest': 'elseclear6han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear4han', 'dest': 'elseclear7han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear5han', 'dest': 'elseclear8han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear6han', 'dest': 'elseclear9han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear7han', 'dest': 'elseclear10han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear8han', 'dest': 'elseclear11han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear9han', 'dest': 'elseclear12han', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "clear_han3",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "clear_han3",
        },

        #########################
        # dealer clear 5 han cal
        {
            'trigger': 'go_han', 'source': 'dealerclear', 'dest': 'dealerclear5han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear1han', 'dest': 'dealerclear6han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear2han', 'dest': 'dealerclear7han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear3han', 'dest': 'dealerclear8han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear4han', 'dest': 'dealerclear9han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear5han', 'dest': 'dealerclear10han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear6han', 'dest': 'dealerclear11han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear7han', 'dest': 'dealerclear12han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "clear_han5",
        },
        # else clear 5 han cal
        {
            'trigger': 'go_han', 'source': 'elseclear', 'dest': 'elseclear5han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear1han', 'dest': 'elseclear6han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear2han', 'dest': 'elseclear7han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear3han', 'dest': 'elseclear8han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear4han', 'dest': 'elseclear9han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear5han', 'dest': 'elseclear10han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear6han', 'dest': 'elseclear11han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear7han', 'dest': 'elseclear12han', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "clear_han5",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "clear_han5",
        },
        #########################
        # dealer clear 6 han cal
        {
            'trigger': 'go_han', 'source': 'dealerclear', 'dest': 'dealerclear6han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear1han', 'dest': 'dealerclear7han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear2han', 'dest': 'dealerclear8han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear3han', 'dest': 'dealerclear9han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear4han', 'dest': 'dealerclear10han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear5han', 'dest': 'dealerclear11han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear6han', 'dest': 'dealerclear12han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear7han', 'dest': 'dealerfullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "clear_han6",
        },
        # else clear 6 han cal
        {
            'trigger': 'go_han', 'source': 'elseclear', 'dest': 'elseclear6han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear1han', 'dest': 'elseclear7han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear2han', 'dest': 'elseclear8han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear3han', 'dest': 'elseclear9han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear4han', 'dest': 'elseclear10han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear5han', 'dest': 'elseclear11han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear6han', 'dest': 'elseclear12han', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear7han', 'dest': 'elsefullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "clear_han6",
        },
        {
            'trigger': 'go_han', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "clear_han6",
        },
        #####################
        # dealer clear full han
        {
            'trigger': 'go_han', 'source': ['dealerclear', 'dealerclear1han', 'dealerclear2han',  'dealerclear3han',  'dealerclear4han',  'dealerclear5han'
                                            , 'dealerclear6han',  'dealerclear7han',  'dealerclear8han',  'dealerclear9han',  'dealerclear10han',  'dealerclear11han',  'dealerclear12han'],
            'dest': 'dealerfullhan', 'conditions': "clear_full_han",
        },
        # dealer not clear full han
        {
            'trigger': 'go_han', 'source': ['dealernotclear', 'dealernotclear1han', 'dealernotclear2han',  'dealernotclear3han',  'dealernotclear4han',  'dealernotclear5han'
                                            , 'dealernotclear6han',  'dealernotclear7han',  'dealernotclear8han',  'dealernotclear9han',  'dealernotclear10han',  'dealernotclear11han',  'dealernotclear12han'],
            'dest': 'dealerfullhan', 'conditions': "not_clear_full_han",
        },
        #####################
        # else clear full han
        {
            'trigger': 'go_han', 'source': ['elseclear', 'elseclear1han', 'elseclear2han',  'elseclear3han',  'elseclear4han',  'elseclear5han'
                                            , 'elseclear6han',  'elseclear7han',  'elseclear8han',  'elseclear9han',  'elseclear10han',  'elseclear11han',  'elseclear12han'],
            'dest': 'elsefullhan', 'conditions': "clear_full_han",
        },
        # else not clear full han
        {
            'trigger': 'go_han', 'source': ['elsenotclear', 'elsenotclear1han', 'elsenotclear2han',  'elsenotclear3han',  'elsenotclear4han',  'elsenotclear5han'
                                            , 'elsenotclear6han',  'elsenotclear7han',  'elsenotclear8han',  'elsenotclear9han',  'elsenotclear10han',  'elsenotclear11han',  'elsenotclear12han'],
            'dest': 'elsefullhan', 'conditions': "not_clear_full_han",
        },
        #####################

        # bao 1 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear1han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear2han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear3han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerclear4han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerclear5han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerclear6han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerclear7han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerclear8han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerclear9han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerclear10han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerclear11han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerclear12han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao1",
        },
        # bao 1 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear1han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear2han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear3han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealernotclear4han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealernotclear5han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealernotclear6han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealernotclear7han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealernotclear8han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealernotclear9han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealernotclear10han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealernotclear11han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealernotclear12han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao1",
        },
        # bao 1 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear1han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear2han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear3han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elseclear4han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elseclear5han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elseclear6han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elseclear7han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elseclear8han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elseclear9han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elseclear10han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elseclear11han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elseclear12han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao1",
        },
        # bao 1 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear1han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear2han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear3han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsenotclear4han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsenotclear5han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsenotclear6han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsenotclear7han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsenotclear8han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsenotclear9han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsenotclear10han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsenotclear11han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsenotclear12han', 'conditions': "bao1",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao1",
        },
#####################

        # bao 2 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear2han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear3han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear4han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerclear5han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerclear6han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerclear7han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerclear8han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerclear9han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerclear10han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerclear11han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerclear12han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao2",
        },
        # bao 2 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear2han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear3han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear4han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealernotclear5han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealernotclear6han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealernotclear7han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealernotclear8han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealernotclear9han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealernotclear10han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealernotclear11han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealernotclear12han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao2",
        },
        # bao 2 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear2han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear3han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear4han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elseclear5han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elseclear6han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elseclear7han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elseclear8han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elseclear9han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elseclear10han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elseclear11han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elseclear12han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao2",
        },
        # bao 2 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear2han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear3han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear4han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsenotclear5han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsenotclear6han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsenotclear7han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsenotclear8han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsenotclear8han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsenotclear10han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsenotclear11han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsenotclear12han', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao2",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao2",
        },
        #####################

        # bao 3 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear3han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear4han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear5han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerclear6han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerclear7han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerclear8han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerclear9han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerclear10han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerclear11han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerclear12han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao3",
        },
        # bao 3 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear3han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear4han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear5han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealernotclear6han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealernotclear7han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealernotclear8han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealernotclear9han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealernotclear10han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealernotclear11han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealernotclear10han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao3",
        },
        # bao 3 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear3han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear4han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear5han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elseclear6han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elseclear7han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elseclear8han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elseclear9han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elseclear10han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elseclear11han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elseclear12han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao3",
        },
        # bao 3 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear3han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear4han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear5han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsenotclear6han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsenotclear7han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsenotclear8han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsenotclear9han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsenotclear10han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsenotclear11han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsenotclear12han', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao3",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao3",
        },
        #####################

        # bao 4 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear4han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear5han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear6han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerclear7han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerclear8han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerclear9han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerclear10han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerclear11han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerclear12han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao4",
        },
        # bao 4 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear4han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear5han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear6han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealernotclear7han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealernotclear8han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealernotclear9han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealernotclear10han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealernotclear11han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealernotclear12han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealerfullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao4",
        },
        # bao 4 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear4han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear5han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear6han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elseclear7han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elseclear8han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elseclear9han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elseclear10han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elseclear11han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elseclear12han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao4",
        },
        # bao 4 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear4han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear5han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear6han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsenotclear7han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsenotclear8han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsenotclear9han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsenotclear10han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsenotclear11han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsenotclear12han', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsefullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao4",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao4",
        },
#####################

        # bao 5 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear5han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear6han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear7han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerclear8han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerclear9han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerclear10han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerclear11han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerclear12han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        # bao 5 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear5han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear6han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear7han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealernotclear8han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealernotclear9han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealernotclear10han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealernotclear11han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealernotclear12han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao5",
        },
        # bao 5 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear5han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear6han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear7han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elseclear8han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elseclear9han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elseclear10han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elseclear11han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elseclear12han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
        # bao 5 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear5han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear6han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear7han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsenotclear8han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsenotclear9han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsenotclear10han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsenotclear11han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsenotclear12han', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao5",
        },
#####################

        # bao 6 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear6han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear7han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear8han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerclear9han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerclear10han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerclear11han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerclear12han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        # bao 6 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear6han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear7han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear8han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealernotclear9han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealernotclear10han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealernotclear11han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealernotclear12han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao6",
        },
        # bao 6 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear6han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear7han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear8han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elseclear9han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elseclear10han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elseclear11han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elseclear12han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        # bao 6 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear6han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear7han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear8han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsenotclear9han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsenotclear10han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsenotclear11han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsenotclear12han', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao6",
        },
#####################

        # bao 7 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear7han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear8han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear9han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerclear10han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerclear11han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerclear12han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        # bao 7 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear7han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear8han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear9han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealernotclear10han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealernotclear11han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealernotclear12han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao7",
        },
        # bao 7 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear7han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear8han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear9han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elseclear10han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elseclear11han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elseclear12han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        # bao 7 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear7han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear8han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear9han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsenotclear10han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsenotclear11han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsenotclear12han', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao7",
        },
#####################

        # bao 8 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear8han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear9han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear10han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerclear11han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerclear12han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        # bao 8 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear8han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear9han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear10han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealernotclear11han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealernotclear12han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao8",
        },
        # bao 8 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear8han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear9han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear10han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elseclear11han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elseclear12han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        # bao 8 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear8han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear9han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear10han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsenotclear11han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsenotclear12han', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao8",
        },
#####################

        # bao 9 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear9han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear10han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear11han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerclear12han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        # bao 9 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear9han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear10han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear11han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealernotclear12han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao9",
        },
        # bao 9 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear9han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear10han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear11han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elseclear12han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        # bao 9 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear9han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear10han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear11han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsenotclear12han', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao9",
        },
#####################

        # bao 10 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear10han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear11han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerclear12han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        # bao 10 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear10han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear11han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealernotclear12han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao10",
        },
        # bao 10 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear10han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear11han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elseclear12han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        # bao 10 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear10han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear11han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsenotclear12han', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao10",
        },
#####################

        # bao 11 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear11han', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerclear12han', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        # bao 11 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear11han', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealernotclear12han', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao11",
        },
        # bao 11 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear11han', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elseclear12han', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        # bao 11 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear11han', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsenotclear12han', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao11",
        },
#####################

        # bao 12 dealer clear
        {
            'trigger': 'go_bao', 'source': 'dealerclear', 'dest': 'dealerclear12han', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear1han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear2han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear3han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear4han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear5han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear6han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear7han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear8han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear9han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear10han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear11han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealerclear12han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        # bao 12 dealer not clear
        {
            'trigger': 'go_bao', 'source': 'dealernotclear', 'dest': 'dealernotclear12han', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear1han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear2han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear3han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear4han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear5han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear6han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear7han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear8han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear9han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear10han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear11han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'dealernotclear12han', 'dest': 'dealerfullhan', 'conditions': "bao12",
        },
        # bao 12 else clear
        {
            'trigger': 'go_bao', 'source': 'elseclear', 'dest': 'elseclear12han', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear1han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear2han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear3han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear4han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear5han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear6han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear7han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear8han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear9han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear10han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear11han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elseclear12han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        # bao 12 else not clear
        {
            'trigger': 'go_bao', 'source': 'elsenotclear', 'dest': 'elsenotclear12han', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear1han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear2han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear3han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear4han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear5han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear6han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear7han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear8han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear9han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear10han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear11han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        {
            'trigger': 'go_bao', 'source': 'elsenotclear12han', 'dest': 'elsefullhan', 'conditions': "bao12",
        },
        ####################################################################
    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        print(event)
        if machine.state == 'init':
            response = machine.go_next(event)
            if response == False:
                send_text_message(event.reply_token, "輸入無效 請重新再試")
        elif machine.state in check_clear_state:
            clear = machine.check_clear(event)
            if clear == False:
                send_text_message(event.reply_token, "輸入無效 請重新再試")
        elif machine.state in han_cal_state:
            han = machine.go_han(event)
            if han == False:
                boa = machine.go_bao(event)
                if boa == False:
                    end = machine.go_end(event)
                    if end == False:
                        send_text_message(event.reply_token, "輸入無效 請重新再試")
        print(f"\nFSM STATE: {machine.state}")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    #machine.get_graph().draw("fsm.png", prog="dot", format="png")
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
