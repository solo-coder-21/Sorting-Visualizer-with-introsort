# Python Sorting Algorithm Visualizer

A simple and responsive sorting algorithm visualizer built with Python and the Tkinter standard library. This tool allows you to watch various sorting algorithms in real-time, helping you understand how they work step-by-step.

![Sorting Visualizer Screenshot](<INSERT_SCREENSHOT_URL_HERE>)
(After you run the program, take a screenshot and upload it to your repository, then replace the text above with the link)

## 🚀 Features

* *Multiple Algorithms*: Compare several popular sorting algorithms:
    * Introsort
    * Heapsort
    * Insertion Sort
    * Bubble Sort
* *Interactive Controls*:
    * *Algorithm Selection*: Choose your algorithm from a dropdown menu.
    * *Array Size*: Use a slider to set the number of items to sort (from 10 to 200).
    * *Speed*: Control the visualization speed with a delay slider (from 1ms to 500ms).
* *Real-time Visualization*: Bars are color-coded to show their status:
    * *Sky Blue*: Default
    * *Orange*: Being compared
    * *Purple*: Being swapped
    * *Red*: Pivot element (for Introsort/Quicksort)
    * *Green*: Sorted
* *Modern UI*: Uses ttk themed widgets for a cleaner look than standard Tkinter.

## 💻 How to Run

This project uses only Python's standard libraries, so no external packages are needed.

1.  *Clone the repository:*
    bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    

2.  *Ensure you have Python 3:*
    This program requires tkinter, which is included with most Python 3 installations. If you don't have it, you may need to install it:
    bash
    # On Debian/Ubuntu
    sudo apt-get install python3-tk
    
    # On Fedora
    sudo dnf install python3-tkinter
    

3.  *Run the script:*
    bash
    python visualizer.py
    

## 🛠 How It Works

1.  *Generate Array*: Click "Generate New Array" to create a new random list of numbers. The size is based on the "Array Size" slider.
2.  *Select Algorithm*: Choose an algorithm from the dropdown.
3.  *Adjust Speed*: Set the delay between steps. A smaller delay is faster.
4.  *Start Sort*: Click "Start Sort" to begin the visualization. The controls will be disabled until the sort is complete.

Enjoy comparing the algorithms!
