from llm_answers import LLMAnswer

class LLMOutputParser:
    def parse(self, text: str):
        text = text.lower()
        if "the solution is" in text:
            return LLMAnswer.SHOW_SOLUTION
        
        if "you won" in text:
            return LLMAnswer.WIN
        
        if "yes" in text:
            return LLMAnswer.YES
        
        if "no" in text:
            return LLMAnswer.NO
        
        return LLMAnswer.INVALID