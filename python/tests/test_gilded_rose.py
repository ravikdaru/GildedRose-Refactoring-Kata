# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        """Normal item: name unchanged, sell_in and quality updated per rules."""
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    def test_normal_item_decreases_quality_and_sell_in(self):
        """Normal item: quality decreases by 1, sell_in decreases by 1."""
        items = [Item("foo", 2, 5)]
        GildedRose(items).update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(1, items[0].sell_in)
        self.assertEqual(4, items[0].quality)

    def test_normal_item_quality_never_negative(self):
        """Quality never goes below 0."""
        items = [Item("normal item", 0, 0)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_aged_brie_increases_quality(self):
        """Aged Brie increases in quality over time."""
        items = [Item("Aged Brie", 2, 0)]
        GildedRose(items).update_quality()
        self.assertEqual(1, items[0].sell_in)
        self.assertEqual(1, items[0].quality)

    def test_sulfuras_never_changes(self):
        """Sulfuras never has to be sold or decreases in quality."""
        items = [Item("Sulfuras, Hand of Ragnaros", 0, 80)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(80, items[0].quality)

    def test_backstage_passes_increase_quality_faster_near_concert(self):
        """Backstage passes increase in quality; more when sell_in <= 10 or <= 5."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(4, items[0].sell_in)
        self.assertEqual(23, items[0].quality)  # +1 +2 (within 5 days)

    def test_backstage_passes_quality_drops_to_zero_after_concert(self):
        """Backstage passes quality is 0 after sell_in date."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    def test_conjured_item_degrades_twice_as_fast(self):
        """Conjured items degrade in Quality twice as fast as normal items."""
        items = [Item("Conjured Mana Cake", 3, 6)]
        GildedRose(items).update_quality()
        self.assertEqual(2, items[0].sell_in)
        self.assertEqual(4, items[0].quality)  # -2 (twice normal)

    def test_conjured_item_degrades_double_after_sell_by(self):
        """Conjured items degrade by 4 when past sell_in (double the expired rate)."""
        items = [Item("Conjured Mana Cake", 0, 6)]
        GildedRose(items).update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(2, items[0].quality)  # -2 (day) -2 (expired) = -4

    def test_conjured_quality_never_negative(self):
        """Conjured item quality never goes below 0."""
        items = [Item("Conjured Mana Cake", 0, 2)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)


if __name__ == '__main__':
    unittest.main()
