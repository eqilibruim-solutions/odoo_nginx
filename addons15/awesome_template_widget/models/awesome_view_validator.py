# -*- coding: utf-8 -*-

from odoo import tools
from odoo.tools import view_validation
from lxml import etree
import logging
import os

_relaxng_cache = view_validation._relaxng_cache

_logger = logging.getLogger(__name__)

_relaxng_cache['tree'] = None

file_path = os.path.split(os.path.realpath(__file__))[0]

with tools.file_open(os.path.join(file_path, '../rng/tree_view.rng')) as frng:
    try:
        text = frng.read()
        tmp_doc = etree.fromstring(text.encode('utf-8'))
        _relaxng_cache['tree'] = etree.RelaxNG(tmp_doc)
    except Exception as error:
        _logger.exception('Failed to load RelaxNG XML schema for views validation, {error}'.format(
            error=error))
        _relaxng_cache['tree'] = None
        
