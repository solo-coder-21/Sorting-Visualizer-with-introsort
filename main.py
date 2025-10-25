import tkinter as tk
from tkinter import ttk  # Import themed Tkinter widgets
import random
import time

# --- Configuration ---
# Default values
DEFAULT_SIZE = 50
DEFAULT_DELAY = 10
MIN_VALUE = 10
MAX_VALUE = 500

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 550

# --- Global variables ---
data = []
window = None
canvas = None

# --- UI Element Variables ---
delay_scale = None
size_scale = None
algo_combobox = None
generate_button = None
sort_button = None

# --- State Variables ---
ARRAY_SIZE = DEFAULT_SIZE
DELAY_MS = DEFAULT_DELAY

color_map = {
    "default": "skyblue",
    "comparing": "orange",
    "pivot": "red",
    "swapping": "purple",
    "sorted": "green",
    "heap_active": "lightcoral",
    "insertion_active": "yellow"
}

# --- GUI Setup ---
def setup_gui():
    global window, canvas, delay_scale, size_scale, algo_combobox, generate_button, sort_button
    
    window = tk.Tk()
    window.title("Sorting Algorithm Visualizer")
    window.geometry(f"{CANVAS_WIDTH+20}x{CANVAS_HEIGHT+120}")
    window.resizable(False, False)
    
    # Use a themed frame for the controls
    control_frame = ttk.Frame(window, padding="10")
    control_frame.pack(fill=tk.X)

    # --- Algorithm Selection ---
    ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    algo_combobox = ttk.Combobox(
        control_frame,
        state="readonly",
        values=["Introsort", "Heapsort", "Insertion Sort", "Bubble Sort"]
    )
    algo_combobox.current(0)  # Default to Introsort
    algo_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    # --- Array Size Slider ---
    ttk.Label(control_frame, text="Array Size:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    size_scale = ttk.Scale(
        control_frame,
        from_=10,
        to=200,
        orient=tk.HORIZONTAL,
        length=150,
        command=update_size
    )
    size_scale.set(DEFAULT_SIZE)
    size_scale.grid(row=0, column=3, padx=5, pady=5)

    # --- Speed Slider ---
    ttk.Label(control_frame, text="Delay (ms):").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
    delay_scale = ttk.Scale(
        control_frame,
        from_=1,
        to=500,
        orient=tk.HORIZONTAL,
        length=150,
        command=update_delay
    )
    delay_scale.set(DEFAULT_DELAY)
    delay_scale.grid(row=0, column=5, padx=5, pady=5)

    # --- Control Buttons ---
    generate_button = ttk.Button(
        control_frame,
        text="Generate New Array",
        command=generate_new_array
    )
    generate_button.grid(row=0, column=6, padx=10, pady=5)
    
    sort_button = ttk.Button(
        control_frame,
        text="Start Sort",
        command=start_sort
    )
    sort_button.grid(row=0, column=7, padx=10, pady=5)
    
    # Configure columns to stretch
    control_frame.grid_columnconfigure(6, weight=1)
    control_frame.grid_columnconfigure(7, weight=1)

    # --- Canvas ---
    canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
    canvas.pack(pady=10)

    generate_new_array()  # Initial array
    window.mainloop()

# --- GUI Helper Functions ---
def toggle_controls(state):
    """Enable or disable all UI controls."""
    state_str = "disabled" if state == tk.DISABLED else "normal"
    
    algo_combobox.config(state="readonly" if state == tk.NORMAL else "disabled")
    size_scale.config(state=state)
    delay_scale.config(state=state)
    generate_button.config(state=state)
    sort_button.config(state=state)

def update_delay(val):
    global DELAY_MS
    DELAY_MS = int(float(val))

def update_size(val):
    global ARRAY_SIZE
    ARRAY_SIZE = int(float(val))
    generate_new_array() # Regenerate array on size change

# --- Visualization Functions ---
def draw_bars(arr, indices_to_color=None):
    canvas.delete("all")
    bar_width = CANVAS_WIDTH / len(arr)
    
    for i, height in enumerate(arr):
        x0 = i * bar_width
        y0 = CANVAS_HEIGHT - (height / MAX_VALUE) * CANVAS_HEIGHT
        
        gap_width = bar_width * 0.1 # 10% gap
        x1 = (i + 1) * bar_width - gap_width
        y1 = CANVAS_HEIGHT

        fill_color = color_map["default"]
        if indices_to_color and i in indices_to_color:
            fill_color = color_map.get(indices_to_color[i], color_map["default"])
        
        canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="black")
    
    window.update() 
    time.sleep(DELAY_MS / 1000.0)

def finalize_sort_visualization(arr):
    draw_bars(arr, {i: "sorted" for i in range(len(arr))})

