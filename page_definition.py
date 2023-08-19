# Example format for input page:
"""Unit_name: Intro to Golang & Basic Concurrency
Page_name: How is Go different from Java?

1. Look at this code snippet. What does it highlight as a unique feature in Go compared to Java?

```
go func() {
    fmt.Println("Hello from a goroutine!")
}()
```

   A) The use of exceptions.
    - Incorrect. This code snippet doesn't show anything related to exceptions but is showing a significant feature of Go.
      
   B) The function passing mechanism.
    - Incorrect. While it does show a function, it isn't highlighting function passing but a significant concurrent feature of Go.
     
   C) The use of goroutines.
    - Correct. The "go" keyword before the function indicates a goroutine, which is a unique feature in Go for handling light weight concurrency.

2. When handling errors in Go and Java, which of the following statements is true?

   A) Go uses the `try-catch` block mechanism.
    - Incorrect. The `try-catch` mechanism is used in Java, not in Go.
  
   B) Go relies on explicit error handling by returning an error as a separate return value.
    - Correct. Go handles error differently than Java, instead of throwing exceptions, it uses explicit error return values.
    
   C) Go encapsulates all errors in an object and throws them.
    - Incorrect. This option is mirroring Java's error handling mechanism, not Go's.
"""

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
            unit = re.search(r'Unit_name: (.*)', f.readline()).group(1).strip()
            page = re.search(r'Page_name: (.*)', f.readline()).group(1).strip()
            question_blocks = re.split(r'\n\d+\.\s', f.read())
            questions = [Question.from_string(question_block) for question_block in question_blocks[1:]]
        return cls(unit, page, questions)
