# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainPanelBase
###########################################################################

class MainPanelBase ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"ハウスの巻上げ君    Ver 0.0.1 ©keinafarm.com", pos = wx.DefaultPosition, size = wx.Size( 487,459 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer = wx.GridBagSizer( 2, 7 )
		gbSizer.SetFlexibleDirection( wx.BOTH )
		gbSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_bitmap_image = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmap_image.SetMinSize( wx.Size( 320,240 ) )

		gbSizer.Add( self.m_bitmap_image, wx.GBPosition( 1, 0 ), wx.GBSpan( 4, 1 ), wx.ALL, 5 )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"ハウスの巻き上げ君　　　Ver 0.0.1  (C)Keinafarm.com", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		gbSizer.Add( self.m_staticText1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )

		self.m_button_capture = wx.Button( self, wx.ID_ANY, u"キャプチャー", wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer.Add( self.m_button_capture, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_text_message = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_text_message.SetMinSize( wx.Size( 450,50 ) )

		gbSizer.Add( self.m_text_message, wx.GBPosition( 6, 0 ), wx.GBSpan( 2, 2 ), wx.ALL, 5 )

		self.m_button_up = wx.Button( self, wx.ID_ANY, u"開く", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_up.SetMinSize( wx.Size( 100,60 ) )

		gbSizer.Add( self.m_button_up, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_button_stop = wx.Button( self, wx.ID_ANY, u"停止", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		self.m_button_stop.SetMinSize( wx.Size( 100,60 ) )

		gbSizer.Add( self.m_button_stop, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_button_down = wx.Button( self, wx.ID_ANY, u"閉める", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_down.SetMinSize( wx.Size( 100,60 ) )

		gbSizer.Add( self.m_button_down, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_bitmap_motorOn = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"MotorOff.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 64,64 ), 0 )
		bSizer1.Add( self.m_bitmap_motorOn, 0, wx.ALL, 5 )

		self.m_bitmap_motorDir = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"MotorStop.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 64,64 ), 0 )
		bSizer1.Add( self.m_bitmap_motorDir, 0, wx.ALL, 5 )

		self.m_bitmap_Error = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"ErrorOff.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 64,64 ), 0 )
		bSizer1.Add( self.m_bitmap_Error, 2, wx.ALL, 5 )

		self.m_button_cancel = wx.Button( self, wx.ID_ANY, u"エラーキャンセル", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_cancel.SetMinSize( wx.Size( 200,50 ) )

		bSizer1.Add( self.m_button_cancel, 0, wx.ALL, 5 )


		gbSizer.Add( bSizer1, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )


		self.SetSizer( gbSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button_capture.Bind( wx.EVT_BUTTON, self.onCaptureButton )
		self.m_button_up.Bind( wx.EVT_BUTTON, self.onUpButton )
		self.m_button_stop.Bind( wx.EVT_BUTTON, self.onStopButton )
		self.m_button_down.Bind( wx.EVT_BUTTON, self.onDownButton )
		self.m_button_cancel.Bind( wx.EVT_BUTTON, self.onCancelButton )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def onCaptureButton( self, event ):
		event.Skip()

	def onUpButton( self, event ):
		event.Skip()

	def onStopButton( self, event ):
		event.Skip()

	def onDownButton( self, event ):
		event.Skip()

	def onCancelButton( self, event ):
		event.Skip()


