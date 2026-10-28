"""Offline regression checks for SUBTITLE-TRANSLATE-002.

The Cyrillic sample is synthetic; the original Tarabella file is unavailable.
Run directly: uv run --no-project python -B test-srt-blocks.py
"""
import unittest

from normalize_srt import f_split_srt_blocks


CUES = [
    "1\n00:00:01,000 --> 00:00:03,000\nПервая строка.\nВторая строка.",
    "2\n00:00:03,500 --> 00:00:05,000\n<i>Да, всё хорошо.</i>",
    "3\n00:00:06,000 --> 00:00:08,250\nНет! |#| Это часть реплики.",
]
SRT = "\n\n".join(CUES)


class SplitSrtBlocksTests(unittest.TestCase):
    def test_unix_windows_and_classic_mac_line_endings(self):
        for ending in ("\n", "\r\n", "\r"):
            with self.subTest(ending=repr(ending)):
                self.assertEqual(
                    f_split_srt_blocks(SRT.replace("\n", ending)), CUES
                )

    def test_mixed_line_endings(self):
        source = (
            CUES[0].replace("\n", "\r\n") + "\r\n\r\n"
            + CUES[1].replace("\n", "\r") + "\r\r"
            + CUES[2] + "\n"
        )
        self.assertEqual(f_split_srt_blocks(source), CUES)

    def test_blank_separator_lines_may_contain_spaces_or_tabs(self):
        for blank_line in ("\n \n", "\n\t\n", "\n \t \n"):
            with self.subTest(blank_line=repr(blank_line)):
                self.assertEqual(
                    f_split_srt_blocks(blank_line.join(CUES)), CUES
                )

    def test_repeated_and_outer_blank_lines_do_not_create_chunks(self):
        source = "\n \n\t\n" + "\n \n\n\t\n".join(CUES) + "\n\n \n\t"
        self.assertEqual(f_split_srt_blocks(source), CUES)

    def test_initial_utf8_bom_does_not_become_part_of_cue_number(self):
        source = ("\ufeff" + SRT).replace("\n", "\r\n")
        self.assertEqual(f_split_srt_blocks(source), CUES)

    def test_empty_and_whitespace_only_input(self):
        for source in ("", " ", "\t", "\n\r \t\r\n", "\ufeff \r\n"):
            with self.subTest(source=repr(source)):
                self.assertEqual(f_split_srt_blocks(source), [])

    def test_one_cue_without_trailing_newline(self):
        self.assertEqual(
            f_split_srt_blocks(CUES[0].replace("\n", "\r\n")), [CUES[0]]
        )

    def test_decoded_utf8_and_cp1251_uploads_preserve_cyrillic(self):
        for encoding in ("utf-8", "cp1251"):
            with self.subTest(encoding=encoding):
                uploaded = SRT.replace("\n", "\r\n").encode(encoding)
                decoded = uploaded.decode(encoding)
                self.assertEqual(f_split_srt_blocks(decoded), CUES)

    def test_downstream_metadata_and_text_round_trip(self):
        chunks = f_split_srt_blocks(
            ("\ufeff" + SRT + "\n").replace("\n", "\r\n")
        )
        metadata = []
        dialogue = []
        for chunk in chunks:
            lines = chunk.split("\n")
            metadata.append("\n".join(lines[:2]))
            dialogue.append("\n".join(lines[2:]))
        self.assertEqual(metadata, [
            "1\n00:00:01,000 --> 00:00:03,000",
            "2\n00:00:03,500 --> 00:00:05,000",
            "3\n00:00:06,000 --> 00:00:08,250",
        ])
        self.assertEqual(dialogue, [
            "Первая строка.\nВторая строка.",
            "<i>Да, всё хорошо.</i>",
            "Нет! |#| Это часть реплики.",
        ])
        rebuilt = "\n\n".join(
            header + "\n" + text for header, text in zip(metadata, dialogue)
        )
        self.assertEqual(rebuilt, SRT)

    def test_large_cues_are_never_cut_to_chunk_size(self):
        self.assertEqual(f_split_srt_blocks(SRT, chunk_size=1), CUES)

    def test_larger_chunk_size_retains_previous_grouping(self):
        size = len(CUES[0]) + 2 + len(CUES[1])
        self.assertEqual(
            f_split_srt_blocks(SRT, chunk_size=size),
            [CUES[0] + "\n\n" + CUES[1], CUES[2]],
        )

    def test_custom_separator_retains_previous_grouping(self):
        self.assertEqual(
            f_split_srt_blocks("one|#|two|#|three", separator="|#|", chunk_size=9),
            ["one|#|two", "three"],
        )

    def test_empty_custom_separator_still_raises(self):
        with self.assertRaises(ValueError):
            f_split_srt_blocks("text", separator="")


if __name__ == "__main__":
    unittest.main(verbosity=2)
