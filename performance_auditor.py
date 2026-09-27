import json
import time
import urllib.request
from typing import Dict, Any

class PerformanceAuditor:
    """
    Automated Web Performance & Core Web Vitals Auditor
    Analyzes site response metrics, load times, and payload size.
    """
    
    def __init__(self, url: str):
        self.url = url if url.startswith(('http://', 'https://')) else f"https://{url}"

    def audit(self) -> Dict[str, Any]:
        print(f"[*] Starting audit for: {self.url}")
        start_time = time.time()
        
        try:
            req = urllib.request.Request(
                self.url, 
                headers={'User-Agent': 'Mozilla/5.0 (PerformanceAuditorBot/1.0)'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                end_time = time.time()
                
                load_time_ms = round((end_time - start_time) * 1000, 2)
                page_size_kb = round(len(content) / 1024, 2)
                status_code = response.getcode()
                
                # Metric Evaluation Logic
                performance_score = self._calculate_score(load_time_ms, page_size_kb)
                
                return {
                    "target_url": self.url,
                    "status_code": status_code,
                    "metrics": {
                        "time_to_first_byte_est_ms": load_time_ms,
                        "total_page_size_kb": page_size_kb,
                        "performance_score": f"{performance_score}/100"
                    },
                    "recommendations": self._generate_recommendations(load_time_ms, page_size_kb)
                }

        except Exception as e:
            return {"error": str(e), "target_url": self.url}

    def _calculate_score(self, load_time_ms: float, page_size_kb: float) -> int:
        score = 100
        if load_time_ms > 2000:
            score -= 30
        elif load_time_ms > 1000:
            score -= 15
            
        if page_size_kb > 1000:
            score -= 20
        elif page_size_kb > 500:
            score -= 10
            
        return max(score, 0)

    def _generate_recommendations(self, load_time_ms: float, page_size_kb: float) -> list:
        recs = []
        if load_time_ms > 1000:
            recs.append("Optimize server response time and leverage CDN caching.")
        if page_size_kb > 500:
            recs.append("Compress DOM assets, minify JS/CSS, and optimize image formats (WebP/AVIF).")
        if not recs:
            recs.append("Performance parameters are optimal.")
        return recs

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "google.com"
    auditor = PerformanceAuditor(target)
    report = auditor.audit()
    print(json.dumps(report, indent=4))
  
