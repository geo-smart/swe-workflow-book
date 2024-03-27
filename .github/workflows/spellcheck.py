from spellchecker import SpellChecker
import nbformat
import os
import sys
import string  # Import the string module to get a list of punctuation characters

def remove_punctuation(text):
  translator = str.maketrans('', '', string.punctuation)
  return text.translate(translator)

def spell_check_notebook(filepath, ignore_words):
  spell = SpellChecker()
  spell.word_frequency.load_words(ignore_words)

  misspelled_words = {}

  with open(filepath, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

  for cell in nb.cells:
    if cell.cell_type == 'markdown':
      # Preprocess the cell text to remove punctuation before splitting into words
      text = remove_punctuation(cell.source)
      misspelled = spell.unknown(text.split())
      if misspelled:
        if filepath not in misspelled_words:
          misspelled_words[filepath] = set()
        misspelled_words[filepath].update(misspelled)

  return misspelled_words

def spell_check_directory(directory, ignore_words):
  all_misspelled_words = {}
  for subdir, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith('.ipynb'):
        filepath = os.path.join(subdir, file)
        result = spell_check_notebook(filepath, ignore_words)
        if result:
          all_misspelled_words.update(result)

  if all_misspelled_words:
    for filepath, words in all_misspelled_words.items():
      print(f"Misspelled words in {filepath}: {', '.join(words)}")
    sys.exit(1)  # Exit with a non-zero status code to indicate failure

if __name__ == "__main__":
  ignore_list =misspelled_words = [
    "geoweaver", "workflow", "datasets", "snotel", "snowpack", "amsrderived", "highelevation",
    "snowpacktelemetrynetwork", "snowcastwormhole", "500m", "amsr", "decisionmaking",
    "qualitycontrolled", "pagehttpswwwearthdatanasagovsensorsamsre", "netcdf", "daac", "4km",
    "satelliteii", "usthe", "strategizing", "xband", "modis", "pagehttpswwwearthdatanasagovsensorsmodis",
    "nam", "amsrrelated", "adeosii", "mesoscale", "amsradeosii", "apis", "asos", "missionwater",
    "metadata", "shortterm", "groundbased", "hdf", "british", "october", "level2a", "gcomw1", "csv",
    "dataloggers", "columbia", "ascii", "tsv", "amsadeosii", "longterm", "onboard", "wrf", "km", "hdf5",
    "nsidc", "realtime", "satellitebased", "amsre", "level1a", "websitehttpswwwclimatologylaborggridmethtml",
    "124th", "cryospheric", "american", "timestamped", "geolocation", "nrcs", "satellitederived", "awdn",
    "1000m", "snowmelt", "nasas", "amsr2", "dataset", "gridmet", "hightech", "youll", "cryosphere", "µm",
    "250m", "highspatial", "hydroclimatic", "fsca", "workflow", "swe"
  ]
  spell_check_directory('.', ignore_list)
