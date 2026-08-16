import os
import joblib
from typing import List, Optional
from pathlib import Path

from app.domain.entities import Email, ClassificationResult, Category
from app.domain.ports import ClassifierPort
from app.infrastructure.monitoring.metrics import CLASSIFICATIONS, CLASSIFICATION_LATENCY, MODEL_LOAD_FAILURES
import time


class MLClassifier(ClassifierPort):
    """
    Machine Learning classifier using pre-trained scikit-learn model.
    Uses the phishing detection model trained on email data.
    """
    
    def __init__(self, model_path: str = None, vectorizer_path: str = None):
        """
        Initialize the ML classifier with trained model and vectorizer.
        
        Args:
            model_path: Path to the trained model .pkl file
            vectorizer_path: Path to the TF-IDF vectorizer .pkl file
        """
        # Default paths relative to backend root
        backend_root = Path(__file__).parent.parent.parent.parent
        self.model_path = model_path or os.path.join(backend_root, "models", "best_phishing_model.pkl")
        self.vectorizer_path = vectorizer_path or os.path.join(backend_root, "models", "tfidf_vectorizer.pkl")
        
        # Load model and vectorizer
        try:
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            print(f"✓ ML Model loaded successfully from {self.model_path}")
        except Exception as e:
            MODEL_LOAD_FAILURES.inc()
            print(f"✗ Failed to load ML model: {e}")
            raise RuntimeError(f"Could not load ML classifier: {e}")
    
    def classify(
        self,
        email: Email,
        tokens: List[str],
        mood: Optional[str] = None,
        priority: Optional[list[str]] = None
    ) -> ClassificationResult:
        """
        Classify email using the trained ML model.
        
        Args:
            email: Email object with subject and body
            tokens: Preprocessed tokens (not used directly by this classifier)
            mood: Optional mood for reply generation
            priority: Optional priority keywords (not used by this classifier)
            
        Returns:
            ClassificationResult with category, reason, and suggested reply
        """
        started = time.perf_counter()
        try:
            # Combine subject and body for classification
            email_text = f"{email.subject or ''} {email.body or ''}".strip().lower()
            
            if not email_text:
                return ClassificationResult(
                    category=Category.UNPRODUCTIVE,
                    reason="Empty email content",
                    suggested_reply="",
                    used_model="ml_classifier",
                    extra={"confidence": 0.0, "ml_prediction": "unknown"}
                )
            
            # Transform text using TF-IDF vectorizer
            text_vectorized = self.vectorizer.transform([email_text])
            
            # Get prediction
            prediction = self.model.predict(text_vectorized)[0]
            
            # Get confidence score if available
            confidence = 0.0
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(text_vectorized)[0]
                confidence = float(max(proba))
            elif hasattr(self.model, 'decision_function'):
                # For SVM
                decision = self.model.decision_function(text_vectorized)[0]
                confidence = float(abs(decision))
            
            # Map prediction to category
            # Assuming 1 = phishing/unproductive, 0 = ham/productive
            if prediction == 1:
                category = Category.UNPRODUCTIVE
                reason = f"ML model detected potential phishing/spam content (confidence: {confidence:.2f})"
                suggested_reply = ""
            else:
                category = Category.PRODUCTIVE
                reason = f"ML model classified as legitimate email (confidence: {confidence:.2f})"
                # Generate simple reply based on mood
                suggested_reply = self._generate_reply(email, mood)
            
            result = ClassificationResult(
                category=category,
                reason=reason,
                suggested_reply=suggested_reply,
                used_model="ml_classifier",
                extra={
                    "confidence": confidence,
                    "ml_prediction": int(prediction),
                    "model_type": type(self.model).__name__
                }
            )
            CLASSIFICATIONS.labels(category.value, "tfidf").inc()
            return result
            
        except Exception as e:
            # Fallback to unproductive if classification fails
            return ClassificationResult(
                category=Category.UNPRODUCTIVE,
                reason=f"ML classification error: {str(e)}",
                suggested_reply="",
                used_model="ml_classifier_error",
                extra={"error": str(e)}
            )
        finally:
            CLASSIFICATION_LATENCY.observe(time.perf_counter() - started)
    
    def _generate_reply(self, email: Email, mood: Optional[str] = None) -> str:
        """
        Generate a simple reply template based on email content and mood.
        
        Args:
            email: Email object
            mood: Desired tone (formal, casual, friendly, etc.)
            
        Returns:
            Suggested reply text
        """
        sender = email.sender or "there"
        subject = email.subject or "your message"
        
        # Simple template-based replies
        if mood == "formal":
            return f"Dear {sender},\n\nThank you for your email regarding '{subject}'. I will review this and get back to you shortly.\n\nBest regards"
        elif mood == "casual":
            return f"Hi {sender},\n\nThanks for reaching out about '{subject}'. I'll take a look and get back to you soon!\n\nCheers"
        elif mood == "friendly":
            return f"Hey {sender}!\n\nThanks for your message about '{subject}'. I appreciate you getting in touch. I'll review this and respond soon.\n\nWarm regards"
        else:
            # Default neutral tone
            return f"Hello {sender},\n\nThank you for your email about '{subject}'. I have received your message and will respond accordingly.\n\nRegards"
