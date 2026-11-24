# ======================================================================
# FILE: misora.py — PART 03 / 10
# ORIGINAL LINE RANGE : L2881 .. L3686 (total 806 lines of 12835)
# SOURCE SHA-256      : d23baae2be82fe93a18da7d3769af30d19ebe02a8b5f6a3645d56a6f53c0710e
# NOTE FOR AI REVIEWER: Cite ORIGINAL line numbers (L2881..L3686) and symbol names.
# SYMBOLS IN THIS PART (with exact original line numbers):
#   L02881:   MisoraApp._apply_styles (def)
#   L03143:   MisoraApp._build_menu (def)
#   L03522:   MisoraApp._build_search_bar (def)
# ======================================================================

    def _apply_styles(self) -> None:
        """Apply WCAG contrast-safe theme colors & UI font sizing to all ttk widgets."""
        t = self.theme
        u_sz = int(self.prefs["ui_font_size"])
        dark_panel = self._is_dark_color(t["bg_panel"])

        # Compute WCAG optimal foregrounds for every surface & interactive state
        fg_on_dark = best_contrast_fg(t["bg_dark"], t["fg_text"], "#ffffff")
        fg_on_panel = best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff")
        fg_on_editor = best_contrast_fg(t["bg_editor"], t["fg_text"], "#ffffff")

        accent_bg = t["misora_pink"]
        accent_hover = t["misora_pink_hover"]
        accent_press = t["misora_pink_active"]
        fg_accent = best_contrast_fg(accent_bg)
        fg_accent_hover = best_contrast_fg(accent_hover)
        fg_accent_press = best_contrast_fg(accent_press)

        btn_bg = self._shift_hex(t["bg_panel"], 10 if dark_panel else -8)
        btn_hover = self._shift_hex(t["bg_panel"], 22 if dark_panel else -16)
        btn_press = self._shift_hex(t["bg_panel"], -6 if dark_panel else -24)
        fg_btn = best_contrast_fg(btn_bg, t["fg_text"], "#ffffff")
        fg_btn_hover = best_contrast_fg(btn_hover, t["fg_text"], "#ffffff")
        fg_btn_press = best_contrast_fg(btn_press, t["fg_text"], "#ffffff")

        small_bg = t["bg_editor"]
        fg_small = best_contrast_fg(small_bg, t["fg_text"], "#ffffff")

        hl_bg = t["highlight_bg"]
        fg_hl = best_contrast_fg(hl_bg, t["misora_pink"], "#ffffff")

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(".", background=t["bg_dark"], foreground=fg_on_dark, borderwidth=0)
        style.configure("TFrame", background=t["bg_dark"])
        style.configure("Panel.TFrame", background=t["bg_panel"])

        style.configure("TLabel", background=t["bg_dark"], foreground=fg_on_dark, font=("Segoe UI", u_sz))
        style.configure("Panel.TLabel", background=t["bg_panel"], foreground=fg_on_panel, font=("Segoe UI", u_sz))
        style.configure("Header.TLabel", font=("Segoe UI", u_sz + 1, "bold"), foreground=t["misora_pink"])
        style.configure("Muted.TLabel", foreground=t["fg_muted"], font=("Segoe UI", max(8, u_sz - 1)))

        style.configure("TCheckbutton", background=t["bg_dark"], foreground=fg_on_dark, font=("Segoe UI", u_sz))
        style.configure("Panel.TCheckbutton", background=t["bg_panel"], foreground=fg_on_panel, font=("Segoe UI", u_sz))
        style.map("Panel.TCheckbutton",
            background=[("active", t["bg_panel"]), ("!active", t["bg_panel"])],
            foreground=[("active", t["misora_pink"]), ("!active", fg_on_panel)],
        )
        style.configure("Accent.TCheckbutton", background=t["bg_panel"], foreground=t["misora_pink"], font=("Segoe UI", max(8, u_sz - 1), "bold"))
        style.map("Accent.TCheckbutton",
            background=[("active", t["bg_panel"]), ("!active", t["bg_panel"])],
            foreground=[("active", t["misora_pink_hover"]), ("!active", t["misora_pink"])],
        )
        style.configure("TRadiobutton", background=t["bg_dark"], foreground=fg_on_dark, font=("Segoe UI", u_sz))
        style.configure("Panel.TRadiobutton", background=t["bg_panel"], foreground=fg_on_panel, font=("Segoe UI", u_sz))
        style.map("Panel.TRadiobutton",
            background=[("active", t["bg_panel"]), ("!active", t["bg_panel"])],
            foreground=[("active", fg_on_panel), ("!active", fg_on_panel)],
        )

        # Primary Accent Action Button
        style.configure(
            "Pink.TButton",
            background=accent_bg,
            foreground=fg_accent,
            bordercolor=accent_press,
            darkcolor=accent_press,
            lightcolor=accent_hover,
            borderwidth=1,
            relief="raised",
            font=("Segoe UI", u_sz, "bold"),
            padding=(10, 4),
        )
        style.map(
            "Pink.TButton",
            background=[
                ("disabled", btn_bg),
                ("pressed", accent_press),
                ("active", accent_hover),
            ],
            foreground=[
                ("disabled", t["fg_muted"]),
                ("pressed", fg_accent_press),
                ("active", fg_accent_hover),
            ],
        )

        # Distinct Box Navigation Buttons (< Prev / Next >) (#4)
        style.configure(
            "Nav.TButton",
            background=btn_bg,
            foreground=fg_btn,
            bordercolor=t["misora_pink"],
            darkcolor=t["border"],
            lightcolor=t["misora_pink"],
            borderwidth=1,
            relief="raised",
            font=("Segoe UI", u_sz, "bold"),
            padding=(9, 3),
        )
        style.map(
            "Nav.TButton",
            background=[
                ("disabled", t["bg_editor"]),
                ("pressed", accent_press),
                ("active", accent_bg),
            ],
            foreground=[
                ("disabled", t["fg_muted"]),
                ("pressed", fg_accent_press),
                ("active", fg_accent),
            ],
        )

        # Standard Button
        style.configure(
            "TButton",
            background=btn_bg,
            foreground=fg_btn,
            bordercolor=t["border"],
            darkcolor=t["border"],
            lightcolor=btn_hover,
            borderwidth=1,
            relief="raised",
            font=("Segoe UI", u_sz),
            padding=(7, 3),
        )
        style.map(
            "TButton",
            background=[
                ("disabled", t["bg_editor"]),
                ("pressed", btn_press),
                ("active", btn_hover),
            ],
            foreground=[
                ("disabled", t["fg_muted"]),
                ("pressed", fg_btn_press),
                ("active", fg_btn_hover),
            ],
        )

        # Compact Utility Button
        style.configure(
            "Small.TButton",
            background=small_bg,
            foreground=fg_small,
            bordercolor=t["border"],
            borderwidth=1,
            relief="raised",
            font=("Segoe UI", max(8, u_sz - 1)),
            padding=(6, 1),
        )
        style.map(
            "Small.TButton",
            background=[("active", btn_hover), ("pressed", btn_press)],
            foreground=[("active", fg_btn_hover), ("pressed", fg_btn_press)],
        )

        # NGUI Ribbon — Prominent Action Buttons (Color, Grad, Ruby) (#7)
        style.configure(
            "RibbonPrimary.TButton",
            background=accent_bg,
            foreground=fg_accent,
            bordercolor=accent_press,
            borderwidth=1,
            relief="raised",
            font=("Segoe UI", max(8, u_sz - 1), "bold"),
            padding=(3, 1),
        )
        style.map(
            "RibbonPrimary.TButton",
            background=[("active", accent_hover), ("pressed", accent_press)],
            foreground=[("active", fg_accent_hover), ("pressed", fg_accent_press)],
        )

        # NGUI Ribbon — Standard Secondary Button ([-], {player}) (#7)
        style.configure(
            "Ribbon.TButton",
            background=btn_bg,
            foreground=fg_btn,
            bordercolor=t["border"],
            borderwidth=1,
            relief="raised",
            font=("Segoe UI", max(8, u_sz - 1), "bold"),
            padding=(2, 1),
        )
        style.map(
            "Ribbon.TButton",
            background=[("active", hl_bg), ("pressed", btn_press)],
            foreground=[("active", fg_hl), ("pressed", fg_btn_press)],
        )

        # NGUI Ribbon — Tiny Mini-Buttons (B, I, U, S, Sub, Sup, Undo, Redo) (#7)
        style.configure(
            "RibbonMini.TButton",
            background=btn_bg,
            foreground=fg_btn,
            bordercolor=t["border"],
            borderwidth=1,
            relief="raised",
            font=("Segoe UI", max(7, u_sz - 2), "bold"),
            padding=(1, 0),
        )
        style.map(
            "RibbonMini.TButton",
            background=[("active", hl_bg), ("pressed", btn_press)],
            foreground=[("active", fg_hl), ("pressed", fg_btn_press)],
        )

        style.configure(
            "TCombobox",
            fieldbackground=t["bg_editor"],
            background=btn_bg,
            foreground=fg_on_editor,
            arrowcolor=t["misora_pink"],
        )

        # Treeview & Treeview.Heading Styling (BUG-31 / DEP-1 FIRST)
        tree_bg = t["bg_editor"]
        tree_fg = best_contrast_fg(tree_bg, t["fg_text"], "#ffffff")
        sel_bg = t["misora_pink"]
        sel_fg = best_contrast_fg(sel_bg)
        heading_bg = btn_bg
        heading_fg = best_contrast_fg(heading_bg, t["fg_text"], "#ffffff")
        heading_hover = btn_hover
        heading_fg_hover = best_contrast_fg(heading_hover, t["fg_text"], "#ffffff")

        style.configure(
            "Treeview",
            background=tree_bg,
            fieldbackground=tree_bg,
            foreground=tree_fg,
            font=("Segoe UI", u_sz),
            rowheight=max(20, u_sz * 2),
        )
        style.map(
            "Treeview",
            background=[("selected", sel_bg)],
            foreground=[("selected", sel_fg)],
        )

        style.configure(
            "Treeview.Heading",
            background=heading_bg,
            foreground=heading_fg,
            font=("Segoe UI", u_sz, "bold"),
            relief="raised",
            borderwidth=1,
        )
        style.map(
            "Treeview.Heading",
            background=[("active", heading_hover)],
            foreground=[("active", heading_fg_hover)],
        )

    # -------------------------------------------------------------------------
    # Menu Bar (Includes NGUI Glossary Top-Level Menu #6 & Debug Menu #14)
    # -------------------------------------------------------------------------
    def _build_menu(self) -> None:
        t = self.theme
        panel_fg = best_contrast_fg(t["bg_panel"], t["fg_text"], "#ffffff")
        accent_fg = best_contrast_fg(t["misora_pink"])

        self.var_continuous_view = tk.BooleanVar(master=self, value=False)
        self.var_preview_compiled = tk.BooleanVar(master=self, value=False)
        self._all_menus: List[tk.Menu] = []

        menubar = tk.Menu(
            self,
            bg=t["bg_panel"],
            fg=panel_fg,
            activebackground=t["misora_pink"],
            activeforeground=accent_fg,
        )
        self._all_menus.append(menubar)

        self.file_menu = file_menu = tk.Menu(menubar, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)
        file_menu.add_command(label="Open File...", command=self.on_open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Force Open Any File...", command=self.on_force_open_file)
        file_menu.add_command(label="Open Folder...", command=self.on_open_folder, accelerator="Ctrl+Shift+O")

        self.recent_menu = tk.Menu(file_menu, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg, postcommand=self._sync_recent_files_menu)
        file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        self._all_menus.append(self.recent_menu)

        file_menu.add_separator()
        file_menu.add_command(label="Save & Patch Bundle", command=self.on_save, accelerator="Ctrl+S")
        file_menu.add_command(label="Reload Current File", command=self.on_reload, accelerator="F5")
        file_menu.add_separator()
        file_menu.add_command(label="Import Script (CSIF / Text)...", command=self.on_import_script, accelerator="Ctrl+Shift+I")
        file_menu.add_command(label="Export Script (CSIF)...", command=self.on_export_script, accelerator="Ctrl+Shift+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_app_exit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=file_menu)
        self._all_menus.append(file_menu)

        self.edit_menu = tk.Menu(menubar, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg, postcommand=self._sync_edit_menu_states)
        self.edit_menu.add_command(label="Undo", command=self.on_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.on_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Previous Box", command=self.on_prev_box, accelerator="Alt+Left")
        self.edit_menu.add_command(label="Next Box", command=self.on_next_box, accelerator="Alt+Right")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Bold ([b]...[/b])", command=lambda: self.apply_ngui_wrapper("[b]", "[/b]"), accelerator="Ctrl+B")
        self.edit_menu.add_command(label="Italic ([i]...[/i])", command=lambda: self.apply_ngui_wrapper("[i]", "[/i]"), accelerator="Ctrl+I")
        self.edit_menu.add_command(label="Underline ([u]...[/u])", command=lambda: self.apply_ngui_wrapper("[u]", "[/u]"), accelerator="Ctrl+U")
        self.edit_menu.add_command(label="Wrap Selection with Ruby ([rub:...]...[/rub])", command=self.on_insert_ruby, accelerator="Ctrl+R")
        self.edit_menu.add_command(label="NGUI Color & Gradient Picker...", command=self.on_open_color_picker)
        self.edit_menu.add_command(label="Insert {playername}", command=self.on_insert_playername, accelerator="Ctrl+P")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Lock / Unlock Active Box",
            command=self.on_toggle_lock_current_box,
            accelerator="Ctrl+L",
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Copy Script Across Boxes (Triple Enter)...",
            command=self.on_copy_script_triple_enter,
            accelerator="Ctrl+Shift+C",
        )
        self.edit_menu.add_command(
            label="Paste Script Across Boxes...",
            command=self.on_paste_cross_box,
            accelerator="Ctrl+Shift+V",
        )
        menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self._all_menus.append(self.edit_menu)

        view_menu = tk.Menu(menubar, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)
        view_menu.add_checkbutton(
            label="Continuous Dialog View",
            variable=self.var_continuous_view,
            command=self._on_toggle_continuous_view,
            selectcolor=t["misora_pink"]
        )
        view_menu.add_checkbutton(
            label="Preview Compiled NGUI Attributes",
            variable=self.var_preview_compiled,
            command=self._on_toggle_preview_compiled,
            selectcolor=t["misora_pink"]
        )
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Customization Panel", command=lambda: self._toggle_side_drawer("customize"), accelerator="Ctrl+,")
        view_menu.add_command(label="Toggle NGUI Glossary Panel", command=lambda: self._toggle_side_drawer("glossary"), accelerator="F1")
        view_menu.add_separator()
        self.var_show_line_numbers = tk.BooleanVar(master=self, value=self.show_line_numbers)
        view_menu.add_checkbutton(
            label="Show Line Numbers (Vertical)",
            variable=self.var_show_line_numbers,
            command=self._on_toggle_line_numbers,
            selectcolor=t["misora_pink"]
        )
        self.var_show_column_ruler = tk.BooleanVar(master=self, value=self.show_column_ruler)
        view_menu.add_checkbutton(
            label="Show Column Ruler (Horizontal)",
            variable=self.var_show_column_ruler,
            command=self._on_toggle_column_ruler,
            selectcolor=t["misora_pink"]
        )
        menubar.add_cascade(label="View", menu=view_menu)
        self._all_menus.append(view_menu)

        search_menu = tk.Menu(menubar, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)
        search_menu.add_command(label="Find...", command=self.on_show_find, accelerator="Ctrl+F")
        search_menu.add_command(label="Find in Files...", command=self.on_show_find_in_files, accelerator="Ctrl+Shift+F")
        search_menu.add_command(label="Replace...", command=self.on_show_replace, accelerator="Ctrl+H")
        search_menu.add_separator()
        search_menu.add_command(label="Clear Search Results", command=self.on_clear_search)
        menubar.add_cascade(label="Search", menu=search_menu)
        self._all_menus.append(search_menu)

        cust_menu = tk.Menu(menubar, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)
        cust_menu.add_command(label="Display & Theme Settings...", command=lambda: self._toggle_side_drawer("customize"), accelerator="Ctrl+,")
        cust_menu.add_command(label="AI / LLM Translation Prompt Settings...", command=self.on_open_ai_prompt_settings)
        cust_menu.add_separator()
        cust_menu.add_command(label="Increase Dialogue Font Size", command=lambda: self._adjust_dialogue_font_size(1))
        cust_menu.add_command(label="Decrease Dialogue Font Size", command=lambda: self._adjust_dialogue_font_size(-1))
        cust_menu.add_separator()

        preset_sub = tk.Menu(cust_menu, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)
        for preset_name in THEME_PRESETS:
            preset_sub.add_command(
                label=preset_name,
                command=lambda pn=preset_name: self._apply_theme_preset(pn),
            )
        cust_menu.add_cascade(label="Theme Presets", menu=preset_sub)
        self._all_menus.append(preset_sub)

        cust_menu.add_separator()
        cust_menu.add_command(label="Reset Display & Colors to Default", command=self._reset_customization_defaults)
        menubar.add_cascade(label="Customize", menu=cust_menu)
        self._all_menus.append(cust_menu)

        # NGUI GLOSSARY TOP-LEVEL MENU (#6)
        glossary_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=t["bg_panel"],
            fg=panel_fg,
            activebackground=t["misora_pink"],
            activeforeground=accent_fg,
        )
        glossary_menu.add_command(
            label="Open NGUI & Ruby Glossary Drawer",
            command=lambda: self._toggle_side_drawer("glossary"),
            accelerator="F1",
        )
        glossary_menu.add_separator()
        glossary_menu.add_command(
            label="Wrap with Ruby ([rub:...]...[/rub])",
            command=self.on_insert_ruby,
            accelerator="Ctrl+R",
        )
        glossary_menu.add_command(
            label="Color & Gradient Picker...",
            command=self.on_open_color_picker,
        )
        glossary_menu.add_command(
            label="Insert {playername}",
            command=self.on_insert_playername,
            accelerator="Ctrl+P",
        )
        glossary_menu.add_command(
            label="Reset Color Tag ([-])",
            command=lambda: self.apply_ngui_wrapper("[-]", ""),
        )
        menubar.add_cascade(label="NGUI Glossary", menu=glossary_menu)
        self._all_menus.append(glossary_menu)

        # FOLDERS & FILES MENU (#4B)
        folders_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=t["bg_panel"],
            fg=panel_fg,
            activebackground=t["misora_pink"],
            activeforeground=accent_fg,
        )
        folders_menu.add_command(
            label="Configure Paths & Backups...",
            command=self.on_open_paths_dialog,
        )
        folders_menu.add_separator()
        folders_menu.add_command(
            label="Open Backups Folder",
            command=self.on_open_backups_folder,
        )
        folders_menu.add_command(
            label="Open Project / Mod Root Folder",
            command=self.on_open_project_folder,
        )
        folders_menu.add_command(
            label="Open Text Translation Folder (Text / XUAT)",
            command=self.on_open_xuat_text_folder,
        )
        folders_menu.add_command(
            label="Open Redirected Resources Folder",
            command=self.on_open_redirected_resources_folder,
        )
        folders_menu.add_command(
            label="Open Selected Search Folder",
            command=self.on_open_selected_search_folder,
        )
        folders_menu.add_command(
            label="Open Misora Program Folder",
            command=self.on_open_program_folder,
        )
        folders_menu.add_separator()
        folders_menu.add_command(
            label="Register .unity3d Association (Current User)...",
            command=self.on_register_unity3d_association,
        )
        menubar.add_cascade(label="Folders & Files", menu=folders_menu)
        self._all_menus.append(folders_menu)

        # TRANSLATOR MENU
        translator_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=t["bg_panel"],
            fg=panel_fg,
            activebackground=t["misora_pink"],
            activeforeground=accent_fg,
        )
        translator_menu.add_command(
            label="Translator Assistant...",
            command=self.on_open_translator_assistant,
            accelerator="Ctrl+T",
        )
        translator_menu.add_command(
            label="Translate Current Box",
            command=self.on_translate_current_box,
            accelerator="F8",
        )
        translator_menu.add_command(
            label="Batch Translate Story...",
            command=self.on_batch_translate,
        )
        translator_menu.add_separator()
        translator_menu.add_command(
            label="Configure MTL Sources & Keys...",
            command=self.on_open_mtl_settings,
        )
        translator_menu.add_command(
            label="Configure AI / LLM Prompt Header...",
            command=self.on_open_ai_prompt_settings,
        )
        translator_menu.add_separator()
        translator_menu.add_command(
            label="Copy AI Translation Prompt",
            command=self.on_copy_ai_prompt,
            accelerator="Ctrl+Shift+T",
        )
        translator_menu.add_command(
            label="Apply Translation from Clipboard...",
            command=self.on_apply_translation_clipboard,
        )
        translator_menu.add_separator()
        translator_menu.add_command(
            label="Clear Dialogue (Keep Skeleton Only)...",
            command=self.on_clear_dialogue_skeleton,
        )
        menubar.add_cascade(label="Translator", menu=translator_menu)
        self._all_menus.append(translator_menu)

        # DATAMINE MENU (#4C)
        datamine_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=t["bg_panel"],
            fg=panel_fg,
            activebackground=t["misora_pink"],
            activeforeground=accent_fg,
        )
        datamine_menu.add_command(
            label="Launch Datamine Tool",
            command=self.on_launch_datamine,
            accelerator="F9",
        )
        datamine_menu.add_separator()
        datamine_menu.add_command(
            label="Select Datamine Executable / Script...",
            command=self.on_select_datamine_exe,
        )
        datamine_menu.add_command(
            label="Open Datamine Program Folder",
            command=self.on_open_datamine_folder,
        )
        menubar.add_cascade(label="Datamine", menu=datamine_menu)
        self._all_menus.append(datamine_menu)

        # DEBUG MENU (#14 & #4D)
        self.debug_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg=t["bg_panel"],
            fg=panel_fg,
            activebackground=t["misora_pink"],
            activeforeground=accent_fg,
            postcommand=self._sync_debug_menu_states,
        )

        cat_sub = tk.Menu(self.debug_menu, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)
        for cat in LOG_CATEGORIES:
            if cat == ALWAYS_ON_CATEGORY:
                cat_sub.add_checkbutton(
                    label=f"{cat} (Always On)",
                    variable=self.var_log_categories[cat],
                    state="disabled",
                    selectcolor=t["misora_pink"],
                )
            else:
                cat_sub.add_checkbutton(
                    label=cat,
                    variable=self.var_log_categories[cat],
                    command=self._on_debug_settings_changed,
                    selectcolor=t["misora_pink"],
                )
        self.debug_menu.add_cascade(label="Log Categories", menu=cat_sub)
        self._all_menus.append(cat_sub)

        lvl_sub = tk.Menu(self.debug_menu, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)
        for lvl_name in LOG_LEVELS:
            lvl_sub.add_radiobutton(
                label=lvl_name,
                variable=self.var_log_level,
                value=lvl_name,
                command=self._on_debug_settings_changed,
                selectcolor=t["misora_pink"],
            )
        self.debug_menu.add_cascade(label="Log Level", menu=lvl_sub)
        self._all_menus.append(lvl_sub)

        # External Editor submenu (#4D)
        self._ext_editor_menu = tk.Menu(
            self.debug_menu,
            tearoff=0,
            bg=t["bg_panel"],
            fg=panel_fg,
            activebackground=t["misora_pink"],
            activeforeground=accent_fg,
            postcommand=self._sync_external_editor_menu,
        )
        self._sync_external_editor_menu()
        self.debug_menu.add_cascade(label="External Editor", menu=self._ext_editor_menu)
        self._all_menus.append(self._ext_editor_menu)

        self.debug_menu.add_separator()
        self.debug_menu.add_checkbutton(
            label="Log to File",
            variable=self.var_log_to_file,
            command=self._on_debug_settings_changed,
            selectcolor=t["misora_pink"],
        )
        self._idx_open_log = self.debug_menu.index("end") + 1
        self.debug_menu.add_command(label="Open Log File", command=self._on_open_debug_log_file)
        self._idx_clear_log = self.debug_menu.index("end") + 1
        self.debug_menu.add_command(label="Clear Log File", command=self._on_clear_debug_log_file)
        self.debug_menu.add_separator()
        self.debug_menu.add_command(label="Drag & Drop Safety Settings...", command=self._on_dnd_settings_dialog)

        menubar.add_cascade(label="Debug", menu=self.debug_menu)
        self._all_menus.append(self.debug_menu)

        help_menu = tk.Menu(menubar, tearoff=0, bg=t["bg_panel"], fg=panel_fg, activebackground=t["misora_pink"], activeforeground=accent_fg)
        help_menu.add_command(label="NGUI & Ruby Glossary", command=lambda: self._open_side_drawer("glossary"), accelerator="F1")
        help_menu.add_separator()
        help_menu.add_command(label="About Misora", command=self.on_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self._all_menus.append(help_menu)

        self.config(menu=menubar)

    # -------------------------------------------------------------------------
    # Search & Replace Bar (Collapsible Notepad++ Style)
    # -------------------------------------------------------------------------
    def _build_search_bar(self) -> None:
        t = self.theme
        self.search_frame = self._tag_role(
            tk.Frame(self, bg=t["bg_panel"], bd=1, relief="solid", highlightbackground=t["border"], highlightthickness=1),
            "panel_box"
        )
        self.search_frame.pack(fill="x", padx=8, pady=(6, 4))
        # Start collapsed — Ctrl+F will show it; build it packed then immediately hide
        self.search_frame.pack_forget()
        self._search_bar_visible = False

        row1 = self._tag_role(tk.Frame(self.search_frame, bg=t["bg_panel"]), "panel")
        row1.pack(fill="x", padx=8, pady=4)

        self._tag_role(
            tk.Label(row1, text="Find:", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["misora_pink"], width=7, anchor="w"),
            "label_accent"
        ).pack(side="left", padx=(0, 6))

        self.search_var = tk.StringVar(master=self)
        self.search_entry = self._tag_role(
            tk.Entry(
                row1,
                textvariable=self.search_var,
                font=("Consolas", 10),
                bg=t["bg_editor"],
                fg=t["fg_text"],
                insertbackground=t["misora_pink"],
                bd=1,
                relief="solid",
                highlightthickness=1,
                highlightcolor=t["misora_pink"]
            ),
            "entry_editor"
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.search_entry.bind("<Return>", lambda e: self.on_start_search())
        self.search_entry.bind("<Escape>", lambda e: self._hide_search_bar())

        self.ico_find = self.get_icon("search", (14, 14))
        self.ico_cancel = self.get_icon("cancel", (14, 14))
        self.btn_find = ttk.Button(row1, text=" Find in Files", image=self.ico_find, compound="left", style="Pink.TButton", command=self.on_start_search, width=14)
        self.btn_find.pack(side="left", padx=4)

        self.btn_cancel = ttk.Button(row1, text=" Cancel", image=self.ico_cancel, compound="left", style="TButton", command=self.on_cancel_search, state="disabled", width=12)
        self.btn_cancel.pack(side="left", padx=4)

        self.ico_close = self.get_icon("close", (12, 12))
        self.btn_close_search = ttk.Button(row1, text="✕", image=self.ico_close, style="Small.TButton", command=self._hide_search_bar, width=3)
        self.btn_close_search.pack(side="left", padx=(4, 0))
        create_tooltip(self.btn_close_search, "Close Search Bar (Esc)")

        # Row 1.5: Replace row (shown when Ctrl+H / Replace is activated)
        self.row_replace = self._tag_role(tk.Frame(self.search_frame, bg=t["bg_panel"]), "panel")
        self._tag_role(
            tk.Label(self.row_replace, text="Replace:", font=("Segoe UI", 9, "bold"), bg=t["bg_panel"], fg=t["accent_blue"], width=7, anchor="w"),
            "label_voice"
        ).pack(side="left", padx=(0, 6))

        self.replace_var = tk.StringVar(master=self)
        self.replace_entry = self._tag_role(
            tk.Entry(
                self.row_replace,
                textvariable=self.replace_var,
                font=("Consolas", 10),
                bg=t["bg_editor"],
                fg=t["fg_text"],
                insertbackground=t["misora_pink"],
                bd=1,
                relief="solid",
                highlightthickness=1,
                highlightcolor=t["accent_blue"]
            ),
            "entry_editor"
        )
        self.replace_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.replace_entry.bind("<Escape>", lambda e: self._hide_search_bar())
        self.replace_entry.bind("<Return>", lambda e: self.on_replace_next())

        self.ico_replace = self.get_icon("replace", (14, 14))
        self.ico_replace_all = self.get_icon("replace_all", (14, 14))
        self.btn_replace = ttk.Button(self.row_replace, text=" Replace", image=self.ico_replace, compound="left", style="TButton", command=self.on_replace_next, width=14)
        self.btn_replace.pack(side="left", padx=4)

        self.btn_replace_all = ttk.Button(self.row_replace, text=" Replace All", image=self.ico_replace_all, compound="left", style="TButton", command=self.on_replace_all, width=12)
        self.btn_replace_all.pack(side="left", padx=4)

        spacer_close = tk.Frame(self.row_replace, bg=t["bg_panel"], width=28, height=1)
        spacer_close.pack(side="left", padx=(4, 0))
        spacer_close.pack_propagate(False)
        self._replace_row_visible = False

        row2 = self._tag_role(tk.Frame(self.search_frame, bg=t["bg_panel"]), "panel")
        row2.pack(fill="x", padx=8, pady=(0, 4))

        self.var_case = tk.BooleanVar(master=self, value=False)
        self.var_regex = tk.BooleanVar(master=self, value=False)
        self.var_ignore_ws = tk.BooleanVar(master=self, value=True)
        self.var_inc_bundles = tk.BooleanVar(master=self, value=True)
        self.var_inc_text = tk.BooleanVar(master=self, value=True)

        cb_case = ttk.Checkbutton(row2, text="Match Case", variable=self.var_case, style="Panel.TCheckbutton")
        cb_case.pack(side="left", padx=4)

        cb_rx = ttk.Checkbutton(row2, text="Regex", variable=self.var_regex, style="Panel.TCheckbutton")
        cb_rx.pack(side="left", padx=4)

        cb_ws = ttk.Checkbutton(row2, text="Ignore Whitespace & {playername}", variable=self.var_ignore_ws, style="Panel.TCheckbutton")
        cb_ws.pack(side="left", padx=4)

        self._tag_role(tk.Label(row2, text="|", bg=t["bg_panel"], fg=t["border"]), "label_sep").pack(side="left", padx=6)

        self._tag_role(tk.Label(row2, text="Scope:", bg=t["bg_panel"], fg=t["fg_muted"]), "label_muted").pack(side="left", padx=(0, 4))
        self.scope_var = tk.StringVar(master=self, value="project")

        self.rb_proj = ttk.Radiobutton(row2, text="Project", variable=self.scope_var, value="project", style="Panel.TRadiobutton", command=self._sync_scope_widgets)
        self.rb_proj.pack(side="left", padx=2)

        self.rb_folder = ttk.Radiobutton(row2, text="Folder", variable=self.scope_var, value="folder", style="Panel.TRadiobutton", command=self._sync_scope_widgets)
        self.rb_folder.pack(side="left", padx=2)

        self.rb_cur = ttk.Radiobutton(row2, text="Current File(s)", variable=self.scope_var, value="current", style="Panel.TRadiobutton", command=self._sync_scope_widgets)
        self.rb_cur.pack(side="left", padx=2)

        self._tag_role(tk.Label(row2, text="|", bg=t["bg_panel"], fg=t["border"]), "label_sep").pack(side="left", padx=6)
        cb_bdl = ttk.Checkbutton(row2, text=".unity3d", variable=self.var_inc_bundles, style="Panel.TCheckbutton")
        cb_bdl.pack(side="left", padx=2)
        cb_txt = ttk.Checkbutton(row2, text=".txt", variable=self.var_inc_text, style="Panel.TCheckbutton")
        cb_txt.pack(side="left", padx=2)

        self._tag_role(tk.Label(row2, text="|", bg=t["bg_panel"], fg=t["border"]), "label_sep").pack(side="left", padx=6)

        # Browse [...] button on LEFT of entry
        self.btn_browse_search_folder = ttk.Button(row2, text="...", style="Small.TButton", command=self.on_browse_scope_path, width=3)
        self.btn_browse_search_folder.pack(side="left", padx=(0, 2))

        # Directory path entry on RIGHT of [...], expands to fill remaining space
        self.folder_path_var = tk.StringVar(master=self, value="")
        self.folder_path_var.trace_add("write", lambda *args: self._on_folder_path_var_trace())
        self.folder_path_entry = self._tag_role(
            tk.Entry(
                row2,
                textvariable=self.folder_path_var,
                font=("Segoe UI", 9),
                bg=t["bg_editor"],
                fg=t["fg_text"],
                bd=1,
                relief="solid",
            ),
            "entry_editor"
        )
        self.folder_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 2))
        self.folder_path_entry.bind("<Return>", lambda e: self.on_start_search())
        self.folder_path_entry.bind("<FocusOut>", lambda e: self._save_user_prefs(silent=True))

        self.progress_bar = ttk.Progressbar(self.search_frame, mode="determinate")
        self.progress_bar.pack(fill="x", padx=8, pady=(0, 2))
        self.progress_bar.pack_forget()

        # Initialize scope widgets with project path
        self._sync_scope_widgets()

    # -------------------------------------------------------------------------
    # Main Workspace (#4 Distinct Nav Buttons, #5/#6 Clean Header, #7 Inline Ribbon)
    # -------------------------------------------------------------------------
