# import the opencv library
import cv2

# define a video capture object
vid = cv2.VideoCapture(1 + cv2.CAP_DSHOW)

vid.set(cv2.CAP_PROP_POS_FRAMES, 1)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)

while True:

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow("frame", frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
