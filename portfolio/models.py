from django.db import models

class Application(models.Model):
    """
    Core model representing a bank application or satellite system.
    Covers domain, criticality, lifecycle, ownership, and tech stack.
    """
    # Basic Info

    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=100) # e.g., Retail Banking, Corporate Banking, etc.
    criticality = models.CharField(max_length=50, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    lifecycle = models.CharField(max_length=50) # e.g., Development, Production, Maintenance

    # Ownership
    business_owner = models.CharField(max_length=255)
    it_owner = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255, blank=True, null=True)

    # Technology Stack
    programming_languages = models.CharField(max_length=255) # e.g., Java, Python, etc.
    database = models.CharField(max_length=255) # e.g., Oracle, MySQL, etc.
    hosting_environment = models.CharField(max_length=255) # e.g., On-Premises, Cloud, Hybrid

    # Capabilities
    capabilities = models.TextField() # e.g., List of key functionalities or services provided
    technical_dependencies = models.TextField() # e.g., Other systems or technologies this application depends on
    tech_debt_score = models.IntegerField(default=0) # A simple numeric score to represent technical debt level, for example

    # Returns a string representation of the application
    def __str__(self) -> str:
        return self.name
    
# Table to represent the integration between applications
class Integration(models.Model):
    """
    Represents data flow between two applications. 
    Required for generating Mermaid diagrams and tracking data sensitivity.
    """
    # Relationship between apps 
    # Saves 2 columns for source and target app, to track direction and details of integration
    source_app = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='outgoing_integrations'
    )
    target_app = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE, 
        related_name='incoming_integrations'
    )
    
    # Integration Details [cite: 104]
    integration_type = models.CharField(max_length=50) # API, File, Message
    direction = models.CharField(max_length=50)        # Inbound, Outbound
    data_volume = models.CharField(max_length=100)     # e.g., High, 1M/day
    data_sensitivity = models.CharField(max_length=100) # e.g., GDPR, Internal, Public

    def __str__(self):
        return f"{self.source_app} -> {self.target_app} ({self.integration_type})"
    
# New model to store Q&A interactions for the Q&A mode
class ChatMessage(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Orders messages by creation time, newest first