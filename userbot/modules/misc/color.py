import io
import re

import spectra
from PIL import Image

from ..help import add_help_item
from userbot.utils import parse_arguments
from userbot.events import register


@register(outgoing=True, pattern=r"^\.color\s+(.*)")
async def color_props(e):
    params = e.pattern_match.group(1) or ""
    args, color = parse_arguments(params, ['format', 'extended'])
    reply_message = await e.get_reply_message()

    if not color:
        await e.edit("Please provide a color...", delete_in=3)
        return

    if args.get('format') == 'rgb':
        r, g, b = re.findall(r'[\-.0-9]+', color)
        parsed = spectra.rgb(r, g, b)
    elif args.get('format') == 'lab':
        l, a, b = re.findall(r'[\-.0-9]+', color)
        parsed = spectra.lab(l, a, b)
    elif args.get('format') == 'lch':
        l, c, h = re.findall(r'[\-.0-9]+', color)
        parsed = spectra.lch(l, c, h)
    elif args.get('format') == 'hsl':
        h, s, l = re.findall(r'[\-.0-9]+', color)
        parsed = spectra.hsl(h, s, l)
    elif args.get('format') == 'hsv':
        h, s, v = re.findall(r'[\-.0-9]+', color)
        parsed = spectra.hsv(h, s, v)
    elif args.get('format') == 'xyz':
        x, y, z = re.findall(r'[\-.0-9]+', color)
        parsed = spectra.xyz(x, y, z)
    elif args.get('format') == 'cmy':
        c, m, y = re.findall(r'[\-.0-9]+', color)
        parsed = spectra.cmy(c, m, y)
    elif args.get('format') == 'cmyk':
        c, m, y, k = re.findall(r'[\-.0-9]+', color)
        parsed = spectra.cmyk(c, m, y, k)
    else:
        parsed = spectra.html(color)

    rgb = [round(x * 255) for x in parsed.to('rgb').clamped_rgb]
    hsl = parsed.to('hsl').values
    hsv = parsed.to('hsv').values

    formats = {
        'hex': parsed.hexcode,
        'rgb': values__to_str(rgb),
        'hsl': values__to_str(hsl),
        'hsv': values__to_str(hsv)
    }

    if args.get('extended'):
        formats.update({
            'lab': values__to_str(parsed.to('lab').values),
            'lch': values__to_str(parsed.to('lch').values),
            'xyz': values__to_str(parsed.to('xyz').values),
            'cmyk': values__to_str(parsed.to('cmyk').values)
        })

    message = ""
    for fmt in formats.items():
        message += f"**{fmt[0]}**: `{fmt[1]}` \n"

    swatch = make_swatch(tuple(rgb))
    await e.delete()
    await e.client.send_file(e.chat_id, swatch, caption=message, reply_to=reply_message)


def values__to_str(vals):
    vals = [round(val, 3) for val in vals]
    return ', '.join(map(str, vals))


def make_swatch(color, size=(300, 128)):
    output = io.BytesIO()
    color_swatch = Image.new(mode='RGB', size=size, color=color)
    color_swatch.save(output, format="PNG")
    return output.getvalue()


add_help_item(
    ".color",
    "Misc",
    "Show the supplied color and return it "
    "in different colorspaces.",
    """
    `.color [options] (color)`
    
    Options:
    `.format`: Format of the supplied color. Defaults to `html` which can be any valid HTML color (hex or name). Other valid values are `rgb`, `lab`, `lch`, `hsl`, `hsv`, `xyz`, `cmy`, and `cmyk`.
    `.extended`: Return some non-typical colorspaces in addition to the usual.
    """
)
