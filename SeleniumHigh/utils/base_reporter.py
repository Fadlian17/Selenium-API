from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional
import os


class BaseReporter(ABC):
    """Base class for all reporters"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        self.results: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.metadata: Dict[str, Any] = {}
    
    def start_session(self, **kwargs):
        """Start test session with optional metadata"""
        self.start_time = datetime.now()
        self.metadata.update(kwargs)
        self._on_session_start()
    
    def end_session(self):
        """End test session"""
        self.end_time = datetime.now()
        self._on_session_end()
    
    def add_result(self, **kwargs):
        """Add test result with standardized format"""
        result = {
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        self.results.append(result)
        self._on_result_added(result)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get test statistics"""
        total = len(self.results)
        passed = len([r for r in self.results if r.get("status") == "PASS"])
        failed = len([r for r in self.results if r.get("status") == "FAIL"])
        skipped = len([r for r in self.results if r.get("status") == "SKIP"])
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "duration": (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        }
    
    @abstractmethod
    def generate_report(self, filename: str = None) -> str:
        """Generate report and return filepath"""
        pass
    
    def _on_session_start(self):
        """Hook for session start"""
        pass
    
    def _on_session_end(self):
        """Hook for session end"""
        pass
    
    def _on_result_added(self, result: Dict[str, Any]):
        """Hook for result added"""
        pass
    
    def _ensure_output_dir(self):
        """Ensure output directory exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir) 