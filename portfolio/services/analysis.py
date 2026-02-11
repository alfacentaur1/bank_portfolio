from portfolio.services.ai_client import AIClient

class PortfolioAnalyzer:
    def __init__(self):
        self.client = AIClient()

    # Method for global portfolio summary
    def global_portfolio_summary(self, apps_data):
        """Generates risks and tech debt summary"""
        prompt = f"Analyze this bank portfolio and list top 5 risks and tech debt areas: {apps_data}"
        return self.client.get_completion(prompt)

    # Method for Q&A mode
    def ask_about_portfolio(self, question, context):
        """Handles the Q&A mode"""
        prompt = f"Context: {context}\nQuestion: {question}\nAnswer briefly with references to app names."
        return self.client.get_completion(prompt)

    # Method to generate Mermaid diagram with one automated check and fix
    def generate_checked_mermaid(self, app_name, integration_context):
        """
        Generates Mermaid code with one automated check and fix.
        """
        # 1. Initial generation
        gen_prompt = f"Generate Mermaid diagram code for {app_name} and its neighbors: {integration_context}"
        mermaid_code = self.client.get_completion(gen_prompt, system_prompt="Return ONLY Mermaid code.")

        # 2. Automated Check & Fix (The mandatory step from assignment)
        check_prompt = f"Check this Mermaid code for syntax errors and return it fixed. If it is fine, return it as is: {mermaid_code}"
        fixed_code = self.client.get_completion(check_prompt, system_prompt="Return ONLY the corrected Mermaid code.")
        
        return clean_mermaid(fixed_code)
    
def clean_mermaid(text):
    import re
    cleaned = re.sub(r'```[a-z]*', '', text)
    cleaned = cleaned.replace('```', '')
    return cleaned.strip()