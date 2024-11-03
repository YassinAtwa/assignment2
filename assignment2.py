import psutil
import time
import logging
from logging.handlers import RotatingFileHandler
import datetime

# Define CPU utilization thresholds
CPU_LEVELS = {
    "idle": 0,
    "normal": 20,
    "moderate": 50,
    "high": 75,
    "critical": 90
}

# Set up logging
log_formatter = logging.Formatter('%(asctime)s - %(message)s')
log_handler = RotatingFileHandler("cpu_monitor.log", maxBytes=1024 * 1024, backupCount=3)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger("CPU_Monitor")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Additional print to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

def get_cpu_level(usage):
    """Determine the CPU level based on usage percentage."""
    if usage >= CPU_LEVELS["critical"]:
        return "Critical"
    elif usage >= CPU_LEVELS["high"]:
        return "High"
    elif usage >= CPU_LEVELS["moderate"]:
        return "Moderate"
    elif usage >= CPU_LEVELS["normal"]:
        return "Normal"
    else:
        return "Idle"

def monitor_cpu():
    """Monitor CPU usage and log usage level every 2 seconds."""
    prev_usage = 0
    interval = 2  # seconds
    
    while True:
        usage = psutil.cpu_percent(interval=1)
        
        # Avoid logging short spikes (changes lasting for less than a second)
        if abs(usage - prev_usage) > 5:
            prev_usage = usage
            continue
            
        cpu_level = get_cpu_level(usage)
        log_msg = f"CPU Usage: {usage}% - Level: {cpu_level}"
        
        # Log and print
        logger.info(log_msg)
        
        # Critical event warning if CPU is critical for a long period
        if cpu_level == "Critical":
            logger.warning("CPU has been critical for an extended period!")
        
        time.sleep(interval)

if __name__ == "__main__":
    try:
        monitor_cpu()
    except KeyboardInterrupt:
        print("CPU monitoring stopped.")