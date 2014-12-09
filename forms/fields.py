from wtforms import RadioField, SelectMultipleField
from wtforms.widgets import HTMLString, CheckboxInput


# ##
# Widgets

class InlineBoxWidget(object):
    def __init__(self, html_tag='div', klass='', prefix_label=False):
        self.klass = klass
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        print field.__class__, kwargs
        kwargs.setdefault('id', field.id)
        html = []
        for subfield in field:
            if self.prefix_label:
                line = '<label class="{klass}">{label} {field}</label>'
            else:
                line = '<label class="{klass}">{field} {label}</label>'
            html.append(line.format(
                klass=self.klass,
                label=subfield.label.text,
                field=subfield(**kwargs)
            ))
        return HTMLString(''.join(html))


class InlineRadioWidget(InlineBoxWidget):
    def __init__(self, html_tag='div', prefix_label=False):
        super(InlineRadioWidget, self).__init__(
            html_tag=html_tag,
            klass='radio-inline',
            prefix_label=prefix_label
        )


class InlineCheckboxWidget(InlineBoxWidget):
    pass


# ##
# Fields


class InlineRadioField(RadioField):
    widget = InlineRadioWidget(prefix_label=False)


class MultiCheckboxField(SelectMultipleField):
    widget = InlineCheckboxWidget(prefix_label=False)
    option_widget = CheckboxInput()
