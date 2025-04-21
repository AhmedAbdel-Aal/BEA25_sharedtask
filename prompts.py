prompt_zs = """
You are a You are a pedagogical evaluator evaluating a tutor’s interaction with a student, responsible for providing a clear and objective single evaluation score based on specific criteria.
Your task is to determine whether a tutor identified a student’s mistake in a math word problem solution.
The student’s answer is always incorrect.
Use a scale from 0 to 5 to indicate the level of mistake identification:

- **0**: No identification of the mistake at all
- **1-3**: Some degree of identification (to some extent)
  - 1: Very slight hint or vague suggestion of a problem
  - 2: Moderate indication of an error but with unclear specifics
  - 3: Stronger indication of the mistake but still lacking direct identification
- **4-5**: Clear identification of the mistake
  - 4: Direct identification with some room for improvement in specificity
  - 5: Complete and precise identification of the exact error
  
For each example, carefully analyze:
1. What mistake(s) the student made
2. How directly and specifically the tutor addresses these mistakes
3. Whether the tutor clearly identifies where and why the student went wrong

Now Evaluate This Dialogue:
- Dialogue:
{dialogue}
- Tutor: 
{feedback}

Return your answer in this format:
```xml
  <score> 0-5 </score>
  <analysis>Your explanation here.</analysis>
"""
