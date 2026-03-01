"""Streamlit app runner."""

import subprocess
import sys
import os


def run_streamlit_app():
    """Run the Streamlit app (non-blocking)."""
    
    # Get the project root directory (parent of scripts)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Path to the dashboard app
    app_path = os.path.join(project_root, "src", "ui", "app.py")
    
    print(f"Starting HR Automation Agent Dashboard...")
    print(f"App path: {app_path}")
    print(f"Project root: {project_root}")
    print()
    
    # Use Popen for non-blocking execution
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", app_path, "--logger.level=info"],
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Dashboard is starting...")
        print("It will open in your browser at: http://localhost:8501")
        print()
        
        # Read output without blocking
        while True:
            try:
                output = process.stdout.readline()
                if output:
                    print(output.strip())
                error = process.stderr.readline()
                if error:
                    print(f"ERROR: {error.strip()}")
                if process.poll() is not None:
                    break
            except KeyboardInterrupt:
                print("\nShutting down dashboard...")
                process.terminate()
                break
                
    except Exception as e:
        print(f"Error starting dashboard: {e}")
        print(f"\nTry running manually:")
        print(f"  cd {project_root}")
        print(f"  streamlit run src/ui/app.py")


if __name__ == "__main__":
    run_streamlit_app()
