"""
critique_engine.py
Refactored modular critique engine
Specialized logic, philosophical, and evidence detectors
Enhanced Socratic feedback and reflection prompts
"""

import re
from typing import List, Dict, Any, Optional
import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback if model is not downloaded
    import subprocess
    subprocess.run(["python3", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class BaseDetector:
    """Base class for all detectors."""
    def detect(self, text: str) -> List[Dict[str, Any]]:
        raise NotImplementedError

class LogicDetector(BaseDetector):
    """Detects logical fallacies and structural issues."""
    
    FALLACIES = [
        {
            "name": "Hasty Generalization",
            "pattern": r"\b(all|every|always|never|none|everyone|everything)\b",
            "severity": 0.8,
            "explanation": "The statement makes a universal claim that may not hold in all cases.",
            "recommendation": "Try to qualify the statement with words like 'many', 'often', or 'some'."
        },
        {
            "name": "Causal Oversimplification",
            "pattern": r"\b(only|just|simply)\b.*\b(cause|leads to|results in|because)\b",
            "severity": 0.7,
            "explanation": "This reasoning attributes a complex outcome to a single cause without sufficient justification.",
            "recommendation": "Consider other contributing factors that might influence the outcome."
        },
        {
            "name": "Circular Reasoning",
            "pattern": r"\b(because|since)\b.*\b(it is|it's)\b.*\b(true|fact|obvious)\b",
            "severity": 0.85,
            "explanation": "The conclusion is used as a premise to support itself.",
            "recommendation": "Provide independent evidence or reasoning for your claim."
        },
        {
            "name": "Appeal to Authority",
            "pattern": r"\b(experts say|scientists prove|studies show)\b",
            "severity": 0.4,
            "explanation": "Relying solely on authority without explaining the underlying reasoning.",
            "recommendation": "Briefly explain the evidence or mechanism behind the expert consensus."
        }
    ]

    def detect(self, text: str) -> List[Dict[str, Any]]:
        issues = []
        for fallacy in self.FALLACIES:
            if re.search(fallacy["pattern"], text, re.IGNORECASE):
                issues.append({
                    "category": "Logic",
                    "issue": fallacy["name"],
                    "severity": fallacy["severity"],
                    "explanation": fallacy["explanation"],
                    "recommendation": fallacy["recommendation"],
                    "affected_text": text
                })
        return issues

class PhilosophyDetector(BaseDetector):
    """Detects philosophical assumptions and ethical frameworks."""
    
    ETHICAL_FRAMEWORKS = [
        {
            "name": "Consequentialist",
            "pattern": r"\b(consequence|result|outcome|maximize|utility|happiness|ends justify)\b",
            "explanation": "Focuses on the outcomes or consequences of actions."
        },
        {
            "name": "Deontological",
            "pattern": r"\b(duty|obligation|rule|rights|principle|absolute|must|should)\b",
            "explanation": "Focuses on duties, rules, and inherent rights regardless of consequences."
        },
        {
            "name": "Virtue Ethics",
            "pattern": r"\b(character|virtue|habit|excellence|wisdom|flourishing|integrity)\b",
            "explanation": "Focuses on the moral character and habits of the individual."
        }
    ]

    def detect(self, text: str) -> List[Dict[str, Any]]:
        issues = []
        doc = nlp(text)
        
        # Implicit assumptions check
        for sent in doc.sents:
            if any(tok.lemma_ in ["assume", "presume", "suppose", "believe"] for tok in sent):
                issues.append({
                    "category": "Philosophy",
                    "issue": "Implicit Assumption",
                    "severity": 0.6,
                    "explanation": "This statement relies on an unexamined belief or assumption.",
                    "recommendation": "State your assumptions clearly and explain why they are held.",
                    "affected_text": sent.text
                })

        # Ethical framework detection
        for framework in self.ETHICAL_FRAMEWORKS:
            if re.search(framework["pattern"], text, re.IGNORECASE):
                issues.append({
                    "category": "Philosophy",
                    "issue": "Ethical Framework Detected",
                    "severity": 0.3,
                    "explanation": f"The reasoning aligns with a {framework['name']} framework: {framework['explanation']}",
                    "recommendation": "Consider how other ethical frameworks might view this issue differently.",
                    "affected_text": text,
                    "framework": framework["name"]
                })
        
        return issues

class EvidenceDetector(BaseDetector):
    """Evaluates the quality and presence of evidence."""
    
    EVIDENCE_MARKERS = [
        {"name": "Numerical", "pattern": r"\b\d+(\.\d+)?%?\b", "score": 0.4},
        {"name": "Examples", "pattern": r"\b(for example|e\.g\.|such as|including)\b", "score": 0.3},
        {"name": "Citations", "pattern": r"\b([A-Z][a-z]+ et al\.|source:|according to)\b", "score": 0.4}
    ]

    def detect(self, text: str) -> Dict[str, Any]:
        details = []
        score = 0.0
        for marker in self.EVIDENCE_MARKERS:
            if re.search(marker["pattern"], text, re.IGNORECASE):
                score += marker["score"]
                details.append(f"Found {marker['name']} evidence.")
        
        return {
            "score": min(score, 1.0),
            "details": details
        }

class CritiqueEngine:
    """Unified engine to coordinate detectors and generate feedback."""
    
    def __init__(self):
        self.logic_detector = LogicDetector()
        self.philosophy_detector = PhilosophyDetector()
        self.evidence_detector = EvidenceDetector()

    def analyze(self, text: str) -> Dict[str, Any]:
        logic_issues = self.logic_detector.detect(text)
        philosophy_issues = self.philosophy_detector.detect(text)
        evidence = self.evidence_detector.detect(text)
        
        all_issues = logic_issues + philosophy_issues
        # Sort issues by severity
        all_issues.sort(key=lambda x: x.get("severity", 0), reverse=True)
        
        # Calculate overall strength
        base_strength = 0.5
        penalties = sum(i["severity"] for i in logic_issues) * 0.2
        bonuses = evidence["score"] * 0.3
        strength = max(min(base_strength - penalties + bonuses, 1.0), 0.1)
        
        # Generate reflection prompts
        prompts = self._generate_prompts(all_issues, evidence)
        
        return {
            "text": text,
            "issues": all_issues,
            "evidence": evidence,
            "strength": round(strength, 2),
            "reflection_prompts": prompts
        }

    def _generate_prompts(self, issues: List[Dict], evidence: Dict) -> List[str]:
        prompts = []
        if not issues:
            prompts.append("Your argument seems well-structured. Can you think of any counter-arguments?")
        
        for issue in issues[:3]: # Top 3 issues
            if issue["issue"] == "Hasty Generalization":
                prompts.append("What are some exceptions to this universal claim?")
            elif issue["issue"] == "Implicit Assumption":
                prompts.append(f"Why do you assume that '{issue['affected_text']}' is true?")
            elif issue["issue"] == "Ethical Framework Detected":
                prompts.append(f"How would a different ethical perspective (e.g., if you are {issue.get('framework')}, then a deontological view) change the conclusion?")
        
        if evidence["score"] < 0.3:
            prompts.append("What specific evidence or examples would strengthen this claim?")
        
        # Default generic prompts if needed
        if len(prompts) < 2:
            prompts.extend([
                "How could you strengthen your argument?",
                "What assumptions are implicit in your reasoning?"
            ])
            
        return list(set(prompts)) # Unique prompts

# Global instance for easy access
engine = CritiqueEngine()

def critique(statement: str, reasoning: Optional[str] = None) -> Dict[str, Any]:
    # Combine statement and reasoning for unified analysis
    # Since the user only submits a statement now, we treat it as both.
    text_to_analyze = statement
    if reasoning and reasoning != statement:
        text_to_analyze = f"{statement} {reasoning}"
    
    return engine.analyze(text_to_analyze)
