# ------------------------------------------------------
# Better Search & Rename Tool for Maya
# Inspired by mRebaseRenamer by mRebase on Gumroad. Recreated the same ideas with a few tweaks in Python so that I can use it. Cuz it's originally in PyMel, and my schooi can't install PyMel in their computers.
# Version: 4.0.0 (Soft Neon Theme)
# ------------------------------------------------------
# Purple Rename Button Colour could be better. It's a bit brighter than the rest at the moment. At least it looks like it.
# The border colours could also be made a bit brighter. Who knows.
# ------------------------------------------------------


import maya.cmds as cmds
import maya.OpenMayaUI as omui
import fnmatch
import re

try:
    from PySide6 import QtWidgets, QtCore, QtGui
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2 import QtWidgets, QtCore, QtGui
    from shiboken2 import wrapInstance

# ------------------------------------------------------
# STYLESHEET
# Palette:
#   Blue   #66b3ff  — primary accent, focus, radio/checkbox active
#   Purple #bf80ff  — rename section title + rename button
#   Pink   #ff99ff  — prefix/suffix section title + add buttons
#   Mint   #99ffcc  — search & replace section title + apply button
#   Remove buttons stay a muted red (neutral, not from palette)
# ------------------------------------------------------
STYLESHEET = """
/* === BASE === */
QWidget {
    background-color: #1e1e24;
    color: #d0d0d8;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 12px;
}

QDialog {
    background-color: #18181e;
    border: 1px solid #111116;
}

/* === SECTION FRAMES === */
QFrame#sectionFrame {
    background-color: #26262e;
    border: 1px solid #32323c;
    border-radius: 6px;
}

/* === GENERIC LABEL === */
QLabel {
    color: #e0e0ea;
    font-size: 11px;
    background: transparent;
}

/* === SECTION TITLE LABELS (colored per section via objectName) === */
QLabel#titleScope {
    color: #66b3ff;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1.5px;
    background: transparent;
}
QLabel#titleSelect {
    color: #66b3ff;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1.5px;
    background: transparent;
}
QLabel#titleRename {
    color: #bf80ff;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1.5px;
    background: transparent;
}
QLabel#titleAffix {
    color: #ff99ff;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1.5px;
    background: transparent;
}
QLabel#titleReplace {
    color: #99ffcc;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 1.5px;
    background: transparent;
}

/* === LINE EDITS === */
QLineEdit {
    background-color: #14141a; /*field BG*/
    border: 1px solid #36363f;
    border-radius: 4px;
    padding: 4px 8px;
    color: #e0e0ea; /*typed colour*/
    font-weight: bold;
    selection-background-color: #66b3ff; /*highlight when selecting text*/
    selection-color: #0a0a12; /* selected text colour*/
}
QLineEdit:focus {
    border: 1px solid #66b3ff;
    background-color: #1a1a22;
}
QLineEdit:hover {
    border: 1px solid #505060;
}

/* === BUTTONS - DEFAULT === */
QPushButton {
    background-color: #2e2e38;
    border: 1px solid #3e3e4a;
    border-radius: 4px;
    padding: 4px 10px;
    color: #b0b0c0;
    min-height: 22px;
}
QPushButton:hover {
    background-color: #38384a;
    border: 1px solid #58587a;
    color: #e0e0f0;
}
QPushButton:pressed {
    background-color: #1e1e28;
}

/* === SELECT BUTTON — Dim blue === */
QPushButton#selectButton {
    background-color: #222830;
    border: 1px solid #3a5068;
    border-radius: 4px;
    color: #6a96b8;
    font-weight: bold;
    min-height: 22px;
    padding: 4px 10px;
}
QPushButton#selectButton:hover {
    background-color: #2a3340;
    border: 1px solid #4e7095;
    color: #88b4d4;
}
QPushButton#selectButton:pressed {
    background-color: #181e26;
}

/* === RENAME BUTTON — Dim purple === */
QPushButton#renameButton {
    background-color: #26222e;
    border: 1px solid #4a3860;
    border-radius: 4px;
    color: #a885d6;
    font-weight: bold;
    min-height: 22px;
    padding: 4px 10px;
}
QPushButton#renameButton:hover {
    background-color: #302840;
    border: 1px solid #6a5080;
    color: #9a80c0;
}
QPushButton#renameButton:pressed {
    background-color: #1a1620;
}

/* === ADD BUTTONS — Dim pink === */
QPushButton#addButton {
    background-color: #2e222e;
    border: 1px solid #603060;
    border-radius: 4px;
    color: #9c61a1;
    font-weight: bold;
    min-height: 22px;
    padding: 4px 10px;
}
QPushButton#addButton:hover {
    background-color: #3c2a3c;
    border: 1px solid #804880;
    color: #b070b0;
}
QPushButton#addButton:pressed {
    background-color: #1e161e;
}

/* === APPLY BUTTON — Dim mint === */
QPushButton#applyButton {
    background-color: #1e2a24;
    border: 1px solid #305040;
    border-radius: 4px;
    color: #7baf8a;
    font-weight: bold;
    min-height: 22px;
    padding: 4px 10px;
}
QPushButton#applyButton:hover {
    background-color: #263830;
    border: 1px solid #487860;
    color: #70aa88;
}
QPushButton#applyButton:pressed {
    background-color: #141e18;
}

/* === REMOVE BUTTONS — Dim red === */
QPushButton#removeButton {
    background-color: #2a1e1e;
    border: 1px solid #4a2e2e;
    border-radius: 4px;
    color: #8d5a59;
    min-height: 22px;
    padding: 4px 10px;
}
QPushButton#removeButton:hover {
    background-color: #362626;
    border: 1px solid #623c3c;
    color: #9a6868;
}
QPushButton#removeButton:pressed {
    background-color: #1a1212;
}

/* === SWAP BUTTON === */
QPushButton#swapButton {
    background-color: #242430;
    border: 1px solid #3e3e50;
    border-radius: 4px;
    color: #606080;
    font-size: 14px;
    min-height: 22px;
    padding: 2px 6px;
}
QPushButton#swapButton:hover {
    background-color: #2e2e3e;
    color: #99ffcc;
    border-color: #99ffcc;
}

/* === RADIO BUTTONS === */
QRadioButton {
    color: #e0e0ea;
    spacing: 5px;
    background: transparent;
}
QRadioButton::indicator {
    width: 12px;
    height: 12px;
    border-radius: 6px;
    border: 1px solid #484860;
    background-color: #14141a;
}
QRadioButton::indicator:checked {
    background-color: #66b3ff;
    border: 1px solid #99ccff;
}
QRadioButton::indicator:hover {
    border: 1px solid #66b3ff;
}
QRadioButton:checked {
    color: #99ccff;
}

/* === CHECKBOXES === */
QCheckBox {
    color: #e0e0ea;
    spacing: 5px;
    background: transparent;
}
QCheckBox::indicator {
    width: 12px;
    height: 12px;
    border-radius: 2px;
    border: 1px solid #484860;
    background-color: #14141a;
}
QCheckBox::indicator:checked {
    background-color: #66b3ff;
    border: 1px solid #99ccff;
}
QCheckBox::indicator:hover {
    border: 1px solid #66b3ff;
}
QCheckBox:checked {
    color: #99ccff;
}

/* === SCROLL AREA === */
QScrollArea {
    border: none;
    background-color: #18181e;
}
QScrollBar:vertical {
    background: #18181e;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #38383f;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #66b3ff;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


# ------------------------------------------------------
# HELPERS
# ------------------------------------------------------
def num_to_alpha(num, is_lower=False):
    result = ""
    while num > 0:
        num -= 1
        result = chr((num % 26) + 65) + result
        num //= 26
    return result.lower() if is_lower else result

def alpha_to_num(alpha):
    num = 0
    for char in alpha.upper():
        if char.isalpha():
            num = num * 26 + (ord(char) - 64)
    if num <= 0:
        cmds.warning("Invalid start index '{}', defaulting to 1.".format(alpha))
        return 1
    return num

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


# ------------------------------------------------------
# SECTION FRAME HELPER
# Now accepts a title_object_name so each section
# title can be styled independently via QSS.
# ------------------------------------------------------
def make_section(title, title_object_name, parent_layout):
    frame = QtWidgets.QFrame()
    frame.setObjectName("sectionFrame")
    frame.setFrameShape(QtWidgets.QFrame.StyledPanel)

    outer = QtWidgets.QVBoxLayout(frame)
    outer.setContentsMargins(10, 8, 10, 10)
    outer.setSpacing(6)

    lbl = QtWidgets.QLabel(title.upper())
    lbl.setObjectName(title_object_name)
    outer.addWidget(lbl)

    inner = QtWidgets.QVBoxLayout()
    inner.setSpacing(6)
    outer.addLayout(inner)

    parent_layout.addWidget(frame)
    return inner


# ------------------------------------------------------
# MAIN TOOL LOGIC
# ------------------------------------------------------
def run_tool(action, ui):
    sel_txt    = ui.select_field.text()
    ren_txt    = ui.rename_field.text()
    ren_mode   = ui.mode_group.checkedId()
    use_uscore = ui.underscore_check.isChecked()
    pad_str    = ui.pad_field.text()
    start_str  = ui.start_field.text()
    pfx        = ui.prefix_field.text()
    sfx        = ui.suffix_field.text()
    search_txt  = ui.search_field.text()
    replace_txt = ui.replace_field.text()
    scope_idx  = ui.scope_group.checkedId()
    is_case    = ui.case_check.isChecked()

    s = cmds.optionVar
    s(intValue=('bst_scope',      scope_idx))
    s(intValue=('bst_case',       int(is_case)))
    s(intValue=('bst_ren_mode',   ren_mode))
    s(intValue=('bst_ren_uscore', int(use_uscore)))
    s(stringValue=('bst_select',      sel_txt))
    s(stringValue=('bst_rename',      ren_txt))
    s(stringValue=('bst_pad',         pad_str))
    s(stringValue=('bst_start',       start_str))
    s(stringValue=('bst_prefix',      pfx))
    s(stringValue=('bst_suffix',      sfx))
    s(stringValue=('bst_rep_search',  search_txt))
    s(stringValue=('bst_rep_replace', replace_txt))

    nodes_to_process = []
    if action == "rename":
        nodes_to_process = cmds.ls(selection=True, long=True)
        if not nodes_to_process:
            cmds.warning("Rename requires an active selection!")
            return
    else:
        if scope_idx == 1:
            selected = cmds.ls(selection=True, long=True)
            if not selected:
                cmds.warning("Please select an object for Hierarchy scope!")
                return
            children = cmds.listRelatives(selected, type="transform", ad=True, fullPath=True) or []
            nodes_to_process = selected + children
        elif scope_idx == 2:
            nodes_to_process = cmds.ls(selection=True, type="transform", long=True)
        elif scope_idx == 3:
            nodes_to_process = cmds.ls(type="transform", long=True)

    nodes_to_process.sort(key=len, reverse=True)
    if not nodes_to_process:
        return

    if action == "rename":
        if not ren_txt:
            cmds.warning("Please enter a base name to rename.")
            return
        try:
            padding = int(pad_str) if pad_str else 0
        except ValueError:
            padding = 0
        current_idx = 1
        if start_str:
            if ren_mode == 1:
                try:
                    current_idx = int(start_str)
                except ValueError:
                    current_idx = 1
            else:
                current_idx = alpha_to_num(start_str)

    final_selection = []
    for node in nodes_to_process:
        if not cmds.objExists(node):
            continue
        short_name = node.split("|")[-1]
        new_name = short_name

        if action == "rename":
            if ren_mode == 1:
                sfx_str = str(current_idx).zfill(max(1, padding))
            elif ren_mode == 2:
                alpha_str = num_to_alpha(current_idx, False)
                sfx_str = alpha_str if len(alpha_str) >= padding else alpha_str.rjust(padding, 'A')
            elif ren_mode == 3:
                alpha_str = num_to_alpha(current_idx, True)
                sfx_str = alpha_str if len(alpha_str) >= padding else alpha_str.rjust(padding, 'a')
            separator = "_" if use_uscore else ""
            new_name = "{}{}{}".format(ren_txt, separator, sfx_str)
            current_idx += 1

        elif action == "prefix" and pfx:
            new_name = pfx + new_name

        elif action == "remove_prefix" and pfx:
            if is_case:
                if new_name.startswith(pfx):
                    new_name = new_name[len(pfx):]
            else:
                if new_name.lower().startswith(pfx.lower()):
                    new_name = new_name[len(pfx):]

        elif action == "suffix" and sfx:
            new_name = new_name + sfx

        elif action == "remove_suffix" and sfx:
            if is_case:
                if new_name.endswith(sfx):
                    new_name = new_name[:-len(sfx)]
            else:
                if new_name.lower().endswith(sfx.lower()):
                    new_name = new_name[:-len(sfx)]

        elif action == "replace" and search_txt:
            if search_txt == "*":
                new_name = replace_txt
            elif search_txt == "$":
                new_name = new_name + replace_txt
            else:
                if is_case:
                    if search_txt in new_name:
                        new_name = new_name.replace(search_txt, replace_txt)
                else:
                    if search_txt.lower() in new_name.lower():
                        pattern = re.compile(re.escape(search_txt), re.IGNORECASE)
                        new_name = pattern.sub(replace_txt, new_name)

        current_node_path = node
        if new_name != short_name and action != "select":
            try:
                current_node_path = cmds.rename(node, new_name)
                current_node_path = cmds.ls(current_node_path, long=True)[0]
            except Exception as e:
                print("Skipped renaming {}: {}".format(short_name, e))

        if action == "select" and sel_txt:
            eval_name = current_node_path.split("|")[-1]
            match_pattern = "*" + sel_txt + "*" if ("*" not in sel_txt and "?" not in sel_txt) else sel_txt
            if is_case:
                is_match = fnmatch.fnmatchcase(eval_name, match_pattern)
            else:
                is_match = fnmatch.fnmatchcase(eval_name.lower(), match_pattern.lower())
            if is_match:
                final_selection.append(current_node_path)
        elif action != "select":
            final_selection.append(current_node_path)

    if final_selection:
        cmds.select(final_selection)
        print("Successfully processed {} objects.".format(len(final_selection)))
    else:
        cmds.select(clear=True)
        if action == "select":
            print("No objects matched the selection criteria.")


# ------------------------------------------------------
# UI CLASS
# ------------------------------------------------------
class BetterRenamerUI(QtWidgets.QDialog):

    WINDOW_TITLE = "Better Search & Rename"

    def __init__(self, parent=get_maya_main_window()):
        super(BetterRenamerUI, self).__init__(parent)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumWidth(460)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setStyleSheet(STYLESHEET)
        self._load_prefs()
        self._build_ui()
        self._connect_signals()

    def _load_prefs(self):
        def iv(key, default):
            return cmds.optionVar(q=key) if cmds.optionVar(exists=key) else default
        def sv(key, default):
            val = cmds.optionVar(q=key) if cmds.optionVar(exists=key) else default
            return val if val != "" else default

        self.p_scope  = iv('bst_scope',      1)
        self.p_case   = iv('bst_case',        1)
        self.p_rmode  = iv('bst_ren_mode',    1)
        self.p_uscore = iv('bst_ren_uscore',  1)
        self.p_sel    = sv('bst_select',      "")
        self.p_ren    = sv('bst_rename',      "")
        self.p_pad    = sv('bst_pad',         "2")
        self.p_start  = sv('bst_start',       "")
        self.p_pfx    = sv('bst_prefix',      "")
        self.p_sfx    = sv('bst_suffix',      "")
        self.p_rs     = sv('bst_rep_search',  "L_")
        self.p_rr     = sv('bst_rep_replace', "R_")

    def _build_ui(self):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        container = QtWidgets.QWidget()
        main = QtWidgets.QVBoxLayout(container)
        main.setContentsMargins(4, 4, 4, 4)
        main.setSpacing(8)
        scroll.setWidget(container)
        root.addWidget(scroll)

        # ── SCOPE ──────────────────────────────────────
        scope_inner = make_section("Scope", "titleScope", main)
        scope_row = QtWidgets.QHBoxLayout()
        scope_row.setSpacing(12)
        self.scope_group = QtWidgets.QButtonGroup(self)
        for i, label in enumerate(["Hierarchy", "Selected", "All"], start=1):
            rb = QtWidgets.QRadioButton(label)
            if i == self.p_scope:
                rb.setChecked(True)
            self.scope_group.addButton(rb, i)
            scope_row.addWidget(rb)
        scope_row.addStretch()
        self.case_check = QtWidgets.QCheckBox("Case Sensitive")
        self.case_check.setChecked(bool(self.p_case))
        scope_row.addWidget(self.case_check)
        scope_inner.addLayout(scope_row)

        # ── SELECT ─────────────────────────────────────
        sel_inner = make_section("Select", "titleSelect", main)
        sel_row = QtWidgets.QHBoxLayout()
        sel_row.setSpacing(6)
        self.select_field = QtWidgets.QLineEdit(self.p_sel)
        self.select_field.setPlaceholderText("ex. *Jnt, Spine_*")
        self.select_btn = QtWidgets.QPushButton("Select")
        self.select_btn.setObjectName("selectButton")
        self.select_btn.setFixedWidth(72)
        sel_row.addWidget(self.select_field)
        sel_row.addWidget(self.select_btn)
        sel_inner.addLayout(sel_row)

        # ── RENAME ─────────────────────────────────────
        ren_inner = make_section("Rename  \u2014  Selection Only", "titleRename", main)
        ren_row = QtWidgets.QHBoxLayout()
        ren_row.setSpacing(6)
        self.rename_field = QtWidgets.QLineEdit(self.p_ren)
        self.rename_field.setPlaceholderText("Base name  (e.g. Spine_Jnt)")
        self.rename_btn = QtWidgets.QPushButton("Rename")
        self.rename_btn.setObjectName("renameButton")
        self.rename_btn.setFixedWidth(72)
        ren_row.addWidget(self.rename_field)
        ren_row.addWidget(self.rename_btn)
        ren_inner.addLayout(ren_row)

        opts_row = QtWidgets.QHBoxLayout()
        opts_row.setSpacing(14)
        mode_lbl = QtWidgets.QLabel("Mode:")
        opts_row.addWidget(mode_lbl)
        self.mode_group = QtWidgets.QButtonGroup(self)
        for i, label in enumerate(["123", "ABC", "abc"], start=1):
            rb = QtWidgets.QRadioButton(label)
            if i == self.p_rmode:
                rb.setChecked(True)
            self.mode_group.addButton(rb, i)
            opts_row.addWidget(rb)
        opts_row.addSpacing(6)
        self.underscore_check = QtWidgets.QCheckBox("Underscore")
        self.underscore_check.setChecked(bool(self.p_uscore))
        opts_row.addWidget(self.underscore_check)
        opts_row.addStretch()
        pad_lbl = QtWidgets.QLabel("Pad:")
        opts_row.addWidget(pad_lbl)
        self.pad_field = QtWidgets.QLineEdit(self.p_pad)
        self.pad_field.setFixedWidth(38)
        opts_row.addWidget(self.pad_field)
        start_lbl = QtWidgets.QLabel("Start:")
        opts_row.addWidget(start_lbl)
        self.start_field = QtWidgets.QLineEdit(self.p_start)
        self.start_field.setFixedWidth(52)
        self.start_field.setPlaceholderText("1")
        opts_row.addWidget(self.start_field)
        ren_inner.addLayout(opts_row)

        # ── PREFIX / SUFFIX ────────────────────────────
        affix_inner = make_section("Prefix  /  Suffix", "titleAffix", main)

        pfx_row = QtWidgets.QHBoxLayout()
        pfx_row.setSpacing(6)
        pfx_lbl = QtWidgets.QLabel("Prefix")
        pfx_lbl.setFixedWidth(38)
        self.prefix_field = QtWidgets.QLineEdit(self.p_pfx)
        self.prefix_field.setPlaceholderText("ex. L_,  R_")
        self.pfx_add_btn = QtWidgets.QPushButton("Add")
        self.pfx_add_btn.setObjectName("addButton")
        self.pfx_add_btn.setFixedWidth(52)
        self.pfx_rem_btn = QtWidgets.QPushButton("Remove")
        self.pfx_rem_btn.setObjectName("removeButton")
        self.pfx_rem_btn.setFixedWidth(66)
        pfx_row.addWidget(pfx_lbl)
        pfx_row.addWidget(self.prefix_field)
        pfx_row.addWidget(self.pfx_add_btn)
        pfx_row.addWidget(self.pfx_rem_btn)
        affix_inner.addLayout(pfx_row)

        sfx_row = QtWidgets.QHBoxLayout()
        sfx_row.setSpacing(6)
        sfx_lbl = QtWidgets.QLabel("Suffix")
        sfx_lbl.setFixedWidth(38)
        self.suffix_field = QtWidgets.QLineEdit(self.p_sfx)
        self.suffix_field.setPlaceholderText("ex. _Geo,  _Grp,  _Jnt")
        self.sfx_add_btn = QtWidgets.QPushButton("Add")
        self.sfx_add_btn.setObjectName("addButton")
        self.sfx_add_btn.setFixedWidth(52)
        self.sfx_rem_btn = QtWidgets.QPushButton("Remove")
        self.sfx_rem_btn.setObjectName("removeButton")
        self.sfx_rem_btn.setFixedWidth(66)
        sfx_row.addWidget(sfx_lbl)
        sfx_row.addWidget(self.suffix_field)
        sfx_row.addWidget(self.sfx_add_btn)
        sfx_row.addWidget(self.sfx_rem_btn)
        affix_inner.addLayout(sfx_row)

        # ── SEARCH & REPLACE ───────────────────────────
        rep_inner = make_section("Search  &  Replace", "titleReplace", main)
        rep_row = QtWidgets.QHBoxLayout()
        rep_row.setSpacing(6)
        self.search_field = QtWidgets.QLineEdit(self.p_rs)
        self.search_field.setPlaceholderText("Search  (* = replace all,  $ = append)")
        self.swap_btn = QtWidgets.QPushButton("\u21c4")
        self.swap_btn.setObjectName("swapButton")
        self.swap_btn.setFixedWidth(30)
        self.replace_field = QtWidgets.QLineEdit(self.p_rr)
        self.replace_field.setPlaceholderText("Replace with")
        self.replace_btn = QtWidgets.QPushButton("Apply")
        self.replace_btn.setObjectName("applyButton")
        self.replace_btn.setFixedWidth(52)
        rep_row.addWidget(self.search_field)
        rep_row.addWidget(self.swap_btn)
        rep_row.addWidget(self.replace_field)
        rep_row.addWidget(self.replace_btn)
        rep_inner.addLayout(rep_row)

        main.addStretch()

    def _connect_signals(self):
        self.select_btn.clicked.connect(lambda: run_tool("select",         self))
        self.rename_btn.clicked.connect(lambda: run_tool("rename",         self))
        self.pfx_add_btn.clicked.connect(lambda: run_tool("prefix",        self))
        self.pfx_rem_btn.clicked.connect(lambda: run_tool("remove_prefix", self))
        self.sfx_add_btn.clicked.connect(lambda: run_tool("suffix",        self))
        self.sfx_rem_btn.clicked.connect(lambda: run_tool("remove_suffix", self))
        self.replace_btn.clicked.connect(lambda: run_tool("replace",       self))
        self.swap_btn.clicked.connect(self._swap_search_replace)

    def _swap_search_replace(self):
        a = self.search_field.text()
        b = self.replace_field.text()
        self.search_field.setText(b)
        self.replace_field.setText(a)


# ------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------
def show_better_search_ui():
    global _renamer_window
    try:
        _renamer_window.close()
        _renamer_window.deleteLater()
    except Exception:
        pass
    _renamer_window = BetterRenamerUI()
    _renamer_window.show()

show_better_search_ui()
