import psutil
from psutil._common import bytes2human
import tkinter as tk
from tkinter import font
import gpustat

from memory_profiler import profile

prev_sent = psutil.net_io_counters().bytes_sent
prev_received = psutil.net_io_counters().bytes_recv

@profile
def update_stats():
    global prev_sent, prev_received

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    netw = psutil.net_io_counters()
    sent = netw.bytes_sent
    received = netw.bytes_recv
    gpu_stats = gpustat.new_query()
    gpu_percent = gpu_stats[0].utilization
    
    sent_per_sec = sent - prev_sent
    received_per_sec = received - prev_received
    prev_sent = sent
    prev_received = received

    cpu_string = f"CPU: {cpu}%"
    ram_string = f"RAM: {ram}%"
    net_string = f"Network Sent: {bytes2human(sent_per_sec)}/s\nNetwork Received: {bytes2human(received_per_sec)}/s"
    net_total = f"Total Sent: {bytes2human(sent)}\nTotal Received: {bytes2human(received)}"
    gpu_string = f"GPU: {gpu_percent}%"
    
    cpu_label.config(text=cpu_string)
    gpu_label.config(text=gpu_string)
    ram_label.config(text=ram_string)
    net_label.config(text=net_string)
    net_total_label.config(text=net_total)

    # Update progress bar colors based on their values
    for progress, value in [(cpu_progress, cpu), (gpu_progress, gpu_percent), (ram_progress, ram)]:
        progress.delete("all")
        if value > 80:
            color = 'red'
        elif value > 50:
            color = 'yellow'
        else:
            color = 'green'
        progress.create_rectangle(0, 0, value*2, 25, fill=color)
    del gpu_stats
    
    root.after(1000, update_stats)  # update every 1 second

root = tk.Tk()
root.title("System Monitor")

# Use a larger font
large_font = font.Font(family="Helvetica", size=14)

# Use a frame for padding
frame = tk.Frame(root, padx=10, pady=10)
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create labels with the large font
cpu_label = tk.Label(frame, text="", font=large_font, width=25, anchor='w')
cpu_label.grid(column=0, row=0, sticky=(tk.W))

gpu_label = tk.Label(frame, text="", font=large_font, width=25, anchor='w')
gpu_label.grid(column=0, row=1, sticky=(tk.W))

ram_label = tk.Label(frame, text="", font=large_font, width=25, anchor='w')
ram_label.grid(column=0, row=2, sticky=(tk.W))

net_label = tk.Label(frame, text="", font=large_font, width=30, anchor='w', justify='left')
net_label.grid(column=0, row=3, sticky=(tk.W))

net_total_label = tk.Label(frame, text="", font=large_font, anchor='w', justify='left')
net_total_label.grid(column=1, row=3, sticky=(tk.W))

# Create progress bars
cpu_progress = tk.Canvas(frame, width=200, height=25)
cpu_progress.grid(column=1, row=0, sticky=(tk.W))

gpu_progress = tk.Canvas(frame, width=200, height=25)
gpu_progress.grid(column=1, row=1, sticky=(tk.W))

ram_progress = tk.Canvas(frame, width=200, height=25)
ram_progress.grid(column=1, row=2, sticky=(tk.W))

# Call update_stats to start the loop
update_stats()

# Make the window not resizable
root.resizable(False, False)

root.mainloop()