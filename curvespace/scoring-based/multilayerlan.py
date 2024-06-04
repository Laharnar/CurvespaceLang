
from core.mincore import aiLang
from core.mincore import sendWithMessage as ai

task = "write webpage with 3 sites, selling, buying, user dashboard"
answer = ai(task)

ai("score accuracy of last message", [task, answer])
aiLang("")