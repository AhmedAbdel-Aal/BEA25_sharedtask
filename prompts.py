nli_prompt = """
You are a natural‑language inference (NLI) judge.
Given a *premise* (the tutor’s last utterance) and a fixed *hypothesis*

  H: "The tutor has identified the student's mistake following a pedagogical approach."

decide whether the premise ENTAILS H, CONTRADICTS H, or is NEUTRAL.

Definitions  
- ENTAILS: The tutor clearly locates the student’s error and responds with a purposeful teaching move—e.g., explicitly states what is wrong, asks a sharply focused question about the faulty step, or directs the student to recompute / rethink that step. In short, the utterance both recognises the mistake and uses a pedagogical tactic to address it.
- NEUTRAL: The tutor gives vague feedback, shows doubt or mild guidance but does **not** pinpoint the mistake.  
- CONTRADICTS: The tutor affirms the student’s (wrong) answer, gives unrelated praise, or otherwise indicates no mistake.

Return one token: **"entailment"**, **"neutral"**, or **"contradiction"**.

-------------------------------
## Evaluation Process

Follow these steps carefully when making your judgment:

1. **Identify the student's actual mistake**  
   Carefully examine the student's final explanation and identify the specific error(s) in their reasoning or calculation.

2. **Analyze the error precisely**  
   Determine exactly what step, assumption, or concept the student misunderstood. Be specific about the nature of the error.

3. **Evaluate the tutor's response in relation to this specific error**  
   Focus on whether the tutor's response addresses the actual mistake you identified, not just any mistake:
   - Does the tutor directly point out the specific error you identified?
   - Does the tutor ask questions or provide guidance specifically targeting this error?
   - Is the tutor's pedagogical move (Focus, Probing, or Telling) directly related to the correct misconception?

4. **Beware of false positives**
   A tutor may appear to identify "a mistake" but target the wrong aspect of the student's work. This does NOT count as correctly identifying the mistake.

5. **Determine your judgment**
   - ENTAILS: Tutor correctly identified the actual mistake (explicitly or pedagogically)
   - NEUTRAL: Tutor gave vague guidance or identified something problematic but missed the core error
   - CONTRADICTS: Tutor failed to recognize any issue or affirmed the incorrect work

Remember, identifying the wrong mistake is equivalent to not identifying the mistake at all.
-------------------------------
### Example: Telling – Polite Reframing
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Sophia is thinking of taking a road trip in her car, and would like to know how far she can drive on a single tank of gas. She has traveled 100 miles since last filling her tank, and she needed to put in 4 gallons of gas to fill it up again. The owner's manual for her car says that her tank holds 12 gallons of gas. How many miles can Sophia drive on a single tank of gas?
- Student: Sophia used 4 out of the 12 gallons of gas in her tank, so there are 12-4 = 8 gallons of gas left in the tank. If Sophia can drive 100 miles on 4 gallons of gas, then she can drive 100/4 = 25 miles per gallon. Therefore, with 8 gallons of gas left in the tank, Sophia can drive 25 x 8 = 200 miles on a single tank of gas.
- Tutor: talk me through your solution
- Student: Hi I started by figuring out how many gallons of gas were left in Sophia's tank. I knew that she had used 4 gallons of gas to fill it up so I subtracted 4 from 12 to get 8 gallons of gas left in the tank. Then I figured out how many miles Sophia could drive on a single gallon of gas. I knew that she had driven 100 miles on 4 gallons of gas so I divided 100 by 4 to get 25 miles per gallon. Finally I multiplied 25 by 8 to get 200 miles which is how many miles Sophia can drive on a single tank of gas."

- focus:
You're close, but I'd like to walk you through an alternative approach that's even simpler and more straightforward. Let's analyze this together.

<analysis>
1. Student’s last message: treats 8 gallons as the tank’s capacity and scales 25 mi/gal by 8 ⇒ 200 mi.  
2. Precise error: the wrong assumption is that only the remaining 8 gallons matter; the range should be based on the full 12‑gallon tank.  
3. Tutor’s feedback: offers “an alternative approach” and invites joint re‑analysis— a classic **Telling** move that implicitly signals the solution path is flawed without revealing the answer.  
4. The tutor clearly recognises a mistake and initiates guidance to correct it. Therefore the premise entails H.
</analysis>
<label>entailment</label>
---
### Example: Telling – Explicit Correction
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Sophia is thinking of taking a road trip in her car, and would like to know how far she can drive on a single tank of gas. She has traveled 100 miles since last filling her tank, and she needed to put in 4 gallons of gas to fill it up again. The owner's manual for her car says that her tank holds 12 gallons of gas. How many miles can Sophia drive on a single tank of gas?
- Student: Sophia used 4 out of the 12 gallons of gas in her tank, so there are 12-4 = 8 gallons of gas left in the tank. If Sophia can drive 100 miles on 4 gallons of gas, then she can drive 100/4 = 25 miles per gallon. Therefore, with 8 gallons of gas left in the tank, Sophia can drive 25 x 8 = 200 miles on a single tank of gas.
- Tutor: talk me through your solution
- Student: Hi I started by figuring out how many gallons of gas were left in Sophia's tank. I knew that she had used 4 gallons of gas to fill it up so I subtracted 4 from 12 to get 8 gallons of gas left in the tank. Then I figured out how many miles Sophia could drive on a single gallon of gas. I knew that she had driven 100 miles on 4 gallons of gas so I divided 100 by 4 to get 25 miles per gallon. Finally I multiplied 25 by 8 to get 200 miles which is how many miles Sophia can drive on a single tank of gas."

- focus:
Your calculations are correct, but your initial assumption is wrong. Sophia's tank capacity is 12 gallons, and she had consumed 4 gallons to travel 100 miles, meaning she had a full tank to begin with, not that she only has 8 gallons left.

<analysis>
1. Student’s final explanation: assumes the tank now holds only 8 gal and bases the range on that smaller amount.
2. Error pinpointed: mis‑identifying “8 gal left” as the effective tank capacity instead of recognising the full 12‑gal tank was merely topped up after using 4 gal.
3. Tutor’s feedback: states plainly “your initial assumption is wrong” and clarifies the correct interpretation of the 4 gal refill → an unmistakable explicit correction of the precise step.
4. The tutor directly identifies the mistake. Therefore the premise entails H.
</analysis>
<label>entailment</label>
---
### Example: Guided Self‑Check / Sanity Test
- History:
- Tutor: Let me know if you need any help with it.
- Student: it is 20
- Tutor: What is 3 multiplied by 4?
- Student: 20",

- focus:
That is incorrect. Please use your calculator to double check your answer.

<analysis>
1. Student’s last message: answers “20” for 3 × 4.  
2. Error: the multiplication 3 × 4 should be 12, not 20.  
3. Tutor’s feedback: states plainly “That is incorrect.” and directs the learner to verify with a calculator—an explicit identification of the mistake plus a concrete self‑check instruction.  
4. The tutor has recognised the exact error and guides the student to correct it. Therefore the premise entails H.
</analysis>
<label>entailment</label>
---
### Example: Praise + Redirection
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: The toothpaste in Anne's family's bathroom contains 105 grams. Anne's dad uses 3 grams at each brushing, her mom uses 2 grams, Anne and her brother use 1 gram each. Each member of the family brushes their teeth three times a day. How many days will it take for the toothpaste to run out?
- Student: Each family member uses a total of 3+2+1+1 = 7 grams of toothpaste per day nFor the whole family, they use 7 x 4 = 28 grams of toothpaste per day. Therefore, the toothpaste will last for 105/28 = 3.75 days. Since they can't use a partial day of toothpaste, the toothpaste will last for 3 days.
- Tutor: Hello, Luca! Can you walk me through your solution?
- Student: Sure! I calculated that each family member uses 7 grams of toothpaste per day. So for the whole family, they use 28 grams of toothpaste per day. Then I divided 105 by 28 to get 3.75 days. Since they can't use a partial day of toothpaste, I concluded that the toothpaste will last for 3 days.
- Tutor: Let's walk through the problem. How many grams does the family use each time they brush their teeth?\
- Student: The family uses 3+2+1+1 = 7 grams of toothpaste each time they brush their teeth.
- Tutor: Good! Now we need to find out how much they use per day. How many grams of toothpaste does the family use each day?
- Student: The family uses 7 x 4 = 28 grams of toothpaste each day."

- focus:
Great effort, but let's take a closer look at how many times they brush their teeth each day - the problem states they brush three times a day, not four.

<analysis>
1. Student’s final explanation: multiplies 7 g per brushing by 4 to get daily usage of 28 g.  
2. Specific mistake: assumes the family brushes **four** times a day; the problem says **three** times.  
3. Tutor’s feedback: begins with praise (“Great effort”) **then redirects** attention to the exact step — “they brush three times a day, not four” — prompting a recalculation. This is a Praise + Redirection move that squarely targets the error.  
4. The tutor clearly recognises and points out the student’s mistake. Therefore the premise entails H.
</analysis>
<label>entailment</label>
---
### Example: Focus move – Targeted Re‑compute
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Tyson decided to make muffaletta sandwiches for the big game.\u00a0\u00a0Each sandwich required 1 pound each of meat and cheese and would serve 4 people.\u00a0\u00a0There would be 20 people in total watching the game.\u00a0\u00a0The meat cost $7.00 per pound and the cheese cost $3.00 per pound.\u00a0\u00a0How much money would he spend on the meat and cheese to make enough sandwiches to serve 20 people?\u00a0\n\u00a0
- Student: To serve 20 people, Tyson needs to make 20/4 = 5 sandwiches.\nEach sandwich requires 1+1 = 2 pounds of meat and cheese.\nFor 5 sandwiches, he needs a total of 2 x 5 = 10 pounds of meat and cheese.\nThe cost of 10 pounds of meat is 10 x $7.00 = $70.\nThe cost of 10 pounds of cheese is 10 x $3.00 = $30.\nThe total cost of meat and cheese is $70 + $30 = $100.
- Tutor: How many pounds of meat are needed for each sandwich?
- Student: Each sandwich requires 1 pound of meat and 1 pound of cheese.
- Tutor: What is the cost of 1 pound of meat?
- Student: The cost of 1 pound of meat is $7.00.",

- focus:
Great, you've correctly identified the cost of the meat, now let's focus on calculating the total cost of meat for all the sandwiches needed.

<analysis>
1. Student’s last reply is correct per pound ($7), yet earlier they scaled to **10 lb of meat** instead of the required **5 lb**; that doubling produced the wrong \$100 total.  
2. Misstep: over‑counting the total pounds of meat (and cheese) when moving from one sandwich to five sandwiches.  
3. Tutor’s feedback: after confirming the per‑pound price, says “**now let’s focus on calculating the total cost of meat for all the sandwiches**”—explicitly directing the student to recompute the batch total. This is a **Focus move – Targeted Re‑compute** that zeroes in on the exact erroneous step.  
4. The tutor has recognised the mistake and guides the student to correct it. Therefore the premise entails H.
</analysis>
<label>entailment</label>
--
### Example: Irrelevant Feedback
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: The toothpaste in Anne's family's bathroom contains 105 grams. Anne's dad uses 3 grams at each brushing, her mom uses 2 grams, Anne and her brother use 1 gram each. Each member of the family brushes their teeth three times a day. How many days will it take for the toothpaste to run out?
- Student: Each family member uses a total of 3+2+1+1 = 7 grams of toothpaste per day nFor the whole family, they use 7 x 4 = 28 grams of toothpaste per day. Therefore, the toothpaste will last for 105/28 = 3.75 days. Since they can't use a partial day of toothpaste, the toothpaste will last for 3 days.
- Tutor: Hello, Luca! Can you walk me through your solution?
- Student: Sure! I calculated that each family member uses 7 grams of toothpaste per day. So for the whole family, they use 28 grams of toothpaste per day. Then I divided 105 by 28 to get 3.75 days. Since they can't use a partial day of toothpaste, I concluded that the toothpaste will last for 3 days.
- Tutor: Let's walk through the problem. How many grams does the family use each time they brush their teeth?\
- Student: The family uses 3+2+1+1 = 7 grams of toothpaste each time they brush their teeth.
- Tutor: Good! Now we need to find out how much they use per day. How many grams of toothpaste does the family use each day?
- Student: The family uses 7 x 4 = 28 grams of toothpaste each day."

- focus:
To solve a quadratic equation, you can use the quadratic formula: (x = frac(-b pm sqrt(b^2 - 4ac))(2a)). Is there anything else you would like to know about solving quadratic equations?

<analysis>
irrelevant feedback to the problem. Therefore the premise contradicts H.
</analysis>
<label>contradiction</label>
---
### Example: Misleading Praise (Affirms Wrong Answer)
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: The length of the straight part of a river is three times shorter than the crooked part. If the river is 80 miles long, how long is the straight part of the river?
- Student: Let x be the length of the crooked part of the river. Then, the length of the straight part of the river is 3x. And we know that the total length of the river is 80 miles. So, we have the equation x + 3x = 80. Simplifying the equation, we get 4x = 80. Solving for x, we get x = 20. Therefore, the length of the straight part of the river is 3x = 3(20) = 60 miles.
- Tutor: guide me through your thinking please?
- Student: I started by letting x be the length of the crooked part of the river. Then I used the given information that the length of the straight part of the river is three times shorter than the crooked part, so I set up the equation x + 3x = 80. I then simplified the equation to 4x = 80 and solved for x to get x = 20. Finally, I used the value of x to calculate the length of the straight part of the river, which is 3x = 3(20) = 60 miles.
- Tutor: ok if you read the question again how long is the crooked part of the river?
- Student: The length of the crooked part of the river is x = 20 miles.

- focus:
You correctly found that the length of the crooked part of the river is 20 miles, which makes sense because it's half of the total length of the river since the straight part is three times shorter.

<analysis>
1. Student’s last message: repeats their earlier reasoning and states the crooked part is 20 mi.  
2. Actual mistake: the phrase “three times shorter” means the straight part is **⅓** of the crooked part, not three times longer; correct setup should be x + (⅓ x) = 80.  
3. Tutor’s feedback: praises the student — “You correctly found … 20 miles” — and even justifies it (“makes sense … half of the total length”), thereby **confirming the erroneous reasoning** instead of correcting or probing it.  
4. The tutor does **not** recognise the mistake; they validate the wrong answer. Therefore the premise contradicts H.
</analysis>
<label>contradiction</label>
---
### Example: Praise with No Correction
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: 7 out of 40 people in a cafeteria are wearing checkered shirts. The rest of the people are wearing vertical stripes and horizontal stripes. The number of people wearing horizontal stripes is 4 times as many as the people wearing checkered shirts. How many people are wearing vertical stripes?
- Student: There are 40-7 = 33 people wearing stripes. Let x be the number of people wearing horizontal stripes. Then, the number of people wearing checkered shirts is 7, and the total number of people is 7+x+(4*7) = 35+x. We know that the total number of people wearing stripes is 33, so:\n33 = x + 4*7\n33 = x + 28\nx = 33-28\nx = 5\nTherefore, there are 7+5 = 12 people wearing vertical stripes.
- Tutor: can you walk me through how you got to your answer?
- Student: Sure. I started by subtracting 7 from 40 to get the total number of people wearing stripes which is 33. Then I let x be the number of people wearing horizontal stripes. I knew that the total number of people wearing stripes was 33 so I set up the equation 33 = x + 4*7. Then I solved for x by subtracting 28 from both sides which gave me x = 5. Finally I added 7 and 5 together to get the total number of people wearing vertical stripes which was 12.
- Tutor: Okay so if 33 people total are wearing stripes and 7 people are wearing checkered shirts and there are 4 times as many people wearing horizontal stripes as there are wearing checkered shirts...
- Student: That means that the number of people wearing horizontal stripes is 4*7 = 28. Then the number of people wearing vertical stripes is 33 - 28 = 12.",

- focus:
That's great, you figured out the key information to solve the problem!

<analysis>
1. Student’s last message: repeats their reasoning and concludes 12 people wear vertical stripes.  
2. Actual mistake: the student’s algebra double‑counts the 7 checkered shirts when totalling stripe wearers; correct setup is 33 = 28 + x ⇒ x = 5 vertical stripes (not 12).  
3. Tutor’s final feedback: offers pure praise (“That’s great, you figured it out…”) without noting any error, asking for a re‑check, or guiding further. No Focus, Probing, or Telling move is present.  
4. The tutor does not identify the student’s mistake. Therefore the premise contradicts H.
</analysis>
<label>contradiction</label>
----

### Example: Probing Question (Vague Hint)
### Dialogue:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Hansel has a created album on Spotify that contains 25 songs and each song is 3 minutes long. If she adds 10 more songs to the album with the same duration, how many minutes will it take her to finish all the songs in the album?
- Student: The total duration of the original 25 songs is 25 x 3 = 75 minutes.\nThe total duration of the album after adding 10 more songs is (25 + 10) x 3 = 105 minutes.\nTherefore, it will take Hansel 75 + 105 = 180 minutes to finish all the songs in the album.
- Tutor: Hey Claire, can you work me through your solution please?
- Student: Sure. I started by calculating the total duration of the original 25 songs, which is 25 x 3 = 75 minutes. Then, I calculated the total duration of the album after adding 10 more songs, which is (25 + 10) x 3 = 105 minutes. Finally, I added the two numbers together to get the total duration of 180 minutes.

- focus:
Can you tell me why you have added the two figures together?

<analysis>
1. Student’s last message: adds 75 min and 105 min, double‑counting the original songs, and claims the album lasts 180 min.  
2. Incorrect step: treating the two totals as disjoint and adding them instead of using only the updated 105 min.  
3. Tutor’s feedback: asks “why you have added the two figures together?”—a probing question that signals something may be wrong but gives no hint about what should be done instead. The guidance is minimal and could leave the student unsure how to correct the error.  
4. The tutor shows partial awareness of a mistake but offers only a vague prompt without directing the student toward the correct reasoning. Therefore the premise is neutral to H.
</analysis>
<label>neutral</label>
---
### Example:
### Dialogue:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Wendy wants to place 20 more than double the number of books in a shelving system with 6 rows and 6 columns. How many books will she need to carry to complete her task?
- Student: There are a total of 6 x 6 = 36 slots in the shelving system.\nLet's call the number of books she needs to carry \"x\".\nShe wants to place 20 more than double the number of books, which can be expressed as 2x + 20.\nAccording to the problem, 2x + 20 = 36.\nSubtracting 20 from both sides, 2x = 16.\nDividing both sides by 2, x = 8.\nTherefore, Wendy needs to carry 8 books to complete her task.
- Tutor: Explain your solution
- Student: To solve this problem, I first determined the total number of slots in the shelving system by multiplying the number of rows and columns, which is 6 x 6 = 36. Then, I expressed the number of books Wendy needs to carry as 2x + 20, since she wants to place 20 more than double the number of books. Since 2x + 20 = 36, I subtracted 20 from both sides to get 2x = 16. Dividing both sides by 2, I got x = 8, which means Wendy needs to carry 8 books to complete her task.
- Tutor: How many books is the capacity
- Student: The capacity of the shelving system is 36 books, since there are 6 rows and 6 columns, each with 6 slots. Therefore, Wendy can place a maximum of 36 books in the shelving system.
- Tutor: Can you double that
- Student: Yes, if Wendy doubles the number of books she places in the shelving system, she can place a maximum of 72 books. This can be expressed as 2(2x + 20), which is equal to 2(36) = 72.",

- focus:
Wendy wants 20 more than that

<analysis>
1. Student’s last statement: says doubling the 36‑book capacity gives 72 and stops there.  
2. Incorrect step: the problem asks for **20 more than** that doubled amount (i.e., 72 + 20), but the student has not added the extra 20 and still thinks in terms of x = 8.  
3. Tutor’s feedback: supplies a new prompt “Wendy wants 20 more than that”, building on the earlier perturbation (“double that”).  This hints the earlier answer is incomplete, yet it does not spell out the final computation or pinpoint how the algebraic set‑up was wrong.  
4. The tutor shows awareness of the mistake and nudges the student with a perturbing cue, but gives no full explanation or explicit correction. Therefore the premise is neutral to H.
</analysis>
<label>neutral</label>
---
### Example: Partial Fix (Corrects One Detail, Misses Deeper Error)
Premise:
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Mike wants to buy a new car. He has chosen a red car for $35000. To be able to pay this price, he needs to loan part of the money from the bank, at a rate of 15%. How much money in total will Mike need to pay for the car, if he has to take $20000 from the bank?
- Student: Mike needs to pay $35000 for the car and he takes $20000 from the bank, so in total he needs to pay $35000 + $20000 = $55000.\nThe bank charges an interest rate of 15%, so Mike needs to pay an additional 15/100 x $20000 = $3000 in interest.\nTherefore, in total Mike needs to pay $55000 + $3000 = $58000 for the car.
- Tutor: Good morning, Cody! Can you tell me how you solved this problem?
- Student: Hi, Tutor! To solve this problem, I first calculated the total cost of the car, which was $35000 + $20000 = $55000. Then I realized that the bank loaned Mike $20000 at a rate of 15%, so I calculated the additional interest he had to pay, which was 15/100 x $20000 = $3000. Finally, I added the interest to the total cost of the car, which was $55000 + $3000 = $58000.
- Tutor: You are very good at calculations! Let's break the problem down a bit. Can you let me know how much interest Mike would need to pay on the amount he borrowed?
- Student: Sure! The amount Mike borrowed was $20000 and the interest rate was 15%, so the interest he needs to pay is 15/100 x $20000 = $3000.

- focus:
That's correct, the interest Mike needs to pay on the amount he borrowed is indeed $3000.

<analysis>
1. Student’s last message: repeats earlier work; interest =\$3 000 and total =\$58 000.  
2. Full error: student double‑counted the car price by adding the \$35 000 purchase price to the \$20 000 loan principal (they should pay \$35 000 + \$3 000 = \$38 000).  
3. Tutor’s feedback: asks for and verifies the interest amount (\$3 000) — a secondary detail the student already had right — **but never addresses the wrongful \$55 000 subtotal**. The core mis‑calculation remains unchallenged.  
4. The tutor shows limited awareness of a potential issue (breaks the problem down, checks a sub‑step) yet fails to identify the main mistake or guide toward the correct total. Therefore the premise is neutral to H.
</analysis>
<label>neutral</label>
----------------------------------
Now judge the new case:

Premise: 
- History: {dialogue}
- focus: {feedback}
<analysis> your analysis here </analysis>
<label>entailment/contradiction/neutral</label>
"""


