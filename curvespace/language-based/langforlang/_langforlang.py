
from core.mincore import sendWithMessage as ai
from core.mechanistic_layers import BinaryConstruct as Bin

task = "find which fields of project in current folder could be improved"

#answer = ai("create new language for creating languages")
#answer = ai("create new language for creating interpreted programming languages")
#answer = ai("create new language for creating languages for this", [task])
#answer = ai("create new language for creating interpreted languages for this", [task])
#answer = ai("create new broad language for creating specific languages for this", [task])
#answer = ai("create new definition language for creating smaller languages")
#answer = ai("create new definition language for creating smaller languages for this", [task])

#answer = ai("create new language for creating interpreted programming languages")
#answer = ai("create new language for this, by using existing language", [answer, task])
#answer = ai("create new language for this, by using existing language in context", [answer, task])

#answer = ai("what are 'crossroad' ideas for you? ideas that have many options and go in my directions?")

#answer = ai("create new language for this", [task])
#answer = ai("create new formal language based on this language", [answer])

answer = ai("create new language for this", [task])
#answer = ai("create new formal language that contains this language", [answer])
#answer = ai("create new recursive formal language that contains this language", [answer])
answer = ai("create new language that contains this language", [answer])
answer = ai("create new formal language that contains this language and allows infinite abstractions", [answer])

#answer = ai("define testable solution for this, with its own syntax and semantics", [task])
#answer = ai("define solution for this, with its own syntax and semantics", [task])
