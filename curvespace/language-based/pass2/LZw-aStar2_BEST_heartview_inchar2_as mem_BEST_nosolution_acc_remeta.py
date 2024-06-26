
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "read folder for files, analyze them and send them to database for link of which is in specific folder found on C:."
character = "some punk from street"
personality = "chill, but gets mad sometimes if there isnt enough of something"

# personality or role/character can have <<ABORT>>
def aiChar(task, character, personality, canZeroShot=True):
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
    while("SOLVED" not in answer or steps <= 2):

        # it feels like this has just the right balance of prioritization and openness. removing "task" loses some
        # creating new language for every step alleviates on previous failures
        # this specific solution just FEELS like something else, like much more solid
        # concept of interjecting languages work to guide more
        # "solved" and solution, help with guiding to goal
        answer = ai("describe state of task, what was done so far, and prediction for how much work is left in ideal scenario.", [task, answer, "using language to complete task", language, view])
        subhearts = list(hearts[:-4])
        for i in [character, personality, answer]:
            subhearts.append(i)
        # talk about acc here is worse
        heart = ai("react to it in character, and talk about it's accuracy", subhearts)
        if("<<ABORT>>" in heart):
            break
        # 3 abstrac tabs make it worse
        metas = ai("describe it in character what are 3 abstract abstractions in this", [character, personality, heart])
        hearts.append(metas)
        hearts.append(heart)
        view = ai("describe layout and view in character", [character, personality, answer, metas])
        language = ai("create new language for this", [task, metas, answer, view])
        solutions = solutions[:-6]
        solutions.append(view)
        solutions.append(language)
        solutions.append(answer)
        answer = ai("implement and validate solution with provided language. reply <<SOLVED>> if it's solved.\n", solutions)
        steps+=6
    print("steps", steps)
    return answer

if __name__ == '__main__':
    answer = aiChar(task, character, personality, canZeroShot=False)
    answer = ai("extract TODOs. add <<USER>> if user should do these things.", [answer])
    if( "USER" in answer):
        print("WAITING USER")
        input()