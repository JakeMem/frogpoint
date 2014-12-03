from wtforms import RadioField
from wtforms.widgets import HTMLString


class InlineRadioWidget(object):
    def __init__(self, html_tag='div', prefix_label=False):
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = []
        for subfield in field:
            if self.prefix_label:
                line = '<label class="radio-inline">{label} {field}</label>'
            else:
                line = '<label class="radio-inline">{field} {label}</label>'
            html.append(line.format(
                label=subfield.label.text,
                field=subfield(**kwargs)
            ))
        return HTMLString(''.join(html))


class InlineRadioField(RadioField):
    widget = InlineRadioWidget(prefix_label=False)
