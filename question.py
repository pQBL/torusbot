# Example format for input:
"""Consider the following struct in Go:

```go
type Student struct {
    name   string
    age    int
    grades []int
}
```

Which of the following is the correct way to instantiate this struct?

    A) `s := Student("John", 20, {90, 80, 85})`
    - Incorrect. In Go, a struct is instantiated using curly braces `{}` with field-value pairs. Also, slice values need to be specified with the `[]int` keyword.

    B) `s := Student{name: "John", age: 20, grades: []int{90, 80, 85}}`
    - Correct. This is the correct way to instantiate a struct in Go, using the field names followed by colon `:` and their corresponding values inside curly braces `{}`.

    C) `s := Student{"John", 20, []int{90, 80, 85}}`
    - Incorrect. Though this method of instantiation is technically correct, it is not recommended for structs with more than a few fields or if fields are added/removed over time, as it relies on the order of the fields.
"""

from typing import List
from dataclasses import dataclass
import re


@dataclass
class Question:
    question_text: str
    answer_options: List[str]
    feedback: List[str]
    correct_option: int

    @classmethod
    def from_string(cls, question_block: str) -> 'Question':
        question_text = re.search(r'(.+?)\s+A\)',
                                  question_block, re.DOTALL).group(1).strip()
        # Only takes the first 3 answer options
        answer_options = re.findall(r'[A-Z]\)\s+(.+)', question_block)[:3]
        feedback = re.findall(r'\n\s*-\s+(.*)', question_block)
        correct_option = next((i for i, text in enumerate(
            feedback) if text[:7].lower() == "correct"), None)

        return cls(question_text, answer_options, feedback, correct_option)
