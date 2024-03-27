from spellchecker import SpellChecker
import nbformat
import os
import sys

def spell_check_notebook(filepath, ignore_words):
  spell = SpellChecker()
  spell.word_frequency.load_words(ignore_words)

  misspelled_words = {}  # Dictionary to collect misspelled words

  with open(filepath, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

  for cell in nb.cells:
    if cell.cell_type == 'markdown':
      text = cell.source
      misspelled = spell.unknown(text.split())
      if misspelled:
        if filepath not in misspelled_words:
          misspelled_words[filepath] = set()  # Use a set to avoid duplicate words
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
  ignore_list = [
    'slippy', 'hist', 'NAM', 'gage', 'swe', 'geoweaver', 'workflow', 'datasets', 'snotel',
    'adeos-ii', 'monthly,', 'products,', 'nsidc', 'separately,', 'control.', '##', 'caps,',
    'dataset.', 'research**:', 'prediction,', 'atmosphere.', 'amsr?', 'fingertips!', 'risk,',
    'amsr-related', 'amsr2', 'snowfall,', 'properties.', 'netcdf,', '**cryosphere', 'moisture,',
    'extent,', 'scheduling.', 'scales.', '1,000m.', 'tourism**:', 'format,', 'temperature,',
    'purposes,', 'hiking,', '**recreation', 'datasets.', 'workflow,', '(coop),', 'periods.',
    '[gridmet', '**temporal', '(nam)', 'snow,', 'agriculture,', 'amsr,', 'terrain,', 'beyond.',
    'data,', '(plain', 'data.', 'u.s.the', '(swe),', 'resolutions:', '**oceanography**:', 'daac',
    'forestry**:', '*runoff', 'format.', 'hdf5', 'information.', 'instruments.', 'ams/adeos-ii,',
    'land,', 'typically,', 'reliability,', 'capabilities.', 'gage,', '(network', 'environment.,',
    'dynamics,', 'trends*:', 'dynamics.', 'hydroclimatic', 'studies*:', 'visualization.', 'degree)',
    'models:', 'snowboarding,', 'camping.', 'salinity,', 'intervals.', 'multi-disciplinary',
    'monitoring*:', 'endeavors.', 'columbia', 'conditions.', 'nasa\'s', 'metadata',
    'snowpacktelemetrynetwork', 'satellite-ii', 'winds,', 'mo', 'fsca', 'modis', 'gridmet'
  ]
  spell_check_directory('.', ignore_list)