# --- Data Generation ---
def generate_new_array():
    global data
    data = [random.randint(MIN_VALUE, MAX_VALUE) for _ in range(ARRAY_SIZE)]
    draw_bars(data)

# --- Sorting Algorithms ---

# 1. Bubble Sort
def bubble_sort_visualized(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            colors = {j: "comparing", j + 1: "comparing"}
            for k in range(n - i, n): colors[k] = "sorted" # Mark sorted end
            draw_bars(arr, colors)
            
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                draw_bars(arr, {j: "swapping", j + 1: "swapping"})
        if not swapped:
            break # Already sorted
    finalize_sort_visualization(arr)

# 2. Insertion Sort (Standalone)
def insertion_sort_standalone(arr):
    insertion_sort_visualized(arr, 0, len(arr) - 1)
    finalize_sort_visualization(arr)

# 3. Heap Sort (Standalone)
def heap_sort_standalone(arr):
    heap_sort_visualized(arr, 0, len(arr) - 1)

# 4. Introsort (Standalone)
def introsort_visualized(arr):
    max_depth = 2 * (len(arr).bit_length() - 1) 
    introsort_recursive(arr, 0, len(arr) - 1, max_depth)
    finalize_sort_visualization(arr)

# --- Introsort/Heapsort/Insertion Sort Helper Functions ---

def insertion_sort_visualized(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        colors = {i: "insertion_active"}
        for k in range(low, i): colors[k] = "sorted"
        
        while j >= low and key < arr[j]:
            arr[j + 1] = arr[j]
            colors[j] = "comparing"
            colors[j+1] = "insertion_active"
            draw_bars(arr, colors)
            if j in colors: del colors[j]
            j -= 1
        arr[j + 1] = key
        
        colors[j+1] = "sorted"
        draw_bars(arr, colors)

def heapify_visualized(arr, n, i, offset):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    colors = {offset + i: "heap_active"}
    if left < n: colors[offset + left] = "comparing"
    if right < n: colors[offset + right] = "comparing"
    draw_bars(arr, colors)
    if left < n and arr[offset + left] > arr[offset + largest]: largest = left
    if right < n and arr[offset + right] > arr[offset + largest]: largest = right
    if largest != i:
        arr[offset + i], arr[offset + largest] = arr[offset + largest], arr[offset + i]
        draw_bars(arr, {offset + i: "swapping", offset + largest: "swapping"})
        heapify_visualized(arr, n, largest, offset)

def heap_sort_visualized(arr, low, high):
    n = high - low + 1
    offset = low
    for i in range(n // 2 - 1, -1, -1):
        heapify_visualized(arr, n, i, offset)
    for i in range(n - 1, 0, -1):
        arr[offset], arr[offset + i] = arr[offset + i], arr[offset]
        draw_bars(arr, {offset: "heap_active", offset + i: "sorted"}) 
        heapify_visualized(arr, i, 0, offset)
    colors = {i: "sorted" for i in range(low, high + 1)}
    draw_bars(arr, colors)

def partition_visualized(arr, low, high):
    pivot_index = random.randint(low, high)
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high]
    draw_bars(arr, {high: "pivot"})
    i = low - 1
    for j in range(low, high):
        colors = {high: "pivot", j: "comparing"}
        if i >= low: colors[i] = "comparing"
        draw_bars(arr, colors)
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            colors[i] = "swapping"
            colors[j] = "swapping"
            draw_bars(arr, colors)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw_bars(arr, {i+1: "pivot"})
    return i + 1

def introsort_recursive(arr, low, high, depth_limit):
    if high - low + 1 <= 16: # Threshold for Insertion Sort
        insertion_sort_visualized(arr, low, high)
        return
    if depth_limit == 0: # Fallback to Heapsort
        heap_sort_visualized(arr, low, high)
        return
    if low < high:
        pi = partition_visualized(arr, low, high)
        introsort_recursive(arr, low, pi - 1, depth_limit - 1)
        introsort_recursive(arr, pi + 1, high, depth_limit - 1)

# --- Sort Initiation ---
def start_sort():
    global data
    
    selected_algo_name = algo_combobox.get()
    
    algo_functions = {
        "Introsort": introsort_visualized,
        "Heapsort": heap_sort_standalone,
        "Insertion Sort": insertion_sort_standalone,
        "Bubble Sort": bubble_sort_visualized
    }
    
    sort_function = algo_functions.get(selected_algo_name)
    if not sort_function:
        print(f"Error: Algorithm '{selected_algo_name}' not found.")
        return

    toggle_controls(tk.DISABLED)
    sort_function(data)
    toggle_controls(tk.NORMAL)

if _name_ == "_main_":
    setup_gui()
