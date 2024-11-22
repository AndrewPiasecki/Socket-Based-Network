import socket
import os
from datetime import time
from time import time
import pandas as pd


class NetworkAnalysis:
  
  # Initializing
    def initialize(self, log_file="NetworkAnalysisStatistics.csv"):
        self.log_file = log_file
        self.columns = ['Action', 'File', 'Size (bytes)', 'Transfer Time (s)', 'Data Rate (bytes/s)']
        
        if os.path.exists(self.log_file):
            self.stats = pd.read_csv(self.log_file)
        else:
            self.stats = pd.DataFrame(columns=self.columns)
          
# Log Transfer
    def logTransfer(self, action, file_name, file_size, transfer_time):
        
        data_rate = file_size / transfer_time if transfer_time > 0 else 0

        
        new_entry = pd.DataFrame([{
            'Action': action,
            'File': file_name,
            'Size (bytes)': file_size,
            'Transfer Time (s)': transfer_time,
            'Data Rate (bytes/s)': data_rate
        }])

        
        if self.stats.empty:
            
            self.stats = new_entry
        else:
            
            self.stats = pd.concat([self.stats, new_entry], ignore_index=True)


  # Saving
    def save(self):
        
        self.stats.to_csv(self.log_file, index=False)

  # Summary 
    def displaySummary(self):
        
        if self.stats.empty:
            print("Date Is Not Available")
        else:
            print("Summary of Network Analysis:")
            print(self.stats.groupby('Action').agg({
                'Size (bytes)': 'sum',
                'Transfer Time (s)': 'mean',
                'Data Rate (bytes/s)': 'mean'
            }))

