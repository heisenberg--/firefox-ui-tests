# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.decorators import skip_under_xvfb
from firefox_ui_harness.testcase import FirefoxTestCase


@skip_under_xvfb
class TestEscapeAutocomplete(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)

        # Clear complete history so there's no interference from previous entries.
        self.places.remove_all_history()

        self.test_urls = [
            'layout/mozilla.html',
            'layout/mozilla_community.html',
        ]
        self.test_urls = [self.marionette.absolute_url(t)
                          for t in self.test_urls]

        self.test_string = 'mozilla'

        self.locationbar = self.browser.navbar.locationbar
        self.autocomplete_results = self.locationbar.autocomplete_results

    def tearDown(self):
        self.autocomplete_results.close(force=True)
        FirefoxTestCase.tearDown(self)

    def test_escape_autocomplete(self):
        # Open some local pages
        def load_urls():
            with self.marionette.using_context('content'):
                for url in self.test_urls:
                    self.marionette.navigate(url)
        self.places.wait_for_visited(self.test_urls, load_urls)

        # Clear the location bar, type the test string, check that autocomplete list opens
        self.locationbar.clear()
        self.locationbar.urlbar.send_keys(self.test_string)
        self.assertEqual(self.locationbar.value, self.test_string)
        self.wait_for_condition(lambda _: self.autocomplete_results.is_open)

        # Press escape, check location bar value, check autocomplete list closed
        self.locationbar.urlbar.send_keys(self.keys.ESCAPE)
        self.assertEqual(self.locationbar.value, self.test_string)
        self.wait_for_condition(lambda _: not self.autocomplete_results.is_open)

        # Press escape again and check that locationbar returns to the page url
        self.locationbar.urlbar.send_keys(self.keys.ESCAPE)
        self.assertEqual(self.locationbar.value, self.test_urls[-1])
