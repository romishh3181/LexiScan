from config import SUMMARIZATION_MODEL
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
tokenizer=PegasusTokenizer.from_pretrained(SUMMARIZATION_MODEL)
summarizer=PegasusForConditionalGeneration.from_pretrained(SUMMARIZATION_MODEL)
def summarize(text):
    inputs=tokenizer(text,truncation=True,padding="longest",return_tensors="pt")
    summary_ytd=summarizer.generate(
        inputs['input_ids'],
        max_length=200,
        num_beams=7,
        length_penalty=2.0,
        early_stopping=True
    )
    summary=tokenizer.decode(summary_ytd[0],skip_special_tokens=True)
    summary = summary.replace("<n>", " ")
    return summary
