"""
Video Comparator Engine
Compares Old Video (Video A) vs New Video (Video B) metrics,
sentiment shifts, and calculates Iteration Improvement Score.
"""

from typing import Dict, Any

def compare_two_videos(old_video: Dict[str, Any], old_sentiment: Dict[str, Any],
                        new_video: Dict[str, Any], new_sentiment: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two videos side-by-side and calculate progress metrics."""
    
    views_diff = new_video.get("views", 0) - old_video.get("views", 0)
    views_pct_change = round((views_diff / max(1, old_video.get("views", 1))) * 100, 1)
    
    old_eng = round(((old_video.get("likes", 0) + old_video.get("comments_count", 0)) / max(1, old_video.get("views", 1))) * 100, 2)
    new_eng = round(((new_video.get("likes", 0) + new_video.get("comments_count", 0)) / max(1, new_video.get("views", 1))) * 100, 2)
    eng_diff = round(new_eng - old_eng, 2)
    
    pos_shift = new_sentiment.get("positive_pct", 0) - old_sentiment.get("positive_pct", 0)
    
    # Calculate Overall Iteration Improvement Score out of 100
    base_score = 70
    if views_pct_change > 0:
        base_score += min(15, int(views_pct_change / 2))
    if eng_diff > 0:
        base_score += min(10, int(eng_diff * 3))
    if pos_shift > 0:
        base_score += min(10, pos_shift // 2)
        
    iteration_score = min(98, max(45, base_score))
    
    if iteration_score >= 80:
        verdict = "🚀 Excellent Upgrade! Your new video performed significantly better across views, engagement & sentiment."
        badge = "HIGH GROWTH"
    elif iteration_score >= 65:
        verdict = "📈 Solid Progress! Positive audience response. Minor tweaks needed in intro hook for next video."
        badge = "MODERATE IMPROVEMENT"
    else:
        verdict = "⚠️ Needs Adjustment. Engagement or retention dropped slightly. Apply the Next Video Action Blueprint."
        badge = "NEEDS REFINEMENT"
        
    return {
        "old_title": old_video.get("title"),
        "new_title": new_video.get("title"),
        "old_views": old_video.get("views"),
        "new_views": new_video.get("views"),
        "views_diff": views_diff,
        "views_pct_change": views_pct_change,
        "old_eng": old_eng,
        "new_eng": new_eng,
        "eng_diff": eng_diff,
        "old_pos_sentiment": old_sentiment.get("positive_pct"),
        "new_pos_sentiment": new_sentiment.get("positive_pct"),
        "sentiment_shift": pos_shift,
        "iteration_score": iteration_score,
        "badge": badge,
        "verdict": verdict
    }
