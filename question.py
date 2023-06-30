# Format for input:
"""When is it more advantageous to use pointer receivers over value receivers in Go?

    A) When the method needs to modify the receiver value or when the receiver is a large struct.
    - Correct! Using pointer receivers can be more efficient when the receiver is a large struct because it avoids copying the value. Also, if the method needs to modify the receiver value, a pointer receiver is required.

    B) It is always better to use value receivers in Go.
    - Incorrect! This is a misconception. While value receivers can be easier to understand and use, there are situations where pointer receivers are more efficient or necessary, such as when the method needs to modify the receiver value or when the receiver is a large struct.

    C) It is always better to use pointer receivers in Go.
    - Incorrect! This is a misconception. The choice between value receivers and pointer receivers depends on the specific requirements and constraints of the situation. For example, value receivers are typically used when the method does not need to modify the receiver and the receiver is a small struct.
"""

from typing import List
from dataclasses import dataclass

@dataclass
class Question:
    question_text: str
    answer_options: List[str]
    feedback: List[str]
    correct_option: int

    @classmethod
    def from_string(cls, question_block: str) -> 'Question':
        lines = question_block.strip().split("\n")
        question_text = lines[0].strip()
        answer_options = [lines[i].strip()[3:] for i in range(2, len(lines), 3)]
        feedback = [lines[i].strip()[2:] for i in range(3, len(lines), 3)]
        correct_option = next((i for i, x in enumerate(feedback) if x[:7].lower() == "correct"), None)
        return cls(question_text, answer_options, feedback, correct_option)
