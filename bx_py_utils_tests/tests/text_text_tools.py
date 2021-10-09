import inspect

from bx_py_utils.text_tools import cutout


def test_cutout():
    text = inspect.cleandoc('''
        line 1
        line 2
        01234567890 line 3
        line 4
        line 5
    ''')

    output = cutout(text, line_no=3, column=5, extra_lines=1)
    assert output == inspect.cleandoc('''
        02 line 2
        03 01234567890 line 3
        --------^
        04 line 4
    ''')

    output = cutout(text, line_no=3, column=1, extra_lines=0)
    assert output == inspect.cleandoc('''
        03 01234567890 line 3
        ----^
    ''')

    output = cutout(text, line_no=3, column=10, extra_lines=2)
    assert output == inspect.cleandoc('''
        01 line 1
        02 line 2
        03 01234567890 line 3
        -------------^
        04 line 4
        05 line 5
    ''')

    text = '\n'.join(f'The Line {no}' for no in range(20))
    output = cutout(text, line_no=18, column=9, extra_lines=2)
    assert output == inspect.cleandoc('''
        016 The Line 15
        017 The Line 16
        018 The Line 17
        -------------^
        019 The Line 18
        020 The Line 19
    ''')
