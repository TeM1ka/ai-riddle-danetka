from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from pathlib import Path
import json
from llm_answers import LLMAnswer
from llm_output_parser import LLMOutputParser

class GameEngine:
    def __init__(self, prompt_path="prompt.md", games_path="games"):
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0)
        self.prompt = self.load_prompt(prompt_path)
        self.games = self.load_games(games_path)
        
        
    def load_prompt(self, path):
        prompt_file = Path(path)
        return prompt_file.read_text(encoding="utf-8")
    
    def load_games(self, folder_path):
        games = []
        folder = Path(folder_path)
        
        for file in folder.glob("*.json"):
            data = json.loads(file.read_text(encoding="utf-8"))
            games.append(data)
        return games
    
    def pick_game(self):
        print("\nAvailable games:")
        for i, g in enumerate(self.games, 1):
            print(f"{i}. {g['title']}")
            
        while(True):
            choice = input("Pick a game number ")
            try:
                idx = int(choice) - 1 
                if 0 <= idx < len(self.games):
                    return self.games[idx]
            except Exception:
                pass
            print("Invalid choice, try again")
            
            
    def build_chain(self, game):
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),
            ("system", f"The riddle is: {game['riddle']}"),
            ("system", f"The hidden solution is: {game['solution']}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        return ConversationChain(llm=self.llm, prompt=prompt, memory=memory, verbose=False)
    
    
    def start(self):
        print("Welcome to Danetka game!")
        parser = LLMOutputParser()
        
        while True:
            game = self.pick_game()
            
            if game is None:
                print("Exiting..")
                break
            
            chain = self.build_chain(game)
            print(f"\nRiddle: {game['riddle']}\n")
            
            while True:
                user_input = input("Player: ")
                if user_input.lower() in ["quit", "exit", "end"]:
                    print("Game ended by the player\n")
                    break
                  
                response = chain.run(input=user_input)
                parsed_response = parser.parse(response)
                
                if parsed_response in [LLMAnswer.YES, LLMAnswer.NO, LLMAnswer.WIN, LLMAnswer.INVALID]:
                    print("LLM: ", parsed_response.value)
                    
                if parsed_response == LLMAnswer.SHOW_SOLUTION:
                    print(f"LLM: {game['solution']} Game over!")
                    
                if parsed_response in [LLMAnswer.WIN, LLMAnswer.SHOW_SOLUTION]:
                    break                    
                
                
            continue_the_game = input("Do you want to play another game? (y/n)")
            if continue_the_game.lower() != "y":
                print("Ending the game..")
                break
                
    