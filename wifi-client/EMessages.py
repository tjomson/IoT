#!/usr/bin/env python3

from enum import Enum

# class syntax

class SupportedMessages(Enum):
    CO2 = auto()
    TEMPERATURE = auto()
    RH = auto()
