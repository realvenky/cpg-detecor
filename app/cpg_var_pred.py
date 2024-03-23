from flask import Flask, render_template, request
import torch
import os

from app.cpg_var_def import CpGPredictor

# Alphabet helpers
alphabet = 'NACGT'
dna2int = {a: i for a, i in zip(alphabet, range(1, 6))}
int2dna = {i: a for a, i in zip(alphabet, range(1, 6))}

MODELS_FOLDER = 'models'
app = Flask(__name__)

# Model instantiation with necessary params
model = CpGPredictor(128, 256, 2, 1)

model_path = os.path.join(MODELS_FOLDER, "model_var_len.pth")
# Load the model parameters
model.load_state_dict(torch.load(model_path))

# Set the model to evaluation mode
model.eval()

# Function to preprocess given DNA sequence
def preprocess_sequence(sequence):
    # Convert sequence to ints and create a tensor
    processed_sequence = [dna2int.get(base, 0) for base in sequence]
    # Pad sequence to have a fixed length of 128
    pad_length = 128
    if len(processed_sequence) < pad_length:
        processed_sequence += [0] * (pad_length - len(processed_sequence))
    elif len(processed_sequence) > pad_length:
        processed_sequence = processed_sequence[:pad_length]
    processed_sequence_tensor = torch.tensor(processed_sequence)
    return processed_sequence_tensor

# Define route for home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        dna_sequence = request.form["dna_sequence"]
        # Preprocess input sequence
        processed_sequence = preprocess_sequence(dna_sequence)
        # Run inference
        with torch.no_grad():
            output = model(processed_sequence.unsqueeze(0))
        predicted_count = output.item()
        return render_template("result.html", predicted_count=predicted_count)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
