import pytest
from unittest.mock import patch, Mock
from financial import request_processing, main

# Тестовые данные
SAMPLE_HTML = """
<html>
<div class="row lv-0 yf-t22klz">
    <span>Total Revenue</span>
    <span>100,000</span>
    <span>90,000</span>
</div>
</html>
"""



def test_request_processing_valid_data():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = request_processing("MSFT", "Total Revenue")

        assert isinstance(result, tuple)

        assert result[0] == "Total Revenue"
        print(result)
        assert len(result) == 3  # Название + 5 значения



def test_request_processing_invalid_field():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Field 'Invalid Field' not found"):
            request_processing("AAPL", "Invalid Field")


def test_main_valid_args(capsys):
    test_args = ["financial.py", "AAPL", "Total Revenue"]
    with patch('sys.argv', test_args), \
            patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        main()

        captured = capsys.readouterr()
        assert "Total Revenue" in captured.out

def test_main_invalid_args(capsys):
    test_args = ["financial.py", "AAPL"]  # Нет table_field
    with patch('sys.argv', test_args):
        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()
        assert "Invalid command" in captured.out

def test_data_structure():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = request_processing("AAPL", "Total Revenue")


        assert all(isinstance(item, str) for item in result)
        assert result[1].replace(',', '').isdigit()
        assert result[2].replace(',', '').isdigit()