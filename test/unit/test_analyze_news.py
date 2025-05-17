import pytest
import sys
import os
import requests
from unittest.mock import patch, MagicMock
import logging
from langchain_community.document_loaders import WebBaseLoader
from langchain.chat_models import init_chat_model
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.analyze_news import get_news_content, analyze_news_content, analyze_all_summaries

# Test get_news_content function
def test_get_news_content_success():
    """Test successful content retrieval from a valid URL"""
    mock_loader = MagicMock(spec=WebBaseLoader)
    mock_loader.lazy_load.return_value = ["Test content"]
    
    with patch('src.analyze_news.WebBaseLoader', return_value=mock_loader):
        result = get_news_content("https://example.com")
        assert result == ["Test content"]
        mock_loader.lazy_load.assert_called_once()

def test_get_news_content_invalid_url():
    """Test handling of invalid URL schema"""
    with patch('src.analyze_news.WebBaseLoader') as mock_loader:
        mock_loader.side_effect = requests.exceptions.InvalidSchema("Invalid URL")
        result = get_news_content("invalid://url")
        assert result == []
        assert logging.getLogger().handlers[0].level == logging.ERROR

# Test analyze_news_content function
def test_analyze_news_content_success():
    """Test successful analysis of news content"""
    mock_llm = MagicMock()
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = "Test summary"
    
    with patch('src.analyze_news.init_chat_model', return_value=mock_llm), \
         patch('src.analyze_news.create_stuff_documents_chain', return_value=mock_chain), \
         patch('src.analyze_news.get_news_content', return_value=["Test content"]):
        result = analyze_news_content("https://example.com")
        assert result == "Test summary"
        mock_chain.invoke.assert_called_once()

def test_analyze_news_content_exception():
    """Test handling of exceptions during analysis"""
    with patch('src.analyze_news.init_chat_model', side_effect=Exception("Test error")):
        result = analyze_news_content("https://example.com")
        assert result == ""
        assert logging.getLogger().handlers[0].level == logging.ERROR

# Test analyze_all_summaries function
def test_analyze_all_summaries_success():
    """Test successful analysis of multiple summaries"""
    mock_analyze_news_content = MagicMock()
    mock_analyze_news_content.side_effect = ["Summary 1", "Summary 2"]
    
    with patch('src.analyze_news.analyze_news_content', mock_analyze_news_content):
        result = analyze_all_summaries(["url1", "url2"])
        assert mock_analyze_news_content.call_count == 3  # 2 for individual summaries, 1 for final analysis

def test_analyze_all_summaries_empty_list():
    """Test handling of empty input list"""
    result = analyze_all_summaries([])
    assert result == ""  # Should return empty string for empty input

def test_analyze_all_summaries_single_item():
    """Test analysis of single summary"""
    mock_analyze_news_content = MagicMock(return_value="Single summary")
    
    with patch('src.analyze_news.analyze_news_content', mock_analyze_news_content):
        result = analyze_all_summaries(["url1"])
        assert result == "Single summary"
        assert mock_analyze_news_content.call_count == 2  # 1 for individual summary, 1 for final analysis 