from pathlib import Path
import zipfile


class TestingFiles:
    ARCHIVE_FILEPATH = Path('tests/testing_data/testing_data.zip')
    file_mapping = {
        'allience': 'alliances_162_en_20200422_165757_062851.xml',
        'highscore_total': 'highscore_162_en_1_0_20200422_170240_197857.xml',
        'highscore_economy': 'highscore_162_en_1_1_20200422_170240_348153.xml',
        'highscore_research': 'highscore_162_en_1_2_20200422_170240_500826.xml',
        'highscore_military': 'highscore_162_en_1_3_20200422_170240_665208.xml',
        'highscore_mil_built': 'highscore_162_en_1_4_20200422_170240_816050.xml',
        'highscore_mil_destroyed': 'highscore_162_en_1_5_20200422_170240_975528.xml',
        'highscore_mil_lost': 'highscore_162_en_1_6_20200422_170241_126518.xml',
        'highscore_honor': 'highscore_162_en_1_7_20200422_170241_295144.xml',
        'players': 'players_162_en_20200422_165756_623433.xml',
        'universe': 'universe_162_en_20200422_165756_915643.xml',
        'universe_data': 'universes_20200422_171937_861597.json',
    }

    def get_file_path(self, file_type: str):
        if file_type not in self.file_mapping.keys():
            raise KeyError(
                f'got `{file_type}`. valid ones are {list(self.file_mapping)}.'
            )
        return self.file_mapping[file_type]

    def load_file(self, file_type: str) -> bytes:
        with zipfile.ZipFile(self.ARCHIVE_FILEPATH, 'r') as zf:
            file_name = self.get_file_path(file_type)
            data = zf.read(file_name)
        return data

    def load_file_as_str(self, file_type: str) -> str:
        return self.load_file(file_type).decode()
