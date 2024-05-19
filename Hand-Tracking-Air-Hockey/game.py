import tkinter as tk
import random
import cv2
from cvzone.HandTrackingModule import HandDetector
import threading
import time
import math
import pygame

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

player1_score = 0
player2_score = 0

player1_disabled = False
player2_disabled = False
paused = False
winscreen = False
winscreen1 = False
winscreen2 = False
titlescreen = True
quit_game = False
powerup_flag = False

player1_text = canvas.create_text(220, 25, text="Player 1: 0", fill="black", font=("Press Start 2P", 19))
player2_text = canvas.create_text(380, 25, text="Player 2: 0", fill="black", font=("Press Start 2P", 19))
player1_pu = canvas.create_text(220, 50, text="No Powerups :(", fill="black", font=("Press Start 2P", 12))
player2_pu = canvas.create_text(380, 50, text="No Powerups :(", fill="black", font=("Press Start 2P", 12))

pygame.init()

button_sound = pygame.mixer.Sound('button_click1.wav')
score_sound = pygame.mixer.Sound('score.wav')
powerup_sound = pygame.mixer.Sound('byebye.mp3')
hit_sound = pygame.mixer.Sound('hit_12.wav')
win_sound = pygame.mixer.Sound('win-tune.wav')
pause_sound = pygame.mixer.Sound('pause.wav')

def update_scores():
    canvas.itemconfig(player1_text, text="Player 1: " + str(player1_score))
    canvas.itemconfig(player2_text, text="Player 2: " + str(player2_score))

def create_puck(canvas, position, width, color):
    x, y = position
    return canvas.create_oval(x - width, y - width, x + width, y + width, fill=color, outline="black")

def create_paddle(canvas, position, width, color):
    x, y = position
    paddle = canvas.create_oval(x - width, y - width, x + width, y + width, fill=color, outline="black")
    return paddle

def generate_powerup(player):
    if(player):
         canvas.itemconfig(player1_pu, text="Use Powerup!")
    else:
         canvas.itemconfig(player2_pu, text="Use Powerup!")

def reset_player_disabled(player):
    global player1_disabled, player2_disabled
    if(player):
        player1_disabled = False
    else:
        player2_disabled = False

def reset_game():
    global player1_score, player2_score
    player1_score = 0
    player2_score = 0
    update_scores()
    canvas.itemconfig(player2_pu, text="No Powerups :(")
    canvas.itemconfig(player1_pu, text="No Powerups :(")
    reset_puck()

def use_powerup(player):
    global player1_disabled, player2_disabled
    if player:
        if canvas.itemcget(player2_pu, "text") == "Use Powerup!":
            powerup_sound.play()
            canvas.itemconfig(player2_pu, text="No Powerups :(")
            powerup_sound.play()
            player2_disabled = True
            canvas.after(5000, lambda: reset_player_disabled(0))
    else:
        if canvas.itemcget(player1_pu, "text") == "Use Powerup!":
            powerup_sound.play()
            canvas.itemconfig(player1_pu, text="No Powerups :(")
            powerup_sound.play()
            player1_disabled = True
            canvas.after(5000, lambda: reset_player_disabled(1))

def move_puck():
    global dx, dy, player1_score, player2_score, paused, winscreen
    if not paused and not winscreen and not titlescreen:
        x, y, _, _ = canvas.coords(puck)

        dx *= 0.999
        dy *= 0.999

        if x + dx < 0 and 130 < y + dy < 270:
            player2_score += 1
            score_sound.play()
            update_scores()
            if player2_score % 2 == 0:
                generate_powerup(0)
            if player2_score % 5 == 0:
                win_sound.play()
                winscreen = True
            reset_puck()

        if x + dx > 600 and 130 < y + dy < 270:
            player1_score += 1
            score_sound.play()
            update_scores()
            if player1_score % 2 == 0:
                generate_powerup(1)
            if player1_score % 5 == 0:
                win_sound.play()
                winscreen = True
            reset_puck()

        if x + dx < 0 or x + dx > 600:
            dx = -dx

        if y + dy < 0 or y + dy > 400:
            dy = -dy

        paddle1_coords = canvas.coords(paddle1)
        if paddle1_coords[0] - 20 < x + dx < paddle1_coords[2] and paddle1_coords[1] - 5 < y + dy < paddle1_coords[3] + 5:
            hit_sound.play()
            dx = -dx
            if dx == 0:
                dx = random.uniform(-1,1)
            dy = random.uniform(-8, 8) 
            dx *= 1.1
            dy *= 1.1

        paddle2_coords = canvas.coords(paddle2)
        if paddle2_coords[0] - 20 < x + dx < paddle2_coords[2] and paddle2_coords[1] - 5 < y + dy < paddle2_coords[3] + 5:
            hit_sound.play()
            dx = -dx
            if dx == 0:
                dx = random.uniform(-1,1)
            dy = random.uniform(-8, 8)
            dx *= 1.1
            dy *= 1.1

        canvas.move(puck, dx, dy)
    
    root.after(20, move_puck)




