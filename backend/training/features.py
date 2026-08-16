"""Module 2: reusable text and URL feature engineering helpers."""
import re
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s<>'\"]+", re.I)
SUSPICIOUS_TERMS = {
    "verify", "urgent", "password", "login",
    "account", "bank", "winner",
}


def safe_domain(url: str) -> str:
    """Return a URL domain without failing on malformed dataset URLs."""
    try:
        return urlparse(url).netloc
    except ValueError:
        return ""


def engineered_features(text: str) -> dict[str, float]:
    text = str(text)
    urls = URL_RE.findall(text)
    tokens = re.findall(r"\b\w+\b", text.lower())
    domains = [safe_domain(url) for url in urls]

    return {
        "text_length": len(text),
        "url_count": len(urls),
        "unique_domain_count": len({domain for domain in domains if domain}),
        "exclamation_count": text.count("!"),
        "suspicious_term_count": sum(
            token in SUSPICIOUS_TERMS for token in tokens
        ),
        "uppercase_ratio": sum(char.isupper() for char in text) / max(len(text), 1),
    }