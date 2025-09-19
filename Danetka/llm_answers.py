from enum import Enum

class LLMAnswer(str, Enum):
    YES = "Yes"
    NO = "No"
    WIN = "You won! Game over"
    SHOW_SOLUTION = "the solution"
    INVALID = "Please ask only yes/no questions"