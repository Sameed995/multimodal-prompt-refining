from typing import Dict, List
import re

def refine_prompt(extracted_text: str, is_image: bool = False) -> Dict[str, object]:
    refined = {
        "core_intent": "",
        "functional_requirements": [],
        "technical_constraints": [],
        "expected_output": [],
        "assumptions": [],
        "missing_information": []
    }

    if not extracted_text or not extracted_text.strip():
        refined["missing_information"].append("No meaningful textual content found")
        return refined

   
    raw_lines = extracted_text.splitlines()
    cleaned_lines = []
    for l in raw_lines:
        line = l.strip()
        if not line:
            continue
        line = re.sub(r"^[•▪●eE]\s*", "", line)  # remove bullets prefix
        line = re.sub(r"\s{2,}", " ", line)
        cleaned_lines.append(line)

    # merging broken lines
    lines: List[str] = []
    for line in cleaned_lines:
        if lines and not lines[-1].endswith((".", "?", "!", ":")) and line[0].islower():
            lines[-1] += " " + line
        else:
            lines.append(line)

    # detection of core intent
    core_intent_line = None
    for line in lines:
        if any(k in line.lower() for k in ["develop", "build", "create", "design", "launch"]):
            refined["core_intent"] = line
            core_intent_line = line  # remember this line
            break


    current_section = None
    section_headers = {
        "functional": ["functional requirement"],
        "technical": ["technical constraint"],
        "output": ["expected output", "deliverable"],
        "missing": ["missing information", "notes"]
    }

    for line in lines:
        if line == core_intent_line:
            continue

        lower = line.lower()
     
        detected = False
        for key, keywords in section_headers.items():
            for kw in keywords:
                if kw in lower:
                    current_section = key
                    detected = True
                    break
            if detected:
                break
        if detected:
            continue  

        # Route content
        if current_section == "functional":
            refined["functional_requirements"].append(line)
        elif current_section == "technical":
            refined["technical_constraints"].append(line)
        elif current_section == "output":
            refined["expected_output"].append(line)
        elif current_section == "missing":
            refined["missing_information"].append(line)
        else:
           
            refined["functional_requirements"].append(line)

    # deduplicate
    def dedupe(items: List[str]) -> List[str]:
        seen = set()
        result = []
        for item in items:
            key = item.lower()
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result

    refined["functional_requirements"] = dedupe(refined["functional_requirements"])
    refined["technical_constraints"] = dedupe(refined["technical_constraints"])
    refined["expected_output"] = dedupe(refined["expected_output"])
    refined["missing_information"] = dedupe(refined["missing_information"])

#    final check for missing information
    if not refined["core_intent"]:
        refined["missing_information"].append("Core intent not clearly specified")
    if not refined["expected_output"]:
        refined["missing_information"].append("Expected output or deliverables are not explicitly mentioned")
    if not refined["technical_constraints"]:
        refined["assumptions"].append("No explicit technical constraints detected")

    return refined
