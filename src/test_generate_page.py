import unittest

from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        text = """# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
* Disney *didn't ruin it*
* It created an entirely new genre of fantasy

## My favorite characters (in order)"""
        result = extract_title(text)
        expected = "Tolkien Fan Club"
        self.assertEqual(result, expected)

    def test_extract_title_no_heading(self):
        text = """## Reasons I like Tolkien
    
    * You can spend years studying the legendarium and still not understand its depths
    * It can be enjoyed by children and adults alike
    * Disney *didn't ruin it*
    * It created an entirely new genre of fantasy"""
        with self.assertRaises(ValueError) as context:
            extract_title(text)
        self.assertEqual(str(context.exception), "No h1 heading in md file")

