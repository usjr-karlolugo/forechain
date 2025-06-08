from transformers import pipeline
import math

# Initialize summarization pipeline once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def smart_summarize(text, max_chunk_tokens=1024, max_length=130, min_length=30):
    # Rough token count = word count (approximate)
    tokens = len(text.split())
    
    if tokens <= max_chunk_tokens:
        # Text fits in one chunk: summarize all at once
        try:
            summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"[Summarization error]: {e}")
            return ""
    else:
        # Split text into chunks by word count
        chunks = []
        words = text.split()
        for i in range(0, tokens, max_chunk_tokens):
            chunk = " ".join(words[i:i + max_chunk_tokens])
            chunks.append(chunk)
        
        combined_summary = ""
        for chunk in chunks:
            try:
                summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                combined_summary += summary[0]['summary_text'] + " "
            except Exception as e:
                print(f"[Summarization error]: {e}")
                continue
        return combined_summary.strip()

