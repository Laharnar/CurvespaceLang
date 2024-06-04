
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "read folder for files, analyze them and send them to database for link of which is in specific folder found on C:."
character = "some punk from street"
personality = "chill, but gets mad sometimes if there isnt enough of something"

def aiLang(task, canZeroShot=True):
    solutions = list()
    languages = list()
    answer = ai("+add <<SOLVED>> if its solved.=>\n"+task)
    steps=1
    if(canZeroShot and "SOLVED" in answer):
        return answer
    solutions.append(task)
    language = ai("create new language for this\n" + task)
    solutions.append(language)
    hearts = list()
    steps=2
    metas = ai("what are meta-meta 5 layers in this", [character, personality, answer])
    view = ai("describe layout and view", [answer, language, metas])
    while("SOLVED" not in answer):

        answer = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", [task, answer, "using language to complete task", language, view])
        subhearts = list(hearts[:-4])
        for i in [character, personality, answer]:
            subhearts.append(i)
        metas = ai("describe it in character what are abstract abstractions in this", [character, personality, answer])
        heart = ai("react to it in character", subhearts)
        hearts.append(metas)
        hearts.append(heart)
        language = ai("create new language for this", [task, heart, answer])
        # more concise i guess? not as open ended. defined better. but i liked interpretor one, from in char
        view = ai("describe layout and view in character", [character, personality, answer, metas])
        solutions.append(view)
        solutions.append(language)
        solutions.append(answer)
        answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)
        steps+=6
    print("steps", steps)
    return answer

aiLang(task, canZeroShot=False)