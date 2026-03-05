from src.Batch_Handling.duplicate_checking import check_duplication, hashing, time_processing
from unittest.mock import MagicMock
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

def test_check_duplication(mocker):
    cur_mock = MagicMock()
    cur_mock.fetchall.return_value = [("abc123", "uploaded")]

    conn_mock = MagicMock()
    conn_mock.__enter__.return_value = conn_mock
    conn_mock.cursor.return_value.__enter__.return_value = cur_mock

    mocker.patch("src.Batch_Handling.duplicate_checking.psycopg.connect", return_value = conn_mock)

    docs = [{"topic_name": "crypto", "list_of_art":[
        {"hash": "abc123", "art_title": "Old article"},
        {"hash": "xyz999", "art_title": "New article"}
    ]}]

    check_duplication("fake_connection_string", docs)

    assert len(docs[0]["list_of_art"]) == 1
    assert docs[0]["list_of_art"][0]["hash"] == "xyz999"