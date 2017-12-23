# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

import re
# Create your tests here.

class TwitterClientTests(TestCase):

	def is_clean_tweet(self):
		test_string = 'this is a real life example of a tweet with special characters \ \r \t'
		result = clean_tweet(self, test_string)
		if re.match("^[a-zA-Z0-9_]*$", result):
			self.assertTrue(True)
		else:
			self.assertFalse(True)

