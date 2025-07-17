# 🧠 AI Math Teacher Assistant

An AI-powered web application designed to assist primary school math teachers in generating custom math tests and automatically grading student answers submitted via scanned photos or images.

## 📌 Features

### ✅ Test Generation
- Generate math tests based on:
  - Topic (e.g., fractions, geometry)
  - Class level (grades 4–8)
  - Difficulty (easy / medium / hard)
  - Question type: open-ended, multiple-choice, or mixed
- Smart prompt design ensures:
  - If mixed type is selected, max. 1/3 are multiple-choice
  - The last question (if open-ended) is always more complex

### ✅ Answer Key Management
- Teacher defines the answer key:
  - Number of questions
  - Type of each question (open/closed)
  - Correct answer or expected result
  - Maximum number of points per question

### ✅ Automatic Test Grading
- Upload a scanned image of the student's answers (JPG/PNG)
- The app uses GPT-4 Vision to:
  - Read handwritten answers from the image
  - Compare them to the provided answer key
  - Calculate points and generate feedback
- Supports open-ended and multiple-choice grading

### ✅ PWA (Progressive Web App)
- Installable on mobile devices
- Optimized for use directly from a smartphone