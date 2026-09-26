# AI Engineer MVP

An internal AI knowledge & action platform, built as a small but end-to-end reference implementation covering the core AI engineering stack: RAG, agents, MCP, model serving, fine-tuning, graph-based retrieval, evaluation, and a full container/Kubernetes/CI-CD/GitOps deployment path.

The product stays intentionally small (a tiny real document corpus, small models, one agent, one vector database). The goal is breadth of engineering coverage over product sophistication — every layer below is real and runnable, not mocked.

## What it does

- Answers questions over a real document corpus using RAG (chunking → embeddings → vector search → LLM).
- Routes between RAG and tool-calling via an agent with explicit multi-step reasoning.
- Exposes at least one tool through a local MCP server.
- Serves an open-source LLM locally (direct Hugging Face/PyTorch inference, then vLLM for production-style serving).
- Includes a small supervised fine-tuning (LoRA/QLoRA) experiment.
- Includes a small knowledge-graph / GraphRAG retrieval experiment, compared against vector retrieval.
- Has a CLI-runnable evaluation pipeline for RAG, agent, and model quality/latency.
- Runs as a containerized, production-style Python service, deployable to Kubernetes via Helm, with CI/CD and GitOps.
- Supports a local-only / on-prem-style deployment mode (no external model API required).

## Data source

A small real slice of [`home-assistant/core`](https://github.com/home-assistant/core): its markdown documentation (RAG corpus), a sample of its real GitHub issues (tickets), and its `CODEOWNERS` file (used to derive a real `Service -> owned_by -> Team` / `Service -> depends_on -> Database` knowledge graph). No synthetic or fictional "internal company" data is used for these parts.

## Architecture

```text
                         User
                          |
                          v
                     FastAPI App
                          |
                          v
                    LangGraph Agent
                    /      |       \
                   /       |        \
                  v        v         v
               RAG      MCP Tool   Direct LLM
                |          |
                v          v
             Qdrant     MCP Server
                |          |
                v          v
          HA Docs      HA Issues/CODEOWNERS
                 \        /
                  \      /
                   v    v
                  Model API
                     |
                     v
                    vLLM
                     |
                     v
            Hugging Face / PyTorch
                     |
                     v
                Local LLM
```

Fine-tuning side path: synthetic dataset → SFT → LoRA / QLoRA → adapter → small evaluation.

Graph side path: CODEOWNERS/module structure → knowledge graph → GraphRAG experiment.

Deployment path: Git → GitHub Actions → Docker images → Helm → GitOps (Argo CD) → Kubernetes.

## Tech stack

Python, PyTorch, Hugging Face Transformers, Sentence Transformers, Qdrant, LangGraph, MCP, vLLM, PEFT (LoRA/QLoRA), NetworkX, FastAPI, pytest, Docker, Kubernetes, Helm, GitHub Actions, Argo CD.

## Status

Early-stage, built incrementally in stages (data ingestion → inference → RAG → agents → MCP → graph → serving → fine-tuning → evaluation → containerization → Kubernetes → CI/CD → GitOps). Follow along in the commit history.
