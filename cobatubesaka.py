import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def swap(M, i, j):
    """Helper function to swap elements i and j of list M."""

    if i != j:
        M[i], M[j] = M[j], M[i]

def mergesort(M, start, end):
    """Merge sort."""

    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from mergesort(M, start, mid)
    yield from mergesort(M, mid + 1, end)
    yield from merge(M, start, mid, end)
    yield M

def merge(M, start, mid, end):
    """Helper function for merge sort."""
    
    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if M[leftIdx] < M[rightIdx]:
            merged.append(M[leftIdx])
            leftIdx += 1
        else:
            merged.append(M[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(M[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(M[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        M[start + i] = sorted_val
        yield M
        
def selectionsort(M):
    """In-place selection sort."""
    if len(M) == 1:
        return

    for i in range(len(M)):
        # Find minimum unsorted value.
        minVal = M[i]
        minIdx = i
        for j in range(i, len(M)):
            if M[j] < minVal:
                minVal = M[j]
                minIdx = j
            yield M
        swap(M, i, minIdx)
        yield M
        

if __name__ == "__main__":
    # Get user input to determine range of integers (1 to N) and desired
    # sorting method (algorithm).
    N = int(input("Masukkan jumlah bilangan bulat: "))
    method_msg = "masukan metode sorting :\n(a)merge\n(b)selection\n"
    method = input(method_msg)

    # Build and randomly shuffle list of integers.
    M = [x + 1 for x in range(N)]
    random.seed(time.time())
    random.shuffle(M)

    # Get appropriate generator to supply to matplotlib FuncAnimation method.
    if method == "a":
        title = "merge sort"
        generator = mergesort(M, 0, N - 1)
    else:
        title = "Selection sort"
        generator = selectionsort(M)

    # Initialize figure and axis.
    fig, ax = plt.subplots()
    ax.set_title(title)

    # Initialize a bar plot. Note that matplotlib.pyplot.bar() returns a
    # list of rectangles (with each bar in the bar plot corresponding
    # to one rectangle), which we store in bar_rects.
    bar_rects = ax.bar(range(len(M)), M, align="edge")

    # Set axis limits. Set y axis upper limit high enough that the tops of
    # the bars won't overlap with the text label.
    ax.set_xlim(0, N)
    ax.set_ylim(0, int(1.07 * N))

    # Place a text label in the upper-left corner of the plot to display
    # number of operations performed by the sorting algorithm (each "yield"
    # is treated as 1 operation).
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    # Define function update_fig() for use with matplotlib.pyplot.FuncAnimation().
    # To track the number of operations, i.e., iterations through which the
    # animation has gone, define a variable "iteration". This variable will
    # be passed to update_fig() to update the text label, and will also be
    # incremented in update_fig(). For this increment to be reflected outside
    # the function, we make "iteration" a list of 1 element, since lists (and
    # other mutable objects) are passed by reference (but an integer would be
    # passed by value).
    # NOTE: Alternatively, iteration could be re-declared within update_fig()
    # with the "global" keyword (or "nonlocal" keyword).
    iteration = [0]
    def update_fig(M, rects, iteration):
        for rect, val in zip(rects, M):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text("# of operations: {}".format(iteration[0]))

    anim = animation.FuncAnimation(fig, func=update_fig,
        fargs=(bar_rects, iteration), frames=generator, interval=1,
        repeat=False)
    plt.show()
