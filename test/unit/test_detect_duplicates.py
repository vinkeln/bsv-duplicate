import pytest
from unittest.mock import patch
from src.util.detector import detect_duplicates
from src.util.parser import Article


# Test suite for detect_duplicates function
class TestDetectDuplicates:
    """Unit tests for detect_duplicates function"""
    
    # TC1: Empty string
    @pytest.mark.unit
    def test_empty_string_raises_valueerror(self):
        """Test that empty input raises ValueError"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.return_value = []
            
            with pytest.raises(ValueError):
                detect_duplicates("")
    
    # TC2: Single article
    @pytest.mark.unit
    def test_single_article_raises_valueerror(self):
        """Test that single article raises ValueError per docstring"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.return_value = [
                Article(key="key1", doi="10.1234/abc")
            ]
            
            with pytest.raises(ValueError):
                detect_duplicates("single article")
    
    # TC3: Two unique articles
    @pytest.mark.unit
    def test_two_unique_articles_returns_empty_list(self):
        """Test that two unique articles return empty list"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.return_value = [
                Article(key="key1", doi="10.1234/abc"),
                Article(key="key2", doi="10.5678/def")
            ]
            
            result = detect_duplicates("two unique articles")
            assert len(result) == 0
    
    # TC4: Same key, no DOI
    @pytest.mark.unit
    def test_same_key_no_doi_detects_duplicate(self):
        """Test that same key without DOI detects duplicate"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.return_value = [
                Article(key="key1", doi=None),
                Article(key="key1", doi=None)
            ]
            
            result = detect_duplicates("duplicate by key")
            assert len(result) == 1
            assert result[0].key == "key1"
    
    # TC5: Same key, same DOI
    @pytest.mark.unit
    def test_same_key_same_doi_detects_duplicate(self):
        """Test that same key and DOI detects duplicate"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.return_value = [
                Article(key="key1", doi="10.1234/abc"),
                Article(key="key1", doi="10.1234/abc")
            ]
            
            result = detect_duplicates("duplicate by key and DOI")
            assert len(result) == 1
    
    # TC6: Different key, same DOI
    @pytest.mark.unit
    def test_different_key_same_doi_detects_duplicate(self):
        """Test that same DOI with different keys detects duplicate"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.return_value = [
                Article(key="key1", doi="10.1234/abc"),
                Article(key="key2", doi="10.1234/abc")
            ]
            
            result = detect_duplicates("same DOI different key")
            assert len(result) == 1
    
    # TC7: Same key, different DOI
    @pytest.mark.unit
    def test_same_key_different_doi_no_duplicate(self):
        """Test that same key but different DOI is not duplicate"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.return_value = [
                Article(key="key1", doi="10.1234/abc"),
                Article(key="key1", doi="10.5678/def")
            ]
            
            result = detect_duplicates("same key different DOI")
            assert len(result) == 0
    
    # TC8: One has DOI, same key
    @pytest.mark.unit
    def test_one_has_doi_same_key_detects_duplicate(self):
        """Test that same key with one having DOI detects duplicate"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.return_value = [
                Article(key="key1", doi="10.1234/abc"),
                Article(key="key1", doi=None)
            ]
            
            result = detect_duplicates("one has DOI same key")
            assert len(result) == 1
    
    # TC9: Three articles, two duplicates
    @pytest.mark.unit
    def test_multiple_articles_with_duplicates(self):
        """Test detection of multiple duplicates"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.return_value = [
                Article(key="key1", doi="10.1234/abc"),
                Article(key="key1", doi="10.1234/abc"),
                Article(key="key2", doi="10.5678/def")
            ]
            
            result = detect_duplicates("multiple articles")
            assert len(result) == 1
    
    # TC10: Invalid BibTeX format
    @pytest.mark.unit
    def test_invalid_bibtex_format_raises_error(self):
        """Test that invalid format raises appropriate error"""
        with patch('src.util.detector.parse') as mock_parse:
            mock_parse.side_effect = ValueError("Invalid BibTeX format")
            
            with pytest.raises(ValueError):
                detect_duplicates("invalid format")
