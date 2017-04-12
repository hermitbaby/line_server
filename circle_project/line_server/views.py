# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
from django.conf import settings
from .models import LineText

# TEXT_URL = "http://www.gutenberg.org/cache/epub/3300/pg3300.txt"

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def pre_process_text(request):
    initial_count = LineText.objects.count()

    if initial_count == 0:
        FILE_PATH = "{}/assets/adam_smith.txt".format(settings.BASE_DIR)
        line_text_list = []
        with open(FILE_PATH) as f:
            for idx, line in enumerate(f):
                # todo: consider compressing the line_text
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
        return HttpResponse("{} lines of text added to db.".format(count))

    else:
        return HttpResponse("Already initialized.")


def get_line(request, line_num):
    line_num = int(line_num)
    total = LineText.objects.count()
    if line_num > total:
        return HttpResponse("Out of bound. Total {} lines.".format(total), status=413)

    try:
        lt = LineText.objects.get(line_num=line_num)
    except LineText.DoesNotExist as e:
        pass

    text = lt.line_text
    return HttpResponse(text)




