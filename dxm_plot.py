from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, TextInput, Button, CustomJS
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.palettes import Spectral11 as palette

# Specify a file to write the plot to
output_file("index.html")

# Tuples of groups (year, party)
x = [item for item in range(1,1400)]
y = []
c = [i for i in range(1,12)]
for i in c:
    y.insert(i, [(360000/(item*i))-100 for item in x])
data = {}
data['x_values'] = x
for item in c:
    data[f'{item}f'] = y[item-1]
# Bokeh wraps your data in its own objects to support interactivity
source = ColumnDataSource(data)
source2 = ColumnDataSource(data=dict(x=[], y=[]))

# Make the plot
p = figure(plot_height=400, plot_width=1200, title="DXM")

#p.varea_stack([f'{item}f' for item in c], x='x_values', source=source, color=palette)
for item in c:
    p.varea(x='x_values', y1=f'{item-1}f', y2=f'{item}f', source=source, color=palette[item-1], legend_label=f'{item}f', name=f'{item}f')
# Customise some display properties
p.y_range.start = 0
p.y_range.end = 400
p.x_range.range_padding = 0
p.yaxis.axis_label = 'Arsenal Fire Rate Support'
p.xaxis.axis_label = 'Weapon Fire Rate'
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None
text_input1 = TextInput(value="", title="Fire rate")
text_input2 = TextInput(value="", title="Arsenal fire rate support")

p.circle(x='x', y='y', source=source2, size=10, color='black')
p.ray(x=0, y='y', length=0, source=source2, line_width=2, color='black')
p.ray(x='x', y=0, length=0, angle=1.5708, source=source2, line_width=2, color='black')

callback = CustomJS(args=dict(x=text_input1, y=text_input2, source=source2), code="""
    var d = source.data;
    d['x'] = [x.value];
    d['y'] = [y.value];
    source.change.emit();
""")


button = Button(label='Calculate')
button.js_on_click(callback)
# hover = HoverTool()
# hover.tooltips = """
# <div style=padding=5px>Fire rate: @x_values</div>
# """
column1 = column(text_input1, text_input2, button)
layout = row(column1, p)
show(layout)
