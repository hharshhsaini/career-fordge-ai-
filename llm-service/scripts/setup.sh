#!/bin/bash
# CareerForge AI - LLM Service Setup Script
# Sets up Ollama and downloads the required model

set -e

echo "=============================================="
echo "🚀 CareerForge AI - LLM Service Setup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on macOS, Linux, or WSL
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo -e "${GREEN}Detected OS: $OS${NC}"

# Install Ollama
install_ollama() {
    echo ""
    echo "📦 Installing Ollama..."
    
    if command -v ollama &> /dev/null; then
        echo -e "${GREEN}✅ Ollama is already installed${NC}"
        ollama --version
        return 0
    fi
    
    case $OS in
        "macos")
            echo "Installing via Homebrew..."
            if ! command -v brew &> /dev/null; then
                echo -e "${YELLOW}Homebrew not found. Installing from curl...${NC}"
                curl -fsSL https://ollama.com/install.sh | sh
            else
                brew install ollama
            fi
            ;;
        "linux")
            echo "Installing Ollama for Linux..."
            curl -fsSL https://ollama.com/install.sh | sh
            ;;
        *)
            echo -e "${RED}Please install Ollama manually from https://ollama.com${NC}"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}✅ Ollama installed successfully${NC}"
}

# Start Ollama service
start_ollama() {
    echo ""
    echo "🔄 Starting Ollama service..."
    
    # Check if Ollama is already running
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo -e "${GREEN}✅ Ollama is already running${NC}"
        return 0
    fi
    
    # Start Ollama in background
    ollama serve &> /dev/null &
    OLLAMA_PID=$!
    
    # Wait for service to start
    echo "Waiting for Ollama to start..."
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags &> /dev/null; then
            echo -e "${GREEN}✅ Ollama started successfully (PID: $OLLAMA_PID)${NC}"
            return 0
        fi
        sleep 1
    done
    
    echo -e "${RED}❌ Failed to start Ollama${NC}"
    exit 1
}

# Download the model
download_model() {
    MODEL_NAME="mistral:7b-instruct-v0.3-q4_K_M"
    FALLBACK_MODEL="mistral:7b-instruct"
    
    echo ""
    echo "📥 Downloading $MODEL_NAME..."
    echo "   (This may take a few minutes on first run)"
    echo ""
    
    # Try to pull the specific version first
    if ollama pull "$MODEL_NAME"; then
        echo -e "${GREEN}✅ Model $MODEL_NAME downloaded successfully${NC}"
        return 0
    fi
    
    # Fallback to generic version
    echo -e "${YELLOW}Trying fallback model: $FALLBACK_MODEL${NC}"
    if ollama pull "$FALLBACK_MODEL"; then
        echo -e "${GREEN}✅ Model $FALLBACK_MODEL downloaded successfully${NC}"
        return 0
    fi
    
    echo -e "${RED}❌ Failed to download model${NC}"
    exit 1
}

# Create custom model from Modelfile
create_custom_model() {
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    MODELFILE="$SCRIPT_DIR/../Modelfile"
    
    if [[ -f "$MODELFILE" ]]; then
        echo ""
        echo "🔧 Creating custom CareerForge model..."
        ollama create careerforge -f "$MODELFILE"
        echo -e "${GREEN}✅ Custom model 'careerforge' created${NC}"
    else
        echo -e "${YELLOW}⚠️  Modelfile not found, skipping custom model creation${NC}"
    fi
}

# Verify installation
verify_setup() {
    echo ""
    echo "🔍 Verifying setup..."
    
    # Check API endpoint
    if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo -e "${RED}❌ Ollama API not responding${NC}"
        exit 1
    fi
    
    # List models
    echo ""
    echo "📋 Available models:"
    ollama list
    
    # Quick test
    echo ""
    echo "🧪 Running quick test..."
    RESPONSE=$(curl -s -X POST http://localhost:11434/api/generate \
        -H "Content-Type: application/json" \
        -d '{
            "model": "mistral:7b-instruct",
            "prompt": "Say hello in exactly 5 words",
            "stream": false,
            "options": {"num_predict": 20}
        }' | jq -r '.response // empty')
    
    if [[ -n "$RESPONSE" ]]; then
        echo -e "${GREEN}✅ LLM test successful: $RESPONSE${NC}"
    else
        echo -e "${YELLOW}⚠️  Quick test didn't get response (may be first load)${NC}"
    fi
}

# Print summary
print_summary() {
    echo ""
    echo "=============================================="
    echo -e "${GREEN}🎉 Setup Complete!${NC}"
    echo "=============================================="
    echo ""
    echo "LLM Service Details:"
    echo "  - Endpoint: http://localhost:11434"
    echo "  - Model: mistral:7b-instruct-v0.3-q4_K_M"
    echo "  - Context: 32K tokens"
    echo ""
    echo "To start the backend API:"
    echo "  cd ../backend"
    echo "  uvicorn main_v2:app --reload --port 8000"
    echo ""
    echo "API Documentation: http://localhost:8000/docs"
    echo "=============================================="
}

# Main execution
main() {
    install_ollama
    start_ollama
    download_model
    create_custom_model
    verify_setup
    print_summary
}

main "$@"
