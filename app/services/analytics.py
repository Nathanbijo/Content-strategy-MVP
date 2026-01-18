from typing import List
from typing import Literal


def score_post(caption: str, hashtags: List[str]) -> Literal["Low", "Medium", "High"]:
    """
    Very simple heuristic scoring.
    """
    length = len(caption)
    tag_count = len(hashtags)

    if length < 60 or tag_count < 2:
        return "Low"
    if length < 180:
        return "Medium"
    return "High"
