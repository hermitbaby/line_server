# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class LineText(models.Model):
    # create index on line number field in db
    line_num = models.IntegerField(default=0, db_index=True)
    line_text = models.CharField(max_length=512)
