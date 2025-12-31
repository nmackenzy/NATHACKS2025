# Digital Garden

**Digital Garden** is a personal plant management application built with **CustomTkinter** and **TensorFlow/Keras**.  
It allows users to maintain a digital log of their real plants, automatically identifying each plant and diagnosing its health using **Convolutional Neural Networks (CNNs)**.

---

## Features

### Plant Management
- Add new plants by uploading an image.
- The app automatically identifies the plant species using a trained CNN model.
- Maintain a list of all plants with thumbnails and names.
- Supports adding and deleting plants.

### Machine Learning Integration
- **Plant Identification Model** – A CNN trained on the [New Plant Diseases Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset) identifies the plant species.
- **Disease Detection Models** – For each plant species, a separate CNN model classifies whether the plant is:
  - Healthy
  - Affected by a specific disease (e.g., Mosaic Virus, Rust, Leaf Spot)
- The app logs diagnosis results, potential causes, and suggested treatments.

### Digital Garden Log
- Each time a new image is uploaded for a plant:
  - Disease detection is re-run automatically.
  - A timestamped entry is added to the **Digital Garden Log**, including:
    - Date
    - Diagnosis result
    - Cause
    - Recommended next steps or treatment
- Logs allow users to track plant health changes over time.

### Clean and Simple Interface
- Built using **CustomTkinter**.
- User-friendly layout featuring:
  - A sidebar with a list of plants
  - A central image upload and diagnosis area
  - A scrollable plant health log
- Designed to remain lightweight while supporting multiple plants.

---

## Data Model (ER Diagram)

### Entity Relationships

### 1. `Plants`
| Field | Description |
|------|-------------|
| Plant ID | Unique identifier (Primary Key) |
| Plant name | User-defined name |
| Species | Predicted species name |
| Latest plant image (path) | Path to the most recently uploaded image |

**Primary Key (PK):** `Plant ID`

---

### 2. `PlantLogs`
| Field | Description |
|------|-------------|
| Timestamp | Time of diagnosis (Primary Key) |
| Plant ID | References `Plants(Plant ID)` |
| Disease diagnosed | Predicted disease or “Healthy” |
| Cause | Possible cause of disease |
| Solution | Suggested next steps or treatments |

**Primary Key (PK):** `Timestamp`  
**Foreign Key (FK):** `Plant ID`

---

## Machine Learning Models

### 1. Plant Classifier
- Model file: `plant_classifier.h5`
- Purpose: Identifies plant species
- Output: Species name (e.g., Tomato, Corn, Grape)
- Dataset: [New Plant Diseases Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)

### 2. Disease Classifiers
- One model per plant species (e.g., `tomato_disease_model.h5`, `grape_disease_model.h5`)
- Each model classifies:
  - Healthy plants
  - Species-specific diseases
- Output:
  - Disease label
  - Confidence score

### 3. LLM-Based Diagnosis and Treatment Paraphrasing
- A locally hosted LLM is used to rephrase diagnosis descriptions and treatment recommendations.
- The model generates:
  - A single-sentence diagnostic summary
  - A concise two-sentence treatment guide
- Structured disease data is retrieved first, then passed to the model for paraphrasing, following a retrieval-augmented pattern.
- If the LLM is unavailable, the app falls back to the original dataset text.

## Notes
- The `resources/` folder contains a Jupyter notebook for training the models and generating the required `.h5` files.  
- The notebook relies on the [New Plant Diseases Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset).
- The `tests/` folder provides sample images for testing and evaluation.

