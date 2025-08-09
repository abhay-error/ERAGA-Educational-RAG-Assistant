#!/usr/bin/env python3
"""
Test script for OpenRouter integration

This script tests the OpenRouter configuration and API connectivity.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.config import config
from src.llm_provider import LLMProvider

def test_openrouter_config():
    """Test OpenRouter configuration."""
    print("🔧 Testing OpenRouter configuration...")
    try:
        # Get LLM config
        llm_config = config.get_llm_config()
        openrouter_config = llm_config.get('openrouter', {})
        
        print(f"✅ Configuration loaded successfully")
        print(f"   Provider: {llm_config.get('provider', 'N/A')}")
        print(f"   Model: {llm_config.get('model', 'N/A')}")
        print(f"   OpenRouter API Key: {'✅ Configured' if openrouter_config.get('api_key') else '❌ Not configured'}")
        print(f"   OpenRouter Base URL: {openrouter_config.get('base_url', 'N/A')}")
        print(f"   OpenRouter Model: {openrouter_config.get('model', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_openrouter_connection():
    """Test OpenRouter API connection."""
    print("\n🌐 Testing OpenRouter API connection...")
    try:
        llm = LLMProvider()
        
        if llm.provider != 'openrouter':
            print(f"❌ Provider is set to {llm.provider}, not openrouter")
            return False
        
        print(f"✅ LLM provider initialized: {llm.provider}")
        print(f"   Model: {llm.model}")
        
        # Test a simple query
        test_query = "Hello! Can you tell me what 2+2 equals?"
        print(f"\n🤖 Testing with query: '{test_query}'")
        
        response = llm.generate_response(
            context="",
            query=test_query,
            system_prompt="You are a helpful AI assistant. Please provide a brief and accurate response."
        )
        
        if response.startswith("Error:"):
            print(f"❌ OpenRouter API test failed: {response}")
            return False
        else:
            print(f"✅ OpenRouter API test successful!")
            print(f"   Response: {response[:200]}{'...' if len(response) > 200 else ''}")
            return True
            
    except Exception as e:
        print(f"❌ OpenRouter connection test failed: {e}")
        return False

def test_openrouter_with_context():
    """Test OpenRouter with context."""
    print("\n📚 Testing OpenRouter with context...")
    try:
        llm = LLMProvider()
        
        context = """
        Python is a high-level, interpreted programming language known for its simplicity and readability.
        It was created by Guido van Rossum and first released in 1991.
        Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.
        """
        
        query = "What are the main features of Python?"
        
        print(f"🤖 Testing with context and query: '{query}'")
        
        response = llm.generate_response(
            context=context,
            query=query,
            system_prompt="You are a helpful AI assistant for the School of Engineering at the University of Mysore. Provide accurate and helpful responses based on the context provided."
        )
        
        if response.startswith("Error:"):
            print(f"❌ OpenRouter context test failed: {response}")
            return False
        else:
            print(f"✅ OpenRouter context test successful!")
            print(f"   Response: {response[:300]}{'...' if len(response) > 300 else ''}")
            return True
            
    except Exception as e:
        print(f"❌ OpenRouter context test failed: {e}")
        return False

def main():
    """Run all OpenRouter tests."""
    print("🧪 OpenRouter Integration Test")
    print("=" * 40)
    
    tests = [
        ("Configuration", test_openrouter_config),
        ("API Connection", test_openrouter_connection),
        ("Context Processing", test_openrouter_with_context),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All OpenRouter tests passed! OpenRouter is working correctly.")
        return 0
    else:
        print("⚠️ Some OpenRouter tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
