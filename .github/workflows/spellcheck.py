from spellchecker import SpellChecker
import nbformat
import os
import sys  # Import sys for exiting with a non-zero status code

def spell_check_notebook(filepath, ignore_words):
  spell = SpellChecker()
  spell.word_frequency.load_words(ignore_words)

  has_errors = False  # Flag to track if there are any spelling errors

  with open(filepath, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

  for cell in nb.cells:
    if cell.cell_type == 'markdown':
      text = cell.source
      misspelled = spell.unknown(text.split())
      if misspelled:
        if not has_errors:  # Print the header once per file
          print(f"Misspelled words in {filepath}:")
          has_errors = True
        for word in misspelled:
          print(f"- {word}")
  if has_errors:
    print("\n")  # Print a newline for readability between files
    return True  # Return True to indicate spelling errors were found
  return False

def spell_check_directory(directory, ignore_words):
  error_found = False
  for subdir, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith('.ipynb'):
        filepath = os.path.join(subdir, file)
        if spell_check_notebook(filepath, ignore_words):
          error_found = True  # Error found in at least one file

  if error_found:
    sys.exit(1)  # Exit with a non-zero status code to indicate failure

if __name__ == "__main__":
  ignore_list = ['slippy', 'hist', 'NAM', 'gage']  # Adjust your ignore list as needed
  spell_check_directory('.', ignore_list)
