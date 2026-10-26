##################################################
##  SCRIPT TO EXTRACT DATA FROM FOLDER OF       ##
## USCG MARINERS REPORT PDFS BASED ON KEYWORDS  ##
##################################################

# IMPORT LIBRARIES
import fitz  # PyMuPDF
import os
from pathlib import Path

# FUNCTION TO SEARCH FOR KEYWORDS AND COMBINE RESULTS INTO A PDF
def extract_multi_keyword_pages(folder_path, keywords, output_filename):
    result_pdf = fitz.open()
    # Clean keywords: lowercase and remove extra whitespace
    keywords = [k.lower().strip() for k in keywords]
    
    found_any = False

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            
            try:
                doc = fitz.open(file_path)
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    text = page.get_text().lower()
                    
                    # Check if the keywords are in the text
                    if any(word in text for word in keywords):
                        result_pdf.insert_pdf(doc, from_page=page_num, to_page=page_num)
                        found_any = True
                doc.close()
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if found_any:
        result_pdf.save(output_filename)
        print(f"Success! Compiled into {output_filename}")
    else:
        print("No matches found for any keywords.")
    
    result_pdf.close()

# ----- USAGE -------

home_dir = Path.home()
# Change file path based on location of PDFs of interest
file_path = home_dir / "Documents" / "AIS" / "USCG_LNM" / "District1" / "D01LNM2025"
# Change keywords depending on search
my_keywords = ["wind", "revolution", "vineyard northeast", "park city", "attentive energy", "community offshore","vineyard mid-atlantic", 
"atlantic shores", "southcoast", "south fork", "sunrise", "beacon", "vineyard", "empire", "bay state", "geotechnical",
"OCS-A 0486", "OCS-A 0487", "OCS-A 0500", "OCS-A 0501", "OCS-A 0512", "OCS-A 0517", "OCS-A 0520", "OCS-A 0521", 
"OCS-A 0522", "OCS-A 0534", "OCS-A 0537", "OCS-A 0538", "OCS-A 0539", "OCS-A 0544", "OCS-A 0549", "OCS-A 0561"]
extract_multi_keyword_pages(file_path, my_keywords, file_path / "Combined_Results.pdf")
