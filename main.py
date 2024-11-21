import os
import pdfplumber
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Regex pattern to detect page numbers (e.g., "Page 1", "1/3", "1 of 3", "1")
page_number_pattern = re.compile(
    r"^(Page\s*\d+|\d+\s*/\s*\d+|\d+\s*/|\d+\s+of\s+\d+|\d+)$", re.IGNORECASE
)


# Function to clean and filter text based on position
def clean_text_with_layout(pdf_path, top_margin, bottom_margin):
    with pdfplumber.open(pdf_path) as pdf:
        cleaned_text = []

        for page in pdf.pages:
            text = page.extract_text()  # Extract the full text of the page

            if text:  # Check if there is any text in the page
                lines = text.splitlines()
                filtered_lines = []

                # Skip first and last few lines (headers/footers)
                for i, line in enumerate(lines):
                    # Skip lines that are part of header/footer
                    if i < top_margin or i >= len(lines) - bottom_margin:
                        continue

                    # Skip lines that match the page number pattern
                    if page_number_pattern.match(line.strip()):
                        continue

                    filtered_lines.append(line.strip())  # Keep valid content

                # Join the remaining text with proper paragraph breaks
                cleaned_text.append("\n".join(filtered_lines))

        return "\n\n".join(cleaned_text)


# Function to handle the conversion process
def convert_pdfs():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    try:
        top_margin = int(top_margin_entry.get())
        bottom_margin = int(bottom_margin_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for margins.")
        return

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each PDF in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, file_name)
            txt_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.txt")

            cleaned_text = clean_text_with_layout(pdf_path, top_margin, bottom_margin)

            # Only write to the file if there's content
            if cleaned_text:
                with open(txt_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(cleaned_text)

    messagebox.showinfo("Conversion Complete", "PDF conversion completed successfully!")


# Function to browse for input folder
def browse_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_selected)


# Function to browse for output folder
def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_selected)


# GUI setup
root = tk.Tk()
root.title("PDF Text Extractor")

# Input folder section
tk.Label(root, text="Select Input Folder:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
input_folder_entry = tk.Entry(root, width=50)
input_folder_entry.grid(row=0, column=1, padx=10, pady=10)
input_folder_button = tk.Button(root, text="Browse", command=browse_input_folder)
input_folder_button.grid(row=0, column=2, padx=10, pady=10)

# Output folder section
tk.Label(root, text="Select Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=10)
output_folder_button = tk.Button(root, text="Browse", command=browse_output_folder)
output_folder_button.grid(row=1, column=2, padx=10, pady=10)

# Top margin input
tk.Label(root, text="Top Margin (Header Removal):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
top_margin_entry = tk.Entry(root)
top_margin_entry.grid(row=2, column=1, padx=10, pady=10)

# Bottom margin input
tk.Label(root, text="Bottom Margin (Footer Removal):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
bottom_margin_entry = tk.Entry(root)
bottom_margin_entry.grid(row=3, column=1, padx=10, pady=10)

# Convert button
convert_button = tk.Button(root, text="Start Conversion", command=convert_pdfs)
convert_button.grid(row=4, column=0, columnspan=3, pady=20)

# Run the GUI
root.mainloop()
