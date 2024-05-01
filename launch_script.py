import subprocess
import os


def start_backend():
    print("Starting Flask backend...")
    os.chdir("backend")  # Change directory to backend
    subprocess.Popen(["python", "app.py"])  # Start Flask app
    os.chdir("..")  # Change back to the original directory


def start_frontend():
    print("Starting React frontend...")
    os.chdir("frontend")  # Change directory to frontend
    subprocess.Popen(["npm", "start"])  # Start React app
    os.chdir("..")  # Change back to the original directory


if __name__ == "__main__":
    start_backend()
    start_frontend()
