import json
import logging
from typing import Dict, List, Optional
from transformers import pipeline
import torch

logger = logging.getLogger(__name__)

# Check for GPU availability
DEVICE = 0 if torch.cuda.is_available() else -1

class DocsExtractor:
    """Extract structured resume data using Phi-3 LLM and GLiNER NER"""

    def __init__(self, model_name: str = "microsoft/Phi-3-mini-4k-instruct"):
        """Initialize LLM pipeline for structured extraction"""
        try:
            self.llm_pipe = pipeline(
                "text-generation",
                model=model_name,
                device=DEVICE,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            )
            logger.info(f"Loaded LLM model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading LLM model: {e}")
            self.llm_pipe = None

        # Optional: Load GLiNER for NER
        try:
            from gliner import GLiNER
            self.ner_model = GLiNER.from_pretrained("urchade/gliner_base")
            logger.info("Loaded GLiNER NER model")
        except Exception as e:
            logger.warning(f"GLiNER not available: {e}")
            self.ner_model = None

    def extract_with_llm(self, resume_text: str) -> Dict:
        """Extract structured data from resume using Phi-3 LLM"""
        if not self.llm_pipe:
            logger.error("LLM pipeline not initialized")
            return self._default_structure()

        prompt = f"""Extract from this resume as JSON with exact format:
{{"skills": [], "experience": [], "education": [], "total_years_exp": 0}}

Resume:
{resume_text}

JSON Response:"""

        try:
            result = self.llm_pipe(
                prompt,
                max_new_tokens=1024,
                temperature=0.3,
                do_sample=False,
                return_full_text=False,
            )
            response_text = result[0]["generated_text"].strip()
            
            # Extract JSON from response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                data = json.loads(json_str)
                return data
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON response")
        except Exception as e:
            logger.error(f"Error in LLM extraction: {e}")
        
        return self._default_structure()

    def extract_with_ner(self, resume_text: str) -> Dict:
        """Extract entities using GLiNER NER"""
        if not self.ner_model:
            logger.warning("NER model not available")
            return {}

        entities_of_interest = [
            "skill", "technical skill",
            "job title", "position", "designation",
            "company", "organization",
            "degree", "certification", "qualification"
        ]

        try:
            ner_results = self.ner_model.predict_entities(resume_text, entities_of_interest)
            
            extracted = {
                "skills": [],
                "titles": [],
                "companies": [],
                "degrees": []
            }
            
            for entity in ner_results:
                entity_type = entity["label"].lower()
                entity_text = entity["text"]
                
                if "skill" in entity_type:
                    extracted["skills"].append(entity_text)
                elif "title" in entity_type or "position" in entity_type or "designation" in entity_type:
                    extracted["titles"].append(entity_text)
                elif "company" in entity_type or "organization" in entity_type:
                    extracted["companies"].append(entity_text)
                elif "degree" in entity_type or "certification" in entity_type or "qualification" in entity_type:
                    extracted["degrees"].append(entity_text)
            
            # Remove duplicates
            for key in extracted:
                extracted[key] = list(set(extracted[key]))
            
            return extracted
        except Exception as e:
            logger.error(f"Error in NER extraction: {e}")
            return {}

    def extract(self, resume_text: str, use_ner: bool = True, use_llm: bool = True) -> Dict:
        """Combined extraction using both LLM and NER"""
        result = self._default_structure()
        
        # Get LLM extraction
        if use_llm:
            llm_data = self.extract_with_llm(resume_text)
            result.update(llm_data)
        
        # Get NER extraction
        if use_ner:
            ner_data = self.extract_with_ner(resume_text)
            # Merge NER data with LLM data
            if "skills" in ner_data:
                result["skills"].extend(ner_data["skills"])
            result["titles"] = ner_data.get("titles", [])
            result["companies"] = ner_data.get("companies", [])
            result["degrees"] = ner_data.get("degrees", [])
            
            # Remove duplicates
            result["skills"] = list(set(result["skills"]))
        
        return result

    @staticmethod
    def _default_structure() -> Dict:
        """Return default structure for resume data"""
        return {
            "skills": [],
            "experience": [],
            "education": [],
            "total_years_exp": 0,
            "titles": [],
            "companies": []
        }