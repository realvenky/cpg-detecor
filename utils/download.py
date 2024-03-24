import os
import torch

# Define the URL of the PyTorch model weights


def download_model(model_url,file_path):
    if not os.path.exists(file_path):
        try:
            # Load the model weights from the URL
            state_dict = torch.hub.load_state_dict_from_url(model_url, progress=True)
            
            # Save the model weights to a file
            torch.save(state_dict, file_path)
            print("Model weights downloaded and saved successfully.")
        except Exception as e:
            print(f"An error occurred while downloading the model weights: {e}")
    else:
        print(f"File '{file_path}' already exists.")


model_url = "https://github.com/realvenky/cpg-detecor/releases/download/0.1.0/model.pth"
file_path = os.path.join("models", "model.pth")
download_model(model_url,file_path)

model_url = "https://github.com/realvenky/cpg-detecor/releases/download/0.1.0/model_var_len.pth"
file_path = os.path.join("models", "model_var_len.pth")
download_model(model_url,file_path)