def move_paddle(x, y):
    global player1_disabled
    if(player1_disabled == False):
        min_x, max_x = 320, 590
        min_y, max_y = 20, 400

        if x < min_x:
            x = min_x
        elif x > max_x:
            x = max_x
        if y < min_y:
            y = min_y
        elif y > max_y:
            y = max_y


        canvas.coords(paddle1, x - 20, y - 20, x + 20, y + 20)


def move_paddle2(x, y):
    global player2_disabled
    if(player2_disabled == False):
        min_x, max_x = 0, 280
        min_y, max_y = 20, 400

        if x < min_x:
            x = min_x
        elif x > max_x:
            x = max_x
        if y < min_y:
            y = min_y
        elif y > max_y:
            y = max_y

        canvas.coords(paddle2, x - 20, y - 20, x + 20, y + 20)

def reset_puck():
    global dx, dy
    canvas.coords(puck, 300, 200, 320, 220)
    canvas.coords(paddle1, 480, 180, 520, 220)
    canvas.coords(paddle2, 80, 180, 120, 220)
    dx = 6
    dy = 6

def reset_circles():
    global circle, circle2
    canvas.coords(circle2, 480, 180, 500, 200)
    canvas.coords(circle, 80, 180, 100, 200)


def move_circle(x, y):
    global paused, circle
    if paused or winscreen or titlescreen:
        min_x, max_x = 0, 600
        min_y, max_y = 0, 400

        if x < min_x:
            x = min_x
        elif x > max_x:
            x = max_x
        if y < min_y:
            y = min_y
        elif y > max_y:
            y = max_y

        canvas.coords(circle, x - 10, y - 10, x + 10, y + 10)
        
def move_circle2(x, y):
    global paused, circle2
    if paused or winscreen or titlescreen:
        min_x, max_x = 0, 600
        min_y, max_y = 0, 400

        if x < min_x:
            x = min_x
        elif x > max_x:
            x = max_x
        if y < min_y:
            y = min_y
        elif y > max_y:
            y = max_y

        canvas.coords(circle2, x - 10, y - 10, x + 10, y + 10)


canvas.create_rectangle(0, 150, 40, 250, fill="white", outline="black")
canvas.create_rectangle(560, 150, 600, 250, fill="white", outline="black")

solid_line = canvas.create_line(0, 0, 0, 150, fill="black", width=15)
solid_line = canvas.create_line(0, 250, 0, 400, fill="black", width=15)
solid_line = canvas.create_line(600, 0, 600, 150, fill="black", width=5)
solid_line = canvas.create_line(600, 250, 600, 400, fill="black", width=5)

middle_line = canvas.create_line(300, 0, 300, 400, fill="black", dash=(4, 4))
center_circle = canvas.create_oval(290, 190, 310, 210, outline="black")

paddle1 = create_paddle(canvas, (500, 200), 20, "orange")
paddle2 = create_paddle(canvas, (100, 200), 20, "light blue")
puck = create_puck(canvas, (300, 200), 10, "yellow")

pause1 = canvas.create_rectangle(0, 0, 600, 400, fill="black", outline="")
pause2 = canvas.create_text(300, 200, text="PAUSED", fill="white", font=("Press Start 2P", 40))
play_rectangle = canvas.create_rectangle(280, 260, 320, 300, outline="black", fill="white")
play_button_text = canvas.create_text(300, 280, text="▶", fill="grey", font=("Press Start 2P", 40))

winbg = canvas.create_rectangle(0, 0, 600, 400, fill="black", outline="")
winrect = canvas.create_rectangle(240, 260, 360, 300, outline="black", fill="white")
wintext1 = canvas.create_text(300, 200, text="Player 1 Wins", fill="white", font=("Press Start 2P", 40))
wintext2 = canvas.create_text(300, 200, text="Player 2 Wins", fill="white", font=("Press Start 2P", 40))
restart_button = canvas.create_text(300, 280, text="Restart", fill="grey", font=("Press Start 2P", 20))

