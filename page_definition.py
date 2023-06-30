import re
from typing import List
from dataclasses import dataclass
from question import Question

@dataclass
class Page_definition:
    unit: str
    page: str
    questions: List[str]

    @classmethod
    def from_file(cls, page_definition_file: str) -> 'Page_definition':
        with open(page_definition_file) as f:
            unit = re.search(r'Unit: (.*)', f.readline()).group(1).strip()
            page = re.search(r'Page_name: (.*)', f.readline()).group(1).strip()
            question_blocks = re.split(r'\n\d+\.\s', f.read())
            questions = [Question.from_string(question_block) for question_block in question_blocks[1:]]
        return cls(unit, page, questions)
