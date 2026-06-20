# Weave MVP Workload Specification

## Model Selection

**Model:** `meta-llama/Llama-3.1-8B-Instruct`

### Rationale

| Factor | Llama-3.1-8B-Instruct | Mistral-7B-v0.3 |
|--------|----------------------|------------------|
| Parameter count | 8B | 7B |
| Context window | 128K | 32K |
| Instruction-tuned | Yes | Yes |
| License | Llama 3.1 Community | Apache 2.0 |
| exo support | Confirmed | Confirmed |
| Community adoption | Very high | High |
| Quantized sizes (GGUF) | Q4: ~4.7GB, Q8: ~8.5GB | Q4: ~4.1GB, Q8: ~7.7GB |

**Pick Llama-3.1-8B** — larger community, longer context, better instruction following. Fits in 8GB RAM quantized.

**Fallback:** Mistral-7B if license issues arise.

## Task Type

**Batch text generation** (not interactive chat).

### Why Batch First

1. **Latency tolerance** — batch jobs don't need sub-second response times
2. **Simpler lifecycle** — submit → process → return result (no streaming)
3. **Easier verification** — can hash complete output vs. streaming chunks
4. **Pipeline-parallel friendly** — can buffer activations between nodes without time pressure
5. **SaladCloud comparable** — SaladCloud primarily serves batch API workloads

### Job Specification

```json
{
  "model": "meta-llama/Llama-3.1-8B-Instruct",
  "prompt": "Explain quantum entanglement in simple terms.",
  "max_tokens": 256,
  "temperature": 0.7,
  "task_type": "batch_generation"
}
```

### Non-Goals for MVP

- ❌ Interactive chat (streaming)
- ❌ Multi-turn conversations
- ❌ Image generation
- ❌ Fine-tuning
- ❌ Multiple model selection

## Benchmark Protocol

### Baselines

1. **SaladCloud** — create developer account, run same prompts, log latency + cost
2. **Replicate** — same prompts via their API, log latency + cost
3. **Local single-device** — same model on one machine via llama.cpp, log latency

### Metrics

| Metric | Measurement |
|--------|------------|
| Time to first token (TTFT) | ms from job submission to first output |
| Total generation time | ms from submission to complete result |
| Tokens per second | output tokens / generation time |
| Cost per 1K tokens | credits or USD |
| Job success rate | completed / submitted |
| P2P overhead | (WAN time - local time) / local time |

### Test Prompts (10 standardized)

1. Short factual: "What is the capital of France?" (expect ~20 tokens)
2. Medium explanation: "Explain how a CPU works" (expect ~200 tokens)
3. Long generation: "Write a 500-word essay about renewable energy" (expect ~500 tokens)
4. Code generation: "Write a Python function to sort a list" (expect ~100 tokens)
5. Creative: "Write a haiku about distributed computing" (expect ~20 tokens)
6-10. Variations of above with different temperature settings (0.0, 0.3, 0.7, 1.0, 1.5)
