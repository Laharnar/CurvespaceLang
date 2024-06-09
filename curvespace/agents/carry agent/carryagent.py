import core.agentic_constructs as ai

x = ai.sendWithMessage("describe 1+1 shortly")


class Agent:
    def __init__(self):
        self.world = list()
        self.picked = "Nothing is picked"
        pass

    def pickup(self, observed):
        criteria = "small,clear,independent"
        answer = ai.sendWithMessage("should any of this be picked up based on criteria? <<YES/NO>>.\n"+criteria, ["visible:"+observed])
        if("YES" in answer):
            self.world = self.world[-10:]
            self.world.append(observed)
            self.world.append(answer)
            self.picked = observed

    def dropdown(self, observed):
        criteria = "clear,fits,is required"
        answer = ai.sendWithMessage("is this correct situation to drop picked, based on criteria? describe why? <<YES/NO>>\n"+criteria, ["picked:\n"+self.picked, "situation:\n"+observed])
        if("YES" in answer):
            self.world = self.world[-10:]
            sub = list(self.world)
            sub.append("picked:\n"+self.picked)
            sub.append("observed:\n"+observed)
            answer = ai.sendWithMessage("describe how the item is dropped in observed area, and what is new area. surround new stat with '''", sub)
            if(observed in self.world):
                self.world.remove(observed)
            from core.mechanistic_layers import BinaryConstruct as Bin
            bina = Bin("", answer)
            self.world.append(bina.text)
            self.picked = "Nothing is picked"

    def toolset(self):
        request = "<<EXTRACTCODE>>\n<<EXTRACTTEXT>>"

agent = Agent()
ai.sendWithMessage("create new language for executing picking and dropping objects in correct locations to create complex machines")
ai.sendWithMessage("create new language for executing picking and dropping objects in correct locations to create complex machines\n"+"picked: describe 1+1 shortly")
agent.pickup("describe 1+1 shortly")
agent.dropdown("here is wall")
agent.dropdown("here is paper with math")