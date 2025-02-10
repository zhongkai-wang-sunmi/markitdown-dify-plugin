# ReAG (Reasoning-Augmented Generation)

**Author:** evan  
**Version:** 0.0.1

## Overview

ReAG is a method that skips the retrieval step entirely. Instead of preprocessing documents into searchable snippets, ReAG feeds raw materials—text files, web pages, spreadsheets—directly to the language model. The model then decides what matters and why, synthesizing answers in one go.

## Traditional RAG vs ReAG

### Traditional RAG System
Traditional RAG systems typically operate in two phases:
1. Semantic Search Phase: First uses retrieval techniques to select documents that are superficially similar to the query content
2. Generation Phase: Then uses language models to generate answers from these documents

However, this two-phase approach may overlook deeper contextual relationships in documents and potentially introduce irrelevant content.

### ReAG's Unified Strategy
ReAG adopts a unified approach:
- It passes raw document content directly to the language model, allowing the model to independently evaluate and integrate the complete context
- This method produces more accurate, detailed answers that better reflect complex contextual relationships

## How ReAG Cuts Through the Noise

ReAG operates on a simple idea: let the language model do the heavy lifting. Instead of relying on pre-built indexes or embeddings, ReAG hands the model raw documents and asks two questions:

1. Is this document useful for the task?
2. What specific parts of it matter?

### Example
If you ask, "Why are polar bear populations declining?" a traditional RAG system might fetch documents containing phrases like "Arctic ice melt" or "bear habitats." But ReAG goes further. It scans entire documents, considering their full context and meaning rather than just their semantic similarity to the query. A research paper titled "Thermal Dynamics of Sea Ice" might be ignored—unless the model notices a section linking ice loss to disruptions in bear feeding patterns.

This approach mirrors how humans research: we skim sources, discard irrelevant ones, and focus on passages that address our specific question. ReAG replicates this behavior programmatically, using the model's ability to infer connections rather than relying on superficial semantics.

## Understanding the Difference

### Traditional RAG
Operates like a librarian:
- Indexes books (documents) by summarizing their covers (embeddings)
- Uses those summaries to guess which books might answer your question
- Process is fast but reductive—prioritizes lexical proximity over functional utility

### ReAG
Acts like a scholar:
- Reads every book in full
- Underlines relevant paragraphs
- Synthesizes insights based on the query's deeper intent

## Technical Implementation

### Key Parameters in reag.yaml
The following parameters are utilized in reag.py:

#### model
- Determines the language model used for answer generation
- Configured through LLMModelConfig with provider, model name, and operation mode

#### query
- User input string driving the answer generation process
- Combined with system prompts (e.g., REAG_SYSTEM_PROMPT) to create complete prompt messages

#### files
- Optional parameter for file uploads
- File content processed using MarkItDown module for text extraction

### Workflow
1. Tool trigger: reag.py's _invoke method receives parameters from reag.yaml (model, query, files)
2. File processing: Creates temporary files and converts content to text using MarkItDown
3. Parallel processing: Uses ThreadPoolExecutor for document processing
4. Response structure: Returns JSON object containing:
   - content: Generated answer
   - reasoning: Explanation of reasoning process
   - is_irrelevant: Boolean indicating relevance
   - document: Original document info (name and content)

## Trade-offs and Considerations

### Challenges
- **Cost**: Processing entire documents with LLMs is more expensive than vector search
- **Speed**: Can struggle with massive datasets despite parallelization

### Ideal Use Cases
1. Complex, open-ended queries
2. Dynamic data (news, research repositories)
3. Multimodal data (images, tables, charts)

## Future Prospects

### Key Trends
1. Cheaper, faster language models
   - Improvement in open-source models (Llama, DeepSeek)
   - Advancement in quantization techniques

2. Larger context windows
   - Expanding from millions to billions of tokens
   - Enhanced document processing capabilities

3. Hybrid systems
   - Combining lightweight embedding filters with ReAG
   - Balancing speed and accuracy

## Resources
- Twitter: https://x.com/pelaseyed/status/1886448015533089248
- Blog: https://www.superagent.sh/blog/reag-reasoning-augmented-generation
- GitHub: https://github.com/superagent-ai/reag/tree/main
