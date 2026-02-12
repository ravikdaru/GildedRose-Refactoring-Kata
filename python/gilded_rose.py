# -*- coding: utf-8 -*-

class GildedRose(object):

    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            self._update_item(item)

    def _update_item(self, item):
        if item.name == self.SULFURAS:
            return
        item.sell_in = item.sell_in - 1
        if item.name == self.AGED_BRIE:
            self._update_aged_brie(item)
        elif item.name == self.BACKSTAGE_PASSES:
            self._update_backstage_passes(item)
        else:
            self._update_normal(item)

    def _update_aged_brie(self, item):
        self._increase_quality(item, 1)
        if item.sell_in < 0:
            self._increase_quality(item, 1)

    def _update_backstage_passes(self, item):
        self._increase_quality(item, 1)
        if item.sell_in < 10:
            self._increase_quality(item, 1)
        if item.sell_in < 5:
            self._increase_quality(item, 1)
        if item.sell_in < 0:
            item.quality = 0

    def _update_normal(self, item):
        self._decrease_quality(item, 1)
        if item.sell_in < 0:
            self._decrease_quality(item, 1)

    def _increase_quality(self, item, amount):
        item.quality = min(50, item.quality + amount)

    def _decrease_quality(self, item, amount):
        item.quality = max(0, item.quality - amount)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
