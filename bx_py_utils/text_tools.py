def cutout(text, line_no, column, extra_lines=2):
    """
    Mark a point in a long text by line no + column with context lines around.
    """
    assert isinstance(text, str)
    assert line_no >= 0
    assert column >= 0
    assert extra_lines >= 0

    lines = text.splitlines()
    line_count = len(lines)

    assert line_no <= line_count

    from_line = line_no - extra_lines - 1
    if from_line < 0:
        from_line = 0

    to_line = line_no + extra_lines
    if to_line > line_count:
        to_line = line_count

    line_no_width = len(str(from_line)) + 1

    lines = lines[from_line: to_line]
    result = []
    for no, line in enumerate(lines, from_line + 1):
        result.append(
            f'{no:0{line_no_width}} {line}'
        )
        if no == line_no:
            result.append(
                f'{"-"*(line_no_width+column+1)}^'
            )

    return '\n'.join(result)
