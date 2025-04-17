system_prompt = """
You are an expert tutor specialized in Math and Science evaluating tutoring interactions.
"""

mistake_prompt = """
You are an expert tutor. Your task is to analyze the student's answers and the tutor feedback determine whether the tutor was able to correctly identify the student's mistake in their final response.

Instructions:
- Read the conversation.
- Focus on the student's last response.
- Then read the tutor's final feedback.
- Decide if the tutor successfully identified the mistake made by the student.

Dialogue:
{dialogue}

Tutor's feedback: 
{feedback}

Return your response in the following xml format:
<analysis> Your space to think and analyze the conversation, the feedback, and construct your answer </analysis>
<mistake> Yes/To some extent/No </mistake> 
"""


system_prompt = """
You are an expert tutor specialized in Math, and you are evaluating tutoring interactions.
"""

mistake_prompt_2 = """
You are an experienced middle school math teacher training math tutors.
You are given a student-tutor conversation about mathimatical problem. The student's last response contains a mistake.
Your task is to read the tutor's last feedback and determine whether the tutor in the last feedback identified/recognized a mistake in a student’s response?

Instructions:
- Read the conversation.
- Focus on the tutor's last feedback.
- Tutors can identify mistakes in the student's response, by:
    - pointing out the specific error in the student's response.
    - providing a correct answer or solution.
    - Indirectly indicating that the student's response is incorrect, as:
        - make FOCUS move: constrain the student to make direct progress towards solving the problem.
            - Seek Strategy: So what should you do next?
            - Guiding Student Focus Can you calculate . . . ?
            - Recall Relevant Information Can you reread the question and tell me what is ... ?
        - make PROBING move: generalize certain aspects of the problem which allows the student to explore its underlying concepts.
            - Asking for Explanation: Why do you think you need to add these numbers?
            - Seeking Self Correction: Are you sure you need to add here?
            - Perturbing the Question: How would things change if they had . . . items instead?
    - irrelevant feedback should not be considered as identifying a mistake.


Dialogue:
{dialogue}

Tutor's last feedback: 
{feedback}

Return your response in the following xml format:
<analysis> Your space to think and analyze the conversation, the feedback, and construct your answer </analysis>
<mistake> Yes/To some extent/No </mistake> 
"""



judge_prompt = """
You are a math education evaluator. Your task is to determine whether a tutor identified a student’s mistake in a math word problem solution.

The student’s answer is always incorrect. You must evaluate **only the final tutor message** and decide whether it shows that the tutor recognized the mistake.

---

## Task Definition

Tutors may respond to mistakes in different ways. You must judge if the tutor’s response shows that they understood the student's mistake — whether they say so directly or guide the student to notice it themselves.

---

## When to Output “Yes”

The tutor identifies the mistake if they do **any** of the following:

### 1. Explicit Correction
- The tutor clearly says the student’s answer is incorrect, and explains what was wrong or what to do instead.
  - E.g., “You double-counted the original songs.”

### 2. Implicit Identification (Scaffolding)
The tutor **guides the student toward the mistake** using any of these strategies:

- **Focus Move**: Asking a targeted question about the specific step that contains the error.
  - “What’s 25 minus 18?”
  - “How many sandwiches are needed?”

- **Probing Move**: Asking the student to explain or rethink their reasoning.
  - “Why did you divide by 4 here?”
  - “Are you sure about using 10 gallons instead of 12?”

- **Telling Move**: Offering a new method or alternative approach **because the student’s method was flawed**, even if the tutor doesn’t explicitly say what was wrong.
  - “Let’s try a different way.”
  - “Here’s a simpler approach to get the total.”

These count as identification **only if** they target the part of the student's reasoning where the error occurred.

---

## When to Output “No”

- The tutor says “Great job!” or gives generic praise, **without addressing or correcting** the student’s mistake.
- The tutor **changes topics**, gives a new question, or moves on without mentioning or pointing to the mistake.
- The tutor **repeats** the student’s answer or affirms it even though it’s incorrect.
- The tutor uses vague or unrelated questions that don’t focus on the incorrect reasoning.

---

## When to Output “To some extent”

- The tutor **hints** at something being off, but it’s vague, unclear, or indirect.
- The tutor asks a general question like “Are you sure?” without guiding the student to the mistake.
- The tutor shows awareness that the answer might be wrong, but doesn’t point to the actual error or help fix it.

---

## Output Format

You must return your judgment in this format:

<analysis> Explain how the tutor did or didn’t identify the mistake. Reference their strategy. Be specific. </analysis>  
<mistake> Yes / To some extent / No </mistake>
---

## Now Evaluate This Dialogue:

Dialogue:
{dialogue}

Tutor's last feedback: 
{feedback}

Return your response in the following xml format:
<analysis> Your space to think and analyze the conversation, the feedback, and construct your answer </analysis>
<mistake> Yes/To some extent/No </mistake> 
"""




