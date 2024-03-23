# tests/test_app.py

import unittest
import os
import sys
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.cpg_pred import app

def download_file(url, file_path):
    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"File '{file_path}' already exists.")
        return

    # Make a GET request to download the file
    try:
        print(f"Downloading file from '{url}'...")
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Write the file to the specified path
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded and saved to '{file_path}'.")
        else:
            print(f"Failed to download file from '{url}'. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")

url = "https://github.com/realvenky/cpg-detecor/releases/tag/0.1.0/model.pth"
file_path = "models/model.pth"
download_file(url, file_path)

url = "https://github.com/realvenky/cpg-detecor/releases/tag/0.1.0/model_var_len.pth"
file_path = "models/model_var_len.pth"
download_file(url, file_path)

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>CpG Predictor</title>', response.data)

    def test_prediction(self):
	    # Sample input DNA sequence
	    input_sequence = 'CCNGGCTCCGATACGNCTTTGNCCCNAGCACNNTTAGAAGCTACGTCNTGCCTAATTAAGCACTTACCACANACACANGCGCGNTCNATNTTACGAACAAGAGANNAGNGATNNCCTAGNCNNACNAA'

	    # Expected target CpG count
	    expected_cpg_count = 6.0  # Update this with the expected target CpG count for the input sequence

	    # Send a POST request to the server with the input sequence
	    response = self.app.post('/', data={'dna_sequence': input_sequence})

	    # Check if the response status code is 200
	    self.assertEqual(response.status_code, 200)

	    # Extract the predicted CpG count from the response data
	    response_data = response.data.decode('utf-8')  # Convert bytes to string
	    start_index = response_data.find('Predicted CpG Count:') + len('Predicted CpG Count:')
	    end_index = response_data.find('</p>', start_index)
	    predicted_cpg_count_str = response_data[start_index:end_index].strip()
	    predicted_cpg_count = float(predicted_cpg_count_str)

	    # Check if the predicted CpG count matches the expected target CpG count
	    self.assertAlmostEqual(predicted_cpg_count, expected_cpg_count, delta=0.25)  # Use assertAlmostEqual for float comparison

if __name__ == '__main__':
    unittest.main()
