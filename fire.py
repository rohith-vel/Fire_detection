import cv2
import threading
import playsound
import smtplib

fire_cascade = cv2.CascadeClassifier(
    'fire_detection_cascade_model.xml')
# File is also provided with the code.

vid = cv2.VideoCapture(0)
runOnce = False


def play_alarm_sound_function():  # defined function to play alarm post fire detection using threading
    playsound.playsound('fire_alarm.mp3', True)  # to play alarm # mp3 audio file is also provided with the code.
    print("Fire alarm end")  # to print in console


def send_mail_function():  # defined function to send mail post fire detection using threading

    recipients = "rohithvr29@gmail.com"  # recipients mail
    recipients = recipients.lower()  # To lower case mail

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("rohithvr29@gmail.com", 'batman@14')
        server.sendmail('add recipients mail', recipients,
                        "Warning fire accident has been reported")
        print("Alert mail sent successfully to {}".format(recipients))
        server.close()

    except Exception as e:
        print(e)  # To print error if any


while True:
    Alarm_Status = False
    ret, frame = vid.read()  # Value in ret is True # To read video frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # To convert frame into gray color
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)  # to provide frame resolution

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread

        if not runOnce:
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start()  # To call alarm thread
            runOnce = True
        if runOnce:
            print("Mail is already sent once")
            runOnce = True

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break