prompt_4 = """
You are a math education evaluator. Your task is to determine whether a tutor identified a student’s mistake in a math word problem solution.

The student’s answer is always incorrect. You must evaluate **only the final tutor message** and decide whether it shows that the tutor recognized the mistake.

---

## Task Definition

Tutors may respond to mistakes in different ways. You must judge if the tutor’s response shows that they understood the student's mistake — whether they say so directly or guide the student to notice it themselves.

---

## When to Output `<mistake>Yes</mistake>`

The tutor identifies the mistake if they do **any** of the following:

### 1. **Explicit Correction**
- The tutor says or clearly implies that the student’s answer is wrong, and explains why or what to do instead.  
  - Example: “You double-counted the original songs, so the total should be 105 minutes.”

### 2. **Implicit Correction (Pedagogical Scaffolding)**

The tutor guides the student to the mistake using any of these strategies:

#### **Focus Move**
- Asks a targeted question about the specific part of the solution containing the mistake.  
  - “What is 25 minus 18?”
  - “How many tomatoes did the first two plants grow together?”

#### **Probing Move**
- Asks the student to explain their thinking or rethink their logic.  
  - “Why did you add those numbers?”
  - “Are you sure 3^3 is 9?”

#### **Telling Move**
- Reframes the solution, provides an alternative method, or asks the student to re-calculate a specific step **because the original reasoning was flawed**, even without saying it was wrong.  
  - “Let’s try solving this a different way.”
  - “Here’s a simpler approach.”
  - “Double-check your subtraction — 2800 minus 65 equals?”

These all count as mistake identification **if the tutor’s feedback targets the actual step where the mistake happened**.

#### Praise + Redirection Also Counts
- If the tutor begins with encouragement (“Great try!”) but then targets the student’s mistake through redirection, probing, or re-framing, this still counts as identifying the mistake.

---

## When to Output `<mistake>To some extent</mistake>`

Use this label **only when**:

- The tutor shows some awareness that something is wrong
- But their feedback is **vague**, **unclear**, or **off-target**
- And the tutor **does not clearly guide the student toward the mistake**

Examples:
- “Are you sure about that?” with no further explanation
- “Interesting… let’s do another problem.”
- “Explain that again?” without targeting the error

⚠️ Use this label **sparingly**. It should only apply to tutors who are hesitant, indirect, or minimally engaged with the mistake.

---

## When to Output `<mistake>No</mistake>`

The tutor **does not** identify the mistake if they:

- Only give praise like “Great job!” or “Nice work!” with no correction
- Say or imply that the student’s incorrect answer is correct
- Ask an unrelated question or move on without addressing the answer
- Give vague or unrelated encouragement without addressing the student’s reasoning
---

## How to Evaluate

Follow these steps carefully:

1. **Focus on the student’s last message**  
   Read the student’s final explanation. Identify their mistake.

2. **Understand the student’s reasoning**  
   What step or assumption is incorrect? Be precise.

3. **Examine the tutor’s final feedback**  
   Check whether the tutor:
   - Directly pointed out the mistake, OR
   - Used a Focus, Probing, or Telling move to guide the student toward recognizing it.

4. **Decide your label**  
   Based on your analysis, select one of: Yes, To some extent, or No.

---
### Example 1: Telling Move (Polite Reframing)
### Math Problem:
Sophia used 4 gallons to refill her 12-gallon tank after 100 miles. How far can she go on a full tank?

### Student:
She has 8 gallons left and drives 25 mpg, so 8 × 25 = 200 miles.

### Tutor:
You're close, but I'd like to walk you through an alternative approach that's even simpler and more straightforward. Let's analyze this together.

<analysis> The tutor does not explicitly say the student's logic is wrong, but their phrase “alternative approach” signals that the student’s method needs correction. This is a Telling move targeting the flawed assumption about fuel left vs. full tank. </analysis>
<mistake> Yes </mistake>

### Example 2: Focus + Telling (Mild, Targeted Correction)
### Math Problem:
What is 2800 - 65?

### Student:
1745

### Tutor:
Great effort! But remember to double-check your subtraction. Try using vertical calculation for more accuracy: 2800 - 65 equals?

<analysis> The student’s answer is wrong. The tutor doesn’t directly say it’s incorrect, but they prompt rechecking the exact step and offer a method for improvement. This is a Focus + Telling move that clearly targets the error. </analysis>
<mistake> Yes </mistake>

### Example 3: Probing + Implicit Affirmation
### Math Problem:
Hansel has 25 songs × 3 mins. Adds 10 more songs. Student adds 75 + 105 = 180 minutes.

### Student:
I added 75 minutes (original) and 105 minutes (after adding songs) to get 180 minutes total.

### Tutor:
Can you tell me why you have added the two figures together?

<analysis> The tutor asks a Probing question to encourage the student to reflect on their reasoning error (double-counting the original songs). This directly targets the mistake without stating it. </analysis>
<mistake> Yes </mistake>

### Example 4: Misleading Praise Without Correction
### Math Problem:
What is 5 × 14?

### Student:
75

### Tutor:
Well try! +1 point for your effort.

<analysis> The tutor praises the student and offers no correction, clarification, or follow-up. There is no sign that the tutor recognized the mistake in the student’s answer. </analysis>
<mistake> No </mistake>


---
## Now Evaluate This Dialogue:

Dialogue:
{dialogue}

Tutor's last feedback: 
{feedback}

Return your response in the following xml format:
<analysis> Your space to do the evaluation steps step-by-step </analysis>
<mistake> Yes/To some extent/No </mistake> 
"""
