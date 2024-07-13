import io
import os
import time
from datetime import datetime
import csv
from collections import defaultdict

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt

from sctools.bld import Trainer

def show_plot(fig):
    # Convert plot to PNG image
    buf = io.BytesIO()
    FigureCanvasAgg(fig).print_png(buf)
    buf.seek(0)

    img = plt.imread(buf, format='png')
    plt.imshow(img)
    plt.axis('off')
    plt.show(block=False)
    plt.pause(0.1)

    plt.close(fig)

def create_log_file():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    logs_dir = os.path.join(parent_dir, 'logs')
    
    # Create the logs directory if it doesn't exist
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Generate a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"corners_rec_session_{timestamp}.csv")
    
    # Create the log file and write the header
    with open(log_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Corner", "Reference", "User Input", "Response Time (s)"])
    
    return log_file

def main():
    trainer = Trainer()
    log_file = create_log_file()

    print(f"Logging this session to: {log_file}")

    log_file_handle = open(log_file, 'a', newline='')
    csv_writer = csv.writer(log_file_handle)

    session_stats = defaultdict(int)

    while True:
        # Get and show the plot
        corner = trainer.get_random_piece(ptype="corner")
        show_plot(trainer.draw_corner(corner))
        
        # Get user input
        start_time = time.time()
        user_input = input("Which corner is this?\n").lower()
        end_time = time.time()

        response_time = end_time - start_time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if user_input == 'quit':
            print("Exiting the program.")
            session_stats["total"] = session_stats["correct"] + session_stats["incorrect"]
            stats = (
                "*** Session Stats ***\n"
                f"Correct: {session_stats['correct']}/{session_stats['total']}\n"
            )
            print(stats)
            break
        
        if trainer.check_piece_memo_letter(corner, user_input, ptype="corner"):
            print(f"Correct! (t: {response_time:.1f})")
            session_stats["correct"] += 1
        else:
            print(f"Incorrect! (t: {response_time:.1f})")
            session_stats["incorrect"] += 1

        ref = trainer.get_corner_memo_letter_from_tuple(corner)
        csv_writer.writerow([timestamp, corner, ref, user_input, f"{response_time:.3f}"])
        

if __name__ == "__main__":
    main()