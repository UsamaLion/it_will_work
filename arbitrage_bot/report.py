import csv
from config import LOG_FILE

class Report:
    def __init__(self):
        self.log_file = LOG_FILE

    def log_opportunity(self, opportunity):
        with open(self.log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([opportunity['pair'], opportunity['max_price'], opportunity['min_price'], opportunity['profit_percentage']])

    def generate_report(self):
        # Implement report generation logic if needed
        pass
