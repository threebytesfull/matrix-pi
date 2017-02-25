import unittest

from the_matrix.layout import Layout
from collections import namedtuple

class TestLayout(unittest.TestCase):
    """Test Layout class"""

    def test_create_default(self):
        """Check default layout size"""
        layout = Layout()
        self.assertEqual(layout.width, 24)
        self.assertEqual(layout.height, 5)

    def test_create_24x5(self):
        """Check 24x5 layout size"""
        layout = Layout(width=24, height=5)
        self.assertEqual(layout.width, 24)
        self.assertEqual(layout.height, 5)

    def test_create_12x11(self):
        """Check 12x11 layout size"""
        layout = Layout(width=12, height=11)
        self.assertEqual(layout.width, 12)
        self.assertEqual(layout.height, 11)

    def test_create_bad_layout(self):
        """Check refusal to create layout of bad size"""
        with self.assertRaises(AssertionError):
            layout = Layout(width=10, height=5)

    def test_not_reversed_by_default(self):
        """Check LEDs in layout are not reversed by default"""
        layout = Layout()
        self.assertFalse(layout.reversed)

    def test_layout_reversed_on_request(self):
        """Check LEDs in layout are reversed on request"""
        layout = Layout(reversed=True)
        self.assertTrue(layout.reversed)

    def test_coords_out_of_range(self):
        """Check bad coordinates are rejected"""
        layout = Layout()
        with self.assertRaises(AssertionError):
            led = layout.ledAt(-1, 0)
        with self.assertRaises(AssertionError):
            led = layout.ledAt(0, -1)
        with self.assertRaises(AssertionError):
            led = layout.ledAt(layout.width, 0)
        with self.assertRaises(AssertionError):
            led = layout.ledAt(0, layout.height)

    def _check_expected_leds(self, layout, expected_leds):
        for expected_led, x, y in expected_leds:
            led = layout.ledAt(x, y)
            self.assertEqual(led, expected_led, 'should get LED 0x%02X at %d,%d' % (expected_led, x, y))

    def test_led_for_good_coords_24x5(self):
        """Check good coordinates return an LED for 24x5 matrix"""
        layout = Layout(24, 5)
        expected_leds = [
            [0x00, 0, 0],
            [0xb5, 23, 0],
            [0x09, 1, 4],
            [0xb4, 22, 4],
            [0x57, 11, 2],
        ]
        self._check_expected_leds(layout, expected_leds)

    def test_led_for_good_coords_12x11(self):
        """Check good coordinates return an LED for 12x11 matrix"""
        layout = Layout(12, 11)
        expected_leds = [
            [0x00, 0, 0],
            [0xb0, 11, 0],
            [0x0a, 0, 10],
            [0xba, 11, 10],
            [0x53, 5, 3],
        ]
        self._check_expected_leds(layout, expected_leds)

    def test_led_for_good_coords_24x5_reversed(self):
        """Check good coordinates return an LED for 24x5 reverse-connected matrix"""
        layout = Layout(24, 5, reversed=True)
        expected_leds = [
            [0x10, 0, 0],
            [0x5a, 23, 0],
            [0xa0, 1, 4],
            [0x4a, 22, 4],
            [0x85, 11, 2],
        ]
        self._check_expected_leds(layout, expected_leds)

    def test_addresses_for_led_number(self):
        """Check address mapping for LED by number"""
        layout = Layout()
        LED = namedtuple('LED', 'number on_off_byte on_off_bit blink_byte blink_bit pwm_byte')
        expected_leds = [
            LED(0x00, 0x00, 0, 0x00, 0, 0x18),
            LED(0x21, 0x04, 1, 0x04, 1, 0x2f),
            LED(0x29, 0x05, 1, 0x05, 1, 0x37),
            LED(0x3a, 0x07, 2, 0x07, 2, 0x43),
        ]
        for e in expected_leds:
            self.assertEqual(layout.numToAddressOnOff(e.number), (e.on_off_byte, e.on_off_bit), 'should get correct on/off address for led %02X' % e.number)
            self.assertEqual(layout.numToAddressBlink(e.number), (e.blink_byte, e.blink_bit), 'should get correct blink address for led %02X' % e.number)
            self.assertEqual(layout.numToAddressPWM(e.number), e.pwm_byte, 'should get correct PWM address for led %02X' % e.number)

if __name__ == '__main__':
    unittest.main()
