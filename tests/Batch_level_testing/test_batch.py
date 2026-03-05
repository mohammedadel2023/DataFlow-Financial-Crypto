from src.Batch_Handling.duplicate_checking import check_duplication, hashing, time_processing
from datetime import datetime

def test_time_processing():
    # Define the expected datetime object
    expected_time = datetime(2023, 10, 10, 0, 0)
    
    # Test case 1: Standard format
    assert time_processing({"time": "Updated Oct 10, 2023"}) == expected_time
    
    # Test case 2: Lowercase 'u'
    assert time_processing({"time": "updated Oct 10, 2023"}) == expected_time
    
    # Test case 3: Missing space after comma
    assert time_processing({"time": "Updated Oct 10, 2023"}) == expected_time

def test_hashing_logic():
    sample_data = [{"list_of_art":[{"time": "Updated Oct 10, 2023", "art_title": "Article 1","hash":""}]}]
    sample_data2 = [{"list_of_art":[{"time": "Updated Oct 10, 2023", "art_title": "Article 1","hash":""}]}]
    # A hash should always be consistent for the same input
    hashing(sample_data)
    hashing(sample_data2)
    hash1 = sample_data[0]["list_of_art"][0]["hash"]
    hash2 = sample_data2[0]["list_of_art"][0]["hash"]   
    assert hash1 == hash2
