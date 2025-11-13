#!/usr/bin/env python3
"""
Deployment script for Hugging Face Hub
"""

import os
import sys
import logging

def setup_environment():
    """Setup environment for HF_TOKEN"""
    token = os.environ.get('HF_TOKEN')
    
    if not token:
        print("No HF_TOKEN found in environment!")
        return False
    
    # Clean conflicting variables
    for key in list(os.environ.keys()):
        if key.startswith(('HF_', 'HUGGINGFACE_')) and key != 'HF_TOKEN':
            del os.environ[key]
    
    # Validate token
    token = token.strip()
    if len(token) < 10:
        print("Token appears invalid (too short)")
        return False
    
    print(f"HF_TOKEN found, length: {len(token)}")
    return True

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup environment
if not setup_environment():
    sys.exit(1)

# Import after environment setup
try:
    from huggingface_hub import HfApi, login, create_repo
except ImportError as e:
    logger.error(f"Failed to import libraries: {e}")
    sys.exit(1)

def validate_token():
    """Validate the Hugging Face token"""
    try:
        token = os.environ['HF_TOKEN']
        login(token=token)
        api = HfApi()
        user_info = api.whoami()
        logger.info(f"Token valid! User: {user_info['name']}")
        return True
    except Exception as e:
        logger.error(f"Token validation failed: {e}")
        return False

def deploy_model():
    """Main deployment function"""
    try:
        api = HfApi()
        repo_name = "dhani10/engine-condition-model"
        logger.info(f"Creating repository: {repo_name}")
        
        repo_url = create_repo(repo_id=repo_name, exist_ok=True, private=False)
        logger.info(f"Repository: {repo_url}")
        
        # TODO: Add your file uploads here
        # api.upload_file(...)
        
        logger.info("Deployment completed!")
        return True
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        return False

def main():
    logger.info("Starting deployment...")
    if not validate_token():
        sys.exit(1)
    if not deploy_model():
        sys.exit(1)
    logger.info("Deployment process completed!")

if __name__ == "__main__":
    main()
