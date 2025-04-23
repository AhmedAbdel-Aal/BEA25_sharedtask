from utils import *
from llm import llm_call

def analyze_student_dialogue(example, backend="openai", model="gpt-4o-mini"):
    conv_id = example['conversation_id']
    # Convert dialogue to string format
    dialogue_string = dialogue_to_string(extract_dialogue(example["conversation_history"]))
    
    # Create prompt for the LLM
    prompt = f"""
    You are an expert educational assistant. Analyze the following dialogue between a student and tutor solving a math problem.
    First solve the problem the student was attempting, then identify the student's mistakes.
    
    DIALOGUE:
    {dialogue_string}
    
    Provide your response in the following XML format:
    <correct_solution>
    Detailed step-by-step correct solution to the problem
    </correct_solution>
    
    <student_mistakes>
    Clear identification of the conceptual, logical, and/or procedural mistakes made by the student
    </student_mistakes>
    """
    
    # Call the LLM
    llm_response = llm_call(prompt, backend=backend, model=model)
    
    # Extract the structured response
    analysis = {
        'correct_solution': extract_xml(llm_response, "correct_solution"),
        'student_mistakes': extract_xml(llm_response, "student_mistakes")
    }
    
    # optionally save the analysis to a file
    save_json(f"correct_solutions/{conv_id}.json", analysis)
    
    return analysis