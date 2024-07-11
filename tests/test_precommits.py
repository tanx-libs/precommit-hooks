from unittest.mock import mock_open, patch
from pre_commit_hooks.private_key_check import check_regex_match

class TestPreCommitCheck:
    def test_private_key_success_match(self):
        mock_content = """
         0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6
        '0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6'
        '0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6',
        "0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6"
        "0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6",
        "0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6";
        """

        with patch('builtins.open', mock_open(read_data=mock_content)) as mock_file:
            result = check_regex_match('test.txt')
            assert len(mock_content.splitlines())-2 == len(result.splitlines())  # '-2' as mock_content have 2 empty following """"

    def test_private_key_success_noqa_ignore(self):
        mock_content = """
         0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6  #noqa:keycheck
        '0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6'  #noqa:keycheck
        '0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6',    #noqa:keycheck
        "0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6"# noqa:keycheck
        "0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6",  #    noqa:keycheck
        "0xc12e72dacf06749d6b1ebaaac7eb8bc50af0844b87595ce0491b98dc3d51a6"; #noqa:keycheck
        """

        with patch('builtins.open', mock_open(read_data=mock_content)) as mock_file:
            result = check_regex_match('test.txt')
            assert None == result  # 'None' as hook returns None if no match