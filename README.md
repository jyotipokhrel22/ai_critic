# Reasoning Critique Engine

## Overview
A unified engine to analyze and critique reasoning:

- Detects logical issues and fallacies
- Evaluates evidence quality
- Identifies philosophical assumptions and ethical claims
- Produces structured, actionable JSON feedback

---

## Architecture

```mermaid
flowchart TD
    A[Input: Statement + Reasoning] --> B[Parsing Module]
    B --> C[Logical Analysis]
    B --> D[Evidence Assessment]
    B --> E[Philosophical Critique]
    C --> F[Logical Issues]
    D --> G[Evidence Score]
    E --> H[Philosophical Issues]
    F --> I[Aggregate Issues]
    G --> I
    H --> I
    I --> J[Compute Argument Strength]
    J --> K[JSON Feedback]``` 

## Installation

Clone the repository and install dependencies:

git clone https://github.com/yourusername/reasoning-critique-engine.git  
cd reasoning-critique-engine  
pip install -r requirements.txt  
python -m spacy download en_core_web_sm  

## Usage

Import the critique engine and run an analysis:

from app.api.v1 import critique_engine  

statement = "All humans should always act morally."  
reasoning = "I assume everyone knows what is right and wrong, and it is our duty to act ethically."  

feedback = critique_engine.critique(statement, reasoning)  
print(feedback)  

## License

MIT License