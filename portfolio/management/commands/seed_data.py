import json
import time
from django.core.management.base import BaseCommand
from portfolio.models import Application, Integration
from portfolio.services.ai_client import AIClient

class Command(BaseCommand):
    help = 'Generates 40 apps and 40 integrations in stable batches'

    def handle(self, *args, **kwargs):
        client = AIClient()
        
        # 1. CLEAN SLATE
        self.stdout.write("Wiping existing data...")
        Integration.objects.all().delete()
        Application.objects.all().delete()

        # 2. GENERATE APPLICATIONS IN BATCHES (4 x 10)
        total_apps_target = 40
        batch_size = 10
        
        self.stdout.write(f"Starting batch generation for {total_apps_target} applications...")
        
        for i in range(total_apps_target // batch_size):
            self.stdout.write(f"🚀 Processing App Batch {i+1}/4...")
            
            apps_prompt = f"""
            Generate a JSON list of {batch_size} unique bank applications.
            Include fields: "name", "domain", "criticality" (High/Medium/Low), "lifecycle", 
            "business_owner", "it_owner", "vendor", "programming_languages", 
            "database", "hosting_environment", "capabilities", "technical_dependencies", "tech_debt_score" (1-10).
            Return ONLY raw JSON array.
            """
            
            try:
                # Tip: If your AIClient supports it, you could pass model="gpt-4o" here
                raw = client.get_completion(apps_prompt)
                
                # Clean Markdown
                if "```json" in raw: raw = raw.split("```json")[1].split("```")[0]
                elif "```" in raw: raw = raw.split("```")[1].split("```")[0]
                
                data = json.loads(raw.strip())
                for item in data:
                    # Data pre-processing for lists
                    for field in ['programming_languages', 'capabilities', 'technical_dependencies']:
                        if isinstance(item.get(field), list):
                            item[field] = ", ".join(item[field])
                    Application.objects.create(**item)
                
                self.stdout.write(self.style.SUCCESS(f"✅ Batch {i+1} saved."))
                time.sleep(1) # Small pause for API stability
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Batch {i+1} failed: {e}"))

        # 3. GENERATE INTEGRATIONS IN BATCHES (4 x 10)
        self.stdout.write("Generating 40 integrations...")
        for j in range(4):
            existing_apps = list(Application.objects.values_list('name', flat=True))
            if not existing_apps: break
            
            ints_prompt = f"""
            Based on these apps: {existing_apps}
            Generate a JSON list of 10 unique integrations.
            Fields: "source_app_name", "target_app_name", "integration_type", "direction", "data_volume", "data_sensitivity".
            Return ONLY raw JSON array.
            """
            
            try:
                ints_raw = client.get_completion(ints_prompt)
                if "```json" in ints_raw: ints_raw = ints_raw.split("```json")[1].split("```")[0]
                
                ints_data = json.loads(ints_raw.strip())
                for i_item in ints_data:
                    try:
                        source = Application.objects.get(name=i_item.pop('source_app_name'))
                        target = Application.objects.get(name=i_item.pop('target_app_name'))
                        Integration.objects.create(source_app=source, target_app=target, **i_item)
                    except: continue
                self.stdout.write(self.style.SUCCESS(f"🔗 Integration Batch {j+1}/4 completed."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Integration Batch {j+1} failed: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Done! Final count: {Application.objects.count()} apps, {Integration.objects.count()} ints."))