import tkinter as tk
from simulation import *
import cProfile, pstats

def test_run_sim(rule, num_sims): 
     sim = CaptureSim(rule, num_sims)

# test_run_sim(8, 2000)

cProfile.runctx("test_run_sim(8, 2000)", globals(), locals(), filename = "profiled.stats")

stats = pstats.Stats("profiled.stats")
# Clean up filenames for the report
stats.strip_dirs()
# Sort the statistics by the total time spent in the function itself
stats.sort_stats("cumtime")
stats.print_stats(100) 


# root = tk.Tk()

# root.geometry("400x400")

# frame = tk.Frame(root)

# frame.pack(expand = tk.TRUE, fill = tk.BOTH)

# label = tk.Label(frame, text = "Brett", bg = "green")

# label.pack(expand = tk.TRUE, fill = tk.X)

# input_rule = input("Which rule (0-11)?")

# input_experiments = input("How many random simulations?")

# print("starting simulations")

# iterate_over = RuleIter(input_rule, input_experiments)

# print("done simulations")

# root.mainloop()
