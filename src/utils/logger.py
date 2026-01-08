"""
Logging System - Professional logging configuration
Hệ thống logging chuyên nghiệp với multiple handlers và formatters.

Module này cung cấp centralized logging cho toàn bộ dự án với:
- Console output có màu sắc
- File output với rotation
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Structured log format với timestamps

Usage:
    >>> from utils.logger import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.info("Training started")
    >>> logger.error("Model not found", exc_info=True)
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import os


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter với ANSI color codes cho console output.
    
    Cung cấp màu sắc khác nhau cho từng log level để dễ đọc:
    - DEBUG: Xanh dương (Cyan)
    - INFO: Xanh lá (Green)
    - WARNING: Vàng (Yellow)
    - ERROR: Đỏ (Red)
    - CRITICAL: Đỏ đậm với background (Bold Red)
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[1;31m', # Bold Red
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record với màu sắc.
        
        Args:
            record: Log record object từ logging module
            
        Returns:
            Formatted string với ANSI color codes
        """
        # Add color to levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            )
        
        # Format the message
        formatted = super().format(record)
        
        return formatted


def setup_logging(
    level: int = logging.INFO,
    log_dir: Optional[str] = None,
    console_output: bool = True,
    file_output: bool = True
) -> None:
    """
    Thiết lập logging system cho toàn bộ application.
    
    Tạo logger với console handler (có màu) và file handler (plain text).
    File logs được lưu với timestamp trong tên file.
    
    Args:
        level: Logging level (DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50).
              Mặc định là INFO.
        log_dir: Thư mục chứa log files. Nếu None, sử dụng 'logs/'.
              Thư mục sẽ được tạo tự động nếu chưa tồn tại.
        console_output: Có xuất logs ra console không. Mặc định True.
        file_output: Có ghi logs vào file không. Mặc định True.
        
    Raises:
        OSError: Nếu không thể tạo log directory
        PermissionError: Nếu không có quyền ghi vào log directory
        
    Examples:
        >>> setup_logging(level=logging.DEBUG)  # Enable all logs
        >>> setup_logging(log_dir="my_logs", console_output=False)  # File only
        
    Note:
        - Nên gọi function này một lần duy nhất khi khởi động app
        - Logs file có format: app_YYYYMMDD_HHMMSS.log
        - Console sử dụng colored formatter, file sử dụng plain formatter
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Define log format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Console handler với colors
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Use colored formatter for console
        colored_formatter = ColoredFormatter(log_format, datefmt=date_format)
        console_handler.setFormatter(colored_formatter)
        
        root_logger.addHandler(console_handler)
    
    # File handler without colors
    if file_output:
        # Create log directory
        if log_dir is None:
            log_dir = 'logs'
        
        log_path = Path(log_dir)
        try:
            log_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"[ERROR] Cannot create log directory {log_dir}: {e}")
            raise
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_path / f"app_{timestamp}.log"
        
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            
            # Use plain formatter for file
            plain_formatter = logging.Formatter(log_format, datefmt=date_format)
            file_handler.setFormatter(plain_formatter)
            
            root_logger.addHandler(file_handler)
            
            # Log the log file location
            root_logger.info(f"Log file created: {log_file}")
            
        except (OSError, PermissionError) as e:
            print(f"[ERROR] Cannot create log file {log_file}: {e}")
            raise


def get_logger(name: str) -> logging.Logger:
    """
    Lấy logger instance cho module cụ thể.
    
    Mỗi module nên có logger riêng để dễ trace source của log messages.
    Logger kế thừa configuration từ root logger (được setup bởi setup_logging).
    
    Args:
        name: Tên của logger, thường là __name__ của module.
              Best practice: get_logger(__name__)
              
    Returns:
        Logger instance configured với settings từ setup_logging()
        
    Examples:
        >>> logger = get_logger(__name__)
        >>> logger.debug("Debug info")
        >>> logger.info("Process started")
        >>> logger.warning("Resource low")
        >>> logger.error("Operation failed", exc_info=True)  # Include traceback
        >>> logger.critical("System failure")
        
    Note:
        - Phải gọi setup_logging() trước khi sử dụng logger
        - Nếu chưa setup, logger sẽ dùng default config (warning level)
        - Logger name sẽ xuất hiện trong log output
    """
    return logging.getLogger(name)


# Example usage and testing
if __name__ == "__main__":
    # Setup logging
    setup_logging(level=logging.DEBUG)
    
    # Get logger
    logger = get_logger(__name__)
    
    # Test different levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Test exception logging
    try:
        1 / 0
    except ZeroDivisionError:
        logger.error("Math error occurred", exc_info=True)