reverse_nli_prompt = """
You are a natural‑language inference (NLI) judge.
Given a *premise* (the tutor's last utterance) and a fixed *hypothesis*

  H: "The tutor has failed to identify the student's mistake."

decide whether the premise ENTAILS H, CONTRADICTS H, or is NEUTRAL.

Definitions  
- ENTAILS: The tutor clearly does not recognize the student's error—by affirming the incorrect answer, offering praise without correction, giving irrelevant feedback, or moving on without addressing the mistake. The tutor shows no awareness that the student's solution contains an error.
- NEUTRAL: The tutor gives vague feedback, shows some doubt, or offers minimal guidance that suggests awareness of an issue but does **not** clearly acknowledge or address the specific error.  
- CONTRADICTS: The tutor shows clear recognition of the student's mistake through explicit correction, focused questioning about the error, or directed guidance to reconsider the flawed step.

Return one token: **"entailment"**, **"neutral"**, or **"contradiction"**.
-------------------------------
## Evaluation Process

Follow these steps carefully when making your judgment:

1. **Identify the student's actual mistake**  
   Carefully examine the student's final explanation and identify the specific error(s) in their reasoning or calculation.

2. **Analyze the error precisely**  
   Determine exactly what step, assumption, or concept the student misunderstood. Be specific about the nature of the error.

3. **Evaluate the tutor's response in relation to this specific error**  
   Focus on whether the tutor's response addresses the actual mistake you identified, not just any mistake:
   - Does the tutor miss, overlook, or fail to address the specific error you identified?
   - Does the tutor focus on irrelevant aspects while ignoring the actual error?
   - Does the tutor affirm or praise work that contains the specific error you identified?

4. **Beware of false negatives**
   A tutor who identifies a different mistake but misses the actual core error has still failed to identify the student's mistake.

5. **Determine your judgment**
   - ENTAILS: Tutor failed to identify the actual mistake (missed it, affirmed it, or focused elsewhere)
   - NEUTRAL: Tutor gave vague guidance that partially approaches but doesn't clearly address the core error
   - CONTRADICTS: Tutor correctly identified the specific error (explicitly or pedagogically)

Remember, identifying the wrong mistake is equivalent to not identifying the mistake at all.
-------------------------------
### Example: Irrelevant Feedback
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: The toothpaste in Anne's family's bathroom contains 105 grams. Anne's dad uses 3 grams at each brushing, her mom uses 2 grams, Anne and her brother use 1 gram each. Each member of the family brushes their teeth three times a day. How many days will it take for the toothpaste to run out?
- Student: Each family member uses a total of 3+2+1+1 = 7 grams of toothpaste per day nFor the whole family, they use 7 x 4 = 28 grams of toothpaste per day. Therefore, the toothpaste will last for 105/28 = 3.75 days. Since they can't use a partial day of toothpaste, the toothpaste will last for 3 days.
- Student: Sure! I calculated that each family member uses 7 grams of toothpaste per day. So for the whole family, they use 28 grams of toothpaste per day. Then I divided 105 by 28 to get 3.75 days. Since they can't use a partial day of toothpaste, I concluded that the toothpaste will last for 3 days.
- Student: The family uses 3+2+1+1 = 7 grams of toothpaste each time they brush their teeth.
- Student: The family uses 7 x 4 = 28 grams of toothpaste each day.

- focus:
To solve a quadratic equation, you can use the quadratic formula: (x = frac(-b pm sqrt(b^2 - 4ac))(2a)). Is there anything else you would like to know about solving quadratic equations?

<analysis>
1. Student's last message: states they use 7 × 4 = 28 grams of toothpaste per day, making a calculation error (should be 7 × 3 = 21 grams since they brush three times daily).
2. The tutor's response is completely irrelevant, discussing quadratic equations instead of addressing the toothpaste problem or the calculation error.
3. The tutor shows no recognition whatsoever of the student's mistake and provides feedback that has nothing to do with the problem at hand.
4. Therefore, the premise clearly entails H - the tutor has failed to identify the student's mistake.
</analysis>
<label>entailment</label>
---
### Example: Misleading Praise (Affirms Wrong Answer)
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: The length of the straight part of a river is three times shorter than the crooked part. If the river is 80 miles long, how long is the straight part of the river?
- Student: Let x be the length of the crooked part of the river. Then, the length of the straight part of the river is 3x. And we know that the total length of the river is 80 miles. So, we have the equation x + 3x = 80. Simplifying the equation, we get 4x = 80. Solving for x, we get x = 20. Therefore, the length of the straight part of the river is 3x = 3(20) = 60 miles.
- Student: I started by letting x be the length of the crooked part of the river. Then I used the given information that the length of the straight part of the river is three times shorter than the crooked part, so I set up the equation x + 3x = 80. I then simplified the equation to 4x = 80 and solved for x to get x = 20. Finally, I used the value of x to calculate the length of the straight part of the river, which is 3x = 3(20) = 60 miles.
- Student: The length of the crooked part of the river is x = 20 miles.

- focus:
You correctly found that the length of the crooked part of the river is 20 miles, which makes sense because it's half of the total length of the river since the straight part is three times shorter.

<analysis>
1. Student's last message: reiterates their claim that the crooked part is 20 miles.
2. Student's mistake: misinterprets "three times shorter" as meaning the straight part is three times the crooked part (3x), when it actually means the straight part is 1/3 of the crooked part (x/3).
3. Tutor's response: explicitly affirms the incorrect answer ("you correctly found...") and even provides further justification for the wrong reasoning.
4. The tutor clearly does not recognize the conceptual error in the student's interpretation of "three times shorter" and actively reinforces the misconception.
5. Therefore, the premise entails H - the tutor has failed to identify the student's mistake.
</analysis>
<label>entailment</label>
---
### Example: Praise with No Correction
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: 7 out of 40 people in a cafeteria are wearing checkered shirts. The rest of the people are wearing vertical stripes and horizontal stripes. The number of people wearing horizontal stripes is 4 times as many as the people wearing checkered shirts. How many people are wearing vertical stripes?
- Student: There are 40-7 = 33 people wearing stripes. Let x be the number of people wearing horizontal stripes. Then, the number of people wearing checkered shirts is 7, and the total number of people is 7+x+(4*7) = 35+x. We know that the total number of people wearing stripes is 33, so:\n33 = x + 4*7\n33 = x + 28\nx = 33-28\nx = 5\nTherefore, there are 7+5 = 12 people wearing vertical stripes.
- Student: Sure. I started by subtracting 7 from 40 to get the total number of people wearing stripes which is 33. Then I let x be the number of people wearing horizontal stripes. I knew that the total number of people wearing stripes was 33 so I set up the equation 33 = x + 4*7. Then I solved for x by subtracting 28 from both sides which gave me x = 5. Finally I added 7 and 5 together to get the total number of people wearing vertical stripes which was 12.
- Student: That means that the number of people wearing horizontal stripes is 4*7 = 28. Then the number of people wearing vertical stripes is 33 - 28 = 12.

- focus:
That's great, you figured out the key information to solve the problem!

<analysis>
1. Student's last message: concludes there are 12 people wearing vertical stripes.
2. Student's error: incorrectly adds 7 (checkered shirts) to 5 (calculated value for x) to get 12 vertical stripes, when vertical stripes should just be 5 people (the 7 people are already accounted for as wearing checkered shirts, not stripes).
3. Tutor's response: offers only positive reinforcement ("That's great") without any indication that the student's answer or approach contains an error.
4. The tutor provides no correction, questioning, or guidance that would suggest awareness of the student's mistake.
5. Therefore, the premise entails H - the tutor has failed to identify the student's mistake.
</analysis>
<label>entailment</label>
---
### Example: Probing Question (Vague Hint)
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Hansel has a created album on Spotify that contains 25 songs and each song is 3 minutes long. If she adds 10 more songs to the album with the same duration, how many minutes will it take her to finish all the songs in the album?
- Student: The total duration of the original 25 songs is 25 x 3 = 75 minutes.\nThe total duration of the album after adding 10 more songs is (25 + 10) x 3 = 105 minutes.\nTherefore, it will take Hansel 75 + 105 = 180 minutes to finish all the songs in the album.
- Student: Sure. I started by calculating the total duration of the original 25 songs, which is 25 x 3 = 75 minutes. Then, I calculated the total duration of the album after adding 10 more songs, which is (25 + 10) x 3 = 105 minutes. Finally, I added the two numbers together to get the total duration of 180 minutes.

- focus:
Can you tell me why you have added the two figures together?

<analysis>
1. Student's last message: explains they added 75 minutes (original songs) and 105 minutes (after adding new songs) to get 180 minutes total.
2. Student's error: double-counts the original 25 songs by adding the two durations instead of using only the final 105 minutes.
3. Tutor's response: asks why the student added the two figures together, showing some awareness that this step is problematic.
4. While the tutor doesn't explicitly identify the error or provide direct correction, the question suggests recognition that something is wrong with the addition step.
5. The tutor's response is neither a clear identification of the mistake nor a complete failure to notice it - it shows partial awareness through questioning.
6. Therefore, the premise is neutral to H - the tutor shows some awareness but doesn't clearly succeed or fail at identifying the specific error.
</analysis>
<label>neutral</label>
---
### Example: Minimal Redirect
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Wendy wants to place 20 more than double the number of books in a shelving system with 6 rows and 6 columns. How many books will she need to carry to complete her task?
- Student: There are a total of 6 x 6 = 36 slots in the shelving system.\nLet's call the number of books she needs to carry \"x\".\nShe wants to place 20 more than double the number of books, which can be expressed as 2x + 20.\nAccording to the problem, 2x + 20 = 36.\nSubtracting 20 from both sides, 2x = 16.\nDividing both sides by 2, x = 8.\nTherefore, Wendy needs to carry 8 books to complete her task.
- Student: To solve this problem, I first determined the total number of slots in the shelving system by multiplying the number of rows and columns, which is 6 x 6 = 36. Then, I expressed the number of books Wendy needs to carry as 2x + 20, since she wants to place 20 more than double the number of books. Since 2x + 20 = 36, I subtracted 20 from both sides to get 2x = 16. Dividing both sides by 2, I got x = 8, which means Wendy needs to carry 8 books to complete her task.
- Student: The capacity of the shelving system is 36 books, since there are 6 rows and 6 columns, each with 6 slots. Therefore, Wendy can place a maximum of 36 books in the shelving system.
- Student: Yes, if Wendy doubles the number of books she places in the shelving system, she can place a maximum of 72 books. This can be expressed as 2(2x + 20), which is equal to 2(36) = 72.

- focus:
Wendy wants 20 more than that

<analysis>
1. Student's last message: calculates that doubling the shelf capacity gives 72 books.
2. Student's error: misinterprets the problem, which asks for "20 more than double the number of books" - they should add 20 to get 92 books (72 + 20).
3. Tutor's response: provides a brief hint "Wendy wants 20 more than that" which indicates some awareness that the student's calculation is incomplete.
4. The tutor doesn't fully explain the error or provide explicit correction, but does gesture toward the missing step.
5. The tutor's response shows partial recognition of the issue but lacks specificity or clear guidance on the precise nature of the mistake.
6. Therefore, the premise is neutral to H - the tutor neither completely fails to identify the mistake nor fully addresses it.
</analysis>
<label>neutral</label>
---
### Example: Partial Fix (Corrects One Detail, Misses Deeper Error)
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Mike wants to buy a new car. He has chosen a red car for $35000. To be able to pay this price, he needs to loan part of the money from the bank, at a rate of 15%. How much money in total will Mike need to pay for the car, if he has to take $20000 from the bank?
- Student: Mike needs to pay $35000 for the car and he takes $20000 from the bank, so in total he needs to pay $35000 + $20000 = $55000.\nThe bank charges an interest rate of 15%, so Mike needs to pay an additional 15/100 x $20000 = $3000 in interest.\nTherefore, in total Mike needs to pay $55000 + $3000 = $58000 for the car.
- Student: Hi, Tutor! To solve this problem, I first calculated the total cost of the car, which was $35000 + $20000 = $55000. Then I realized that the bank loaned Mike $20000 at a rate of 15%, so I calculated the additional interest he had to pay, which was 15/100 x $20000 = $3000. Finally, I added the interest to the total cost of the car, which was $55000 + $3000 = $58000.
- Student: Sure! The amount Mike borrowed was $20000 and the interest rate was 15%, so the interest he needs to pay is 15/100 x $20000 = $3000.

- focus:
That's correct, the interest Mike needs to pay on the amount he borrowed is indeed $3000.

<analysis>
1. Student's last message: correctly calculates the interest as $3000 but has previously shown a fundamental misunderstanding by adding the loan principal to the car price for a total of $55000 + $3000 = $58000.
2. Student's major error: double-counting the $20000 loan principal (the correct total should be $35000 + $3000 = $38000).
3. Tutor's response: affirms only the interest calculation ($3000) which was already correct, completely ignoring the major conceptual error of double-counting the loan amount.
4. The tutor focuses on a secondary detail that was already correct while failing to recognize or address the primary misconception in the student's approach.
5. The tutor shows partial engagement with the student's work but misses the significant error that led to an incorrect final answer.
6. Therefore, the premise is neutral to H - the tutor neither completely fails to identify mistakes (they do verify one calculation) nor successfully identifies the critical error.
</analysis>
<label>neutral</label>
---
### Example: Telling – Polite Reframing
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Sophia is thinking of taking a road trip in her car, and would like to know how far she can drive on a single tank of gas. She has traveled 100 miles since last filling her tank, and she needed to put in 4 gallons of gas to fill it up again. The owner's manual for her car says that her tank holds 12 gallons of gas. How many miles can Sophia drive on a single tank of gas?
- Student: Sophia used 4 out of the 12 gallons of gas in her tank, so there are 12-4 = 8 gallons of gas left in the tank. If Sophia can drive 100 miles on 4 gallons of gas, then she can drive 100/4 = 25 miles per gallon. Therefore, with 8 gallons of gas left in the tank, Sophia can drive 25 x 8 = 200 miles on a single tank of gas.
- Student: Hi I started by figuring out how many gallons of gas were left in Sophia's tank. I knew that she had used 4 gallons of gas to fill it up so I subtracted 4 from 12 to get 8 gallons of gas left in the tank. Then I figured out how many miles Sophia could drive on a single gallon of gas. I knew that she had driven 100 miles on 4 gallons of gas so I divided 100 by 4 to get 25 miles per gallon. Finally I multiplied 25 by 8 to get 200 miles which is how many miles Sophia can drive on a single tank of gas.

- focus:
You're close, but I'd like to walk you through an alternative approach that's even simpler and more straightforward. Let's analyze this together.

<analysis>
1. Student's last message: calculates Sophia can drive 200 miles on the remaining 8 gallons of gas.
2. Student's error: misinterprets the question asking about "a single tank of gas" - they should calculate 25 miles/gallon × 12 gallons = 300 miles for a full tank.
3. Tutor's response: indicates the student is "close" but proposes an "alternative approach," implicitly signaling that the current solution is not quite right.
4. The tutor uses a pedagogical technique to redirect the student without bluntly stating they're wrong.
5. The response clearly contradicts the hypothesis that the tutor failed to identify the mistake - the tutor recognized the error and is taking steps to guide the student to a correct understanding.
6. Therefore, the premise contradicts H - the tutor has identified the student's mistake and is using an appropriate pedagogical approach to address it.
</analysis>
<label>contradiction</label>
---
### Example: Telling – Explicit Correction
- History:
- Tutor: Hi, could you please provide a step-by-step solution for the question below? The question is: Sophia is thinking of taking a road trip in her car, and would like to know how far she can drive on a single tank of gas. She has traveled 100 miles since last filling her tank, and she needed to put in 4 gallons of gas to fill it up again. The owner's manual for her car says that her tank holds 12 gallons of gas. How many miles can Sophia drive on a single tank of gas?
- Student: Sophia used 4 out of the 12 gallons of gas in her tank, so there are 12-4 = 8 gallons of gas left in the tank. If Sophia can drive 100 miles on 4 gallons of gas, then she can drive 100/4 = 25 miles per gallon. Therefore, with 8 gallons of gas left in the tank, Sophia can drive 25 x 8 = 200 miles on a single tank of gas.
- Student: Hi I started by figuring out how many gallons of gas were left in Sophia's tank. I knew that she had used 4 gallons of gas to fill it up so I subtracted 4 from 12 to get 8 gallons of gas left in the tank. Then I figured out how many miles Sophia could drive on a single gallon of gas. I knew that she had driven 100 miles on 4 gallons of gas so I divided 100 by 4 to get 25 miles per gallon. Finally I multiplied 25 by 8 to get 200 miles which is how many miles Sophia can drive on a single tank of gas.

- focus:
Your calculations are correct, but your initial assumption is wrong. Sophia's tank capacity is 12 gallons, and she had consumed 4 gallons to travel 100 miles, meaning she had a full tank to begin with, not that she only has 8 gallons left.

<analysis>
1. Student's last message: calculates Sophia can drive 200 miles based on the 8 gallons left in the tank.
2. Student's error: misinterprets the problem context, thinking that 12-4=8 gallons are left rather than understanding that the question asks about a full tank's capacity.
3. Tutor's response: directly states "your initial assumption is wrong" and explicitly corrects the misunderstanding about tank capacity and the problem context.
4. The tutor clearly identifies the specific conceptual error and provides the correct interpretation.
5. This response strongly contradicts the hypothesis that the tutor failed to identify the mistake - the tutor both recognizes and explicitly corrects it.
6. Therefore, the premise contradicts H - the tutor has successfully identified the student's mistake.
</analysis>
<label>contradiction</label>

-------------------------------
Now judge the new case:

Premise: 
- History: {dialogue}
- focus: {feedback}
<analysis> your analysis here </analysis>
<label>entailment/contradiction/neutral</label>
"""