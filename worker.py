"""
Worker thread for handling analysis tasks
"""

import traceback
import logging
from PyQt6.QtCore import QThread, pyqtSignal

class AnalysisWorker(QThread):
    """Worker thread for running analysis operations"""
    
    # Signal for when analysis is complete
    analysis_complete = pyqtSignal(str)
    
    # Signal for when an error occurs
    analysis_error = pyqtSignal(str)
    
    def __init__(self, analyzer, user_data):
        """
        Initialize the worker
        
        Args:
            analyzer (DestinyAnalyzer): The analyzer instance to use
            user_data (dict): Dictionary containing user information
        """
        super().__init__()
        self.analyzer = analyzer
        self.user_data = user_data
        self.logger = logging.getLogger(__name__)
    
    def run(self):
        """Run the analysis in a separate thread"""
        try:
            self.logger.info("Starting analysis in worker thread")
            
            # Run the analysis
            result = self.analyzer.analyze(self.user_data)
            
            # Emit the complete signal with the result
            self.analysis_complete.emit(result)
            
        except Exception as e:
            # Log the error
            self.logger.error(f"Error in analysis worker: {str(e)}")
            self.logger.error(traceback.format_exc())
            
            # Emit the error signal
            self.analysis_error.emit(str(e))