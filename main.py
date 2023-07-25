from dotenv import load_dotenv
from mychat.app import run_app

if __name__ == "__main__":
    
    # load env variables
    load_dotenv(".env", override=True)
    
    # run the app
    run_app()
    
    