titlebg = canvas.create_rectangle(0, 0, 600, 400, fill="black", outline="")
titletext = canvas.create_text(300, 200, text="Air Hockey", fill="white", font=("Press Start 2P", 40))
titlerect = canvas.create_rectangle(240, 260, 360, 300, outline="black", fill="white")
start_button = canvas.create_text(300, 280, text="Start", fill="grey", font=("Press Start 2P", 20))

quitrect = canvas.create_rectangle(240, 320, 360, 360, outline="black", fill="white")
quit_button = canvas.create_text(300, 340, text="Quit", fill="grey", font=("Press Start 2P", 20))

circle = canvas.create_oval(290, 190, 310, 210, fill="light blue", outline="black")
circle2 = canvas.create_oval(290, 190, 310, 210, fill="orange", outline="black")

reset_circles()

def capture_video():
    global paused, winscreen, winscreen1, winscreen2, titlescreen, quit_game, powerup_flag
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    last_face_detection_time = time.time()
            
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hands, _ = detector.findHands(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            last_face_detection_time = time.time()
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        if time.time() - last_face_detection_time > 2.0:
            if not paused:
                pause_sound.play()
                paused = True

        if hands:
            for hand in hands:
                fingers = detector.fingersUp(hand)
                if (hand["type"] == "Left" or hand["type"] == "Right") and all(fingers[i] == 1 for i in [0, 1, 2, 3, 4]):
                    if winscreen is False and titlescreen is False and paused is False:
                        reset_circles()
                        paused = True
                        pause_sound.play()
                elif (hand["type"] == "Left") and fingers[1] == 1 and fingers[2] == 1  and fingers[3] == 1 and all(fingers[i] == 0 for i in [0, 4]):
                    if paused is False and titlescreen is False and winscreen is False:
                        reset_circles()
                        winscreen = True
                        if winscreen1 is False:
                            winscreen2 = True
                        win_sound.play()
                elif (hand["type"] == "Right") and fingers[1] == 1 and fingers[2] == 1  and fingers[3] == 1 and all(fingers[i] == 0 for i in [0, 4]):
                    if paused is False and titlescreen is False and winscreen is False:
                        reset_circles()
                        winscreen = True
                        if winscreen1 is False:
                            winscreen1 = True
                        win_sound.play()
                elif (paused or winscreen or titlescreen) and (hand["type"] == "Left") and fingers[1] == 1 and all(fingers[i] == 0 for i in [0, 2, 3, 4]):
                    x = int(hand["lmList"][8][0])
                    y = int(hand["lmList"][8][1])
                    move_circle(x, y)
                elif (paused or winscreen or titlescreen) and (hand["type"] == "Right") and fingers[1] == 1 and all(fingers[i] == 0 for i in [0, 2, 3, 4]):
                    x = int(hand["lmList"][8][0])
                    y = int(hand["lmList"][8][1])
                    move_circle2(x, y)
                elif (paused or winscreen or titlescreen) and (hand["type"] == "Left" or hand["type"] == "Right"):
                    thumb_tip = hand["lmList"][4]
                    index_tip = hand["lmList"][8]
                    distance = math.sqrt((thumb_tip[0] - index_tip[0])**2 + (thumb_tip[1] - index_tip[1])**2)
                    pinch_threshold = 20
                    circle_coords = canvas.coords(circle)
                    circle2_coords = canvas.coords(circle2)
                    play_button_coords = canvas.coords(play_rectangle)
                    restart_button_coords = canvas.coords(winrect)
                    start_button_coords = canvas.coords(titlerect)
                    quit_button_coords = canvas.coords(quitrect)
                    if paused and distance < pinch_threshold and (play_button_coords[0] - 10 <= circle_coords[0] <= play_button_coords[2] + 10 and play_button_coords[1] - 10  <= circle_coords[1] <= play_button_coords[3] + 10
                    or play_button_coords[0] <= circle2_coords[0] <= play_button_coords[2] and play_button_coords[1] <= circle2_coords[1] <= play_button_coords[3]):
                        button_sound.play()
                        paused = False
                    if winscreen and distance < pinch_threshold and (restart_button_coords[0] - 10 <= circle_coords[0] <= restart_button_coords[2] + 10 and restart_button_coords[1] - 10  <= circle_coords[1] <= restart_button_coords[3] + 10
                    or restart_button_coords[0] <= circle2_coords[0] <= restart_button_coords[2] and restart_button_coords[1] <= circle2_coords[1] <= restart_button_coords[3]):
                        button_sound.play()
                        winscreen = False
                        reset_game()
                        reset_puck()
                        winscreen1 = False
                        winscreen2 = False
                    if titlescreen and distance < pinch_threshold and (start_button_coords[0] - 10 <= circle_coords[0] <= start_button_coords[2] + 10 and start_button_coords[1] - 10  <= circle_coords[1] <= start_button_coords[3] + 10
                    or start_button_coords[0] <= circle2_coords[0] <= start_button_coords[2] and start_button_coords[1] <= circle2_coords[1] <= start_button_coords[3]):
                        titlescreen = False
                        button_sound.play()
                    if distance < pinch_threshold and (quit_button_coords[0] - 10 <= circle_coords[0] <= quit_button_coords[2] + 10 and quit_button_coords[1] - 10  <= circle_coords[1] <= quit_button_coords[3] + 10
                    or quit_button_coords[0] <= circle2_coords[0] <= quit_button_coords[2] and quit_button_coords[1] <= circle2_coords[1] <= quit_button_coords[3]):
                        quit_game = True
                        button_sound.play()
                elif hand["type"] == "Right" and fingers[1] == 1 and all(fingers[i] == 0 for i in [0, 2, 3, 4]):
                    x = int(hand["lmList"][8][0])
                    y = int(hand["lmList"][8][1])
                    move_paddle(x, y)
                elif hand["type"] == "Left" and fingers[1] == 1 and all(fingers[i] == 0 for i in [0, 2, 3, 4]):
                    x = int(hand["lmList"][8][0])
                    y = int(hand["lmList"][8][1])
                    move_paddle2(x, y)
                elif hand["type"] == "Right" and all(fingers[i] == 0 for i in [0, 1, 2, 3, 4]):
                    if paused is False and titlescreen is False and winscreen is False:
                        use_powerup(1)
                elif hand["type"] == "Left" and all(fingers[i] == 0 for i in [0, 1, 2, 3, 4]):
                    if paused is False and titlescreen is False and winscreen is False:
                        use_powerup(0)

                if quit_game:
                    root.quit()

        if paused:
            canvas.itemconfig(pause1, state="normal")
            canvas.itemconfig(pause2, state="normal")
            canvas.itemconfig(play_rectangle, state="normal")
            canvas.itemconfig(play_button_text, state="normal")
        else:
            canvas.itemconfig(pause1, state="hidden")
            canvas.itemconfig(pause2, state="hidden")
            canvas.itemconfig(play_rectangle, state="hidden")
            canvas.itemconfig(play_button_text, state="hidden")

        if winscreen:
            if player1_score == 5 or winscreen1 and winscreen2 is False:
                canvas.itemconfig(wintext1, state="normal")

            if player2_score == 5 or winscreen2 and winscreen1 is False:
                canvas.itemconfig(wintext2, state="normal")

            canvas.itemconfig(winbg, state="normal")
            canvas.itemconfig(winrect, state="normal")
            canvas.itemconfig(restart_button, state="normal")
        else:
            canvas.itemconfig(wintext1, state="hidden")
            canvas.itemconfig(wintext2, state="hidden")
            canvas.itemconfig(winrect, state="hidden")
            canvas.itemconfig(winbg, state="hidden")
            canvas.itemconfig(restart_button, state="hidden")

        if titlescreen:

            canvas.itemconfig(titlebg, state="normal")
            canvas.itemconfig(titletext, state="normal")
            canvas.itemconfig(titlerect, state="normal")
            canvas.itemconfig(start_button, state="normal")
        else:
            titlescreen = False
            canvas.itemconfig(titlebg, state="hidden")
            canvas.itemconfig(titletext, state="hidden")
            canvas.itemconfig(titlerect, state="hidden")
            canvas.itemconfig(start_button, state="hidden")


        if winscreen == False and paused == False and titlescreen == False:
            canvas.itemconfig(circle, state="hidden")
            canvas.itemconfig(circle2, state="hidden")
            canvas.itemconfig(quitrect, state="hidden")
            canvas.itemconfig(quit_button, state="hidden")
        else:
            canvas.itemconfig(circle, state="normal")
            canvas.itemconfig(circle2, state="normal")
            canvas.itemconfig(quitrect, state="normal")
            canvas.itemconfig(quit_button, state="normal")
        if quit_game is True:
            break

        
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

dx = 6
dy = 6
move_puck()

root.protocol("WM_DELETE_WINDOW", capture_video)

cap = cv2.VideoCapture(0)
video_thread = threading.Thread(target=capture_video)
video_thread.start()

root.mainloop()