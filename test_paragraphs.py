from main import prepare_paragraphs

assert prepare_paragraphs("   ") == []
assert prepare_paragraphs("Один абзац") == [
    {"number": 1, "text": "Один абзац"}
]
assert prepare_paragraphs("Первый\n\n\n\nВторой") == [
    {"number": 1, "text": "Первый"},
    {"number": 2, "text": "Второй"}
]