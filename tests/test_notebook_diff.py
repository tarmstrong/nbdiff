from nbdiff.notebook_diff import cells_diff, words_diff, lines_diff


def test_diff():
    A = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": []
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']},
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    ]
    B = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": []
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']}]
    result = cells_diff(A, B, check_modified=False)

    assert result[0]['state'] == 'unchanged'
    assert result[1]['state'] == 'deleted'


def test_diff_modified():
    A = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": []
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']},
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    ]
    B = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": []
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'k']}]

    result = cells_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'modified'
    assert result[1]['state'] == 'deleted'


def test_diff_lines_same():
    A = ['first line', 'second line']
    B = ['first line', 'second line']

    result = lines_diff(A, B)
    assert result[0]['state'] == 'unchanged'
    assert result[1]['state'] == 'unchanged'


def test_diff_lines_different():
    A = ['first line', 'second line']
    B = ['this is a line', 'another one']

    result = lines_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'deleted'
    assert result[2]['state'] == 'added'
    assert result[3]['state'] == 'added'


def test_diff_lines1():
    A = ['this is a line', 'another line']
    B = ['another line', 'first line']

    result = lines_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'unchanged'
    assert result[2]['state'] == 'added'


def test_diff_lines2():
    A = ['this is a line', 'another line']
    B = ['first line', 'another line']

    result = lines_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'modified'
    assert result[2]['state'] == 'added'


def test_diff_line3():
    A = ['first line']
    B = ['another new one', 'second one', 'first line']

    result = lines_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'added'
    assert result[1]['state'] == 'added'
    assert result[2]['state'] == 'unchanged'


def test_diff_lines4():
    A = ['fist line', 'first line']
    B = ['first lin', 'second one', 'first lin']

    result = lines_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'modified'
    assert result[2]['state'] == 'added'
    assert result[3]['state'] == 'added'


def test_diff_lines5():
    A = ['test', ' ']
    B = ['diff']

    result = lines_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'deleted'
    assert result[2]['state'] == 'added'


def test_diff_words_same():
    A = "word is"
    B = "word is"

    result = words_diff(A, B)
    assert result[0]['state'] == 'unchanged'
    assert result[1]['state'] == 'unchanged'


def test_empty_lines():
    A = ['this is a line']
    B = ['']

    result = lines_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'deleted'


def test_empty_words():
    A = "this is a line"
    B = " "

    result = words_diff(A, B)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'deleted'
    assert result[2]['state'] == 'deleted'
    assert result[3]['state'] == 'deleted'


def test_diff_words_different():
    A = "second one"
    B = "first test"

    result = words_diff(A, B)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'deleted'
    assert result[2]['state'] == 'added'
    assert result[3]['state'] == 'added'


def test_diff_word():
    A = "The"
    B = "This"

    result = words_diff(A, B)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'added'


def test_diff_word2():
    A = "hello world"
    B = "hello beautiful"

    result = words_diff(A, B)
    assert result[0]['state'] == 'unchanged'
    assert result[1]['state'] == 'deleted'
    assert result[2]['state'] == 'added'


def test_diff_cells_same():
    A = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']},
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    ]

    B = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']},
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    ]

    result = cells_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'unchanged'
    assert result[1]['state'] == 'unchanged'


def test_diff_cells_different():
    A = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,5]\n', u'z = {1} \n', u'\n', u'y']},
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    ]

    B = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']},
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [9,8,3]\n', u't = {8, 5, 6} \n', u'w']}
    ]

    result = cells_diff(A, B)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'unchanged'
    assert result[2]['state'] == 'added'


def test_diff_empty():
    A = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']},
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    ]
    B = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": []
             }
         ],
         "prompt_number": 29,
         u'input': []}]
    result = cells_diff(A, B, check_modified=True)
    assert result[0]['state'] == 'deleted'
    assert result[1]['state'] == 'deleted'


def test_diff_modified2():
    A = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'm']},
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,3]\n', u'z = {1, 2, 3} \n', u'\n', u'z']}
    ]
    B = [
        {'cell_type': "code",
         'language': "python",
         "outputs": [
             {
                 "output_type": "stream",
                 "stream": "stdout",
                 "text": [
                     "Hello, world!\n",
                     "Hello, world!\n"
                 ]
             }
         ],
         "prompt_number": 29,
         u'input': [u'x = [1,3,4]\n', u'z = {1, 2, 3} \n', u'\n', u'k']}
    ]
    result = cells_diff(A, B, check_modified=True)

    assert result[0]['state'] == 'modified'
    assert result[1]['state'] == 'deleted'
