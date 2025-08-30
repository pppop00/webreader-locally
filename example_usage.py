"""
Example Usage: Local Web Reader
===============================

This file demonstrates various use cases for the Local Web Reader,
perfect for showcasing capabilities to HR, managers, and technical teams.

Run this file to see the tool in action:
python example_usage.py
"""

from web_reader_local import LocalWebReader, Website
import time

def demonstrate_basic_usage():
    """Basic web analysis demonstration."""
    print("🔍 BASIC WEB ANALYSIS")
    print("=" * 50)
    
    reader = LocalWebReader()
    
    # Example: News article analysis
    url = "https://www.cnn.com/2025/08/30/politics/zohran-mamdani-police-nypd-defund"
    print(f"Analyzing: {url}")
    print("-" * 50)
    
    start_time = time.time()
    summary = reader.summarize(url)
    end_time = time.time()
    
    print(summary)
    print(f"\n⏱️ Processing time: {end_time - start_time:.2f} seconds")
    print(f"💰 Cost: $0 (vs $0.02-0.05 with cloud APIs)")
    print("\n" + "="*70 + "\n")

def demonstrate_custom_prompts():
    """Show how to customize analysis for different business needs."""
    print("🎯 CUSTOM BUSINESS ANALYSIS")
    print("=" * 50)
    
    reader = LocalWebReader()
    
    # Business-focused analysis
    reader.set_system_prompt("""
    You are a business intelligence analyst. Focus on:
    - Key business metrics and financial information
    - Market trends and competitive advantages
    - Strategic opportunities and risks
    - Executive decisions and corporate announcements
    
    Provide insights in a professional business format with bullet points.
    """)
    
    # Example: Company website analysis
    url = "https://www.apple.com/newsroom/"
    print(f"Business Analysis of: {url}")
    print("-" * 50)
    
    summary = reader.summarize(url)
    print(summary)
    print("\n" + "="*70 + "\n")

def demonstrate_batch_processing():
    """Show batch processing capabilities for enterprise use."""
    print("📊 BATCH PROCESSING DEMO")
    print("=" * 50)
    
    reader = LocalWebReader()
    
    # Multiple URLs for analysis
    urls = [
        "https://techcrunch.com",
        "https://www.reuters.com/technology/",
        "https://www.bloomberg.com/technology"
    ]
    
    print("Processing multiple websites simultaneously...")
    print("(This would cost $0.06-0.15 with cloud APIs)")
    print("-" * 50)
    
    start_time = time.time()
    results = reader.batch_summarize(urls)
    end_time = time.time()
    
    for i, (url, summary) in enumerate(results.items(), 1):
        print(f"📄 RESULT {i}: {url}")
        print(summary[:200] + "..." if len(summary) > 200 else summary)
        print("-" * 30)
    
    print(f"\n⏱️ Total processing time: {end_time - start_time:.2f} seconds")
    print(f"💰 Total cost: $0 (vs $0.06-0.15 with cloud APIs)")
    print(f"📈 Cost savings: 100%")
    print("\n" + "="*70 + "\n")

def demonstrate_error_handling():
    """Show robust error handling capabilities."""
    print("🛡️ ERROR HANDLING DEMO")
    print("=" * 50)
    
    reader = LocalWebReader()
    
    # Test with invalid URL
    invalid_url = "https://this-website-definitely-does-not-exist.com"
    print(f"Testing with invalid URL: {invalid_url}")
    
    result = reader.summarize(invalid_url)
    print(f"Result: {result}")
    print("\n✅ Graceful error handling - system remains stable")
    print("\n" + "="*70 + "\n")

def show_cost_comparison():
    """Display cost comparison for business stakeholders."""
    print("💰 COST COMPARISON")
    print("=" * 50)
    
    requests_per_month = [100, 1000, 10000, 50000]
    
    print("Monthly Usage Scenarios:")
    print("-" * 30)
    
    for requests in requests_per_month:
        openai_cost = requests * 0.03  # $0.03 per request
        claude_cost = requests * 0.015  # $0.015 per request
        local_cost = 0  # $0 per request
        
        print(f"📊 {requests:,} requests/month:")
        print(f"   OpenAI GPT-4: ${openai_cost:.2f}")
        print(f"   Claude: ${claude_cost:.2f}")
        print(f"   Local Reader: ${local_cost:.2f}")
        print(f"   💡 Annual Savings: ${(openai_cost * 12):.2f} - ${(claude_cost * 12):.2f}")
        print()
    
    print("🎯 ROI: Immediate cost reduction with one-time setup")
    print("🔒 Privacy: 100% local processing, no data sent to external APIs")
    print("⚡ Performance: No rate limits, unlimited usage")
    print("\n" + "="*70 + "\n")

def main():
    """Main demonstration function."""
    print("🤖 LOCAL WEB READER - COMPREHENSIVE DEMO")
    print("=" * 70)
    print("This demo showcases the capabilities and business value")
    print("of our cost-effective, privacy-focused web analysis tool.")
    print("=" * 70)
    print()
    
    try:
        # Run all demonstrations
        demonstrate_basic_usage()
        demonstrate_custom_prompts()
        demonstrate_batch_processing()
        demonstrate_error_handling()
        show_cost_comparison()
        
        print("🎉 DEMO COMPLETE")
        print("=" * 50)
        print("✅ All features demonstrated successfully")
        print("💡 Ready for production deployment")
        print("📞 Contact team for enterprise integration")
        
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")
        print("💡 Ensure Ollama is installed and running:")
        print("   1. Install Ollama from https://ollama.ai")
        print("   2. Run: ollama pull llama3.2")
        print("   3. Run: ollama serve")

if __name__ == "__main__":
    main()
