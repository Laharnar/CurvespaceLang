class Token:
    def __init__(self, value, ambiguity=0, uncertainty=0):
        self.value = value
        self.ambiguity = ambiguity
        self.uncertainty = uncertainty

class Sentence:
    def __init__(self, tokens, operators, context=None):
        self.tokens = tokens
        self.operators = operators
        self.context = context

class Interpreter:
    def __init__(self):
        self.token_dict = {}

    def parse_sentence(self, sentence_str):
        tokens = [Token(word) for word in sentence_str.split()]
        operators = []
        for i, token in enumerate(tokens):
            if token.value in ['~', '≈', '?', '→', '∇']:
                operators.append((token.value, i))
        sentence_obj = Sentence(tokens, operators)
        return sentence_obj

    def apply_implicit_operators(self, sentence):
        for op, idx in sentence.operators:
            if op == '~':
                # implies
                sentence.tokens[idx-1].ambiguity += 1
                sentence.tokens[idx+1].ambiguity += 1
            elif op == '≈':
                # approximates
                sentence.tokens[idx-1].uncertainty += 1
                sentence.tokens[idx+1].uncertainty += 1
            elif op == '?':
                # is_ambiguous
                sentence.tokens[idx-1].ambiguity += 1
                sentence.tokens[idx+1].ambiguity += 1
            elif op == '→':
                # entails
                sentence.tokens[idx-1].ambiguity += 1
                sentence.tokens[idx+1].ambiguity += 1
            elif op == '∇':
                # tone
                sentence.tokens[idx-1].uncertainty += 1
                sentence.tokens[idx+1].uncertainty += 1

    def interpret_sentence(self, sentence_str):
        sentence = self.parse_sentence(sentence_str)
        self.apply_implicit_operators(sentence)
        return sentence

    def run(self, sentences):
        for sentence in sentences:
            print(f" Sentence: {sentence}")
            answer = self.interpret_sentence(sentence)
            print()

interpreter = Interpreter()

# Test the interpreter
sentences = [
    "happy ~ sunny",
    "big ≈ large",
    "? maybe",
    "john → happy ≈ (speaker_intent: uncertainty)",
    "weather → nice ≈ (modality: possibility)",
    "love → you ∇ (tone: hesitation)",
    "policy → confusing ≈ (speaker_intent: uncertainty, tone: frustration)",
    "do → ? ≈ (modality: uncertainty, tone: indecision)"
]

#interpreter.run(sentences)

import unittest

class TestAmbiSpeakInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_happy_path(self):
        sentence_str = "happy ~ sunny"
        sentence = self.interpreter.interpret_sentence(sentence_str)
        self.assertEqual(sentence.tokens[0].ambiguity, 1)
        self.assertEqual(sentence.tokens[2].ambiguity, 1)

    def test_approximation(self):
        sentence_str = "big ≈ large"
        sentence = self.interpreter.interpret_sentence(sentence_str)
        self.assertEqual(sentence.tokens[0].uncertainty, 1)
        self.assertEqual(sentence.tokens[2].uncertainty, 1)

    def test_ambiguity(self):
        sentence_str = "? maybe"
        sentence = self.interpreter.interpret_sentence(sentence_str)
        self.assertEqual(sentence.tokens[0].ambiguity, 1)

    def test_entailment(self):
        sentence_str = "john → happy ≈ (speaker_intent: uncertainty)"
        sentence = self.interpreter.interpret_sentence(sentence_str)
        self.assertEqual(sentence.tokens[0].ambiguity, 1)
        self.assertEqual(sentence.tokens[2].ambiguity, 1)
        self.assertEqual(sentence.tokens[2].uncertainty, 1)

    def test_tone(self):
        sentence_str = "love → you ∇ (tone: hesitation)"
        sentence = self.interpreter.interpret_sentence(sentence_str)
        self.assertEqual(sentence.tokens[0].uncertainty, 0)
        self.assertEqual(sentence.tokens[2].uncertainty, 1)

    def test_multiple_operators(self):
        sentence_str = "policy → confusing ≈ (speaker_intent: uncertainty, tone: frustration)"
        sentence = self.interpreter.interpret_sentence(sentence_str)
        self.assertEqual(sentence.tokens[0].ambiguity, 1)
        self.assertEqual(sentence.tokens[2].ambiguity, 1)
        self.assertEqual(sentence.tokens[2].uncertainty, 1)

    def test_sentence_list(self):
        sentences = [
            "happy ~ sunny",
            "big ≈ large",
            "? maybe",
            "john → happy ≈ (speaker_intent: uncertainty)",
            "weather → nice ≈ (modality: possibility)",
            "love → you ∇ (tone: hesitation)",
            "policy → confusing ≈ (speaker_intent: uncertainty, tone: frustration)",
            "do → ? ≈ (modality: uncertainty, tone: indecision)"
        ]
        for sentence_str in sentences:
            sentence = self.interpreter.interpret_sentence(sentence_str)
            # No assertions, just checking that the interpreter runs without errors

#if __name__ == '__main__':
    #unittest.main()
