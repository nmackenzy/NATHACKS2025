# 🌿 Digital Garden

**Digital Garden** is a personal plant management app built with **Tkinter** and **TensorFlow/Keras**.  
It allows users to maintain a digital log of their real plants, automatically identifying each plant and diagnosing its health using **Convolutional Neural Networks (CNNs)**.

---

## 🧩 Features

### 🌱 Plant Management
- Add new plants by uploading an image.
- The app automatically identifies the plant species using a trained CNN model.
- Maintain a list of all your plants with thumbnails and names.

### 🧠 Machine Learning Integration
- **Plant Identification Model** – A CNN trained on the [New Plant Diseases Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset) identifies the plant type.
- **Disease Detection Models** – For each plant species, separate CNN models classify whether the plant is:
  - Healthy
  - Affected by a specific disease (e.g., Mosaic Virus, Rust, etc.)
- The app automatically logs diagnosis results, potential causes, and suggested treatments.

### 📅 Digital Garden Log
- Each time a new image is uploaded for a plant:
  - The app re-runs disease detection.
  - Adds a timestamped entry to the **Digital Garden Log** showing:
    - Date
    - Diagnosis result
    - Cause
    - Recommended next steps or treatment.

### 🪴 Clean and Simple Interface
- Built using **Tkinter**.
- User-friendly layout featuring:
  - A sidebar with a list of plants.
  - Central image upload and diagnosis area.
  - Scrollable plant health log.
- Supports adding multiple plants and deleting them when needed.

---

## 🗃️ Data Model (ER Diagram)

**Entity Relationships:**

### 1. `Plants`
| Field | Description |
|-------|--------------|
| Plant ID | Unique identifier (Primary Key) |
| Plant name | User-defined name |
| Species | Predicted species name |
| Latest plant image (path) | Path to latest uploaded image |

**Primary Key (PK):** `Plant ID`

---

### 2. `PlantLogs`
| Field | Description |
|--------|-------------|
| Timestamp | Time of diagnosis (Primary Key) |
| Plant ID | References `Plants(Plant ID)` |
| Disease diagnosed | Predicted disease or “Healthy” |
| Cause | Possible cause of disease |
| Solution | Suggested next steps or treatments |

**Primary Key (PK):** `Timestamp`  
**Foreign Key (FK):** `Plant ID`

---

## 🧮 Machine Learning Models

### 1. **Plant Classifier**
- Model: `plant_classifier.h5`
- Purpose: Identifies plant species.
- Output: Species name (e.g., Tomato, Corn, Grape, etc.)
- Dataset: [New Plant Diseases Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)

### 2. **Disease Classifiers**
- One model per plant species (e.g., `tomato_disease_model.h5`, `grape_disease_model.h5`, etc.)
- Each model classifies plant health conditions:
  - Healthy
  - Specific diseases (e.g., Leaf Spot, Mosaic Virus, Rust)
- Outputs: Disease name and confidence score.

---

