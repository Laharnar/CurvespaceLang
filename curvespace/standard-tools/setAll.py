
from collections import OrderedDict
from collections import OrderedDict

class SetAll:
    """Tracks unique words and their sources, allowing you to add words, check if they've been seen, and retrieve their sources."""
    def __init__(self):
        self.seenWords = set()  # set of unique words seen so far
        self.wordSources = OrderedDict()  # ordered dictionary mapping words to their sources

    def addWord(self, word, source):
        """Add a word to the set of seen words and track its source"""
        if word not in self.seenWords:
            self.seenWords.add(word)
            self.wordSources[word] = source

    def hasSeen(self, word):
        """Check if a word has been seen before"""
        return word in self.seenWords

    def addWordsFromSource(self, words, source):
        """Add a list of words from a single source"""
        for word in words:
            self.addWord(word, source)

    def getSource(self, word):
        """Get the source that added a word"""
        return self.wordSources.get(word)

    def allWords(self):
        """Get a list of all words seen so far, in the order they were added"""
        return list(self.wordSources.keys())

    def getAPI(self):
        return [method_name for method_name in dir(self) if callable(getattr(self, method_name))]


class CategoryTracker:
    """Tracks categories, their sources, and data under each category."""

    def __init__(self):
        self.categories = set()  # set of unique categories seen so far
        self.categorySources = OrderedDict()  # ordered dictionary mapping categories to their sources
        self.data = OrderedDict()  # ordered dictionary mapping categories to a list of (source, data)

    def addCategory(self, category, source):
        """Add a category and its source."""
        self.categories.add(category)
        self.categorySources[category] = source
        self.data[category] = []

    def hasCategory(self, category):
        """Check if a category has been seen before."""
        return category in self.categories

    def addData(self, category, source, data):
        """Add data to a category."""
        if category not in self.categories:
            raise ValueError(f"Category {category} has not been added yet.")
        self.data[category].append((source, data))

    def getCategorySource(self, category):
        """Get the source of a category."""
        return self.categorySources.get(category)

    def getData(self, category):
        """Get the data for a category."""
        return self.data.get(category)

    def allCategories(self):
        """Get a list of all categories seen so far."""
        return list(self.categories)

    def getAPI(self):
        return [method_name for method_name in dir(self) if callable(getattr(self, method_name))]