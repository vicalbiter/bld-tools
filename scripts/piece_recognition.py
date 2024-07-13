import io
import os
import time
import argparse
from datetime import datetime
import csv
from collections import defaultdict

from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt

from sctools.bld import Trainer

def show_plot(fig):
    buf = io.BytesIO()
    FigureCanvasAgg(fig).print_png(buf)
    buf.seek(0)

    img = plt.imread(buf, format='png')
    plt.imshow(img)
    plt.axis('off')
    plt.show(block=False)
    plt.pause(0.1)

    plt.close(fig)

def create_log_file(piece_type):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    logs_dir = os.path.join(parent_dir, 'logs')
    
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"{piece_type}_rec_session_{timestamp}.csv")
    
    with open(log_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Piece", "Reference", "User Input", "Response Time (s)"])
    
    return log_file

def main(args):
    piece_type = "corner" if args.type == 'c' else "edge"
    trainer = Trainer()

    log_file = None
    csv_writer = None
    if not args.no_log:
        log_file = create_log_file(piece_type)
        print(f"Logging this session to: {log_file}")
        log_file_handle = open(log_file, 'a', newline='')
        csv_writer = csv.writer(log_file_handle)
    else:
        print("Logging is disabled for this session.")

    session_stats = defaultdict(int)

    while True:
        piece = trainer.get_random_piece(ptype=piece_type)
        show_plot(trainer.draw_edge(piece) if piece_type == "edge" else trainer.draw_corner(piece))
        
        start_time = time.time()
        user_input = input(f"Which {piece_type} is this?\n").lower()
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
        
        if trainer.check_piece_memo_letter(piece, user_input, ptype=piece_type):
            print(f"Correct! (t: {response_time:.1f})")
            session_stats["correct"] += 1
        else:
            print(f"Incorrect! (t: {response_time:.1f})")
            session_stats["incorrect"] += 1

        if csv_writer:
            ref = (trainer.get_edge_memo_letter_from_tuple(piece) if piece_type == "edge" 
                   else trainer.get_corner_memo_letter_from_tuple(piece))
            csv_writer.writerow([timestamp, piece, ref, user_input, f"{response_time:.3f}"])

    if log_file:
        log_file_handle.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLD Cube Piece Recognition Trainer")
    parser.add_argument('-t', '--type', choices=['c', 'e'], required=True,
                        help="Piece type: 'c' for corners, 'e' for edges")
    parser.add_argument('--no-log', action='store_true',
                        help="Disable logging for this session")
    
    args = parser.parse_args()
    main(args)