from __future__ import annotations

import pytest

from khoji.pipeline.content_generator import (
    Flashcard,
    QuizQuestion,
    generate_flashcards,
    generate_quiz,
    _split_sentences,
    _is_definition,
    _is_fact,
    _definition_to_card,
    _fact_to_card,
)


class TestSplitSentences:
    def test_basic_split(self):
        text = "First long sentence here. Second longer sentence here! Third question sentence here?"
        result = _split_sentences(text)
        assert len(result) >= 3

    def test_short_sentences_filtered(self):
        text = "Hi. " * 20
        result = _split_sentences(text)
        assert all(len(s.strip()) > 15 for s in result)


class TestIsDefinition:
    def test_is_definition_patterns(self):
        assert _is_definition("A function is a block of reusable code.")
        assert _is_definition("Python refers to a programming language.")
        assert _is_definition("CPU - Central Processing Unit")
        assert _is_definition("API: Application Programming Interface")
        assert not _is_definition("The cat sat on the mat.")


class TestIsFact:
    def test_is_fact_with_number(self):
        assert _is_fact("Python has 14 data types.")
        assert not _is_fact("The cat sat on the mat.")

    def test_is_fact_with_qualifier(self):
        assert _is_fact("Python always uses indentation.")

    def test_is_fact_with_number(self):
        assert _is_fact("Python has 14 data types.")

    def test_not_fact(self):
        assert not _is_fact("The weather is nice today.")


class TestDefinitionToCard:
    def test_is_definition_card(self):
        card = _definition_to_card("A function is a block of reusable code.")
        assert card is not None
        assert "What is A function" in card.front
        assert "block of reusable code" in card.back

    def test_dash_definition_card(self):
        card = _definition_to_card("CPU - Central Processing Unit")
        assert card is not None
        assert card.front == "CPU"
        assert "Central Processing Unit" in card.back

    def test_non_definition_returns_none(self):
        card = _definition_to_card("The cat sat on the mat.")
        assert card is None


class TestFactToCard:
    def test_fact_card_created(self):
        card = _fact_to_card("Python has 14 standard data types.")
        assert card is not None
        assert card.back == "(See source document)"

    def test_long_sentence_returns_none(self):
        long = "X" * 301
        assert _fact_to_card(long) is None


class TestGenerateFlashcards:
    def test_generates_cards(self, sample_text):
        cards = generate_flashcards(sample_text, max_cards=10)
        assert len(cards) > 0
        assert all(isinstance(c, Flashcard) for c in cards)

    def test_max_cards_respected(self, sample_text):
        cards = generate_flashcards(sample_text, max_cards=3)
        assert len(cards) <= 3

    def test_empty_text(self):
        assert generate_flashcards("") == []

    def test_short_text(self):
        cards = generate_flashcards("Hello world.", max_cards=5)
        assert isinstance(cards, list)


class TestGenerateQuiz:
    def test_generates_questions(self, sample_text):
        questions = generate_quiz(sample_text, num_questions=5)
        assert len(questions) > 0
        assert all(isinstance(q, QuizQuestion) for q in questions)

    def test_question_structure(self, sample_text):
        questions = generate_quiz(sample_text, num_questions=3)
        for q in questions:
            assert len(q.question) > 0
            assert len(q.options) >= 2
            assert 0 <= q.correct_answer_index < len(q.options)

    def test_empty_text(self):
        assert generate_quiz("") == []


class TestRegressionBug3:
    """BUG-3: content_generator returns dataclasses, db.py expects dicts."""

    def test_vars_conversion_works(self, sample_text):
        cards = generate_flashcards(sample_text, max_cards=3)
        for c in cards:
            d = vars(c)
            assert "front" in d
            assert "back" in d
            assert "card_type" in d

    def test_quiz_vars_conversion(self, sample_text):
        questions = generate_quiz(sample_text, num_questions=3)
        for q in questions:
            d = vars(q)
            assert "question" in d
            assert "options" in d
            assert "correct_answer_index" in d
