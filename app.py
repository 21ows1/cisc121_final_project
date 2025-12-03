import random
import gradio as gr
import matplotlib.pyplot as plt

def linear_search(arr, target):
    
# Linear search algorithm with step tracking.

    steps = []
    for index, value in enumerate(arr):
        steps.append(f"Checking index {index}: value {value}")
        if value == target:
            steps.append(f"Found {target} at index {index}")
            return index, steps

    steps.append(f"{target} was not found in the list.")
    return -1, steps

def parse_list(list_str: str):
  
# Convert a comma-separated string into a list of integers.
# Raises an error if invalid input is received

    try:
        parts = [p.strip() for p in list_str.split(",") if p.strip() != ""]
        return [int(x) for x in parts]
    except ValueError:
        raise gr.Error("Please enter a comma-separated list of integers, e.g. 3, 1, 4, 1, 5")

def generate_list():

# Generate a random list of 10 integers between 1 and 49,
# return it as a comma-separated string for the textbox.

    arr = random.sample(range(1, 50), 10)
    list_str = ", ".join(str(x) for x in arr)
    return list_str

def search_interface(list_str: str, target_str: str):

# Connects the UI inputs to the algorithm.

    numbers = parse_list(list_str)

    try:
        target = int(target_str)
    except ValueError:
        raise gr.Error("Target must be an integer, e.g. 4")

    index, steps = linear_search(numbers, target)

# Tell the user what the result was!
    if index != -1:
        result_text = f"🎆 Found {target} at index {index}!"
    else:
        result_text = f"❌ {target} was not found (returned -1)."

    steps_text = "\n".join(steps)

# Visualize where the target was found using matplotlib
    fig, ax = plt.subplots()

# Set the bar graph colours
    colors = ["skyblue"] * len(numbers)

# Highlight the specific index which the target was found at
    if index != -1:
        colors[index] = "limegreen"

# Draw the bars with custom colors
    ax.bar(range(len(numbers)), numbers, color=colors)

    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.set_title("Linear Search Visualization")

    if index != -1 and len(numbers) > 0:
        ax.annotate(
            "Target",
            xy=(index, numbers[index]),
            xytext=(index, numbers[index] + max(1, numbers[index] * 0.1)),
            arrowprops=dict(arrowstyle="->")
        )

    return result_text, steps_text, fig

# Build the Gradio User Interface
with gr.Blocks() as demo:
    gr.Markdown("# Linear Search Visualizer")
    gr.Markdown(
        "Enter a list of numbers and a target value, or click **Generate List**.\n"
        "The app will show how linear search checks each element."
    )

    with gr.Row():
        list_input = gr.Textbox(
            label="List of numbers (comma-separated)",
            placeholder="Example: 3, 1, 4, 1, 5",
            value="3, 1, 4, 1, 5",
        )
        target_input = gr.Textbox(
            label="Target value",
            placeholder="Example: 4",
            value="4",
        )

    gen_btn = gr.Button("Generate List", variant="secondary")
    search_button = gr.Button("Run Linear Search", variant="primary")

    result_output = gr.Textbox(
        label="Result (index of target, -1 = not found)",
        interactive=False,
    )
    steps_output = gr.Textbox(
        label="Step-by-step process",
        lines=10,
        interactive=False,
    )
    plot_output = gr.Plot(
        label="Visualization of the list"
    )

#Create the generate list button that when clicked generates a random list
    gen_btn.click(
        fn=generate_list,
        inputs=[],
        outputs=list_input,
    )

#Create the button for running the linear search
    search_button.click(
        fn=search_interface,
        inputs=[list_input, target_input],
        outputs=[result_output, steps_output, plot_output],
    )

if __name__ == "__main__":
    demo.launch()
