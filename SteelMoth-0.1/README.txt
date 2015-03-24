#===============================================================================
# Acceptance Testing
#===============================================================================
#-------------------------------------------------------- COMPLETENESS YARDSTICK
# Able to layout interfaces discussed in: http://www.tkdocs.com/tutorial/index.html
# Also compare to: objectbrowser -- https://pypi.python.org/pypi/objbrowser
#
#
#===============================================================================
# Project: Steel Moth 
#===============================================================================
#
# Program:
# A simple program for quick-and-easy layout of GUIs and generating the 
# corresponding python code which a programmer can then edit to add actual 
# behaviour and program logic. 
#
# Audience:
# Non-programmers setting out to learn programming
#
# Purpose:
# To present a useful tool impressive to the beginning programming which the 
# beginning programming will later be able to make for himself.
#
# Scope:
# Python, Tk widgets available in python.
#
#
#------------------------------------------------------- USER DATA BRAINSTORMING
#
# Q: How is user widget hierarchy data going to be stored?
# Need:
#     - The index in WidgetTreeview
#     - The name in WidgetTreeview
#     - The widget object itself
#     - list of child data of the widget data (i.e. tree-like)
# So maybe:
#     - We need a list [] for the index number
#     - And a 3-tuple for the rest of it: (iid, widget object, children list)
#
# Q: Where should user widget data be stored?
# Candidates:
#     - New UserDataManager class:
#         - PRO: Obvious answer to this and all future questions
#         - PRO: Encapsulates user data in one place
#         - CON: Opaque grab-bag of 'stuff'
#     - New UserDataDictionary dictionary:
#         - PRO: No need for a class.
#         - CON: Will not be a suitable place for storing common data manipulation facilities.
#         - NB: Widget hierarchy will have to be done as a list in the dictionary since order is important.
#     - New UserGeometryManager or UserGridManager class:
#         - CON: Is a new class
#         - PRO: Is a new class dedicated to storing gridding data so other user data makes sense here.
#     - module global:
#         - PRO: A fairly logical place to look for data not directly available within a class
#         - CON: But isn't this untidy??
#     - New UserToplevelManager class:
#         - PRO: Captures the concept very well
#         - CON: Requires this AND the UserGridManager class. (i.e. 2 new classes)
#         - CON: Yeah, but where do I put the instances of this class?
#     - WidgetTreeviewManager:
#         - CON: Can't be easily accessed from WidgetConfigurationTreeviewManager
#
#
#-------------------------------------------------------- USER DATA ORGANISATION
# Efficiency requirements:
#     - iid -> children iids
#     - insert WIDGET under PARENT_IID at INDEX with IID i.e. insertion efficiency
#         IID -> WIDGET
#         IID -> loc: PIID,INDEX
#     - iid -> parent iid -- why?
#     - iid -> widget
#     - iid -> other data -- could be ALL data
#
#
#--------------------------------------------------------- GUI OBSERVER PATTERNS
# Currently:
#     UserDataManager
#         <- WidgetTreeviewManager
#         <- WidgetConfigurationTreeviewManager
#         
# Should be:
#     UserDataManager
#         <- WidgetTreeviewManager
#             <- WidgetConfigurationTreeviewManager
#                 <- WidgetConfigurationEntryManager
#
#
#---------------------------------------------------------- PMW AND TKINTERTABLE
# Instigating stackoverflow post: 
# http://stackoverflow.com/questions/18562123/python-ttk-treeview-make-item-row-editable
# PMW Homepage: http://pmw.sourceforge.net/
# Tkintertable Homepage: http://pythonhosted.org/tkintertable/
# also available: http://tkintertreectrl.sourceforge.net/
#
# SHORT ANSWER: No. Lets try to keep this demo simple. A student extension may 
# be the right place to include Pmw and Tkintertable.
