# https://www.generacodice.com/jp/articolo/188462/wxPython:+execute+command+asynchronously,+display+stdout+in+text+widget
#https://rightcode.co.jp/blog/information-technology/python-asynchronous-program-multithread-does-not-work-approach
import wx


class   ThreadingFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, title=None):
        super().__init__( parent, id, title)
        self.timer = wx.Timer(self)
        self.timer.Start(500)

    def OnTimer(self, event):
        pass

    def timer_stop(self):
        self.timer.Stop()

class   MyWindow(ThreadingFrame):
    def __init__(self, parent=None, id=-1, title=None):
        super().__init__( parent, id, title)
        self.panel = wx.Panel(self, size=(300, 200))
        self.panel.SetBackgroundColour('WHITE')
        font = wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.stext = wx.StaticText(self.panel)
        self.stext.SetFont(font)
        self.stext.SetWindowStyle(wx.BORDER_SIMPLE)
        self.stext.CenterOnParent()
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Fit()
        self.counter = 20

    def OnTimer(self, event):
        super().OnTimer(event)
        self.stext.SetLabel("%02d" % self.counter)
        self.stext.CenterOnParent()
        if self.counter == 0:
            super().timer_stop()
        else:
            self.counter -= 1

if __name__ == '__main__':
    app = wx.App(False)
    w = MyWindow(title='wx-timer')
    w.Center()
    w.Show()
    app.MainLoop()