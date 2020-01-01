import os
from unittest import TestCase
from unittest.mock import Mock, patch

from tests import TEST_DATA_DIR
from info_utils import work_ua_info


def fake_request_data_with_local_file(url):
    scheme, _, url_without_scheme = url.partition('//')
    filename = os.path.join(
        TEST_DATA_DIR,
        "{0}.htm".format(url_without_scheme.replace('/', '-'))
    )
    with open(filename, encoding='utf-8') as file:
        text_data = file.read()
    return text_data


class ParserTest(TestCase):
    @patch('info_utils.get_content', Mock(side_effect=fake_request_data_with_local_file))
    def test_parses_work_ua_with_all_data(self):
        info = work_ua_info('https://www.work.ua/jobs/3772744/')

        self.assertEqual(info['job_title'],
                         'Middle Front-end Developer (React)')
        self.assertEqual(info['company'], 'Місто Тревел')
        self.assertEqual(info['salary'], 40000)

        self.fail("Hey! You reached the end of the test")
