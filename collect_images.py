import cv2
import os


output_dir = "dataset"  
categories = ["EmptyPlate", "NonRecycled", "Recycled"] 
camera_index = 2 
frame_rate = 5  

# Make directoy
for category in categories:
    category_path = os.path.join(output_dir, category)
    os.makedirs(category_path, exist_ok=True)


# Check cam
camera = cv2.VideoCapture(camera_index)
if not camera.isOpened():
    print("Cam not working")
    exit()

saved_frames = {category: len(os.listdir(os.path.join(output_dir, category))) for category in categories}

try:
    current_category = 0
    print(f"Taking photo for category: {categories[current_category]}")

    while current_category < len(categories):
        ret, frame = camera.read()
        if not ret:
            print("")
            break

        # Show current class
        cv2.putText(frame, f"Category: {categories[current_category]} ({saved_frames[categories[current_category]]} images)",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Collecting Images", frame)

        key = cv2.waitKey(1) & 0xFF

        # save imgs
        if key == ord("s"):
            image_path = os.path.join(output_dir, categories[current_category], f"{saved_frames[categories[current_category]]:04d}.jpg")
            cv2.imwrite(image_path, frame)
            saved_frames[categories[current_category]] += 1
            print(f"Save at: {image_path}")

        if key == ord("n"):
            current_category += 1
            if current_category < len(categories):
                print(f"Moving to: {categories[current_category]}")
            else:
                print("All classes done")
                break

        if key == ord("q"):
            print("stop")
            break

finally:
    camera.release()
    cv2.destroyAllWindows()
