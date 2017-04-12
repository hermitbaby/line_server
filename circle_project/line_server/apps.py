# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
import os
from django.conf import settings


class LineServerConfig(AppConfig):
    name = 'line_server'

    def ready(self):
        pre_process()


# one-time initialization when server is up
def pre_process():
    from .models import LineText

    initial_count = LineText.objects.count()

    if initial_count == 0:
        FILE_PATH = "{}/assets/adam_smith.txt".format(settings.BASE_DIR)
        line_text_list = []
        with open(FILE_PATH) as f:
            for idx, line in enumerate(f):
                # todo: consider compressing the line_text
                # in average, after compression text size will be 1/3 of original
                lt = LineText(line_num=idx, line_text=line)
                line_text_list.append(lt)

                # read 10000 lines and store data to db;
                # in case the file is really big
                if len(line_text_list) % 10000 == 0:
                    LineText.objects.bulk_create(line_text_list)
                    line_text_list = []

            # store the remaining objs in list
            LineText.objects.bulk_create(line_text_list)

        count = LineText.objects.count()
        print("{} lines of text added to db.".format(count))

    else:
        print("Already initialized.")