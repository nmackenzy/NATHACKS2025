import json
import numpy as np
import ollama
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

plant_model = load_model('plant_classifier.h5')

plant_class_names = ['Apple', 'Blueberry', 'Cherry_(including_sour)', 'Corn_(maize)', 
                    'Grape', 'Orange', 'Peach', 'Pepper,_bell', 'Potato', 
                    'Raspberry', 'Soybean', 'Squash', 'Strawberry', 'Tomato']

disease_class_map = {
    'Apple': ['Apple_scab', 'Black_rot', 'Cedar_apple_rust', 'healthy'],
    'Blueberry': ['healthy'],
    'Cherry_(including_sour)': ['Powdery_mildew', 'healthy'],
    'Corn_(maize)': ['Cercospora_leaf_spot Gray_leaf_spot', 'Common_rust_', 'Northern_Leaf_Blight', 'healthy'],
    'Grape': ['Black_rot', 'Esca_(Black_Measles)', 'Leaf_blight_(Isariopsis_Leaf_Spot)', 'healthy'],
    'Orange': ['Haunglongbing_(Citrus_greening)'],
    'Peach': ['Bacterial_spot', 'healthy'],
    'Pepper,_bell': ['Bacterial_spot', 'healthy'],
    'Potato': ['Early_blight', 'Late_blight', 'healthy'],
    'Raspberry': ['healthy'],
    'Soybean': ['healthy'],
    'Squash': ['Powdery_mildew'],
    'Strawberry': ['Leaf_scorch', 'healthy'],
    'Tomato': [
        'Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold',
        'Septoria_leaf_spot', 'Spider_mites Two-spotted_spider_mite',
        'Target_Spot', 'Tomato_Yellow_Leaf_Curl_Virus',
        'Tomato_mosaic_virus', 'healthy'
    ]
}

# cache disease models
disease_models = {}

with open('plant_disease_solutions.json', 'r') as f:
    disease_info_list = json.load(f)

def preprocess_image(img_path, target_size=(128, 128)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array / 255.0

def identify_species(image_path):
    img = preprocess_image(image_path)
    preds = plant_model.predict(img)
    class_idx = np.argmax(preds)
    return plant_class_names[class_idx]

def diagnose_disease(image_path, plant_name):
    model_path = f"{plant_name}_disease_classifier.h5"
    if plant_name not in disease_models:
        if not os.path.exists(model_path):
            return {
                "disease": "Unknown",
                "cause": "Model not found",
                "solution": "Train model for this plant first."
            }
        disease_models[plant_name] = load_model(model_path)

    img = preprocess_image(image_path)
    preds = disease_models[plant_name].predict(img)
    class_idx = np.argmax(preds)

    # use disease_class_map for class names
    class_names = disease_class_map.get(plant_name, ["healthy"])
    disease_label = class_names[class_idx]

    info = get_disease_info(plant_name, disease_label)
    return info

def paraphrase_solution(plant, disease, cause, solution):
    print("func entered")
    prompt = (f"Plant: {plant}. Disease: {disease}. Cause: {cause}. " f"Solution: {solution}. Write a concise 2-sentence treatment guide.")
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': 'Provide ONLY the 2-sentence treatment guide. Do not say "Here is the guide" or "Sure."'},
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content'].strip()
    except Exception:
        print("failed")
        return solution # fallback to raw text if Ollama is offline

def paraphrase_diagnosis(plant, disease, description):
    prompt = f"Plant: {plant}. Condition: {disease}. Description: {description}. Summarize the diagnosis in one clear sentence."
    try:
        response = ollama.chat(model='llama3', messages=[
            {'role': 'system', 'content': 'Provide ONLY a one-sentence diagnostic summary. No conversational filler.'},
            {'role': 'user', 'content': prompt}
        ])
        return response['message']['content'].strip()
    except Exception:
        return description # fallback to raw text if Ollama is offline

def get_disease_info(plant_name, disease_label):
    for entry in disease_info_list:
        if entry["Plant"] == plant_name and entry["Disease"] == disease_label:
            final_sol = paraphrase_solution(plant_name, disease_label, entry.get("Causes"), entry.get("Cures/Management")) if disease_label != "healthy" else entry.get("Cures/Management")
            final_desc = paraphrase_diagnosis(plant_name, disease_label, entry.get("Description", ""))
            return {
                "disease": entry["Disease"],
                "cause": entry.get("Causes", "Unknown"),
                "solution": final_sol,
                "description": final_desc,
                "reference": entry.get("Reference", "")
            }

    if disease_label == "healthy":
        return {
            "disease": "healthy",
            "cause": "No disease present",
            "solution": "Maintain proper care and monitoring",
            "description": "The plant appears to be healthy",
            "reference": ""
        }
    
    return {
        "disease": disease_label,
        "cause": "Not found in dataset",
        "solution": "No solution available"
    }