class StarChatHelper:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def generate_response(
        self,
        instruction,
        code,
        max_new_tokens = 8000,
        do_sample = True,
        temperature = 0.2,
        top_k = 50,
        top_p = 0.95,
        eos_token_id = 49155
    ):

        # Create the prompt template with the instruction and the query placeholder

        prompt_template = "<|system|>{}\n<|end|>\n<|user|>\n{{query}}<|end|>\n<|assistant|>"

        # Add the instruction to the prompt template
        prompt = prompt_template.format(instruction)

        # Paste the query into the prompt
        prompt = prompt.format(query=code)

        # Generate the response
        outputs = self.pipeline(
            prompt,
            max_new_tokens=max_new_tokens, 
            do_sample=do_sample,
            temperature=temperature, 
            top_k=top_k,
            top_p=top_p,
            eos_token_id=eos_token_id
        )
        
        generated_text = outputs[0]['generated_text']

        # Extract the text after the <|assistant|> token
        separator = "<|assistant|>"
        _, _, rest = generated_text.partition(separator)
        
        return rest.strip()
    
    def extract_markdown_code(markdown, language = "python"):

        split_expr = f"```{language}" if language in markdown else "```"
        code_block = markdown.split(split_expr)[1].split("```")[0]

        return code_block