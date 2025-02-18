import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image


# Non-Maximum Suppression
def non_max_suppression(predictions, iou_threshold=0.4):
    """
    Perform Non-Maximum Suppression to remove redundant overlapping boxes.
    """
    if len(predictions) == 0:
        return []
    
    # Convert predictions to numpy for easier processing
    boxes = np.array([pred['bbox'] for pred in predictions])
    scores = np.array([pred['confidence'] for pred in predictions])
    class_ids = np.array([pred['class_id'] for pred in predictions])

    # Compute areas of bounding boxes
    x1, y1, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    areas = w * h

    # Sort boxes by confidence scores (highest to lowest)
    sorted_indices = np.argsort(scores)[::-1]

    keep = []  # Indices of boxes to keep
    while sorted_indices.size > 0:
        # Take the box with the highest confidence
        current = sorted_indices[0]
        keep.append(current)

        # Compute IoU of this box with the others
        xx1 = np.maximum(x1[current], x1[sorted_indices[1:]])
        yy1 = np.maximum(y1[current], y1[sorted_indices[1:]])
        xx2 = np.minimum(x1[current] + w[current], x1[sorted_indices[1:]] + w[sorted_indices[1:]])
        yy2 = np.minimum(y1[current] + h[current], y1[sorted_indices[1:]] + h[sorted_indices[1:]])

        inter_width = np.maximum(0, xx2 - xx1)
        inter_height = np.maximum(0, yy2 - yy1)
        inter_area = inter_width * inter_height
        union_area = areas[current] + areas[sorted_indices[1:]] - inter_area

        iou = inter_area / union_area

        # Remove indices with IoU above the threshold
        sorted_indices = sorted_indices[1:][iou <= iou_threshold]

    # Return the filtered predictions
    return [predictions[i] for i in keep]


# Load the model
interpreter = tf.lite.Interpreter(model_path='best-fp16.tflite')
interpreter.allocate_tensors()

# Streamlit interface
st.title("Animal Footprint Classification")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    
    # Preprocess the image
    image = np.array(image.resize((640, 640)))  # Resize to match the input size expected by the model
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = (image / 255.0).astype(np.float32)  # Normalize the image

    # # Set input tensor
    # input_details = interpreter.get_input_details()
    # interpreter.set_tensor(input_details[0]['index'], image)

    # # Run inference
    # interpreter.invoke()

    # # Get output
    # output_details = interpreter.get_output_details()
    # result = interpreter.get_tensor(output_details[0]['index'])

    # st.write("Prediction:", result)  # Display the prediction
    # Set input tensor
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]['index'], image)

    # Run inference
    interpreter.invoke()

    # Get output
    output_details = interpreter.get_output_details()
    result = interpreter.get_tensor(output_details[0]['index'])  # Tensor shape: (1, 25200, 10)

    # Process predictions
    # Process predictions
    predictions = result[0]  # Remove batch dimension
    confidence_threshold = 0.5
    predictions = predictions[predictions[:, 4] > confidence_threshold]

    # Define class names
    class_names = ['bear', 'canid', 'deer', 'felid', 'mustelid']

    final_predictions = []
    for pred in predictions:
        x, y, w, h, conf, *class_probs = pred
        class_id = np.argmax(class_probs)
        final_predictions.append({
            "class_id": int(class_id),
            "confidence": float(conf),
            "bbox": [float(x), float(y), float(w), float(h)]
        })

    # Apply Non-Maximum Suppression (NMS)
    filtered_predictions = non_max_suppression(final_predictions)

    # Display predictions
    # Display predictions with descriptive sentences
    if filtered_predictions:
        st.write("Detected animal footprints:")
        for pred in filtered_predictions:
            class_name = class_names[pred['class_id']]  # Map class ID to class name
            st.write(f"- A footprint of a {class_name} was detected.")
            st.write(f"- Confidence: {pred['confidence']:.2f}")
            
    else:
        st.write("No animal footprints were detected in the image.")