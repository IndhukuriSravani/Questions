# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 15:46:01 2025

@author: ASUS
"""
import streamlit as st
import docx2txt
import PyPDF2
import wikipedia
from googlesearch import search
import re

# Function to extract text from resume
def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif uploaded_file.name.endswith('.docx'):
        return docx2txt.process(uploaded_file)
    else:
        return "Unsupported file format"

# Function to fetch answer from Wikipedia or Google
def fetch_answer_from_web(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except:
        try:
            result = next(search(query, num=1, stop=1, pause=2))
            return f"Answer might be found here: {result}"
        except:
            return "No relevant information found."

# Function to generate interview questions and answers
def generate_questions(resume_text, job_description):
    combined_text = resume_text + " " + job_description

    # Simple keyword extraction
    keywords = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', combined_text)
    keywords = list(set([k for k in keywords if len(k.split()) < 4]))[:10]

    qa_pairs = []
    for keyword in keywords:
        question = f"Can you explain your experience with {keyword}?"
        answer = fetch_answer_from_web(f"{keyword} in software development")
        qa_pairs.append((question, answer))
    return qa_pairs

# Streamlit UI
st.title("AI Interview Question Generator for Experienced Candidates")

resume_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste the Job Description here")

if st.button("Generate Interview Questions"):
    if resume_file is not None and job_description.strip() != "":
        with st.spinner("Processing..."):
            resume_text = extract_text_from_file(resume_file)
            qa_pairs = generate_questions(resume_text, job_description)

        st.success("Here are your top 10 interview questions and suggested answers:")
        for i, (q, a) in enumerate(qa_pairs, 1):
            st.markdown(f"**Q{i}: {q}**")
            st.markdown(f"**A{i}:** {a}")
            st.markdown("---")
    else:
        st.warning("Please upload a resume and provide the job description.")

