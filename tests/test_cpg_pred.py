# tests/test_app.py

import unittest
import os
import sys
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.cpg_pred import app

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
