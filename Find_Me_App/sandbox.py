# import face_recognition
#
# # Load the jpg files into numpy arrays
# biden_image = face_recognition.load_image_file("./dataset/known/bill.jpg")
# obama_image = face_recognition.load_image_file("./dataset/known/mark.jpg")
# unknown_image = face_recognition.load_image_file("./dataset/unknown/billuk.jpg")
# print(biden_image)
# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
# try:
#     biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
#     obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
#     unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
# except IndexError:
#     print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
#     quit()
#
# known_faces = [
#     biden_face_encoding,
#     obama_face_encoding
# ]
#
# # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
# results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
#
# print("Is the unknown face a picture of Biden? {}".format(results[0]))
# print("Is the unknown face a picture of Obama? {}".format(results[1]))
# print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
import face_recognition

# Load the known face and encode its features
known_face_image = face_recognition.load_image_file("./dataset/known/bill.jpg")
known_face_encoding = face_recognition.face_encodings(known_face_image)[0]

# Load and encode the target faces
target_images = [
    face_recognition.load_image_file("./dataset/unknown/billuk.jpg"),
    face_recognition.load_image_file("./dataset/unknown/muskuk.jpg"),
    face_recognition.load_image_file("./dataset/unknown/markuk.jpg")
]

# Set a similarity threshold (you can adjust this)
similarity_threshold = 0.6

# Compare the target faces with the known face
matches = []
for i, target_image in enumerate(target_images):
    target_encoding = face_recognition.face_encodings(target_image)[0]
    similarity = face_recognition.face_distance([known_face_encoding], target_encoding)
    if similarity < similarity_threshold:
        matches.append(f"Match found with target_face{i + 1}")

# Return matching results (if any)
if matches:
    for match in matches:
        print(match)
else:
    print("No matches found.")
