import re

from typing import Dict, List, Tuple

import spacy

nlp = spacy.load("en_core_web_sm")

class IndianIdentifier:
    '''Regex for common Indian identifiers'''
    PAN = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
    AADHAR = r'[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}'
    INDIAN_PASSPORT = r'[A-PR-WYa-pr-wy][1-9]\d\s?\d{4}[1-9]'
    DRIVING_LICENSE = r'(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}'
    UPI_ID = r'[\.\-a-z0-9]+@[a-z]+'
    INDIAN_BANK_ACCOUNT = r'\d{9,18}'
    IFSC_CODE = r'[A-Z]{4}0[A-Z0-9]{6}'
    INDIAN_PHONE_NUMBER = r'(\+91|\+91\-|0)?[789]\d{9}'
    EMAIL = r'[\w\.-]+@[\w\.-]+\.\w+'

    @classmethod
    def get_all_patterns(cls) -> Dict[str, str]:
        """Returns all regex patterns defined in the class"""
        return {
            name: pattern 
            for name, pattern in vars(cls).items() 
            if isinstance(pattern, str) and not name.startswith('_')
        }

def find_matches(text: str, pattern: str) -> List[Tuple[int, int, str]]:
    """
    Find all matches of a pattern in text and return their positions and matched text
    """
    matches = []
    for match in re.finditer(pattern, text):
        matches.append((match.start(), match.end(), match.group()))
    return matches

def get_replacement_text(identifier_type: str) -> str:
    """
    Returns appropriate replacement text based on the type of identifier
    """
    replacements = {
        'PAN': '[PAN_NUMBER]',
        'AADHAR': '[AADHAR_NUMBER]',
        'INDIAN_PASSPORT': '[PASSPORT_NUMBER]',
        'DRIVING_LICENSE': '[DL_NUMBER]',
        'UPI_ID': '[UPI_ID]',
        'INDIAN_BANK_ACCOUNT': '[BANK_ACCOUNT]',
        'IFSC_CODE': '[IFSC_CODE]',
        'INDIAN_PHONE_NUMBER': '[PHONE_NUMBER]',
        'EMAIL': '[EMAIL_ADDRESS]',
        'PERSON': '[PERSON_NAME]',
        'ORG': '[ORGANIZATION]',
        'GPE': '[LOCATION]'
    }
    return replacements.get(identifier_type, '[MASKED]')

def analyze_identifiers(text: str, mask_char: str = "*") -> Tuple[str, Dict[str, List[str]]]:
    """
    Function to identify and hide sensitive information.
    Returns:
        - masked_text: Text with all sensitive information masked
        - found_identifiers: Dictionary containing all identified sensitive information
    """
    # Initialize variables
    masked_text = text
    found_identifiers = {}
    positions_to_mask = []

    # First, find all regex matches
    for identifier_name, pattern in IndianIdentifier.get_all_patterns().items():
        matches = find_matches(text, pattern)
        if matches:
            found_identifiers[identifier_name] = [match[2] for match in matches]
            positions_to_mask.extend(
                (start, end, identifier_name) for start, end, _ in matches
            )

    # Then, process named entities using spaCy
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]:
            positions_to_mask.append((ent.start_char, ent.end_char, ent.label_))
            if ent.label_ not in found_identifiers:
                found_identifiers[ent.label_] = []
            found_identifiers[ent.label_].append(ent.text)

    # Sort positions by start index in reverse order to handle overlapping matches
    positions_to_mask.sort(key=lambda x: x[0], reverse=True)

    # Apply masking
    for start, end, identifier_type in positions_to_mask:
        replacement = get_replacement_text(identifier_type)
        masked_text = masked_text[:start] + replacement + masked_text[end:]

    return masked_text, found_identifiers

def analyze_prompts(text):
    '''Fucntio call identifiers'''
    masked_text, found_identifiers = analyze_identifiers(sample_text)

    print("Original Text:")
    print(sample_text)
    print("\nMasked Text:")
    print(masked_text)
    print("\nIdentified sensitive information:")
    for identifier_type, values in found_identifiers.items():
        print(f"{identifier_type}: {values}")



# Example usage
sample_text = """
Mr. John Doe's PAN number is ABCDE1234F and Aadhar is 1234 5678 9012.
He lives in Mumbai and works at TechCorp.
His phone number is +919876543210 and email is john.doe@example.com.
Bank account: 123456789012 with IFSC: SBIN0123456
"""
analyze_prompts(sample_text)
