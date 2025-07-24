import base64
#import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
import struct

class TraceDrawer:
    chart = None

    def create_new_chart(self, title):
        fig = Figure(figsize=(9.6, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title(title, fontsize=14, fontweight='bold', fontname='DejaVu Sans')
        ax.set_xlabel("Time in ms")
        self.chart = (fig, ax)

    def add_data(self, name, timestep_ms, b64_data):
        if self.chart is None:
            self.create_new_chart("Trace")
        fig, ax = self.chart
        data = self.get_data_array_from_base64(b64_data)
        x = [(i + 1) * timestep_ms for i in range(len(data))]
        ax.plot(x, data, label=name)
        ax.legend()

    def get_chart_bitmap(self):
        if self.chart is None:
            return None
        fig, ax = self.chart
        canvas = FigureCanvas(fig)
        buf = BytesIO()
        canvas.print_png(buf)
        buf.seek(0)
        return buf.getvalue()  # PNG bytes

    def get_data_array_from_base64(self, base64_string):
        byte_array = base64.b64decode(base64_string)
        # Unpack as little-endian signed short (int16)
        int16_array = list(struct.unpack('<' + 'h' * (len(byte_array) // 2), byte_array))
        return int16_array