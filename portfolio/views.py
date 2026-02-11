from django.shortcuts import render, get_object_or_404
from portfolio.models import Application, ChatMessage, Integration
from portfolio.services.analysis import PortfolioAnalyzer
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Integration
from .forms import IntegrationForm
from django.db.models import Count
from django.http import HttpResponse

# 1. DASHBOARD - High-level metrics overview
def dashboard(request):
    total_apps = Application.objects.count()
    critical_apps = Application.objects.filter(criticality='High').count()
    medium_apps = Application.objects.filter(criticality='Medium').count()
    low_apps = Application.objects.filter(criticality='Low').count()
    cloud_apps = Application.objects.filter(hosting_environment__icontains='Cloud').count()
    integrations_count = Integration.objects.count()

    # Data pro sloupcový graf domén
    domain_data = Application.objects.values('domain').annotate(count=Count('id'))
    domain_labels = [item['domain'] for item in domain_data]
    domain_counts = [item['count'] for item in domain_data]

    context = {
        'total_apps': total_apps,
        'critical_apps': critical_apps,
        'medium_apps': medium_apps,
        'low_apps': low_apps,
        'cloud_apps': cloud_apps,
        'cloud_percentage': int((cloud_apps / total_apps * 100)) if total_apps > 0 else 0,
        'integrations_count': integrations_count,
        'domain_labels': domain_labels,
        'domain_counts': domain_counts,
    }
    return render(request, 'portfolio/dashboard.html', context)

# 2. LIST - Application inventory with basic search
def app_list(request):
    """
    Renders a list of all applications with optional domain filtering.
    """
    apps = Application.objects.all()
    
    # Simple filtering pattern using GET parameters
    domain = request.GET.get('domain')
    if domain:
        apps = apps.filter(domain__icontains=domain)
        
    return render(request, 'portfolio/app_list.html', {'apps': apps})

# 3. DETAIL - Individual application view
def app_detail(request, app_id):
    """
    Shows detailed attributes of a specific application and its integration neighbors.
    """
    app = get_object_or_404(Application, pk=app_id)
    # Fetch all integrations where this app is either source or target
    integrations = Integration.objects.filter(source_app=app) | Integration.objects.filter(target_app=app)
    
    return render(request, 'portfolio/app_detail.html', {
        'app': app,
        'integrations': integrations
    })

# 4. ANALYSIS - AI-driven strategic summary
def global_analysis(request):
    """
    Collects portfolio data and uses LLM to generate risk and tech debt analysis.
    """
    apps = Application.objects.all()
    # Serialize data into a simple string format for the LLM prompt
    summary_for_ai = ", ".join([f"{a.name} ({a.criticality}, {a.hosting_environment})" for a in apps])
    
    analyzer = PortfolioAnalyzer()
    report = analyzer.global_portfolio_summary(summary_for_ai)
    
    return render(request, 'portfolio/analysis.html', {'report': report})
# 5. Q&A MODE - Interactive question-answering interface
def qa_view(request):
    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question and len(question) <= 500:
            apps = Application.objects.all()
            context_data = ", ".join([f"{a.name}: {a.capabilities}" for a in apps])
            analyzer = PortfolioAnalyzer()
            answer = analyzer.ask_about_portfolio(question, context_data)
            ChatMessage.objects.create(question=question, answer=answer)
            
            if "HX-Request" in request.headers:
                chat_history = ChatMessage.objects.all().order_by('-created_at')[:10]
                return render(request, 'portfolio/chat_partial.html', {'chat_history': chat_history})

    chat_history = ChatMessage.objects.all().order_by('-created_at')[:10]
    return render(request, 'portfolio/qa.html', {'chat_history': chat_history})

# 6. MERMAID HELPER - Partial view for interactive diagrams
def generate_mermaid_view(request, app_id):
    """
    Special view triggered via HTMX to generate and validate a Mermaid diagram.
    """
    app = get_object_or_404(Application, pk=app_id)
    ints = Integration.objects.filter(source_app=app) | Integration.objects.filter(target_app=app)
    context_text = f"App {app.name} has these connections: " + \
                   ", ".join([f"{i.source_app.name} -> {i.target_app.name}" for i in ints])
    
    analyzer = PortfolioAnalyzer()
    mermaid_code = analyzer.generate_checked_mermaid(app.name, context_text)
    
    return render(request, 'portfolio/partials/mermaid_content.html', {
        'mermaid_code': mermaid_code,
        'app': app  
    })
def integration_list(request):
    integrations = Integration.objects.all()
    form = IntegrationForm()
    return render(request, 'portfolio/integrations.html', {
        'integrations': integrations,
        'form': form
    })

def integration_create(request):
    if request.method == "POST":
        form = IntegrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('integration_list')
    return redirect('integration_list')

def integration_delete(request, pk):
    integration = get_object_or_404(Integration, pk=pk)
    if request.method == "POST":
        integration.delete()
        # Pro HTMX vracíme prázdný string, aby prvek zmizel z UI
        return HttpResponse("") 
    return redirect('integration_list')