import streamlit as st

# Initialize the question list
if 'questions' not in st.session_state:
    st.session_state.questions = []

# Function to add a question
def add_question(question_text, option1, option2, option3, option4, correct_option):
    st.session_state.questions.append({
        "question": question_text,
        "options": [option1, option2, option3, option4],
        "answer": correct_option
    })
    st.success("Question Added Successfully!")

# Streamlit input fields for adding multiple questions
st.title("Quiz Application")

# Display current questions
if len(st.session_state.questions) > 0:
    st.write("### Current Questions:")
    for i, q in enumerate(st.session_state.questions, 1):
        st.write(f"**Q{i}:** {q['question']}")

# Adding multiple questions functionality
question_input = st.text_input("Question:")
option1_input = st.text_input("Option 1:")
option2_input = st.text_input("Option 2:")
option3_input = st.text_input("Option 3:")
option4_input = st.text_input("Option 4:")
correct_option_input = st.number_input("Correct Option (1-4)", min_value=1, max_value=4, value=1)

# Button to add the question
if st.button("Add Question"):
    if question_input.strip() and option1_input.strip() and option2_input.strip() and \
       option3_input.strip() and option4_input.strip():
        add_question(
            question_input,
            option1_input,
            option2_input,
            option3_input,
            option4_input,
            correct_option_input
        )
        # Clear the inputs after adding
        question_input = ''
        option1_input = ''
        option2_input = ''
        option3_input = ''
        option4_input = ''
        correct_option_input = 1
    else:
        st.warning("Please fill in all fields!")

# Once at least one question is added, allow to start the quiz
if len(st.session_state.questions) > 0:
    if st.button("Start Quiz"):
        st.session_state.score = 0  # Initialize score
        st.session_state.current_question = 0  # Track which question is being asked
        st.session_state.quiz_started = True  # Mark quiz as started

# If the quiz has started, show the questions one by one
if 'quiz_started' in st.session_state and st.session_state.quiz_started:
    current_question = st.session_state.current_question

    # Display the current question
    q = st.session_state.questions[current_question]
    st.write(f"**Q{current_question + 1}:** {q['question']}")

    # Radio buttons to select an option
    answer = st.radio(
        "Choose an option:",
        [f"Option 1: {q['options'][0]}", f"Option 2: {q['options'][1]}",
         f"Option 3: {q['options'][2]}", f"Option 4: {q['options'][3]}"],
        key=f"q{current_question}"  # Unique key for each question
    )

    # Next button to go to the next question
    if st.button("Next Question"):
        if answer == f"Option {q['answer']}: {q['options'][q['answer'] - 1]}":
            st.session_state.score += 1
            st.success("Correct!")
        else:
            st.error(f"Wrong! The correct answer was: {q['options'][q['answer'] - 1]}")
        
        # Move to the next question
        if current_question + 1 < len(st.session_state.questions):
            st.session_state.current_question += 1
        else:
            # If it's the last question, show the final score
            st.session_state.quiz_started = False
            st.write(f"Your final score is {st.session_state.score} out of {len(st.session_state.questions)}!")
