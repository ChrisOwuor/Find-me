# import cv2
# import face_recognition
#
# # Load the jpg file into a numpy array
# image = face_recognition.load_image_file("./dataset/unknown/markuk.jpg")
#
# # Find all the faces in the image using the default HOG-based model.
# # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# # See also: find_faces_in_picture_cnn.py
# face_locations = face_recognition.face_locations(image)
# # Load the image using OpenCV to draw rectangles
# image_cv2 = cv2.imread("./dataset/unknown/markuk.jpg")
#
# for face_location in face_locations:
#
#     # Print the location of each face in this image
#     top, right, bottom, left = face_location
#     print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
#
#     # Draw a rectangle around the detected face using OpenCV
#     color = (0, 255, 0)  # Green color in BGR
#     thickness = 2
#     image_cv2 = cv2.rectangle(image_cv2, (left, top), (right, bottom), color, thickness)
#
# # Display the image with rectangles around the detected faces
# cv2.imshow("Image with Detected Faces", image_cv2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
import face_recognition
known_image = face_recognition.load_image_file("./Fp_Imgs/bill2.jpg")
unknown_image = face_recognition.load_image_file("./Mp_Imgs/bill.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
print(results)