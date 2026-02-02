#!/bin/bash
# CareerForge AI - LLM Health Check Script
# Monitors the health of the Ollama LLM service

set -e

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
MODEL_NAME="${MODEL_NAME:-mistral:7b-instruct-v0.3-q4_K_M}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=============================================="
echo "🏥 CareerForge AI - LLM Health Check"
echo "=============================================="
echo ""

# Check if Ollama is running
check_ollama_service() {
    echo "1. Checking Ollama service..."
    
    if curl -s "$OLLAMA_HOST/api/tags" &> /dev/null; then
        echo -e "   ${GREEN}✅ Ollama is running at $OLLAMA_HOST${NC}"
        return 0
    else
        echo -e "   ${RED}❌ Ollama is not responding at $OLLAMA_HOST${NC}"
        echo "   Try: ollama serve"
        return 1
    fi
}

# Check if model is available
check_model_available() {
    echo ""
    echo "2. Checking model availability..."
    
    MODELS=$(curl -s "$OLLAMA_HOST/api/tags" | jq -r '.models[].name // empty')
    
    if echo "$MODELS" | grep -q "mistral"; then
        echo -e "   ${GREEN}✅ Mistral model is available${NC}"
        echo "   Available models:"
        echo "$MODELS" | sed 's/^/      - /'
        return 0
    else
        echo -e "   ${RED}❌ Mistral model not found${NC}"
        echo "   Run: ollama pull mistral:7b-instruct"
        return 1
    fi
}

# Test model inference
test_inference() {
    echo ""
    echo "3. Testing model inference..."
    
    START_TIME=$(date +%s%3N)
    
    RESPONSE=$(curl -s -X POST "$OLLAMA_HOST/api/generate" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"mistral:7b-instruct\",
            \"prompt\": \"Reply with only the word OK\",
            \"stream\": false,
            \"options\": {\"num_predict\": 10}
        }" 2>&1)
    
    END_TIME=$(date +%s%3N)
    LATENCY=$((END_TIME - START_TIME))
    
    CONTENT=$(echo "$RESPONSE" | jq -r '.response // empty')
    
    if [[ -n "$CONTENT" ]]; then
        echo -e "   ${GREEN}✅ Inference working (${LATENCY}ms)${NC}"
        echo "   Response: $CONTENT"
        return 0
    else
        echo -e "   ${RED}❌ Inference failed${NC}"
        echo "   Response: $RESPONSE"
        return 1
    fi
}

# Check system resources
check_resources() {
    echo ""
    echo "4. Checking system resources..."
    
    # Check available memory
    if command -v free &> /dev/null; then
        TOTAL_MEM=$(free -g | awk '/^Mem:/{print $2}')
        USED_MEM=$(free -g | awk '/^Mem:/{print $3}')
        AVAIL_MEM=$((TOTAL_MEM - USED_MEM))
        
        if [[ $AVAIL_MEM -ge 8 ]]; then
            echo -e "   ${GREEN}✅ Memory: ${AVAIL_MEM}GB available (8GB+ recommended)${NC}"
        elif [[ $AVAIL_MEM -ge 4 ]]; then
            echo -e "   ${YELLOW}⚠️  Memory: ${AVAIL_MEM}GB available (8GB+ recommended)${NC}"
        else
            echo -e "   ${RED}❌ Memory: ${AVAIL_MEM}GB available (8GB+ recommended)${NC}"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS memory check
        MEM_FREE=$(vm_stat | grep "Pages free" | awk '{print $3}' | tr -d '.')
        MEM_INACTIVE=$(vm_stat | grep "Pages inactive" | awk '{print $3}' | tr -d '.')
        AVAIL_MEM=$(( (MEM_FREE + MEM_INACTIVE) * 4096 / 1024 / 1024 / 1024 ))
        echo "   Available memory: ~${AVAIL_MEM}GB"
    fi
    
    # Check GPU (NVIDIA)
    if command -v nvidia-smi &> /dev/null; then
        GPU_MEM=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)
        GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
        echo -e "   ${GREEN}✅ GPU detected: $GPU_NAME (${GPU_MEM}MB free)${NC}"
    else
        echo -e "   ${YELLOW}⚠️  No NVIDIA GPU detected (CPU inference will be slower)${NC}"
    fi
}

# Print summary
print_summary() {
    echo ""
    echo "=============================================="
    if [[ $OVERALL_STATUS == "healthy" ]]; then
        echo -e "${GREEN}🎉 LLM Service Status: HEALTHY${NC}"
    else
        echo -e "${RED}⚠️  LLM Service Status: ISSUES DETECTED${NC}"
    fi
    echo "=============================================="
    echo ""
    echo "Endpoint: $OLLAMA_HOST"
    echo "Model: $MODEL_NAME"
    echo ""
}

# Main execution
main() {
    OVERALL_STATUS="healthy"
    
    if ! check_ollama_service; then
        OVERALL_STATUS="unhealthy"
    fi
    
    if ! check_model_available; then
        OVERALL_STATUS="unhealthy"
    fi
    
    if ! test_inference; then
        OVERALL_STATUS="unhealthy"
    fi
    
    check_resources
    
    print_summary
    
    if [[ $OVERALL_STATUS == "unhealthy" ]]; then
        exit 1
    fi
}

main "$@"
