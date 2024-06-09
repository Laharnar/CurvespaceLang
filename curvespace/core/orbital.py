from mincore import sendWithMessage
from mincore import aiLang

task = "implement project that is saved and loaded on disk in current path"
answer = aiLang(task, False, OUTPUT="list")
items = answer
if(len(items) > 6):
    answer = aiLang("pick items to be erased(it's index) <<INDEX>>_<<NUMBER>> (example: INDEX_3")
