import tkinter as tk
import random
from PIL import Image, ImageTk

# Initialize the window
window = tk.Tk()
window.title("Sky")

# Set up the canvas
canvas = tk.Canvas(window, width=500, height=500)
canvas.pack()

# Draw the background
background = canvas.create_rectangle(0, 0, 500, 500, fill="lightblue")

success_message = None

heart_img = Image.open("heart.png")
heart_img = heart_img.resize((25, 25))
heart_img = ImageTk.PhotoImage(heart_img)

score = 0
score_text = canvas.create_text(450, 20, text=f"Score: {score}", font=("Arial", 12))
hint1 = canvas.create_text(250, 470, text="Find Nini!", font=("Arial", 14), anchor="center")
hint2 = canvas.create_text(250, 490, text="Use the arrow keys ✥ to navigate.", font=("Arial", 12), anchor="center")

# A flag to check if Nini has been found, using a list for mutability
found_nini = [False]


def start_game():
    min_distance = 100
    while True:
        # Randomize the starting positions for Tibik and Nini
        tibik_x = random.randint(100, 400)
        tibik_y = random.randint(100, 400)
        nini_x = random.randint(100, 400)
        nini_y = random.randint(100, 400)

        # Calculate the distance between Tibik and Nini
        distance = ((tibik_x - nini_x) ** 2 + (tibik_y - nini_y) ** 2) ** 0.5

        # Check if the distance is less than the minimum distance
        if distance >= min_distance:
            break

    # Draw Tibik and Nini
    nini = canvas.create_oval(nini_x, nini_y, nini_x + 50, nini_y + 50, fill="pink")
    tibik = canvas.create_oval(tibik_x, tibik_y, tibik_x + 50, tibik_y + 50, fill="spring green")

    # Label Tibik and Nini
    nini_label = canvas.create_text((nini_x + 25, nini_y + 25), text="Nini", font=("Arial", 12))
    tibik_label = canvas.create_text((tibik_x + 25, tibik_y + 25), text="Tibik", font=("Arial", 12))

    # Set to keep track of pressed arrow keys
    pressed_keys = set()

    # Function to move Tibik
    def move_tibik(event):
        # If Nini has already been found, return early without moving Tibik
        if found_nini[0]:
            return
        if event.type == "2":  # KeyPress event
            pressed_keys.add(event.keysym)
        else:  # KeyRelease event
            pressed_keys.discard(event.keysym)

        tibik_coords = canvas.coords(tibik)

        # Handle movement
        if "Up" in pressed_keys and tibik_coords[1] > 0:
            canvas.move(tibik, 0, -10)
            canvas.move(tibik_label, 0, -10)
        if "Down" in pressed_keys and tibik_coords[3] < 500:
            canvas.move(tibik, 0, 10)
            canvas.move(tibik_label, 0, 10)
        if "Left" in pressed_keys and tibik_coords[0] > 0:
            canvas.move(tibik, -10, 0)
            canvas.move(tibik_label, -10, 0)
        if "Right" in pressed_keys and tibik_coords[2] < 500:
            canvas.move(tibik, 10, 0)
            canvas.move(tibik_label, 10, 0)

        # Check if Tibik has found Nini
        tibik_coords = canvas.coords(tibik)
        nini_coords = canvas.coords(nini)
        if tibik_coords[0] < nini_coords[2] and tibik_coords[2] > nini_coords[0] and \
                tibik_coords[1] < nini_coords[3] and tibik_coords[3] > nini_coords[1]:
            found_nini[0] = True
            window.unbind("<Up>")
            window.unbind("<Down>")
            window.unbind("<Left>")
            window.unbind("<Right>")
            # Load the heart image
            heart_image = tk.PhotoImage(file="heart.png")
            # Calculate the center point between Tibik and Nini
            heart_x = (tibik_coords[0] + nini_coords[2]) / 2
            heart_y = (tibik_coords[1] + nini_coords[3]) / 2
            # Display the heart image
            heart = canvas.create_image(heart_x, heart_y, image=heart_img)
            # Show the success message
            success = canvas.create_text(250, 250, text="Success!", font=("Arial", 36))
            # Update the score label
            global score
            canvas.itemconfig(score_text, text=f"Score: {score}")
            window.after(2000, lambda: clear(canvas, tibik, nini, tibik_label, nini_label, success, heart))

    window.bind("<KeyPress>", move_tibik)
    window.bind("<KeyRelease>", move_tibik)


def clear(canvas, tibik, nini, tibik_label, nini_label, success, heart):
    # Reset the found_nini flag
    found_nini[0] = False

    global score
    canvas.delete(tibik, nini, tibik_label, nini_label, success, heart)

    score += 1
    canvas.itemconfigure(score_text, text=f"Score: {score}")

    if score == 10:
        # Display a message from Nini
        message = canvas.create_text(250, 230, text="Thank you Tibik!", font=("Arial", 26), anchor="center")
        message2 = canvas.create_text(250, 280, text="You found me 10 times!", font=("Arial", 26), anchor="center")
        message3 = canvas.create_text(250, 330, text="- Nini", font=("Arial", 22), anchor="center")
        window.after(3000, lambda: window.destroy())
    else:
        start_game()


# Start the game over
start_game()

# Start the game loop
window.mainloop()
