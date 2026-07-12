import numpy as np
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os

class BiomarkerDiseaseClassifier:
    """
    AI model that predicts neurodegenerative disease type
    from biomarker measurements.
    
    Biological context:
    The model learns from patterns in these biomarkers:
    - amyloid_beta_42: Lower = more Alzheimer's risk
    - phospho_tau_181: Higher = more Alzheimer's risk  
    - neurofilament_light: Higher = more neurodegeneration
    - alpha_synuclein: Higher = more Parkinson's risk
    - dopamine_transporter: Lower = more Parkinson's risk
    - sod1_activity: Lower = more ALS risk
    - huntingtin_mutant: Higher = more Huntington's risk
    - glial_fibrillary: Higher = more brain injury
    - brain_derived_nf: Lower = less neuroprotection
    - inflammatory_index: Higher = more neuroinflammation
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        self.scaler = StandardScaler()
        self.disease_labels = [
            "Alzheimer's Disease",
            "Parkinson's Disease", 
            "ALS",
            "Huntington's Disease"
        ]
        self.feature_names = [
            "amyloid_beta_42",
            "phospho_tau_181",
            "neurofilament_light",
            "alpha_synuclein",
            "dopamine_transporter",
            "sod1_activity",
            "huntingtin_mutant",
            "glial_fibrillary_acidic_protein",
            "brain_derived_neurotrophic_factor",
            "inflammatory_index"
        ]
        self.is_trained = False
        self._train_on_synthetic_data()
    
    def _generate_synthetic_data(self, n_samples: int = 1000):
        """
        Generate synthetic biomarker data for training.
        
        In a real research setting, this would come from:
        - ADNI (Alzheimer's Disease Neuroimaging Initiative)
        - PPMI (Parkinson's Progression Markers Initiative)
        - ALS natural history studies
        
        Our synthetic data follows known biological patterns:
        - Alzheimer's: low amyloid_beta, high tau
        - Parkinson's: high alpha_synuclein, low dopamine_transporter
        - ALS: low sod1_activity, very high neurofilament
        - Huntington's: high huntingtin_mutant, high inflammatory
        """
        np.random.seed(42)
        X = []
        y = []
        
        samples_per_class = n_samples // 4
        
        for disease_idx in range(4):
            for _ in range(samples_per_class):
                
                if disease_idx == 0:  # Alzheimer's
                    features = [
                        np.random.normal(500, 100),   # amyloid_beta LOW
                        np.random.normal(400, 80),    # phospho_tau HIGH
                        np.random.normal(1800, 300),  # neurofilament HIGH
                        np.random.normal(1200, 200),  # alpha_synuclein normal
                        np.random.normal(70, 10),     # dopamine_transporter normal
                        np.random.normal(85, 15),     # sod1_activity normal
                        np.random.normal(50, 10),     # huntingtin_mutant low
                        np.random.normal(200, 40),    # GFAP HIGH
                        np.random.normal(15, 3),      # BDNF LOW
                        np.random.normal(7, 1.5),     # inflammatory HIGH
                    ]
                    
                elif disease_idx == 1:  # Parkinson's
                    features = [
                        np.random.normal(1200, 200),  # amyloid_beta normal
                        np.random.normal(180, 40),    # phospho_tau normal
                        np.random.normal(1400, 250),  # neurofilament elevated
                        np.random.normal(2800, 400),  # alpha_synuclein VERY HIGH
                        np.random.normal(35, 8),      # dopamine_transporter VERY LOW
                        np.random.normal(90, 15),     # sod1_activity normal
                        np.random.normal(45, 10),     # huntingtin_mutant low
                        np.random.normal(150, 30),    # GFAP elevated
                        np.random.normal(18, 4),      # BDNF normal
                        np.random.normal(5, 1),       # inflammatory moderate
                    ]
                    
                elif disease_idx == 2:  # ALS
                    features = [
                        np.random.normal(1100, 200),  # amyloid_beta normal
                        np.random.normal(170, 35),    # phospho_tau normal
                        np.random.normal(4500, 800),  # neurofilament EXTREMELY HIGH
                        np.random.normal(1100, 200),  # alpha_synuclein normal
                        np.random.normal(75, 12),     # dopamine_transporter normal
                        np.random.normal(30, 8),      # sod1_activity VERY LOW
                        np.random.normal(48, 10),     # huntingtin_mutant low
                        np.random.normal(350, 60),    # GFAP VERY HIGH
                        np.random.normal(12, 3),      # BDNF low
                        np.random.normal(8, 1.5),     # inflammatory HIGH
                    ]
                    
                else:  # Huntington's
                    features = [
                        np.random.normal(1150, 200),  # amyloid_beta normal
                        np.random.normal(175, 35),    # phospho_tau normal
                        np.random.normal(2200, 400),  # neurofilament HIGH
                        np.random.normal(1300, 200),  # alpha_synuclein normal
                        np.random.normal(68, 12),     # dopamine_transporter slightly low
                        np.random.normal(88, 15),     # sod1_activity normal
                        np.random.normal(850, 150),   # huntingtin_mutant VERY HIGH
                        np.random.normal(180, 35),    # GFAP elevated
                        np.random.normal(14, 3),      # BDNF low
                        np.random.normal(9, 1.5),     # inflammatory VERY HIGH
                    ]
                
                X.append(features)
                y.append(disease_idx)
        
        return np.array(X), np.array(y)
    
    def _train_on_synthetic_data(self):
        """Train the model on synthetic biological data"""
        X, y = self._generate_synthetic_data(1000)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model.fit(X_train_scaled, y_train)
        
        y_pred = self.model.predict(X_test_scaled)
        self.accuracy = accuracy_score(y_test, y_pred)
        self.is_trained = True
        
        print(f"Model trained. Accuracy: {self.accuracy:.2%}")
    
    def predict(self, biomarkers: dict) -> dict:
        """
        Predict disease from biomarker levels.
        
        Input: dictionary of biomarker name -> value
        Output: prediction with probabilities and explanation
        """
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        features = []
        for name in self.feature_names:
            features.append(biomarkers.get(name, 0))
        
        X = np.array(features).reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        
        prediction_idx = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        
        disease_probs = {
            self.disease_labels[i]: round(float(probabilities[i]) * 100, 1)
            for i in range(len(self.disease_labels))
        }
        
        importances = self.model.feature_importances_
        feature_importance = {
            self.feature_names[i]: round(float(importances[i]) * 100, 2)
            for i in range(len(self.feature_names))
        }
        
        sorted_importance = dict(
            sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        )
        
        predicted_disease = self.disease_labels[prediction_idx]
        confidence = round(float(probabilities[prediction_idx]) * 100, 1)
        
        explanation = self._generate_explanation(
            predicted_disease, biomarkers, sorted_importance
        )
        
        return {
            "prediction": predicted_disease,
            "confidence_percent": confidence,
            "all_probabilities": disease_probs,
            "top_features": dict(list(sorted_importance.items())[:5]),
            "explanation": explanation,
            "model_accuracy": round(self.accuracy * 100, 1),
            "disclaimer": "This is a research tool only. Not for clinical diagnosis."
        }
    
    def _generate_explanation(self, disease: str, biomarkers: dict, importances: dict) -> str:
        """Generate a human-readable explanation of the prediction"""
        top_feature = list(importances.keys())[0]
        top_value = biomarkers.get(top_feature, "unknown")
        
        explanations = {
            "Alzheimer's Disease": f"The biomarker pattern suggests Alzheimer's Disease. Key indicator: {top_feature} = {top_value}. Low amyloid-beta combined with elevated tau proteins is characteristic of Alzheimer's pathology.",
            "Parkinson's Disease": f"The biomarker pattern suggests Parkinson's Disease. Key indicator: {top_feature} = {top_value}. Elevated alpha-synuclein with reduced dopamine transporter binding is characteristic of Parkinson's pathology.",
            "ALS": f"The biomarker pattern suggests ALS. Key indicator: {top_feature} = {top_value}. Extremely elevated neurofilament light chain combined with reduced SOD1 activity is characteristic of motor neuron degeneration.",
            "Huntington's Disease": f"The biomarker pattern suggests Huntington's Disease. Key indicator: {top_feature} = {top_value}. Elevated mutant huntingtin protein with high inflammatory index is characteristic of Huntington's pathology."
        }
        
        return explanations.get(disease, "Pattern analysis complete.")


biomarker_classifier = BiomarkerDiseaseClassifier()