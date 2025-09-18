import onnxruntime
import numpy as np
import cv2
import os

# Vehicle class IDs in COCO (YOLOv5 class IDs)
vehicle_classes = {
    2: 'car',
    3: 'motorcycle',
    5: 'bus',
    7: 'truck'
}

# Hardcoded variable to control whether to display image with bounding boxes
SHOW_IMAGE = 0  # Set to 1 to show the image, 0 to disable showing the image

def count_vehicles_in_image(image_path, model_path="yolov5s.onnx", conf_threshold=0.4, iou_threshold=0.5):
    # Initialize the ONNX runtime session
    session = onnxruntime.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    input_name = session.get_inputs()[0].name
    
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read the image from {image_path}")

    # Resize to 640x352 (already assumed to be this size)
    resized = cv2.resize(image, (640, 352))

    # Preprocess the image (convert to RGB, HWC to CHW, normalize)
    img = resized[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, HWC to CHW
    img = np.ascontiguousarray(img).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Inference
    outputs = session.run(None, {input_name: img})
    predictions = outputs[0][0]  # YOLOv5 output shape: (N, 85)
    
    vehicle_count = {name: 0 for name in vehicle_classes.values()}

    # Process predictions
    boxes, confidences, class_ids = [], [], []
    for pred in predictions:
        x1, y1, x2, y2, conf = pred[:5]
        class_scores = pred[5:]
        class_id = int(np.argmax(class_scores))
        score = class_scores[class_id]

        # If the prediction is above the confidence threshold and is a vehicle class
        if conf * score > conf_threshold and class_id in vehicle_classes:
            boxes.append([x1, y1, x2, y2])
            confidences.append(conf * score)
            class_ids.append(class_id)

    # Apply Non-Maximum Suppression (NMS) to filter overlapping boxes
    boxes = np.array(boxes)
    confidences = np.array(confidences)
    class_ids = np.array(class_ids)
    
    indices = cv2.dnn.NMSBoxes(boxes.tolist(), confidences.tolist(), conf_threshold, iou_threshold)

    # Count vehicles
    for idx in indices.flatten():
        vehicle_name = vehicle_classes[class_ids[idx]]
        vehicle_count[vehicle_name] += 1
        
        # Optionally display the image with bounding boxes if SHOW_IMAGE is set to 1
        if SHOW_IMAGE == 1:
            x1, y1, x2, y2 = boxes[idx]
            color = (0, 255, 0)  # Green for bounding boxes
            cv2.rectangle(resized, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(resized, f"{vehicle_name} {int(confidences[idx] * 100)}%", 
                        (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Print results
    #for vehicle, count in vehicle_count.items():
    #    print(f"{vehicle}: {count}")

    # Show the image with bounding boxes (optional)
    if SHOW_IMAGE == 1:
        cv2.imshow("Image with Bounding Boxes", resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return vehicle_count
        
def main():
    # Get filename as input
    image_filename = "good photos/"+input("Enter the image filename (including path): ")+".jpg"

    # Ensure the image file exists
    if not os.path.exists(image_filename):
        print(f"Error: File '{image_filename}' does not exist!")
        return

    # Call the function to count vehicles
    count_vehicles_in_image(image_filename)

if __name__ == "__main__":
    while(True):
        main()
