#!/bin/bash
# CareerForge AI - LLM Benchmark Script
# Tests performance of the LLM service

set -e

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
MODEL_NAME="${MODEL_NAME:-mistral:7b-instruct}"
NUM_ITERATIONS=5

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=============================================="
echo "⚡ CareerForge AI - LLM Benchmark"
echo "=============================================="
echo ""
echo "Model: $MODEL_NAME"
echo "Iterations: $NUM_ITERATIONS"
echo ""

# Simple prompt test
benchmark_simple() {
    echo "📝 Benchmark 1: Simple Response"
    echo "   Prompt: 'Say hello in 5 words'"
    echo ""
    
    TOTAL_TIME=0
    TOTAL_TOKENS=0
    
    for i in $(seq 1 $NUM_ITERATIONS); do
        START_TIME=$(date +%s%3N)
        
        RESPONSE=$(curl -s -X POST "$OLLAMA_HOST/api/generate" \
            -H "Content-Type: application/json" \
            -d "{
                \"model\": \"$MODEL_NAME\",
                \"prompt\": \"Say hello in exactly 5 words\",
                \"stream\": false,
                \"options\": {\"num_predict\": 20}
            }")
        
        END_TIME=$(date +%s%3N)
        LATENCY=$((END_TIME - START_TIME))
        TOKENS=$(echo "$RESPONSE" | jq '.eval_count // 0')
        
        TOTAL_TIME=$((TOTAL_TIME + LATENCY))
        TOTAL_TOKENS=$((TOTAL_TOKENS + TOKENS))
        
        echo "   Run $i: ${LATENCY}ms, ${TOKENS} tokens"
    done
    
    AVG_TIME=$((TOTAL_TIME / NUM_ITERATIONS))
    AVG_TOKENS=$((TOTAL_TOKENS / NUM_ITERATIONS))
    TOKENS_PER_SEC=$(echo "scale=1; $AVG_TOKENS * 1000 / $AVG_TIME" | bc 2>/dev/null || echo "N/A")
    
    echo ""
    echo -e "   ${GREEN}Average: ${AVG_TIME}ms, ${TOKENS_PER_SEC} tok/s${NC}"
    echo ""
}

# JSON generation test
benchmark_json() {
    echo "📋 Benchmark 2: JSON Generation"
    echo "   Prompt: Generate structured career advice"
    echo ""
    
    PROMPT='Generate a JSON object with 3 career tips. Format: {"tips":["tip1","tip2","tip3"]}'
    
    TOTAL_TIME=0
    TOTAL_TOKENS=0
    
    for i in $(seq 1 $NUM_ITERATIONS); do
        START_TIME=$(date +%s%3N)
        
        RESPONSE=$(curl -s -X POST "$OLLAMA_HOST/api/generate" \
            -H "Content-Type: application/json" \
            -d "{
                \"model\": \"$MODEL_NAME\",
                \"prompt\": \"$PROMPT\",
                \"stream\": false,
                \"format\": \"json\",
                \"options\": {\"num_predict\": 200}
            }")
        
        END_TIME=$(date +%s%3N)
        LATENCY=$((END_TIME - START_TIME))
        TOKENS=$(echo "$RESPONSE" | jq '.eval_count // 0')
        
        TOTAL_TIME=$((TOTAL_TIME + LATENCY))
        TOTAL_TOKENS=$((TOTAL_TOKENS + TOKENS))
        
        echo "   Run $i: ${LATENCY}ms, ${TOKENS} tokens"
    done
    
    AVG_TIME=$((TOTAL_TIME / NUM_ITERATIONS))
    AVG_TOKENS=$((TOTAL_TOKENS / NUM_ITERATIONS))
    TOKENS_PER_SEC=$(echo "scale=1; $AVG_TOKENS * 1000 / $AVG_TIME" | bc 2>/dev/null || echo "N/A")
    
    echo ""
    echo -e "   ${GREEN}Average: ${AVG_TIME}ms, ${TOKENS_PER_SEC} tok/s${NC}"
    echo ""
}

# Long generation test
benchmark_long() {
    echo "📜 Benchmark 3: Long Response (~500 tokens)"
    echo "   Prompt: Generate a detailed career roadmap section"
    echo ""
    
    PROMPT='Generate a detailed 3-month learning roadmap for becoming a web developer. Include weekly goals, tools to learn, and projects to build. Be specific and practical.'
    
    TOTAL_TIME=0
    TOTAL_TOKENS=0
    
    for i in $(seq 1 $NUM_ITERATIONS); do
        START_TIME=$(date +%s%3N)
        
        RESPONSE=$(curl -s -X POST "$OLLAMA_HOST/api/generate" \
            -H "Content-Type: application/json" \
            -d "{
                \"model\": \"$MODEL_NAME\",
                \"prompt\": \"$PROMPT\",
                \"stream\": false,
                \"options\": {\"num_predict\": 500}
            }")
        
        END_TIME=$(date +%s%3N)
        LATENCY=$((END_TIME - START_TIME))
        TOKENS=$(echo "$RESPONSE" | jq '.eval_count // 0')
        
        TOTAL_TIME=$((TOTAL_TIME + LATENCY))
        TOTAL_TOKENS=$((TOTAL_TOKENS + TOKENS))
        
        echo "   Run $i: ${LATENCY}ms, ${TOKENS} tokens"
    done
    
    AVG_TIME=$((TOTAL_TIME / NUM_ITERATIONS))
    AVG_TOKENS=$((TOTAL_TOKENS / NUM_ITERATIONS))
    TOKENS_PER_SEC=$(echo "scale=1; $AVG_TOKENS * 1000 / $AVG_TIME" | bc 2>/dev/null || echo "N/A")
    
    echo ""
    echo -e "   ${GREEN}Average: ${AVG_TIME}ms, ${TOKENS_PER_SEC} tok/s${NC}"
    echo ""
}

# Print summary
print_summary() {
    echo "=============================================="
    echo -e "${GREEN}📊 Benchmark Complete${NC}"
    echo "=============================================="
    echo ""
    echo "Performance Guidelines:"
    echo "  - Simple: <500ms = Excellent, <1000ms = Good"
    echo "  - JSON: <1500ms = Excellent, <3000ms = Good"
    echo "  - Long: <5000ms = Excellent, <10000ms = Good"
    echo ""
    echo "Tips for improving performance:"
    echo "  - Use GPU if available (NVIDIA CUDA)"
    echo "  - Increase RAM to 16GB+"
    echo "  - Use quantized models (Q4_K_M)"
    echo "  - Consider vLLM for production"
    echo ""
}

# Main execution
main() {
    # Check if Ollama is running
    if ! curl -s "$OLLAMA_HOST/api/tags" &> /dev/null; then
        echo "❌ Ollama is not running at $OLLAMA_HOST"
        echo "   Run: ollama serve"
        exit 1
    fi
    
    benchmark_simple
    benchmark_json
    benchmark_long
    print_summary
}

main "$@"
