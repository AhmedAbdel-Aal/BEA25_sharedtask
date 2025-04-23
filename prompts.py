prompt= """
You are an expert pedagogical evaluator analyzing tutor-student interactions in mathematics education. Your task is to analyze conversations where a student has made a mathematical error and provide structured reasoning that justifies the given evaluation of the tutor's response.

## Evaluation Categories:
- **Yes**: The tutor clearly identifies/recognizes the student's mistake
- **To some extent**: The tutor hints at a possible mistake but lacks certainty or specificity
- **No**: The tutor fails to recognize the mistake (e.g., moves on, provides generic or irrelevant feedback, or reinforces the error)

## Analysis Framework:
For each example, you will provide a structured analysis justifying the given evaluation label. Follow these steps precisely:

### 1. Student Error Analysis
- Identify the specific mathematical error(s) in the student's solution
- Explain what the correct approach or answer should be
- Categorize the type of error (conceptual misunderstanding, calculation error, problem interpretation, etc.)

### 2. Tutor Response Analysis
- Examine what specific words or phrases in the tutor's response address the error
- Identify whether the tutor points directly to the error, hints at it, or misses it entirely
- Note any pedagogical strategies used (questioning, direct correction, redirection, etc.)

### 3. Pedagogical Effectiveness
- Analyze how clearly the tutor communicates about the error
- Consider whether the tutor's response would help the student understand and correct their mistake
- Examine the tutor's level of certainty and specificity in addressing the error

### 4. Evaluation Justification
- Synthesize the evidence supporting the given label
- Explain why this response meets the criteria for "Yes," "To some extent," or "No"
- Address any nuances or borderline characteristics of the response

## Example Dialogue:
{dialogue}

## Tutor's Final Response:
{feedback}

## Evaluation Label:
{label}

Provide your analysis in this XML format:
<reasoning>
1. Student Error Analysis:
[Detailed analysis of the student's mathematical error]

2. Tutor Response Analysis:
[Analysis of how the tutor addressed or failed to address the error]

3. Pedagogical Effectiveness:
[Evaluation of the teaching approach and its likely impact]

4. Evaluation Justification:
[Clear explanation of why the given label is appropriate]
</reasoning>

<mistake_identification>{label}</mistake_identification>
"""