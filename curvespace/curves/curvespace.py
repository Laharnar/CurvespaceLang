import os
import sys
import traceback
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../core/')))


import core.agentic_constructs as ai

class CurveCatTime:
    def __init__(self, categories):
        self.categories = categories
        self.timeItems = list()

    def parse(self, text):

        for i in range(len(text)):
            char = text[i]
            cats = self.categories
            if char.isdigit():
                catId = cats.index("number")
            elif char.isalpha():
                catId = cats.index("word")
            elif char in ['$', '#', '@']:  # Add more code characters as needed
                catId = cats.index("code")
            elif char.isspace():
                catId = cats.index("whitespace")
            else:
                catId = cats.index("unknown")
            store = [char, i, catId]
            self.timeItems.append(store)

    def print_parsed_text(self):
        print(self.timeItems)
        for char, time, catId in self.timeItems:
            print(f"Category: {self.categories[catId]}, Characters: {char}, Time: {time}]")

import json

class CurveSpace:
    def __init__(self):
        self.curveCatTimes = []

    def add_curve_cat_time(self, curve_cat_time):
        self.curveCatTimes.append(curve_cat_time)

    def remove_curve_cat_time(self, curve_cat_time):
        self.curveCatTimes.remove(curve_cat_time)

    def save(self, filename):
        data = []
        for curve_cat_time in self.curveCatTimes:
            curve_data = {
                'categories': curve_cat_time.categories,
                'timeItems': curve_cat_time.timeItems
            }
            data.append(curve_data)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, filename):
        curve_space = cls()
        with open(filename, 'r') as f:
            data = json.load(f)
            for curve_data in data:
                categories = curve_data['categories']
                time_items = curve_data['timeItems']
                curve_cat_time = CurveCatTime(categories)
                curve_cat_time.timeItems = time_items
                curve_space.add_curve_cat_time(curve_cat_time)
        return curve_space


if __name__ == "__main__":
    parser = CurveCatTime(["number", "word", "code", "whitespace", "unknown"])
    someText = "testing 123"
    parser.parse(someText)
    parser.print_parsed_text()
